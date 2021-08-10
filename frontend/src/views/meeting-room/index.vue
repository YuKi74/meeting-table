<template>
    <div>
        <meeting-room-top class="header" :name="roomName" />
        <board class="board" v-if="connection" :connection="connection"></board>
    </div>
</template>

<script>
import Board from '../../components/meeting-room/Board.vue';
import { defaultErrorHandler } from '../../requests/errors';
import { getMeetingRoomInfo } from '../../requests/meeting-room';
import Connection from '../../connection';
import MeetingRoomTop from '../../components/team/MeetingRoomTop.vue';
export default {
    components: {
        Board,
        MeetingRoomTop,
    },
    data() {
        return {
            connection: null,
            roomName: '',
        };
    },
    mounted: function () {
        getMeetingRoomInfo(this.$route.params.uuid)
            .then((data) => {
                this.connection = new Connection(data.data.id);
                this.roomName = data.data.name;
            })
            .catch(defaultErrorHandler(getMeetingRoomInfo));
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
</style>
