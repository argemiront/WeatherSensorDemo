import Vue from 'vue'
import Router from 'vue-router'
import MainMaps from '@/components/MainMaps'
import AddSensor from '@/components/AddSensor'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'gmap-map',
      component: MainMaps
    },
    {
      path: '/add',
      name: 'add-sensor',
      component: AddSensor
    }
  ]
})
