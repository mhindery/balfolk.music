<template>
    <v-progress-linear :active="loading" color="deep-purple" height="4" indeterminate></v-progress-linear>

    <!-- Search box -->
    <v-text-field class="py-3" v-model="search" hide-details placeholder="Search" prepend-inner-icon="mdi-magnify"
        variant="underlined"></v-text-field>

    <!-- Tabs header -->
    <v-tabs v-model="tab" fixed-tabs>
        <v-tab value=upcoming>Upcoming</v-tab>
        <v-tab value=past>Past</v-tab>
    </v-tabs>

    <!-- Tab content -->
    <v-window v-model="tab">
        <v-window-item value=upcoming>
            <v-container>
                <v-data-iterator :items="get_upcoming_events(objects)" :items-per-page="20" :search="search">
                    <template v-slot:default="{ items }">
                        <v-row dense>
                            <v-col v-for="item in items" :key="item.id" cols="12" lg="4" md="6" sm="12">
                                <!-- Single entry -->
                                <router-link style="text-decoration: none; color: inherit;"
                                    :to="{ name: 'CourseDetail', params: { id: item.raw.id } }">
                                    <v-sheet rounded class="d-flex" color="grey-lighten-3">
                                        <v-row align="center" no-gutters>
                                            <!-- Date rectangle -->
                                            <v-col :style="{ 'background-size': 'cover', 'box-shadow': 'inset 0 0 0 2000px rgba(49, 49, 50, 0.7)', 'background-position': 'center', 'background-origin': 'border-box', 'border-bottom-left-radius': '4px', 'border-bottom-left-radius ': '4px', 'border-top-left-radius': '4px', 'background-image': 'url(https://catamphetamine.gitlab.io/country-flag-icons/3x2/' + item.raw.country_code + '.svg)' }" class="fill-height" cols="3" md="3">
                                                <v-row no-gutters style="line-height: 20px;height: 22px;" justify="center" class="text-subtitle-2 text-grey-lighten-2" v-text="getWeekdayStart(item.raw)"></v-row>
                                                <v-row no-gutters style="line-height: 20px;height: 22px;" justify="center" class="text-h5 font-weight-bold text-white" v-text="getDayOfMonthStart(item.raw)"></v-row>
                                                <v-row no-gutters style="line-height: 20px;height: 22px;" justify="center" class="text-subtitle-1 font-weight-bold text-grey-lighten-2" v-text="getMonthStart(item.raw)"></v-row>
                                            </v-col>
                                            <!-- Event title -->
                                            <v-col>
                                                <v-row class="ml-2 text-h6" no-gutters v-text="item.raw.name"></v-row>
                                                <v-row class="ml-2 text-subtitle-2 text-grey" no-gutters>
                                                    <!-- <v-icon size="x-small" icon="mdi-map-marker"></v-icon> -->
                                                    {{ formatLocation(item.raw) }}
                                                </v-row>
                                            </v-col>
                                        </v-row>
                                    </v-sheet>
                                </router-link>
                            </v-col>
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
            <v-container>
                <v-data-iterator :items="get_past_events(objects)" :items-per-page="20" :search="search">
                    <template v-slot:default="{ items }">
                        <v-row dense>
                            <v-col v-for="item in items" :key="item.id" cols="12" lg="4" md="6" sm="12">
                                <!-- Single entry -->
                                <router-link style="text-decoration: none; color: inherit;"
                                    :to="{ name: 'CourseDetail', params: { id: item.raw.id } }">
                                    <v-sheet rounded class="d-flex" color="grey-lighten-3">
                                        <v-row align="center" no-gutters>
                                            <!-- Date rectangle -->
                                            <v-col :style="{ 'background-size': 'cover', 'box-shadow': 'inset 0 0 0 2000px rgba(49, 49, 50, 0.7)', 'background-position': 'center', 'background-origin': 'border-box', 'border-bottom-left-radius': '4px', 'border-bottom-left-radius ': '4px', 'border-top-left-radius': '4px', 'background-image': 'url(https://catamphetamine.gitlab.io/country-flag-icons/3x2/' + item.raw.country_code + '.svg)' }" class="fill-height" cols="3" md="3">
                                                <v-row no-gutters style="line-height: 20px;height: 22px;" justify="center" class="text-subtitle-2 text-grey-lighten-2" v-text="getWeekdayStart(item.raw)"></v-row>
                                                <v-row no-gutters style="line-height: 20px;height: 22px;" justify="center" class="text-h5 font-weight-bold text-white" v-text="getDayOfMonthStart(item.raw)"></v-row>
                                                <v-row no-gutters style="line-height: 20px;height: 22px;" justify="center" class="text-subtitle-1 font-weight-bold text-grey-lighten-2" v-text="getMonthStart(item.raw)"></v-row>
                                            </v-col>
                                            <!-- Event title -->
                                            <v-col>
                                                <v-row class="ml-2 text-h6" no-gutters v-text="item.raw.name"></v-row>
                                                <v-row class="ml-2 text-subtitle-2 text-grey" no-gutters>
                                                    <!-- <v-icon size="x-small" icon="mdi-map-marker"></v-icon> -->
                                                    {{ formatLocation(item.raw) }}
                                                </v-row>
                                            </v-col>
                                        </v-row>
                                    </v-sheet>
                                </router-link>
                            </v-col>
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
    </v-window>
</template>

<script setup>

import { ref } from 'vue';
import axios from 'axios'

const objects = ref([]);
const loading = ref(true);
const search = ref('');

async function fetchData() {
    loading.value = true;
    var response = await axios.get("/api/courses/");
    objects.value = response.data;
    loading.value = false;
}

// load initial data
fetchData()

const tab = ref(0);

function get_upcoming_events(objects) {
    function is_upcoming(event) {
        return new Date(event.ending_datetime).getTime() >= new Date().getTime();
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
    function is_past(event) {
        return new Date(event.ending_datetime).getTime() < new Date().getTime();
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

function getDayName(date) {
    return date.toLocaleDateString('en-US', { weekday: 'short' });
}

function formatDate(start) {
    let a = new Date(start);

    return getDayName(a) + " " + a.toLocaleDateString()
}


function getWeekdayStart(obj) {
    let date = new Date(obj.starting_datetime);
    return date.toLocaleDateString('en-US', { weekday: 'short' });
}

function getDayOfMonthStart(obj) {
    let date = new Date(obj.starting_datetime);
    return date.getDate();
}

function getMonthStart(obj) {
    let date = new Date(obj.starting_datetime);
    return date.toLocaleDateString('en-US', { month: 'short' }).toUpperCase();
}

function formatLocation(obj) {
    if (obj.country_name && obj.city) {
        return obj.city + ', ' + obj.country_name
    }
    if (obj.country_name) {
        return obj.country_name
    }
    return obj.city
}

</script>
