<template>
    <div class="background">
        <layout class="layout">
            <layout-sider class="sider">
                <team-detail class="team-detail" :uuid="uuid"></team-detail>
                <member-list class="member-list"></member-list>
            </layout-sider>
            <layout>
                <layout-content>
                    <meeting-list class="meeting-list"></meeting-list>
                </layout-content>
                <layout-sider width="70px">
                    <user-detail class="user-detail"></user-detail>
                    <popover placement="leftTop">
                        <template slot="content">
                            <div class="apply-list-content">
                                <apply-list class="apply-list"></apply-list>
                            </div>
                        </template>
                        <a-button
                            icon="notification"
                            type="primary"
                            class="apply-list-button"
                            shape="circle"
                        ></a-button>
                    </popover>
                </layout-sider>
            </layout>
        </layout>
    </div>
</template>

<script>
import { Layout, Popover, Button } from 'ant-design-vue';
import ApplyMessageList from '../../components/team/ApplyMessageList.vue';
import MeetingRoomList from '../../components/team/MeetingRoomList.vue';
import TeamDetail from '../../components/team/TeamDetail.vue';
import MemberList from '../../components/team/MemberList.vue';
import UserDetail from '../../components/team/UserDetail.vue';
export default {
    components: {
        ApplyList: ApplyMessageList,
        MeetingList: MeetingRoomList,
        TeamDetail,
        MemberList,
        Layout,
        LayoutSider: Layout.Sider,
        LayoutContent: Layout.Content,
        UserDetail,
        Popover,
        AButton: Button,
    },
    props: ['uuid'],
};
</script>

<style scoped>
.background {
    background-color: var(--background);
    width: 100%;
    min-height: 100vh;
    text-align: center;
}
.layout {
    min-height: 100vh;
}
.sider {
    background-color: var(--background);
}
.team-detail {
    margin-top: 15px;
}
.member-list {
    margin-top: 40px;
    margin-left: 20px;
}
.header {
    height: 80px;
}
.meeting-list {
    /* margin: 110px; */
}
.user-detail {
    margin-top: 20px;
}
.apply-list-button {
    margin-top: 20px;
}
.apply-list {
    width: 300px;
}
</style>
