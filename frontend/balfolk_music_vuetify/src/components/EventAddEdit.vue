<script setup>
// const props = defineProps(['id',]);

import { ref } from 'vue';
import axios from 'axios';
import { useRoute } from "vue-router";
import { getCountriesToSelect  } from "@/utils/utils";

const model = defineModel();

const isFormValid = ref(false);
const submitting = ref(false);
const success = ref(false);

const obj = ref({
    event_type: 'ball',
    name: '',
    organizer: '',
    description: '',
    site: '',
    facebook: '',
    banner: '',
    poster: '',
    schedule: '',
    pricing: '',
    address: '',
    city: '',
    country: '',
    dates: [],
    starttime: '18:30:00',
    endtime: '23:30:00',
    id: -1
});

const isNewEvent = ref(true);
const loading = ref(false);

async function loadExistingEvent(id) {
    var response = await axios.get('/events/' + id + '/');
    // console.log(response.data);
    obj.value.name = response.data.name;
    obj.value.organizer = response.data.organizer;
    obj.value.description = response.data.description;
    obj.value.site = response.data.site;
    obj.value.facebook = response.data.facebook;
    obj.value.banner = response.data.banner_image;
    obj.value.poster = response.data.poster_image;
    obj.value.schedule = response.data.schedule;
    obj.value.dates = response.data.dates;
    obj.value.pricing = response.data.pricing;
    obj.value.address = response.data.address;
    obj.value.city = response.data.city;
    obj.value.country = response.data.country_code;
    obj.value.starttime = response.data.start_timestamp;
    obj.value.endtime = response.data.end_timestamp;
    obj.value.endtime = response.data.end_timestamp;
    obj.value.event_type = response.data.event_type;
    obj.value.id = response.data.id;
}

const routeParams = useRoute().params;

if ('id' in routeParams) {
    isNewEvent.value = false;
    loadExistingEvent(routeParams.id);
} else {

}

function getDatesToSelect(){
    const datesToSelect = [];
    for (let index = -400; index < 400; index++) {
        let d = new Date();
        d.setDate(d.getDate() + index);
        datesToSelect.push(d.toJSON().slice(0, 10))

    }
    return datesToSelect
}

const sleep = (delay) => new Promise((resolve) => setTimeout(resolve, delay))

async function submit(event) {

    if (isFormValid.value == true) {
        let postData = {
            'id': obj.value.id,
            'event_type': obj.value.event_type,
            'name': obj.value.name,
            'organizer': obj.value.organizer,
            'description': obj.value.description,
            'site': obj.value.site,
            'facebook': obj.value.facebook,
            'schedule': obj.value.schedule,
            'pricing': obj.value.pricing,
            'address': obj.value.address,
            'dates': obj.value.dates,
            'start_timestamp': obj.value.starttime,
            'end_timestamp': obj.value.endtime,
        }

        // console.log(obj);
        // console.log(postData);
        // { headers: { 'X - CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value } }

        let redirectTo = "";

        submitting.value = true;
        loading.value = true;

        await sleep(1000);

        if (obj.value.id == -1) {
            // Submit new event
            axios.post('/events/create', postData)
                .then((response) => {
                    redirectTo = response.data['balfolk_music_url'];
                }, (error) => {
                    console.log(error);
                    return;
                });

        } else {
            // Edit existing event
            axios.put('/events/' + obj.value.id + '/', postData)
                .then((response) => {
                    redirectTo = response.data['balfolk_music_url'];
                }, (error) => {
                    console.log(error);
                    return;
                });
        }

        loading.value = false;
        submitting.value = false;
        success.value = true;
        await sleep(2000);
        window.location.href = redirectTo;

    } else {
        alert('Form is not valid');
    }
}

const rules = {
    required: value => !!value || 'Field is required',
};

</script>

