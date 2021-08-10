<template>
    <div>
        <component :is="currentView" :uuid="uuid" />
    </div>
</template>
<script>
import MembersView from './MembersView.vue';
import VisitorsView from './VisitorsView.vue';
import { getUserinfo } from '../../requests/user';
import Cookies from 'js-cookie';
import router from '../../router';
import { defaultErrorHandler } from '../../requests/errors';

export default {
    mounted: function () {
        if (this.$route.params.uuid) {
            this.uuid = this.$route.params.uuid;
            getUserinfo()
                .then((data) => {
                    if (data.data.team_uuid === this.$route.params.uuid) {
                        this.currentView = MembersView;
                    } else {
                        this.currentView = VisitorsView;
                    }
                })
                .catch(defaultErrorHandler(getUserinfo));
        } else {
            if (!Cookies.get('token')) {
                router.push('/login');
            } else {
                getUserinfo()
                    .then((data) => {
                        this.uuid = data.data.team_uuid;
                        if (!this.uuid) {
                            router.push('/team/create');
                        } else {
                            this.currentView = MembersView;
                        }
                    })
                    .catch(defaultErrorHandler(getUserinfo));
            }
        }
    },
    data() {
        return {
            uuid: '',
            currentView: '',
        };
    },
    methods: {},
};
</script>
