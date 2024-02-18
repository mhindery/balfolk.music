cd ./frontend/balfolk_music_vuetify && \
yarn run build && \
cp ./dist/index.html ../../balfolk_music/templates/index.html && \
cd ../.. && \
# rm -r staticfiles && \
python manage.py collectstatic --noinput && \
rm -r ./frontend/balfolk_music_vuetify/dist
