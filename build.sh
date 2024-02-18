cd ./frontend/balfolk_music_vuetify && \
yarn run build && \
perl -pi -e s,/assets/,https://mhindery.github.io/balfolk.music/staticfiles/,g dist/index.html && \
cp ./dist/index.html ../../balfolk_music/templates/index.html && \
cd ../.. && \
# rm -r staticfiles && \
python manage.py collectstatic --noinput && \
rm -r ./frontend/balfolk_music_vuetify/dist
