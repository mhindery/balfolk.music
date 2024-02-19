

<template>
        <v-progress-linear :active="loading" color="deep-purple" height="4" indeterminate></v-progress-linear>

        <!-- Search box -->
        <v-text-field class="py-3" v-model="search" hide-details placeholder="Search" prepend-inner-icon="mdi-magnify" variant="underlined"></v-text-field>

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
                        <FestivalCard v-for="festival in get_upcoming_events(festivals)" :key="festival.id" :id="festival.id"
                            :name="festival.name" :city="festival.city" :country_name="festival.country_name"
                            :banner_image_url="festival.banner_image_url" :start_timestamp="festival.starting_datetime" :end_timestamp="festival.ending_datetime" />
                    </v-row>
                </v-container>
            </v-window-item>
            <v-window-item value=past>
                <v-container fluid>
                    <v-row dense>
                        <FestivalCard v-for="festival in get_past_events(festivals)" :key="festival.id" :id="festival.id" :name="festival.name"
                            :city="festival.city" :country_name="festival.country_name" :image="festival.image_url"
                            :banner_image_url="festival.banner_image_url" :start_timestamp="festival.starting_datetime" :end_timestamp="festival.ending_datetime" />
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
const loading = ref(true);

async function fetchFestivalListData() {
    loading.value = true;
    var response = await axios.get("/api/festivals/");
    festivals.value = response.data;
    loading.value = false;
}

// load initial data
fetchFestivalListData();

const tab = ref(0);
const search = ref('');

function get_upcoming_events(festivals) {
    function is_upcoming(festival) {
        let festival_date = new Date(festival.ending_datetime).getTime();
        let now = new Date().getTime();
        return festival_date >= now;
    }
    return festivals.filter(is_upcoming).sort((a, b) => {
        if (a.starting_datetime < b.starting_datetime) {
            return -1;
        }
        if (a.starting_datetime > b.starting_datetime) {
            return 1;
        }
        return 0;
    });
}

function get_past_events(festivals) {
    function is_past(festival) {
        let festival_date = new Date(festival.ending_datetime).getTime();
        let now = new Date().getTime();
        return festival_date < now;
    }
    return festivals.filter(is_past).sort((a, b) => {
        if (a.starting_datetime < b.starting_datetime) {
            return 1;
        }
        if (a.starting_datetime > b.starting_datetime) {
            return -1;
        }
        return 0;
    });
}

</script>
