import Vue from 'vue';
import VueRouter from 'vue-router';

Vue.use(VueRouter);

const routes = [
    {
        path: '/',
        name: 'Index',
        component: () => import('../views'),
    },
    {
        path: '/login',
        name: 'Login',
        component: () => import('../views/login'),
    },
    {
        path: '/register',
        name: 'Register',
        component: () => import('../views/register'),
    },
    {
        path: '/team',
        name: 'Team',
        component: () => import('../views/team'),
    },
    {
        path: '/team/create',
        component: () => import('../views/team/create'),
    },
    {
        path: '/team/:uuid',
        component: () => import('../views/team'),
    },
    {
        path: '/meeting-room/:uuid',
        component: () => import('../views/meeting-room'),
    },
    {
        path: '*',
        name: '404',
        component: () => import('../views/404'),
    },
];

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes,
});

export default router;
