
<script setup>
defineProps(['id', 'name', 'country_name', 'city', 'start_timestamp', 'end_timestamp', 'banner_image_url'])

function getDayName(date) {
    return date.toLocaleDateString('en-US', { weekday: 'short' });
}

const dateFormat = { timeZone: 'UTC', weekday: "long", year: "numeric", month: "short", day: "numeric" };
const timeFormat = { timeStyle: 'short' };

function formatMultiDayEventDate(start, stop) {
    if (start == undefined || stop == undefined) {
        return '';
    }
    // console.log(start);
    // console.log(stop);
    let a = new Date(start);
    let b = new Date(stop);
    let userTimezoneOffset = a.getTimezoneOffset() * 60000;
    // console.log(a);
    // console.log(userTimezoneOffset);
    a = new Date(a - userTimezoneOffset * Math.sign(userTimezoneOffset));
    b = new Date(b - userTimezoneOffset * Math.sign(userTimezoneOffset));
    // console.log(a);


    return a.toLocaleDateString('en-us', dateFormat) + " -> " + b.toLocaleDateString('en-us', dateFormat);
}


</script>


<template>
    <v-col cols="12" md="6" lg="6">
        <router-link style="text-decoration: none; color: inherit;" :to="{ name: 'FestivalDetail', params: { id: id } }">
            <v-card variant="flat">
                <v-img :src="banner_image_url" class="align-end" gradient="to bottom, rgba(0,0,0,.3), rgba(0,0,0,.7)" height="200px"
                    cover >
                    <v-card-title class="text-white" v-text="name"></v-card-title>
                    <v-card-text style="white-space: pre-line;" class="text-white">
                        {{ formatMultiDayEventDate(start_timestamp, end_timestamp) }}
                        <br>
                        {{ city }}, {{ country_name}}
                    </v-card-text>
                </v-img>
            </v-card>

        </router-link>
    </v-col>
</template>
