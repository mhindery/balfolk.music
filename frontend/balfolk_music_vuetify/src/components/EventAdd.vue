<script setup>
// const props = defineProps(['id',]);

import { ref } from 'vue';
import axios from 'axios'

const isFormValid = ref(false);

const eventType = ref('ball');
const eventName = ref('');
const eventOrganizer = ref('');
const eventDescription = ref('');
const eventSite = ref('');
const eventFacebook = ref('');
const eventBanner = ref('');
const eventPoster = ref('');
const eventSchedule = ref('');
const eventPricing = ref('');
const eventAddress = ref('');
const eventDates = ref([]);
const eventStartTime = ref('18:30:00');
const eventEndTime = ref('23:30:00');
const eventCity = ref('');
const eventCountry = ref('');

const loading = ref(false);


// Country names object using 2-letter country codes to reference country name
// ISO 3166 Alpha-2 Format: [2 letter Country Code]: [Country Name]
// Sorted alphabetical by country name (special characters on bottom)
const countryListAlpha2 = {
    "AF": "Afghanistan",
    "AL": "Albania",
    "DZ": "Algeria",
    "AS": "American Samoa",
    "AD": "Andorra",
    "AO": "Angola",
    "AI": "Anguilla",
    "AQ": "Antarctica",
    "AG": "Antigua and Barbuda",
    "AR": "Argentina",
    "AM": "Armenia",
    "AW": "Aruba",
    "AU": "Australia",
    "AT": "Austria",
    "AZ": "Azerbaijan",
    "BS": "Bahamas (the)",
    "BH": "Bahrain",
    "BD": "Bangladesh",
    "BB": "Barbados",
    "BY": "Belarus",
    "BE": "Belgium",
    "BZ": "Belize",
    "BJ": "Benin",
    "BM": "Bermuda",
    "BT": "Bhutan",
    "BO": "Bolivia (Plurinational State of)",
    "BQ": "Bonaire, Sint Eustatius and Saba",
    "BA": "Bosnia and Herzegovina",
    "BW": "Botswana",
    "BV": "Bouvet Island",
    "BR": "Brazil",
    "IO": "British Indian Ocean Territory (the)",
    "BN": "Brunei Darussalam",
    "BG": "Bulgaria",
    "BF": "Burkina Faso",
    "BI": "Burundi",
    "CV": "Cabo Verde",
    "KH": "Cambodia",
    "CM": "Cameroon",
    "CA": "Canada",
    "KY": "Cayman Islands (the)",
    "CF": "Central African Republic (the)",
    "TD": "Chad",
    "CL": "Chile",
    "CN": "China",
    "CX": "Christmas Island",
    "CC": "Cocos (Keeling) Islands (the)",
    "CO": "Colombia",
    "KM": "Comoros (the)",
    "CD": "Congo (the Democratic Republic of the)",
    "CG": "Congo (the)",
    "CK": "Cook Islands (the)",
    "CR": "Costa Rica",
    "HR": "Croatia",
    "CU": "Cuba",
    "CW": "Curaçao",
    "CY": "Cyprus",
    "CZ": "Czechia",
    "CI": "Côte d'Ivoire",
    "DK": "Denmark",
    "DJ": "Djibouti",
    "DM": "Dominica",
    "DO": "Dominican Republic (the)",
    "EC": "Ecuador",
    "EG": "Egypt",
    "SV": "El Salvador",
    "GQ": "Equatorial Guinea",
    "ER": "Eritrea",
    "EE": "Estonia",
    "SZ": "Eswatini",
    "ET": "Ethiopia",
    "FK": "Falkland Islands (the) [Malvinas]",
    "FO": "Faroe Islands (the)",
    "FJ": "Fiji",
    "FI": "Finland",
    "FR": "France",
    "GF": "French Guiana",
    "PF": "French Polynesia",
    "TF": "French Southern Territories (the)",
    "GA": "Gabon",
    "GM": "Gambia (the)",
    "GE": "Georgia",
    "DE": "Germany",
    "GH": "Ghana",
    "GI": "Gibraltar",
    "GR": "Greece",
    "GL": "Greenland",
    "GD": "Grenada",
    "GP": "Guadeloupe",
    "GU": "Guam",
    "GT": "Guatemala",
    "GG": "Guernsey",
    "GN": "Guinea",
    "GW": "Guinea-Bissau",
    "GY": "Guyana",
    "HT": "Haiti",
    "HM": "Heard Island and McDonald Islands",
    "VA": "Holy See (the)",
    "HN": "Honduras",
    "HK": "Hong Kong",
    "HU": "Hungary",
    "IS": "Iceland",
    "IN": "India",
    "ID": "Indonesia",
    "IR": "Iran (Islamic Republic of)",
    "IQ": "Iraq",
    "IE": "Ireland",
    "IM": "Isle of Man",
    "IL": "Israel",
    "IT": "Italy",
    "JM": "Jamaica",
    "JP": "Japan",
    "JE": "Jersey",
    "JO": "Jordan",
    "KZ": "Kazakhstan",
    "KE": "Kenya",
    "KI": "Kiribati",
    "KP": "Korea (the Democratic People's Republic of)",
    "KR": "Korea (the Republic of)",
    "KW": "Kuwait",
    "KG": "Kyrgyzstan",
    "LA": "Lao People's Democratic Republic (the)",
    "LV": "Latvia",
    "LB": "Lebanon",
    "LS": "Lesotho",
    "LR": "Liberia",
    "LY": "Libya",
    "LI": "Liechtenstein",
    "LT": "Lithuania",
    "LU": "Luxembourg",
    "MO": "Macao",
    "MG": "Madagascar",
    "MW": "Malawi",
    "MY": "Malaysia",
    "MV": "Maldives",
    "ML": "Mali",
    "MT": "Malta",
    "MH": "Marshall Islands (the)",
    "MQ": "Martinique",
    "MR": "Mauritania",
    "MU": "Mauritius",
    "YT": "Mayotte",
    "MX": "Mexico",
    "FM": "Micronesia (Federated States of)",
    "MD": "Moldova (the Republic of)",
    "MC": "Monaco",
    "MN": "Mongolia",
    "ME": "Montenegro",
    "MS": "Montserrat",
    "MA": "Morocco",
    "MZ": "Mozambique",
    "MM": "Myanmar",
    "NA": "Namibia",
    "NR": "Nauru",
    "NP": "Nepal",
    "NL": "Netherlands (the)",
    "NC": "New Caledonia",
    "NZ": "New Zealand",
    "NI": "Nicaragua",
    "NE": "Niger (the)",
    "NG": "Nigeria",
    "NU": "Niue",
    "NF": "Norfolk Island",
    "MP": "Northern Mariana Islands (the)",
    "NO": "Norway",
    "OM": "Oman",
    "PK": "Pakistan",
    "PW": "Palau",
    "PS": "Palestine, State of",
    "PA": "Panama",
    "PG": "Papua New Guinea",
    "PY": "Paraguay",
    "PE": "Peru",
    "PH": "Philippines (the)",
    "PN": "Pitcairn",
    "PL": "Poland",
    "PT": "Portugal",
    "PR": "Puerto Rico",
    "QA": "Qatar",
    "MK": "Republic of North Macedonia",
    "RO": "Romania",
    "RU": "Russian Federation (the)",
    "RW": "Rwanda",
    "RE": "Réunion",
    "BL": "Saint Barthélemy",
    "SH": "Saint Helena, Ascension and Tristan da Cunha",
    "KN": "Saint Kitts and Nevis",
    "LC": "Saint Lucia",
    "MF": "Saint Martin (French part)",
    "PM": "Saint Pierre and Miquelon",
    "VC": "Saint Vincent and the Grenadines",
    "WS": "Samoa",
    "SM": "San Marino",
    "ST": "Sao Tome and Principe",
    "SA": "Saudi Arabia",
    "SN": "Senegal",
    "RS": "Serbia",
    "SC": "Seychelles",
    "SL": "Sierra Leone",
    "SG": "Singapore",
    "SX": "Sint Maarten (Dutch part)",
    "SK": "Slovakia",
    "SI": "Slovenia",
    "SB": "Solomon Islands",
    "SO": "Somalia",
    "ZA": "South Africa",
    "GS": "South Georgia and the South Sandwich Islands",
    "SS": "South Sudan",
    "ES": "Spain",
    "LK": "Sri Lanka",
    "SD": "Sudan (the)",
    "SR": "Suriname",
    "SJ": "Svalbard and Jan Mayen",
    "SE": "Sweden",
    "CH": "Switzerland",
    "SY": "Syrian Arab Republic",
    "TW": "Taiwan",
    "TJ": "Tajikistan",
    "TZ": "Tanzania, United Republic of",
    "TH": "Thailand",
    "TL": "Timor-Leste",
    "TG": "Togo",
    "TK": "Tokelau",
    "TO": "Tonga",
    "TT": "Trinidad and Tobago",
    "TN": "Tunisia",
    "TR": "Turkey",
    "TM": "Turkmenistan",
    "TC": "Turks and Caicos Islands (the)",
    "TV": "Tuvalu",
    "UG": "Uganda",
    "UA": "Ukraine",
    "AE": "United Arab Emirates (the)",
    "GB": "United Kingdom of Great Britain and Northern Ireland (the)",
    "UM": "United States Minor Outlying Islands (the)",
    "US": "United States of America (the)",
    "UY": "Uruguay",
    "UZ": "Uzbekistan",
    "VU": "Vanuatu",
    "VE": "Venezuela (Bolivarian Republic of)",
    "VN": "Viet Nam",
    "VG": "Virgin Islands (British)",
    "VI": "Virgin Islands (U.S.)",
    "WF": "Wallis and Futuna",
    "EH": "Western Sahara",
    "YE": "Yemen",
    "ZM": "Zambia",
    "ZW": "Zimbabwe",
    "AX": "Åland Islands"
};

