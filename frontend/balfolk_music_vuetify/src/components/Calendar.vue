<script setup>
// const props = defineProps(['id',]);

import { ref } from 'vue'
import { useDate } from 'vuetify'
import axios from 'axios'

const events = ref([]);
const value = ref([new Date()]);
const weekday = ref([1, 2, 3, 4, 5, 6, 0]);
const viewmode = ref("month");
const viewmodes = ['month', 'week', 'day'];
const loading = ref(true);
const showAdjacent = ref(true);

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

function getStartDate(event)  {
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
    // console.log(start)
    // console.log(end)

    loading.value = true;
    var response = await axios.get("/api/calendar_events/");
    // console.log(response)

    response.data.forEach(element => {
        events.value.push({
            title: getTitle(element),
            start: getStartDate(element),
            end: getEndDate(element),
            color: getColor(element),
            // color: this.colors[this.rnd(0, this.colors.length - 1)],
            allDay: false,
        })
    });

    // console.log(events)


    loading.value = false;
}

getEvents(1, 2)

</script>

<template>
        <v-sheet
          tile
          height="54"
          class="d-flex"
        >
          <v-select
            v-model="viewmode"
            :items="viewmodes"
            dense
            variant="outlined"
            hide-details
            class="ma-2"
            label="View Mode"
          ></v-select>
        </v-sheet>
    <v-sheet>
          <v-calendar
            ref="calendar"
            v-model="value"
            :weekdays="weekday"
            :view-mode="viewmode"
            :events="events"
            :show-adjacent-months="showAdjacent"
          ></v-calendar>
    </v-sheet>
</template>
