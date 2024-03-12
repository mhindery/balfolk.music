

<template>
    <v-sheet>
        <iframe v-for="object in objects" :key="object.id" style="border-radius:12px"
            :src="getSpotifyLink(object)" width="100%"
            height="152" frameBorder="0" allowfullscreen=""
            allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
    </v-sheet>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios'

const objects = ref([]);

async function fetchData() {
    var response = await axios.get("/api/playlists/");
    objects.value = response.data;
    // console.log(objects.value);
}

// load initial data
fetchData()

function getSpotifyLink(object) {
    return 'https://open.spotify.com/embed/playlist/' + object.platform_id + '?utm_source=generator&theme=0';
}

</script>
