/**
 * router/index.ts
 *
 * Automatic routes for `./src/pages/*.vue`
 */

// Composables
import { createRouter, createWebHistory } from 'vue-router'
import FestivalList from '../components/FestivalList.vue'
import BallList from '../components/BallList.vue'
import EventDetail from '../components/EventDetail.vue'
import CourseList from '../components/CourseList.vue'
import EventAddEdit from '../components/EventAddEdit.vue'
import Calendar from '../components/Calendar.vue'
import Playlists from '../components/Playlists.vue'
import ICalFeed from '../components/ICalFeed.vue'

// import { setupLayouts } from 'virtual:generated-layouts'

const routes = [
  { path: '/', name: 'Index', meta: {title: 'Balfolk.music'}, component: FestivalList },
  { path: '/festivals/', name: 'FestivalList', meta: {title: 'Balfolk.music > Festivals'}, component: FestivalList, props: true },
  { path: '/festivals/:id/', name: 'FestivalDetail', meta: {title: 'Balfolk.music > Event details'}, component: EventDetail, props: route => ({ id: route.params.id, apiURL: '/events/' }) },
  { path: '/balls/', name: 'BallList', meta: {title: 'Balfolk.music > Balls'}, component: BallList, props: true },
  { path: '/balls/:id/', name: 'BallDetail', meta: {title: 'Balfolk.music > Event details'}, component: EventDetail, props: route => ({ id: route.params.id, apiURL: '/events/' }) },
  { path: '/courses/', name: 'CourseList', meta: {title: 'Balfolk.music > Courses/Workshops'}, component: CourseList, props: true },
  { path: '/courses/:id/', name: 'CourseDetail', meta: {title: 'Balfolk.music > Event details'}, component: EventDetail, props: route => ({ id: route.params.id, apiURL: '/events/' }) },
  { path: '/add/', name: 'EventAdd', meta: {title: 'Balfolk.music > Add new event'}, component: EventAddEdit, props: true },
  { path: '/edit/:id/', name: 'EventEdit', meta: { title: 'Balfolk.music > Edit event' }, component: EventAddEdit, props: true },
  { path: '/calendar/', name: 'Calendar', meta: {title: 'Balfolk.music > Calendar'}, component: Calendar, props: true },
  { path: '/icalfeed/', name: 'ICalFeed', meta: { title: 'Balfolk.music > ICal feed' }, component: ICalFeed, props: true },
  { path: '/playlists/', name: 'Playlists', meta: {title: 'Balfolk.music > Playlists'}, component: Playlists, props: true },

]

const router = createRouter({
  history: createWebHistory(),
  routes: routes,
})

// router.beforeEach((to, from, next) => {
//   document.title = to.meta?.title ?? 'Balfolk.music'
//   // const titleFromParams = to.query?.pageTitle

//   // if (titleFromParams) {
//   //   document.title = `${titleFromParams} - ${document.title}`
//   // } else {
//   //   document.title = to.meta?.title ?? 'Balfolk.music'
//   // }
// })

export default router
