<script setup>
// const props = defineProps(['id',]);

import { ref } from 'vue';
import { useDate } from 'vuetify';
import axios from 'axios';
import { getCountriesToSelect } from "@/utils/utils";

const events = ref([]);
const value = ref([new Date()]);
const eventTypes = [{ title: 'Festivals', value: 'festival' }, { title: 'Balls', value: 'ball' }, { title: 'Classes / Worshops', value: 'course' }];
const eventTypeSelected = ref(['festival', 'ball', 'course']);
const weekday = ref([1, 2, 3, 4, 5, 6, 0]);
const viewmode = ref("month");
const viewmodes = ['month', 'week', 'day'];
const loading = ref(true);
const showAdjacent = ref(true);

const countriesSelected = ref(['BE']);

function getColor(event) {
    if (event.event_type == "ball") {
        return "blue"
    }
    if (event.event_type == "festival") {
        return "red"
    }
    return "green"
}

function getLink(event) {
    if (event.event_type == "ball") {
        return "/api/balls/" + event.id;
    }
    if (event.event_type == "festival") {
        return "/api/festivals/" + event.id;
    }
    return "/api/courses/" + event.id;
}

function getTitle(event) {

    let text = event.name + ' (' + event.country_code + ')';
    let href = getLink(event);

    return text;
    // return '<a href="' + href + '">' + text + '</a>';
}

function getStartDate(event) {
    let a = new Date(event.starting_datetime);
    let userTimezoneOffset = a.getTimezoneOffset() * 60000;
    return new Date(a - userTimezoneOffset * Math.sign(userTimezoneOffset));
}

function getEndDate(event) {
    let a = new Date(event.ending_datetime);
    let userTimezoneOffset = a.getTimezoneOffset() * 60000;
    return new Date(a - userTimezoneOffset * Math.sign(userTimezoneOffset));
}

async function getEvents(start, end) {
    loading.value = true;
    let event_types = eventTypeSelected.value.join('&event_type=');
    let countries = countriesSelected.value.join('&country=');
    var response = await axios.get("/events/calendar/?event_type=" + event_types + '&country=' + countries);

    events.value = [];

    response.data.forEach(element => {
        events.value.push({
            title: getTitle(element),
            start: getStartDate(element),
            end: getEndDate(element),
            color: getColor(element),
            allDay: false,
        })
    });

    loading.value = false;
}

getEvents(1, 2)

</script>

<template>
    <v-progress-linear :active="loading" color="deep-purple" height="4" indeterminate></v-progress-linear>

    <v-sheet tile height="58" class="d-flex">
        <v-select v-model="viewmode" :items="viewmodes" variant="outlined" class="mb-3" label="View Mode"></v-select>
        <v-select chips label="Event types" multiple variant="outlined" v-model="eventTypeSelected" :items="eventTypes"
            @update:modelValue="getEvents(1, 2)" class="mb-3">
        </v-select>
        <v-select label="Country" v-model="countriesSelected" variant="outlined" item-value="alpha_2" item-title="name"
            multiple :items="getCountriesToSelect()" @update:modelValue="getEvents(1, 2)">

            <template v-slot:selection="{ item, index }">
                <v-chip v-if="index < 3">
                    <span>{{ item.title }}</span>
                </v-chip>
                <span v-if="index === 3" class="text-grey text-caption align-self-center">
                    (+{{ countriesSelected.length - 3 }} others)
                </span>
            </template>
        </v-select>

    </v-sheet>
    <v-sheet>
        <v-calendar ref="calendar" v-model="value" :weekdays="weekday" :view-mode="viewmode" :events="events"
            :show-adjacent-months="showAdjacent"></v-calendar>
    </v-sheet>
</template>
