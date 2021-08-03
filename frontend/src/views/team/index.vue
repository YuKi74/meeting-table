<template>
    <div>
        <component :is="currentView" :uuid="uuid" />
    </div>
</template>

<script>
// TODO 移除此注释
// eslint-disable-next-line no-unused-vars
import MembersView from './MembersView.vue';
import VisitorsView from './VisitorsView.vue';

export default {
    beforeCreate: function () {
        if (this.$route.params.uuid) {
            this.uuid = this.$route.params.uuid;
            // TODO 判断登录状态以及是否是该团队成员，决定要显示的视图
        } else {
            // TODO 判断登录状态，决定要显示的视图以及是否路由到创建页面
        }
    },
    data() {
        return {
            uuid: '',
            currentView: VisitorsView,
        };
    },
};
</script>

<style scoped></style>
