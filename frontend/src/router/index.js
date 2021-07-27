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
        path: '/login',
        name: 'Login',
        component: () => import('../views/login'),
    },
    {
        path: '/create',
        name: 'Create',
        component: () =>
            import(
                /* webpackChunkName: "about" */ '../views/create-team/Create.vue'
            ),
    },
    {
        path: '/create/list',
        name: 'CreateList',
        component: () =>
            import(
                /* webpackChunkName: "about" */ '../views/create-team/CreateList.vue'
            ),
    },
];

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes,
});

export default router;
