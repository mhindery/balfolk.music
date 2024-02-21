

<template>
    <v-sheet class="pa-2 mx-auto">
        <h4 class="text-h5 font-weight-bold mb-4">Export events to your calendar</h4>
        <p>Here you can export events from this site to your preferred calendar application.</p>
        <br>

        <v-select
            chips
            label="Select the event types you want to include"
            multiple
            variant="outlined"
            v-model="eventTypeSelected"
            :items="eventTypes"
            @update:modelValue="constructIcalLink"
        ></v-select>

        <p class="pb-4">You can download an .ics file by clicking the button below. This file contains all events from this site at this point in time.</p>
        <a style="text-decoration: none; color: inherit;" :href="icalLink">
            <v-btn size="large" prepend-icon="mdi-file-download-outline" block color="blue">Download ICS file</v-btn>
        </a>

        <br>
        <v-divider></v-divider>
        <p class="py-4">You can copy the link to the calendar by clicking the button below. You can subscribe to this calendar as a feed in your own calendar application (e.g. in Google calendar of your own account).</p>
        <v-btn size="large" prepend-icon="mdi-content-copy" block color="blue" @click="copyText">Copy Ical link to clipboard</v-btn>
    </v-sheet>
</template>

<script setup>
import { ref } from 'vue';

const eventTypes = [{title: 'Festivals', value: 'festival'}, { title: 'Balls', value: 'ball' }, { title: 'Classes / Worshops', value: 'course' }];
const eventTypeSelected = ref(['festival', 'ball', 'course']);
const icalLink = ref('');

function constructIcalLink(selectedValues) {
    let event_types = eventTypeSelected.value.join(',');
    icalLink.value = location.protocol + '//' + location.hostname + '/events/feed.ics' + '?event_type=' + event_types;
}

constructIcalLink()

function copyText() {
    navigator.clipboard.writeText(icalLink.value);
}

</script>
