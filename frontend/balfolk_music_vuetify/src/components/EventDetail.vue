<script setup>
const props = defineProps(['id', 'apiURL']);

import { ref } from 'vue';
import axios from 'axios'

const obj = ref({});
const zoom = ref(12);
const coordinates = ref([47.41322, -1.219482]);

async function fetchObjDetailData() {
    var response = await axios.get(props.apiURL + props.id + '/');
    // var response = await axios.get("/api/balls/" + props.id + '/');
    obj.value = response.data;
    coordinates.value = [obj.value.lattitude, obj.value.longitude];
}

// load initial data
fetchObjDetailData()

function getGoogleMapsLink(obj) {
    if (obj.address != null) {
        return 'https://www.google.com/maps?daddr=' + encodeURI(obj.address.replaceAll('\n', ' '))
    }
    return ''
    
}

function getDayName(date) {
    return date.toLocaleDateString('en-US', { weekday: 'short' });
}

function formatMultiDayEventDate(start, stop) {
    let a = new Date(start);
    let b = new Date(stop);

    return getDayName(a) + " " + a.toLocaleDateString() + " " + a.toLocaleTimeString() + " -> " + getDayName(b) + " " + b.toLocaleDateString() + " " + b.toLocaleTimeString()
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

function getWeekdayStart(obj) {
    let date = new Date(obj.start);
    return date.toLocaleDateString('en-US', { weekday: 'short' });
}

function getDayOfMonthStart(obj) {
    let date = new Date(obj.start);
    return date.getDate();
}

function getMonthStart(obj) {
    let date = new Date(obj.start);
    return date.toLocaleDateString('en-US', { month: 'short' }).toUpperCase();
}

function getYearStart(obj) {
    let date = new Date(obj.start);
    return date.getFullYear();
}



import L from 'leaflet';
globalThis.L = L;


import "leaflet/dist/leaflet.css";
import { LMap, LMarker, LTileLayer } from "@vue-leaflet/vue-leaflet";


</script>

<template>
    <v-card class="mx-auto my-12">

        <v-img cover max-height="250" :src="obj.banner_image_url"></v-img>

        <v-sheet rounded class="d-flex" color="grey-lighten-3">
            <v-row align="center" no-gutters>
                <!-- Date rectangle -->
                <v-col :style="{ 'background-size': 'cover', 'box-shadow': 'inset 0 0 0 2000px rgba(49, 49, 50, 0.7)', 'background-position': 'center', 'background-origin': 'border-box', 'border-bottom-left-radius': '4px', 'border-bottom-left-radius ': '4px', 'background-image': 'url(https://catamphetamine.gitlab.io/country-flag-icons/3x2/' + obj.country_code + '.svg)' }"
                    class="fill-height" cols="2">
                    <v-row no-gutters style="line-height: 20px;height: 24px;" justify="center" class="text-subtitle-2 text-grey" v-text="getWeekdayStart(obj)"></v-row>
                    <v-row no-gutters style="line-height: 20px;height: 24px;" justify="center" class="text-h5 font-weight-bold text-white" v-text="getDayOfMonthStart(obj)"></v-row>
                    <v-row no-gutters style="line-height: 20px;height: 24px;" justify="center" class="text-subtitle-1 font-weight-bold text-grey" v-text="getMonthStart(obj) + ' ' + getYearStart(obj)"></v-row>

                </v-col>
                <!-- Event title -->
                <v-col>
                    <v-row class="ml-2 text-h6" no-gutters v-text="obj.name"></v-row>
                    <v-row class="ml-2 text-subtitle-2 text-grey" no-gutters>
                        <!-- <v-icon size="x-small" icon="mdi-map-marker"></v-icon> -->
                        {{ formatLocation(obj) }}
                    </v-row>
                </v-col>
            </v-row>
        </v-sheet>

        <v-card-item>
            <v-card-subtitle>{{ obj.event_type_display }}<span v-if="obj.organizer"> by {{ obj.organizer }}</span></v-card-subtitle>
        </v-card-item>

        <v-divider></v-divider>

        <v-container>
            <v-row dense justify="center" align="center">
                <v-col v-if="obj.site" cols="auto">
                    <a target="_blank" style="text-decoration: none; color: inherit;" :href="obj.site">
                        <v-btn variant="text" prepend-icon="mdi-web">
                            <template v-slot:prepend>
                                <v-icon></v-icon>
                            </template>
                            Visit site
                        </v-btn>
                    </a>
                </v-col>
                <v-col v-if="obj.facebook" cols="auto">
                    <a target="_blank" style="text-decoration: none; color: inherit;" :href="obj.facebook">
                        <v-btn variant="text" prepend-icon="mdi-facebook">
                            <template v-slot:prepend>
                                <v-icon></v-icon>
                            </template>
                            Facebook
                        </v-btn>
                    </a>
                </v-col>
                <v-col v-if="obj.address" cols="auto">
                    <a style="text-decoration: none; color: inherit;" target="_blank"
                        :href="getGoogleMapsLink(obj)">
                        <v-btn variant="text" prepend-icon="mdi-navigation">
                            <template v-slot:prepend>
                                <v-icon></v-icon>
                            </template>
                            Open navigation
                        </v-btn>
                    </a>
                </v-col>
                <v-col cols="auto">
                    <a target="_blank" style="text-decoration: none; color: inherit;" :href="obj.ical_link">
                        <v-btn variant="text" prepend-icon="mdi-calendar">
                            <template v-slot:prepend>
                                <v-icon></v-icon>
                            </template>
                            Add to calendar
                        </v-btn>
                    </a>
                </v-col>
            </v-row>
        </v-container>

        <v-divider></v-divider>

        <v-card-title><v-icon size="medium" icon="mdi-information"></v-icon> Information</v-card-title>
        <v-card-text style="white-space: pre-line;">
            {{ obj.description }}
        </v-card-text>

        <div v-if="obj.poster_image">
            <v-divider></v-divider>
            <v-card-title><v-icon size="medium" icon="mdi-image"></v-icon> Poster</v-card-title>
            <v-container class="fill-height" fluid>
                <v-img cover :src="obj.poster_image"></v-img>

            </v-container>
        </div>

        <div v-if="obj.schedule">
            <v-divider class="mx-4 mb-1"></v-divider>
            <v-card-title><v-icon size="medium" icon="mdi-clock-outline"></v-icon> Line-up</v-card-title>
            <v-card-text style="white-space: pre-line;" v-html="formatMultiDayEventDate(obj.start, obj.end)">
            </v-card-text>
                <v-card-text style="white-space: pre-line;" v-html="obj.schedule">
                </v-card-text>
        </div>

        <div v-if="obj.pricing">
            <v-divider class="mx-4 mb-1"></v-divider>
            <v-card-title><v-icon size="medium" icon="mdi-ticket"></v-icon> Pricing</v-card-title>
            <v-card-text style="white-space: pre-line;" v-html="obj.pricing">
            </v-card-text>
        </div>

        <div v-if="obj.address">
        <v-divider class="mx-4 mb-1"></v-divider>
        <v-card-title><v-icon size="medium" icon="mdi-map-marker"></v-icon> Location</v-card-title>
        <v-card-text style="white-space: pre-line;">
            {{ obj.address }}
            <br>
            {{ obj.country_name }}
        </v-card-text>

        <div v-if="obj.longitude">
        <v-card-text>
            <div style="height:400px; width:100%">
                <LMap ref="map" :zoom="zoom" :center="coordinates">
                    <LTileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" layer-type="base"
                        name="OpenStreetMap"></LTileLayer>
                    <LMarker :lat-lng="coordinates" draggable> </LMarker>
                </LMap>
            </div>
        </v-card-text>
        </div>
        </div>
    </v-card>
</template>
