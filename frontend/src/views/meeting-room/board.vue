<template>
    <div class="board" ref="board"></div>
</template>

<script>
import Board from '../../paint-board';
export default {
    data() {
        return {
            board: {},
        };
    },
    mounted: function () {
        this.board = new Board(this.$refs.board);
    },
};
</script>

<style scoped>
.board {
    width: 100%;
    height: 100%;
    overflow: hidden;
}
</style>
