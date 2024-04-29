<template>
    <layout class="layout">
        <layout-header class="header flex main-axis-between">
            <team-detail :uuid="uuid" :is-creator="isCreator" />
            <div class="flex">
                <div v-if="isCreator">
                    <popover placement="bottomRight">
                        <div class="apply-list-content" slot="content">
                            <apply-list class="apply-list"></apply-list>
                        </div>
                        <a-button
                            icon="notification"
                            type="primary"
                            class="apply-list-button"
                            shape="circle"
                            @mouseover="refresh"
                        />
                    </popover>
                </div>
                <user-detail class="user-detail"></user-detail>
            </div>
        </layout-header>
        <layout>
            <layout-sider class="sider" width="265">
                <member-list
                    class="member-list"
                    :uuid="uuid"
                    :is-creator="isCreator"
                />
            </layout-sider>
            <layout-content class="content">
                <meeting-list class="meeting-list"></meeting-list>
            </layout-content>
        </layout>
    </layout>
</template>

<script>
import { Layout, Popover, Button } from 'ant-design-vue';
import ApplyMessageList from '../../components/team/ApplyMessageList.vue';
import MeetingRoomList from '../../components/team/MeetingRoomList.vue';
import TeamDetail from '../../components/team/TeamDetail.vue';
import MemberList from '../../components/team/MemberList.vue';
import UserDetail from '../../components/team/UserDetail.vue';
import { getTeaminfo } from '../../requests/team';
import { defaultErrorHandler } from '../../requests/errors';
export default {
    components: {
        ApplyList: ApplyMessageList,
        MeetingList: MeetingRoomList,
        TeamDetail,
        MemberList,
        Layout,
        LayoutHeader: Layout.Header,
        LayoutSider: Layout.Sider,
        LayoutContent: Layout.Content,
        UserDetail,
        Popover,
        AButton: Button,
    },
    props: ['uuid'],
    data() {
        return {
            isCreator: false,
        };
    },
    mounted: function () {
        getTeaminfo(this.uuid)
            .then((data) => {
                this.isCreator = data.data.is_creator;
            })
            .catch(defaultErrorHandler(getTeaminfo));
    },
    methods: {
        refresh() {
            this.bus.$emit('refresh');
        },
    },
};
</script>

<style scoped>
.layout {
    width: 100%;
    min-height: 100vh;
}
.header {
    width: 100%;
    background-color: #273868;
}
.sider {
    background-color: var(--white);
    border-right: solid 2px var(--secondary-color-2);
}
.content {
    padding: 20px;
    background-color: var(--background);
}
.apply-list-button {
    width: 40px;
    height: 40px;
}
.apply-list-content {
    width: 300px;
}
.user-detail {
    margin-left: 20px;
    width: 40px;
    height: 40px;
}
</style>
