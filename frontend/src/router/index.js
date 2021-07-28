import Vue from 'vue';
import VueRouter from 'vue-router';

Vue.use(VueRouter);

const routes = [
    {
        path: '/',
        name: 'index',
        // component: ,
    },
    {
        path: '/register',
        name: 'Register',
        component: () => import('../views/register'),
    },
    {
        path: '/login',
        name: 'Login',
        component: () => import('../views/login'),
    },
    {
        path: '/create',
        name: 'Create',
        component: () => import('../views/create-team/Create.vue'),
    },
    {
        path: '/create/list',
        name: 'CreateList',
        component: () => import('../views/create-team/CreateList.vue'),
    },
    {
        path: '/team-outside',
        name: 'TeamOutside',
        component: () =>
            import(
                /* webpackChunkName: "about" */ '../views/team-outside/TeamOutside.vue'
            ),
    },
    {
        path: '/team-outside',
        name: 'TeamOutside',
        component: () =>
            import(
                /* webpackChunkName: "about" */ '../views/team-outside/TeamOutside.vue'
            ),
    },
];

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes,
});

export default router;
