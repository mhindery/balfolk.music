<script setup>
// const props = defineProps(['id',]);

import { ref } from 'vue'
import { useDate } from 'vuetify'
import axios from 'axios'

const events = ref([]);
const value = ref([new Date()]);
const weekday = ref([0, 1, 2, 3, 4, 5, 6]);
const viewmode = ref("month");
const loading = ref(true);
const showAdjacent = ref(true);

function getColor(event) {
    if (event.event_type == "ball") {
        return "blue"
    }
    if (event.event_type == "ball") {
        return "red"
    }
    return "green"
}

async function getEvents(start, end) {
    // console.log(start)
    // console.log(end)

    loading.value = true;
    // var response = await axios.get("http://localhost:8000/api/calendar_events/");
    var response = await axios.get("/api/calendar_events/");
    // console.log(response)

    response.data.forEach(element => {
        events.value.push({
            title: element.name,
            start: new Date(element.starting_datetime),
            end: new Date(element.ending_datetime),
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