function getDatesToSelect(){
    const datesToSelect = [];
    for (let index = 0; index < 365; index++) {
        let d = new Date();
        d.setDate(d.getDate() + index);
        datesToSelect.push(d.toJSON().slice(0, 10))

    }
    return datesToSelect
}




async function submit(event) {
    console.log(isFormValid);
    if (isFormValid.value == true) {
        loading.value = true

        let postData = {
            'event_type': eventType.value,
            'name': eventName.value,
            'organizer': eventOrganizer.value,
            'description': eventDescription.value,
            'site': eventSite.value,
            'facebook': eventFacebook.value,
            'schedule': eventSchedule.value,
            'pricing': eventPricing.value,
            'address': eventAddress.value,
            'dates': eventDates.value,
            'start_timestamp': eventStartTime.value,
            'end_timestamp': eventEndTime.value,
        }

        console.log('posting...')

        // console.log(postData);

        // axios.post('http://localhost:8000/events/api/create', postData)
        axios.post('/events/api/create', postData)
            .then((response) => {
                loading.value = false;
                console.log(response.data);
                window.open(response.data['balfolk_music_url']);
            }, (error) => {
                loading.value = false;
                console.log(error);
            });

    } else {
        console.log('Form not valid');
    }
}

const rules = {
    required: value => !!value || 'Field is required',
};

