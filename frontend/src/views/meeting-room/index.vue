<template>
    <div>
        <board class="board" @complete-init="connect"></board>
    </div>
</template>

<script>
import Board from '../../components/meeting-room/board.vue';
import { defaultErrorHandler } from '../../requests/errors';
import { getMeetingRoomInfo } from '../../requests/meeting-room';
import Connection from '../../connection';
export default {
    components: {
        Board,
    },
    data() {
        return {
            connection: {},
        };
    },
    methods: {
        connect: function (board) {
            getMeetingRoomInfo(this.$route.params.uuid)
                .then((data) => {
                    this.connection = new Connection(data.data.id, board);
                })
                .catch(defaultErrorHandler(getMeetingRoomInfo));
        },
    },
};
</script>

<style scoped>
.board {
    width: 100vw;
    height: 100vh;
}
</style>
