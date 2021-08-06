<template>
    <div class="content">
        <toolbar
            class="toolbar"
            @tool-change="getTool"
            @stroke-color-change="getStrokeColor"
            @fill-color-change="getFillColor"
            @stroke-width-change="getStrokeWidth"
        ></toolbar>
        <div class="board" ref="board"></div>
    </div>
</template>

<script>
import Board from '../../paint-board';
import Toolbar from './Toolbar.vue';
import { getUserinfo } from '../../requests/user';
import { defaultErrorHandler } from '../../requests/errors';
export default {
    components: {
        Toolbar,
    },
    data() {
        return {
            board: {},
        };
    },
    mounted: function () {
        getUserinfo()
            .then((data) => {
                this.board = new Board(this.$refs.board, data.data.id);
                this.$emit('complete-init', this.board);
            })
            .catch(defaultErrorHandler(getUserinfo));
    },
    methods: {
        getTool: function (name) {
            this.board.tool = name;
            if (name === '移动') {
                this.board.stage.to({
                    duration: 0,
                    draggable: true,
                });
            } else {
                this.board.stage.to({
                    duration: 0,
                    draggable: false,
                });
            }
        },
        getStrokeColor: function (color) {
            this.board.strokeColor = color;
        },
        getFillColor: function (color) {
            this.board.fillColor = color;
        },
        getStrokeWidth: function (width) {
            this.board.strokeWidth = width;
        },
    },
};
</script>

<style scoped>
.content {
    position: relative;
    width: 100%;
    height: 100%;
    overflow: hidden;
}
.toolbar {
    position: absolute;
    left: 10px;
    top: 10px;
    z-index: 1;
}
.board {
    width: 100%;
    height: 100%;
    overflow: hidden;
    background-color: lightgray;
}
</style>
