python build.py --full $1
postcss style/tailwind.css -o static/tailwind.css
mkdir -p static/images
cp -r images/*.pdf static/images/
cp -r images/*.mp4 static/images/
cp -r images/*.mov static/images/
cp -r favicon/144x144.png static/favicon.png
cp -r rss.xml static/rss.xml

echo "Website is published locally at file://$(dirname $(realpath "$0"))/static/index.html"
