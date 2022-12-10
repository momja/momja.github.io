python build.py --full
postcss style/tailwind.css -o static/tailwind.css
mkdir -p static/images
cd images
for IMAGE in *.jpg
do
    magick $IMAGE -resize 720x720\> ../static/images/$IMAGE
done
for IMAGE in *.png
do
    magick $IMAGE -format jpg -resize 720x720\> ../static/images/$IMAGE
done
for IMAGE in *.gif
do
    magick $IMAGE -format jpg -resize 720x720\> ../static/images/$IMAGE
done
cd ..
cp images/*.pdf static/images/
cp images/*.mp4 static/images/