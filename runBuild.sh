python build.py --full $1
postcss style/tailwind.css -o static/tailwind.css
mkdir -p static/images
echo "copying resources"
cp -r images/*.pdf static/images/
cp -r images/*.mp4 static/images/
cp -r images/*.mov static/images/
cp -r favicon/144x144.png static/favicon.png
cp -r rss.xml static/rss.xml
echo "resizing images"
# mogrify -resize 720x720\> -path static/images/ images/*.jpg
# mogrify -resize 720x720\> -path static/images/ images/*.gif
# mogrify -resize 720x720\> -format jpg -path static/images/ images/*.png
# mogrify -resize 720x720\> -format jpg -path static/images/ images/*.HEIC

echo "Website is published locally at file://$(dirname $(realpath "$0"))/static/index.html"
