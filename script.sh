TAG=${GITHUB_REF_NAME}
echo "TAG: " $TAG
echo "-------------"
cd server_config/helm
sed "s/{IMAGE_TAG}/$TAG/g" balfolk_music/values.tmpl.yaml > balfolk_music/values.yaml
mkdir rendered
mkdir rendered/$TAG
cp -r balfolk_music/. rendered/$TAG/
rm rendered/$TAG/values.tmpl.yaml
rm balfolk_music/values.yaml

ls rendered/$TAG
