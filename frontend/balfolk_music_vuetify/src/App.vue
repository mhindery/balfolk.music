<template>
  <v-app>
    <v-container>
      <v-app-bar scroll-behavior="collapse" :elevation="2" color="teal-darken-4"
        image="https://picsum.photos/1920/1080?random">

        <template v-slot:image>
          <v-img gradient="to top right, rgba(19,84,122,.8), rgba(128,208,199,.8)"></v-img>
        </template>

        <template v-slot:prepend>
          <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
        </template>

        <v-app-bar-title>Balfolk.music</v-app-bar-title>

        <template v-slot:append>
          <!-- <v-btn icon="mdi-heart"></v-btn> -->

          <!--  'How to call function from subcomponent '?' -->
          <!-- <v-btn @click="fetchFestivalListData" icon="mdi-refresh"></v-btn> -->

          <!-- <v-btn icon="mdi-dots-vertical"></v-btn> -->
        </template>
      </v-app-bar>

      <v-navigation-drawer v-model="drawer" temporary>
        <v-list nav>
          <v-list-item prepend-icon="mdi-tent" title="Festivals" value="festivals"
            :to="{ name: 'FestivalList' }"></v-list-item>
          <v-list-item prepend-icon="mdi-party-popper" title="Bals" value="bals" :to="{ name: 'BallList' }"></v-list-item>
          <v-list-item prepend-icon="mdi-school" title="Courses / Workshops" value="courses_workshops"
            :to="{ name: 'CourseList' }"></v-list-item>
            <v-list-item prepend-icon="mdi-plus-circle-outline" title="Add event" value="add_event"
              :to="{ name: 'EventAdd' }"></v-list-item>
        </v-list>
      </v-navigation-drawer>

      <v-main>
        <router-view />
      </v-main>

    </v-container>
  </v-app>
</template>

<script setup>
import { ref } from 'vue';

const drawer = ref(0);
drawer.value = true;
</script>
