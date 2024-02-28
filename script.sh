TAG=${GITHUB_REF_NAME}
echo "TAG: " $TAG
echo "-------------"
cd server_config/helm
sed "s/{IMAGE_TAG}/$TAG/g" webapp1/values.tmpl.yaml > webapp1/values.yaml
mkdir rendered
mkdir rendered/$TAG
cp -r webapp1/. rendered/$TAG/
rm rendered/$TAG/values.tmpl.yaml
rm webapp1/values.yaml

ls rendered/$TAG