<template>
    <v-sheet class="mx-auto">
        <h1>{{ isNewEvent? 'Add a new event' : 'Edit existing event: ' + obj.name }}</h1>
        <p v-if="isNewEvent">Fill in the information below to add a new event to the site and save at the bottom of the page.</p>
        <p v-if="!isNewEvent">Update the information of the event below and save at the bottom of the page.</p>
        <v-divider class="ma-4"></v-divider>
        <v-form v-model="isFormValid" @submit.prevent="submit">

            <h4 class="my-4">Basic information</h4>

            <h5 class="my-4">Which type of event is this?</h5>
            <v-radio-group v-model="obj.event_type">
                <v-radio label="Ball" value="ball"></v-radio>
                <v-radio label="Festival" value="festival"></v-radio>
                <v-radio label="Course / Workshop" value="course"></v-radio>
            </v-radio-group>

            <v-text-field v-model="obj.name" :rules="[rules.required]" label="Event name"></v-text-field>
            <v-text-field v-model="obj.organizer" :rules="[rules.required]" label="Organizer"></v-text-field>

            <v-textarea v-model="obj.description" auto-grow :rules="[]" label="Description"></v-textarea>

            <v-divider></v-divider>
            <h4 class="my-4">When is the event</h4>

            <v-select label="Date(s)" :rules="[rules.required]" multiple v-model="obj.dates" :items="getDatesToSelect()"></v-select>

            <v-row>
                <v-col cols="6">
                    <v-text-field label="Start time" :rules="[rules.required]" v-model="obj.starttime"
                        type="time"></v-text-field>
                </v-col>
                <v-col cols="6">
                    <v-text-field label="End time" :rules="[rules.required]" v-model="obj.endtime"
                        type="time"></v-text-field>
                </v-col>
            </v-row>


            <v-divider></v-divider>
            <h4 class="my-4">Where is the event</h4>

            <v-textarea prepend-inner-icon="mdi-map-marker" v-model="obj.address" :rules="[]"
                label="Full address information"></v-textarea>

            <v-row>
                <v-col cols="6">
                    <v-text-field v-model="obj.city" :rules="[rules.required]"
                        label="City"></v-text-field>
                </v-col>
                <v-col cols="6">
                    <v-select label="Country" v-model="obj.country" :rules="[rules.required]" item-value="alpha_2"
                        item-title="name"
                        :items="getCountriesToSelect()"></v-select>

                </v-col>
            </v-row>


            <v-divider></v-divider>
            <h4 class="my-4">Extended information</h4>

            <v-row dense>
                <v-col cols="12" sm="12" md="6" lg="6">
                    <v-text-field prepend-inner-icon="mdi-web" v-model="obj.site" label="Website"></v-text-field>
                </v-col>
                <v-col cols="12" sm="12" md="6" lg="6">
                    <v-text-field prepend-inner-icon="mdi-facebook" v-model="obj.facebook"
                        label="Facebook event link"></v-text-field>
                </v-col>
                <v-col cols="12" sm="12" md="6" lg="6">
                    <v-text-field prepend-inner-icon="mdi-image" v-model="obj.banner" label="Banner image link"></v-text-field>
                    <v-container v-if="obj.banner">
                        <h5>Banner image preview:</h5>
                        <v-img cover :src="obj.banner"></v-img>
                    </v-container>
                </v-col>
                <v-col cols="12" sm="12" md="6" lg="6">
                    <v-text-field prepend-inner-icon="mdi-image" v-model="obj.poster" label="Poster image link"></v-text-field>
                    <v-container v-if="obj.poster">
                        <h5>Poster image preview:</h5>
                        <v-img cover :src="obj.poster"></v-img>
                    </v-container>
                </v-col>
            </v-row>

            <br>

            <p>Provide some information about the schedule or line-up of the event. Which bands are playing at what time? Is there an initiation?</p>
            <v-textarea prepend-inner-icon="mdi-clock-outline" v-model="obj.schedule" auto-grow label="Schedule information"></v-textarea>
            <p>Provide some information about the ticket prices and formulas.</p>
            <v-textarea prepend-inner-icon="mdi-ticket" v-model="obj.pricing" auto-grow label="Pricing information"></v-textarea>

            <v-alert type="warning" v-if="!isFormValid" text="There are errors on the form, or not all required data is provided. Please fix these before you can submit."></v-alert>
            <v-progress-linear :active="submitting" color="deep-purple" height="4" indeterminate></v-progress-linear>
            <v-alert type="success" v-if="success" text="Success. Redirecting you to event page ..."></v-alert>

            <v-btn :disabled="!isFormValid" color="blue"  type="submit" block class="mt-2">Save</v-btn>
        </v-form>
    </v-sheet>
</template>