</script>

<template>
    <v-sheet class="mx-auto">
        <h1>Add a new event</h1>
        <p>Fill in the information below to add a new event to the site.</p>
        <v-divider class="ma-4"></v-divider>
        <v-form v-model="isFormValid" @submit.prevent="submit">

            <h4 class="my-4">Basic information</h4>

            <h5 class="my-4">Which type of event is this?</h5>
            <v-radio-group v-model="eventType">
                <v-radio label="Ball" value="ball"></v-radio>
                <v-radio label="Festival" value="festival"></v-radio>
                <v-radio label="Course / Workshop" value="course"></v-radio>
            </v-radio-group>

            <v-text-field v-model="eventName" :rules="[rules.required]" label="Event name"></v-text-field>
            <v-text-field v-model="eventOrganizer" :rules="[rules.required]" label="Organizer"></v-text-field>

            <v-textarea v-model="eventDescription" auto-grow :rules="[rules.required]" label="Description"></v-textarea>

            <v-divider></v-divider>
            <h4 class="my-4">When is the event</h4>

            <v-select label="Date(s)" :rules="[rules.required]" multiple v-model="eventDates"
                :items="getDatesToSelect()"></v-select>

            <v-row>
                <v-col cols="6">
                    <v-text-field label="Start time" :rules="[rules.required]" v-model="eventStartTime"
                        type="time"></v-text-field>
                </v-col>
                <v-col cols="6">
                    <v-text-field label="End time" :rules="[rules.required]" v-model="eventEndTime"
                        type="time"></v-text-field>
                </v-col>
            </v-row>


            <v-divider></v-divider>
            <h4 class="my-4">Where is the event</h4>

            <v-textarea prepend-inner-icon="mdi-map-marker" v-model="eventAddress" :rules="[rules.required]"
                label="Full address information"></v-textarea>

            <v-row>
                <v-col cols="6">
                    <v-text-field v-model="eventCity" :rules="[rules.required]"
                        label="City"></v-text-field>
                </v-col>
                <v-col cols="6">
                    <v-select label="Country" v-model="eventCountry" :rules="[rules.required]" item-value="alpha_2"
                        item-title="name"
                        :items="Object.keys(countryListAlpha2).map((key) => ({ alpha_2: key, name: countryListAlpha2[key] }))"></v-select>

                </v-col>
            </v-row>


            <v-divider></v-divider>
            <h4 class="my-4">Extended information</h4>

            <v-row dense>
                <v-col cols="12" sm="12" md="6" lg="6">
                    <v-text-field prepend-inner-icon="mdi-web" v-model="eventSite" label="Website"></v-text-field>
                </v-col>
                <v-col cols="12" sm="12" md="6" lg="6">
                    <v-text-field prepend-inner-icon="mdi-facebook" v-model="eventFacebook"
                        label="Facebook event link"></v-text-field>
                </v-col>
                <v-col cols="12" sm="12" md="6" lg="6">
                    <v-text-field prepend-inner-icon="mdi-image" v-model="eventBanner"
                        label="Banner image link"></v-text-field>
                </v-col>
                <v-col cols="12" sm="12" md="6" lg="6">
                    <v-text-field prepend-inner-icon="mdi-image" v-model="eventPoster"
                        label="Poster image link"></v-text-field>
                </v-col>
            </v-row>

            <p>Provide some information about the schedule of the event. Which bands are playing at what time? Is there an initiation?</p>
            <v-textarea prepend-inner-icon="mdi-clock-outline" v-model="eventSchedule" auto-grow label="Schedule information"></v-textarea>
            <p>Provide some information about the ticket prices and formulas.</p>
            <v-textarea prepend-inner-icon="mdi-ticket" v-model="eventPricing" auto-grow label="Pricing information"></v-textarea>


            <v-btn type="submit" block class="mt-2">Submit</v-btn>
        </v-form>
    </v-sheet>
</template>
