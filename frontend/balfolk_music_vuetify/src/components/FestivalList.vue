

<template>
    <v-progress-linear :active="loading" color="deep-purple" height="4" indeterminate></v-progress-linear>

    <!-- Search box -->
    <v-text-field class="pb-3" v-model="search" hide-details placeholder="Search" prepend-inner-icon="mdi-magnify" variant="underlined"></v-text-field>

    <!-- Tabs header -->
    <v-tabs v-model="tab" fixed-tabs>
        <v-tab value=upcoming>Upcoming</v-tab>
        <v-tab value=past>Past</v-tab>
    </v-tabs>

    <!-- Tab content -->
    <v-window v-model="tab">
        <v-window-item value=upcoming>
            <v-container fluid>
                <v-data-iterator :items="get_upcoming_events(objects)" :items-per-page="20" :search="search">
                    <template v-slot:default="{ items }">
                        <v-row dense>
                            <FestivalCard v-for="item in items" :key="item.raw.id" :id="item.raw.id" :name="item.raw.name"
                                :city="item.raw.city" :country_name="item.raw.country_name" :image="item.raw.image_url"
                                :banner_image_url="item.raw.banner_image_url" :start_timestamp="item.raw.starting_datetime"
                                :end_timestamp="item.raw.ending_datetime" />
                        </v-row>
                    </template>

                    <template v-slot:footer="{ page, pageCount, prevPage, nextPage }">
                        <div class="d-flex align-center justify-center pa-4">
                            <v-btn :disabled="page === 1" icon="mdi-arrow-left" density="comfortable" variant="tonal"
                                rounded @click="prevPage"></v-btn>

                            <div class="mx-2 text-caption">
                                Page {{ page }} of {{ pageCount }}
                            </div>

                            <v-btn :disabled="page >= pageCount" icon="mdi-arrow-right" density="comfortable"
                                variant="tonal" rounded @click="nextPage"></v-btn>
                        </div>
                    </template>
                </v-data-iterator>
            </v-container>
        </v-window-item>
        <v-window-item value=past>
            <v-container fluid>
                <v-data-iterator :items="get_past_events(objects)" :items-per-page="20" :search="search">
                    <template v-slot:default="{ items }">
                        <v-row dense>
                            <FestivalCard v-for="item in items" :key="item.raw.id" :id="item.raw.id" :name="item.raw.name"
                                :city="item.raw.city" :country_name="item.raw.country_name" :image="item.raw.image_url"
                                :banner_image_url="item.raw.banner_image_url" :start_timestamp="item.raw.starting_datetime"
                                :end_timestamp="item.raw.ending_datetime" />
                        </v-row>
                    </template>

                    <template v-slot:footer="{ page, pageCount, prevPage, nextPage }">
                        <div class="d-flex align-center justify-center pa-4">
                            <v-btn :disabled="page === 1" icon="mdi-arrow-left" density="comfortable" variant="tonal"
                                rounded @click="prevPage"></v-btn>

                            <div class="mx-2 text-caption">
                                Page {{ page }} of {{ pageCount }}
                            </div>

                            <v-btn :disabled="page >= pageCount" icon="mdi-arrow-right" density="comfortable"
                                variant="tonal" rounded @click="nextPage"></v-btn>
                        </div>
                    </template>
                </v-data-iterator>
            </v-container> æ
        </v-window-item>
    </v-window>
</template>

<script setup>
import FestivalCard from './FestivalCard.vue';

import { ref } from 'vue';
import axios from 'axios'

const objects = ref([]);
const loading = ref(true);

async function fetchData() {
    loading.value = true;
    var response = await axios.get("/api/festivals/");
    objects.value = response.data;
    // console.log(objects);
    loading.value = false;
}

// load initial data
fetchData();

const tab = ref(0);
const search = ref('');

function get_upcoming_events(objects) {
    function is_upcoming(festival) {
        let festival_date = new Date(festival.ending_datetime).getTime();
        let now = new Date().getTime();
        return festival_date >= now;
    }
    return objects.filter(is_upcoming).sort((a, b) => {
        if (a.starting_datetime < b.starting_datetime) {
            return -1;
        }
        if (a.starting_datetime > b.starting_datetime) {
            return 1;
        }
        return 0;
    });
}

function get_past_events(objects) {
    function is_past(festival) {
        let festival_date = new Date(festival.ending_datetime).getTime();
        let now = new Date().getTime();
        return festival_date < now;
    }
    return objects.filter(is_past).sort((a, b) => {
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
