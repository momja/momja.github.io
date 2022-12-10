python build.py --full
postcss style/tailwind.css -o static/tailwind.css
mkdir -p static/images
cp -r images/*.pdf static/images/
cp -r images/*.mp4 static/images/
cp -r images/*.mov static/images/
mogrify -resize 720x720\> -format jpg -path static/images/ images/*.png
mogrify -resize 720x720\> -path static/images/ images/*.jpg
mogrify -resize 720x720\> -path static/images/ images/*.gif