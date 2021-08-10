<template>
    <div>
        <meeting-room-top class="header" :name="roomName" />
        <board class="board" v-if="connection" :connection="connection"></board>
        <mt-video
            v-if="userId && token"
            class="video"
            :roomUuid="$route.params.uuid"
            :token="token"
            :userId="userId"
        />
    </div>
</template>

<script>
import Board from '../../components/meeting-room/Board.vue';
import { defaultErrorHandler } from '../../requests/errors';
import { getMeetingRoomInfo, getVideoToken } from '../../requests/meeting-room';
import Connection from '../../connection';
import MeetingRoomTop from '../../components/team/MeetingRoomTop.vue';
import Video from '../../components/meeting-room/Video.vue';
import { getUserinfo } from '../../requests/user';

export default {
    components: {
        Board,
        MtVideo: Video,
        MeetingRoomTop,
    },
    data() {
        return {
            connection: null,
            roomName: '',
            userId: null,
            token: null,
        };
    },
    mounted: function () {
        getUserinfo()
            .then((data) => {
                this.userId = data.data.id;
            })
            .catch(defaultErrorHandler(getUserinfo));
        getMeetingRoomInfo(this.$route.params.uuid)
            .then((data) => {
                this.connection = new Connection(data.data.id);
                this.roomName = data.data.name;
            })
            .catch(defaultErrorHandler(getMeetingRoomInfo));
        getVideoToken(this.$route.params.uuid).then((data) => {
            console.log(data);
            this.token = data.data;
        });
    },
    methods: {},
};
</script>

<style scoped>
.header {
    position: absolute;
    top: 0;
    left: 0;
    width: 100vw;
    z-index: 20;
}
.board {
    width: 100vw;
    height: 100vh;
}
.video {
    position: absolute;
    top: 80px;
    right: 30px;
    z-index: 10;
}
</style>
