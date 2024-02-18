

<template>
        <!-- Tabs header -->
        <v-tabs v-model="tab" fixed-tabs>
            <v-tab value=upcoming>Upcoming</v-tab>
            <v-tab value=past>Past</v-tab>
        </v-tabs>

        <!-- Tab content -->
        <v-window v-model="tab">
            <v-window-item value=upcoming>
                <v-container fluid>
                    <v-row dense>
                        <FestivalCard v-for="festival in get_upcoming_events(festivals)" :id="festival.id"
                            :name="festival.name" :city="festival.city" :country_name="festival.country_name"
                            :banner_image_url="festival.banner_image_url" :start_timestamp="festival.start" :end_timestamp="festival.end" />
                    </v-row>
                </v-container>
            </v-window-item>
            <v-window-item value=past>
                <v-container fluid>
                    <v-row dense>
                        <FestivalCard v-for="festival in get_past_events(festivals)" :id="festival.id" :name="festival.name"
                            :city="festival.city" :country_name="festival.country_name" :image="festival.image_url"
                            :start_timestamp="festival.start" :end_timestamp="festival.end" />
                    </v-row>
                </v-container>
            </v-window-item>
        </v-window>
</template>

<script setup>
import FestivalCard from './FestivalCard.vue';

import { ref } from 'vue';
import axios from 'axios'

const festivals = ref([]);

async function fetchFestivalListData() {
    // var response = await axios.get("http://localhost:8000/api/festivals/");
    var response = await axios.get("/api/festivals/");
    festivals.value = response.data;
}

// load initial data
fetchFestivalListData()

const tab = ref(0);

function get_upcoming_events(festivals) {
    function is_upcoming(festival) {
        let festival_date = new Date(festival.end).getTime();
        let now = new Date().getTime();
        return festival_date >= now;
    }
    return festivals.filter(is_upcoming).sort((a, b) => {
        if (a.start < b.start) {
            return -1;
        }
        if (a.start > b.start) {
            return 1;
        }
        return 0;
    });
}

function get_past_events(festivals) {
    function is_past(festival) {
        let festival_date = new Date(festival.end).getTime();
        let now = new Date().getTime();
        return festival_date < now;
    }
    return festivals.filter(is_past).sort((a, b) => {
        if (a.start < b.start) {
            return 1;
        }
        if (a.start > b.start) {
            return -1;
        }
        return 0;
    });
}

</script>
