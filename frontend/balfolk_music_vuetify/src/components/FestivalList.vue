<template>
    <div>
        <!-- Search box -->
        <v-text-field class="pb-1" v-model="search" hide-details placeholder="Search" prepend-inner-icon="mdi-magnify"
            variant="underlined"></v-text-field>

        <!-- Tabs header -->
        <v-tabs v-model="tab" fixed-tabs class="mb-3">
            <v-tab value=upcoming>Upcoming</v-tab>
            <v-tab value=past>Past</v-tab>
        </v-tabs>

        <!-- Tab content -->
        <v-window v-model="tab">
            <div v-if="loading">
                <v-row dense>
                    <v-col v-for="x in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0]" cols="12" lg="4" md="6" sm="12">
                        <v-skeleton-loader type="list-item-avatar-three-line"></v-skeleton-loader>
                    </v-col>
                </v-row>
            </div>
            <v-window-item value=upcoming>
                <v-data-iterator :items="get_upcoming_events(objects)" :items-per-page="30" :search="search">
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
            </v-window-item>
            <v-window-item value=past>
                <v-data-iterator :items="get_past_events(objects)" :items-per-page="30" :search="search">
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
            </v-window-item>
        </v-window>
    </div>
</template>

<script setup>
import FestivalCard from './FestivalCard.vue';
import { ref, onMounted } from 'vue';
import { get_upcoming_events, get_past_events, fetchEventData } from "@/utils/utils";

const objects = ref([]);
const loading = ref(true);
const tab = ref(0);
const search = ref('');

onMounted(
    () => fetchEventData('festival', objects, loading)
);
</script>
