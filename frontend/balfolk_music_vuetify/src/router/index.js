/**
 * router/index.ts
 *
 * Automatic routes for `./src/pages/*.vue`
 */

// Composables
import { createRouter, createWebHistory } from 'vue-router'
import FestivalList from '../components/FestivalList.vue'
import FestivalDetail from '../components/FestivalDetail.vue'
import BallList from '../components/BallList.vue'
import BallDetail from '../components/BallDetail.vue'
import CourseList from '../components/CourseList.vue'
import CourseDetail from '../components/CourseDetail.vue'
import EventAdd from '../components/EventAdd.vue'
// import { setupLayouts } from 'virtual:generated-layouts'

const routes = [
  { path: '/', name: 'Index', component: FestivalList },
  { path: '/festivals', name: 'FestivalList', component: FestivalList, props: true },
  { path: '/festivals/:id', name: 'FestivalDetail', component: FestivalDetail, props: true },
  { path: '/balls', name: 'BallList', component: BallList, props: true },
  { path: '/balls/:id', name: 'BallDetail', component: BallDetail, props: true },
  { path: '/courses', name: 'CourseList', component: CourseList, props: true },
  { path: '/courses/:id', name: 'CourseDetail', component: CourseDetail, props: true },
  { path: '/add', name: 'EventAdd', component: EventAdd, props: true },
  // { path: '/workshops', component: FestivalList },
  // { path: '/music', component: FestivalList },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
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
