
<script setup>
defineProps(['id', 'name', 'country_name', 'city', 'start_timestamp', 'end_timestamp', 'tagline', 'banner_image_url'])

function getDayName(date) {
    return date.toLocaleDateString('en-US', { weekday: 'short' });
}

function formatFromTo(start, stop) {
    let a = new Date(start);
    let b = new Date(stop);

    return getDayName(a) + " " + a.toLocaleDateString() + " -> " + getDayName(b) + " " + b.toLocaleDateString()
}


</script>


<template>
    <v-col cols="12" md="6" lg="6">
        <router-link style="text-decoration: none; color: inherit;" :to="{ name: 'FestivalDetail', params: { id: id } }">
            <v-card variant="flat">
                <v-img :src="banner_image_url" class="align-end" gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)" height="200px"
                    cover>
                    <v-card-title class="text-white" v-text="name"></v-card-title>
                    <v-card-text class="text-white"
                        v-text="formatFromTo(start_timestamp, end_timestamp) + ' @ ' + city + ', ' + country_name"></v-card-text>
                    <!-- <v-card-text class="text-white" v-text="tagline"></v-card-text> -->
                </v-img>
            </v-card>

        </router-link>
    </v-col>
</template>
