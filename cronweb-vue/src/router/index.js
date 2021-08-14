import { createRouter, createWebHistory } from 'vue-router'
import Layout from "../views/Layout";
import Login from "../views/Login";

const routes = [
  {
    path: '/cron',
    name: 'Layout',
    component:  Layout
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
