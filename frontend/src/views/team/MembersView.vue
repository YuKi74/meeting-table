<template>
    <layout class="layout">
        <layout-header class="header flex main-axis-between">
            <team-detail
                :uuid="uuid"
                :is-creator="team.is_creator"
            ></team-detail>
            <div class="flex">
                <popover placement="bottomRight" v-if="team.is_creator">
                    <div class="apply-list-content" slot="content">
                        <apply-list class="apply-list"></apply-list>
                    </div>
                    <a-button
                        icon="notification"
                        type="primary"
                        class="apply-list-button"
                        shape="circle"
                    />
                </popover>
                <user-detail class="user-detail"></user-detail>
            </div>
        </layout-header>
        <layout>
            <layout-sider class="sider" width="250">
                <member-list
                    class="member-list"
                    :uuid="uuid"
                    :is-creator="team.is_creator"
                ></member-list>
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
            team: {},
        };
    },
    mounted: function () {
        getTeaminfo(this.uuid)
            .then((data) => {
                this.team = data.data;
            })
            .catch(defaultErrorHandler(getTeaminfo));
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
}
</style>
