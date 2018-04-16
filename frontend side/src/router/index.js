import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Bigone from '@/components/BigOne';
import Dashboard from '@/components/DashBoard';
import Bold from '@/components/Bold'
Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'BigOne',
      component: Bigone
    },
    {
      path: '/Dashboard',
      name: 'DashBoard',
      component: Dashboard
    },
    {
      path: '/Bold',
      name: "Bold",
      component: Bold
    }
  ]
})
