"""Convert article images to AVIF + WebP.

This replaces the old ImageMagick "shrink on build" step. For every raster
image under ``images/`` and co-located with articles under ``src/articles/``,
it emits ``<basename>.avif`` and ``<basename>.webp`` mirrors under ``static/``.

Browser delivery (see ``pictureify_html``) is a ``<picture>`` element that
serves AVIF when supported and falls back to WebP otherwise. Animated GIFs
are converted to *animated* AVIF/WebP, and the original GIF is additionally
copied to ``static/`` as the last-resort fallback for browsers without WebP
support. Still images need no fallback beyond WebP, so their originals are
not copied to ``static/``.

Outputs are cached: a source whose ``.avif``/``.webp`` outputs are both newer
than itself is skipped, so repeated builds are cheap.

Usage:
    python convert_images.py   # run from the repository root
"""

import os
import re
import sys
from pathlib import Path

# Absolute URL prefix used for article images in production builds.
# Must stay in sync with the base URL used in build.py.
BASE_URL = 'http://dizzard.net/'

REPO_ROOT = Path(__file__).resolve().parent
STATIC_ROOT = REPO_ROOT / 'static'

# Source extensions we convert (matched case-insensitively).
STILL_EXTS = {'.jpg', '.jpeg', '.png', '.heic', '.heif'}
ANIMATED_EXTS = {'.gif'}
CONVERTIBLE_EXTS = STILL_EXTS | ANIMATED_EXTS

# Directories searched for source images, relative to the repo root.
SOURCE_DIRS = [Path('images'), Path('src/articles')]

WEBP_QUALITY = 80
AVIF_QUALITY = 60

_img_lib_ready = False


def _ensure_img_lib():
    """Import Pillow + format plugins (deferred so build.py fails loudly only
    when conversion/markup is actually needed)."""
    global _img_lib_ready
    if _img_lib_ready:
        return
    try:
        import pillow_avif  # noqa: F401  (registers the AVIF plugin)
        import pillow_heif
        pillow_heif.register_heif_opener()
    except ImportError as e:
        raise SystemExit(
            f"convert_images: missing image dependency ({e}). "
            "Run: pip install -r requirements.txt"
        )
    _img_lib_ready = True


def _outputs_current(src: Path, dests):
    """True when every dest exists and is at least as new as src."""
    try:
        src_mtime = src.stat().st_mtime
    except OSError:
        return False
    for dest in dests:
        try:
            if dest.stat().st_mtime < src_mtime:
                return False
        except OSError:
            return False
    return True


def _normalise_still(img):
    """Normalise mode for encoding, preserving transparency when present."""
    from PIL.ImageOps import exif_transpose
    img = exif_transpose(img)
    if img.mode in ('RGBA', 'LA', 'RGB', 'L'):
        return img.convert('RGBA') if img.mode == 'LA' else img
    if img.mode == 'P':
        return img.convert('RGBA') if 'transparency' in img.info else img.convert('RGB')
    return img.convert('RGB')


def convert_still(src: Path, avif_dest: Path, webp_dest: Path):
    from PIL import Image
    with Image.open(src) as img:
        img = _normalise_still(img)
        avif_dest.parent.mkdir(parents=True, exist_ok=True)
        img.save(str(avif_dest), quality=AVIF_QUALITY, speed=6)
        img.save(str(webp_dest), quality=WEBP_QUALITY, method=6)


def _decode_gif_frames(src: Path):
    """Decode GIF frames with disposal-method compositing so partial-frame
    (delta) GIFs convert to correct full-frame animations."""
    from PIL import Image, ImageSequence
    with Image.open(src) as im:
        size = im.size
        loop = im.info.get('loop', 0)
        canvas = Image.new('RGBA', size, (0, 0, 0, 0))
        frames, durations = [], []
        for frame in ImageSequence.Iterator(im):
            disposal = getattr(frame, 'disposal_method', 0)
            previous = canvas.copy() if disposal == 3 else None
            canvas.paste(frame.convert('RGBA'), (0, 0), frame.convert('RGBA'))
            frames.append(canvas.copy())
            durations.append(frame.info.get('duration', 100) or 100)
            if disposal == 2:  # restore to background
                canvas = Image.new('RGBA', size, (0, 0, 0, 0))
            elif disposal == 3:  # restore to previous
                canvas = previous
        return frames, durations, loop


