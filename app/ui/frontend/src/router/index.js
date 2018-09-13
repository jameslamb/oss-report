import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import Router from 'vue-router'
import ActivityStats from '@/components/ActivityStats.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      components: {
        activity_stats: ActivityStats
      }
    }
  ]
})
