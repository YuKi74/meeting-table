<template>
    <div>
        <board class="board" v-if="connection" :connection="connection"></board>
    </div>
</template>

<script>
import Board from '../../components/meeting-room/Board.vue';
import { defaultErrorHandler } from '../../requests/errors';
import { getMeetingRoomInfo } from '../../requests/meeting-room';
import Connection from '../../connection';
export default {
    components: {
        Board,
    },
    data() {
        return {
            connection: null,
        };
    },
    mounted: function () {
        getMeetingRoomInfo(this.$route.params.uuid)
            .then((data) => {
                this.connection = new Connection(data.data.id);
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
}
.board {
    width: 100vw;
    height: 100vh;
}
</style>
