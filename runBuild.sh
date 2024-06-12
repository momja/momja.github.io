python build.py --full $1
postcss style/tailwind.css -o static/tailwind.css
mkdir -p static/images
cp -r images/*.pdf static/images/
cp -r images/*.mp4 static/images/
cp -r images/*.mov static/images/
cp -r favicon/144x144.png static/favicon.png
mogrify -resize 720x720\> -format jpg -path static/images/ images/*.png
mogrify -resize 720x720\> -path static/images/ images/*.jpg
mogrify -resize 720x720\> -path static/images/ images/*.gif
cp -r rss.xml static/rss.xml

echo "Website is published locally at file:///Users/maxwellomdal/Documents/projects/personal_website/static/index.html"
