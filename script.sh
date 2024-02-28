cd server_config/helm
sed 's/{IMAGE_TAG}/1.0.0/g' balfolk_music/values.tmpl.yaml > balfolk_music/values.yaml
mkdir rendered/1.0.0
cp -r balfolk_music/ rendered/1.0.0/
rm rendered/1.0.0/values.tmpl.yaml
rm balfolk_music/values.yaml