def convert_animated(src: Path, avif_dest: Path, webp_dest: Path):
    frames, durations, loop = _decode_gif_frames(src)
    avif_dest.parent.mkdir(parents=True, exist_ok=True)
    duration = durations if len(set(durations)) > 1 else durations[0]
    frames[0].save(str(webp_dest), save_all=True, append_images=frames[1:],
                   duration=duration, loop=loop, minimize_size=True)
    frames[0].save(str(avif_dest), save_all=True, append_images=frames[1:],
                   duration=duration, loop=loop,
                   quality=AVIF_QUALITY, speed=8)


def iter_source_images():
    """Yield (source, static_dest_dir) for every convertible image."""
    for source_dir in SOURCE_DIRS:
        root = REPO_ROOT / source_dir
        if not root.is_dir():
            continue
        for dirpath, _dirnames, filenames in os.walk(root):
            for name in filenames:
                if name.startswith('.'):
                    continue
                if Path(name).suffix.lower() not in CONVERTIBLE_EXTS:
                    continue
                src = Path(dirpath) / name
                rel_parent = src.parent.relative_to(REPO_ROOT)
                if rel_parent.parts[:1] == ('src',):
                    # Article pages render to static/articles/..., so
                    # co-located images must mirror without the src/ prefix.
                    rel_parent = Path(*rel_parent.parts[1:])
                yield src, STATIC_ROOT / rel_parent


def convert_all(verbose=True):
    """Convert every source image; return (converted, skipped) counts."""
    _ensure_img_lib()
    import shutil
    converted, skipped = 0, 0
    for src, dest_dir in iter_source_images():
        animated = src.suffix.lower() in ANIMATED_EXTS
        avif_dest = dest_dir / (src.stem + '.avif')
        webp_dest = dest_dir / (src.stem + '.webp')
        dests = [avif_dest, webp_dest]
        gif_dest = None
        if animated:
            # Original GIF stays available as the final fallback.
            gif_dest = dest_dir / src.name
            dests.append(gif_dest)
        if _outputs_current(src, dests):
            skipped += 1
            continue
        if verbose:
            print(f"converting {src}")
        if animated:
            convert_animated(src, avif_dest, webp_dest)
            dest_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, gif_dest)
        else:
            convert_still(src, avif_dest, webp_dest)
        converted += 1
    if verbose:
        print(f"images: {converted} converted, {skipped} up to date")
    return converted, skipped


# ---------------------------------------------------------------------------
# HTML rewriting: <img> -> <picture> (AVIF first, WebP fallback)
# ---------------------------------------------------------------------------

IMG_TAG_RE = re.compile(r'<img\b([^>]*?)\s*/?>', re.IGNORECASE | re.DOTALL)
SRC_ATTR_RE = re.compile(r'''\bsrc\s*=\s*(['"])(.*?)\1''', re.IGNORECASE | re.DOTALL)


def _split_src(src):
    """Split an image URL into (path, suffix) where suffix is a trailing
    query string and/or fragment (possibly empty)."""
    m = re.search(r'[?#]', src)
    if not m:
        return src, ''
    return src[:m.start()], src[m.start():]


def _static_fs_path(src_path, page_dir):
    """Map an <img> src path to its file under static/, or None when the
    image is external (or otherwise not one we convert). page_dir is the
    page's directory relative to static/ (e.g. 'articles/blooming')."""
    if src_path.startswith(BASE_URL):
        rel = src_path[len(BASE_URL):]
    elif re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', src_path):
        return None  # some other absolute URL (or data: URI)
    elif src_path.startswith('/'):
        return None  # root-absolute; this site uses relative links
    else:
        rel = os.path.normpath(os.path.join(page_dir, src_path))
        if rel.startswith('..'):
            return None
    return STATIC_ROOT / rel


def _with_ext(src, new_ext):
    path, suffix = _split_src(src)
    stem, _dot, _old_ext = path.rpartition('.')
    if not _dot or '/' in _old_ext:
        return None
    return stem + new_ext + suffix


def pictureify_html(html, page_dir):
    """Rewrite convertible <img> tags as <picture> elements serving AVIF
    with a WebP fallback.

    Only images whose converted files already exist under static/ are
    rewritten (so run convert_images.py before build.py); anything else is
    left untouched. Animated GIFs keep the original GIF as the final <img>
    fallback for browsers without WebP support.
    """
    def repl(match):
        attrs = match.group(1)
        src_match = SRC_ATTR_RE.search(attrs)
        if not src_match:
            return match.group(0)
        quote, src = src_match.group(1), src_match.group(2)
        path, _suffix = _split_src(src)
        ext = os.path.splitext(path)[1].lower()
        if ext not in CONVERTIBLE_EXTS:
            return match.group(0)
        fs_path = _static_fs_path(path, page_dir)
        if fs_path is None:
            return match.group(0)
        base = fs_path.parent / fs_path.stem
        has_avif = (base.with_suffix('.avif')).is_file()
        has_webp = (base.with_suffix('.webp')).is_file()
        is_gif = ext == '.gif'
        has_gif = is_gif and fs_path.is_file()
        if not (has_avif or has_webp or has_gif):
            return match.group(0)

        avif_src = _with_ext(src, '.avif') if has_avif else None
        webp_src = _with_ext(src, '.webp') if has_webp else None
        # Animated GIFs keep the original GIF as the final <img> fallback
        # for browsers without WebP support; everything else falls back
        # to WebP, which is universally supported.
        if is_gif and has_gif:
            fallback_src = src
        else:
            fallback_src = webp_src
        if fallback_src is None:
            return match.group(0)

        rest = SRC_ATTR_RE.sub('', attrs).strip().rstrip('/')
        rest = (' ' + rest.strip()) if rest.strip() else ''
        if not re.search(r'''\balt\s*=''', rest, re.IGNORECASE):
            rest += ' alt=""'
        sources = ''
        if avif_src:
            sources += f'<source srcset={quote}{avif_src}{quote} type="image/avif">'
        if webp_src:
            sources += f'<source srcset={quote}{webp_src}{quote} type="image/webp">'
        return (f'<picture>{sources}'
                f'<img src={quote}{fallback_src}{quote}{rest}></picture>')

    return IMG_TAG_RE.sub(repl, html)


IMAGE_REF_RE = re.compile(
    r'!\[[^\]]*\]\(([^)\s]+)\)'
    r'|<img\b[^>]*\bsrc\s*=\s*["\']([^"\']+)["\']',
    re.IGNORECASE)


def referenced_basenames():
    """Basenames (sans extension) of every raster image referenced by
    article sources."""
    names = set()
    articles_root = REPO_ROOT / 'src' / 'articles'
    for dirpath, _dirnames, filenames in os.walk(articles_root):
        for name in filenames:
            if not name.endswith(('.md', '.html')):
                continue
            text = (Path(dirpath) / name).read_text(encoding='utf-8', errors='replace')
            for md_src, html_src in IMAGE_REF_RE.findall(text):
                src = md_src or html_src
                path, _suffix = _split_src(src)
                if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', path) and not path.startswith(BASE_URL):
                    continue
                stem = os.path.splitext(os.path.basename(path))[0]
                if stem:
                    names.add(stem)
    return names


def available_basenames():
    """Basenames (sans extension) of every convertible source image."""
    return {src.stem for src, _dest in iter_source_images()}


def warn_missing_sources(verbose=True):
    """Warn about referenced images with no convertible source file."""
    missing = sorted(referenced_basenames() - available_basenames())
    if verbose and missing:
        print("warning: referenced images with no source file (left as-is):")
        for name in missing:
            print(f"  {name}")
    return missing


def main():
    convert_all()
    missing = warn_missing_sources()
    return 1 if missing else 0


if __name__ == '__main__':
    sys.exit(main())
