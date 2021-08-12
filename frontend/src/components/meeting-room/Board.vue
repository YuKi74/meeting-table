<template>
    <div class="content" ref="page">
        <toolbar
            class="toolbar"
            @tool-change="getTool"
            @stroke-color-change="getStrokeColor"
            @fill-color-change="getFillColor"
            @stroke-width-change="getStrokeWidth"
            ref="toolbar"
        ></toolbar>
        <div class="board" ref="board"></div>
        <component-container
            v-for="(component, id) in components"
            :key="id"
            :connection="connection"
            :style="component.style"
            :id="id"
            :component="component.node"
            :content="component.content"
            class="component"
            @mousedown="onMouseDown"
            @close="onClose"
        />
    </div>
</template>

<script>
import { notification, Button } from 'ant-design-vue';
import Board from '../../paint-board';
import Toolbar from './Toolbar.vue';
import { getUserinfo } from '../../requests/user';
import { defaultErrorHandler } from '../../requests/errors';
import ComponentContainer from './ComponentContainer.vue';
import {
    calcStyle,
    isComponent,
    getComponent,
    restoreComponent,
} from '../../components-utils';
import Vue from 'vue';
Vue.use(Button);

export default {
    props: ['connection'],
    components: {
        Toolbar,
        ComponentContainer,
    },
    data() {
        return {
            board: {},
            lastX: 0,
            lastY: 0,
            selectedComponent: null,
            moved: false,
            components: {},
            userID: 0,
        };
    },
    mounted: function () {
        getUserinfo()
            .then((user) => {
                this.userID = user.data.id;
                this.board = new Board(
                    this.$refs.board,
                    user.data.id,
                    this.onBoardMove
                );
                this.board.registerMessageHandler(this.connection);
                this.connection.addMessageHandler(
                    (data) => {
                        return data.Type === 'component';
                    },
                    this.handleComponentCreate,
                    this
                );
                this.connection.addMessageHandler(
                    (data) => {
                        return data.Type === 'component_move';
                    },
                    this.handleComponentMove,
                    this
                );
                this.connection.addMessageHandler(
                    (data) => {
                        return data.Type === 'component_delete';
                    },
                    this.handleComponentDelete,
                    this
                );
                this.connection.addMessageHandler(
                    (data) => {
                        return (
                            data.Type === 'view_share' &&
                            data.Data.id !== this.userID
                        );
                    },
                    this.onShareRequest,
                    this
                );
                this.connection.start();
            })
            .catch(defaultErrorHandler(getUserinfo));
        window.addEventListener('mousedown', (event) => {
            if (event.origin) {
                return;
            }
            if (
                event.target.tagName === 'CANVAS' &&
                isComponent(this.board.tool)
            ) {
                this.createComponent(event.clientX, event.clientY);
                this.board.blur();
                this.$refs.toolbar.reset();
            }
        });
        window.addEventListener('mousemove', (event) => {
            if (event.origin) {
                return;
            }
            if (this.selectedComponent) {
                this.moved = true;
                this.onDrag(event.clientX, event.clientY);
            }
        });
        window.addEventListener('mouseup', (event) => {
            if (event.origin) {
                return;
            }
            if (this.selectedComponent && this.moved) {
                this.onDragEnd(event.clientX, event.clientY);
            }
            this.selectedComponent = null;
            this.moved = false;
        });
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
        onMouseDown: function (id, x, y) {
            this.selectedComponent = id;
            this.lastX = x;
            this.lastY = y;
        },
        onDrag: function (x, y) {
            calcStyle(
                this.components[this.selectedComponent].style,
                this.board,
                x - this.lastX,
                y - this.lastY
            );
            this.lastX = x;
            this.lastY = y;
        },
        onDragEnd: function (x, y) {
            const component = this.components[this.selectedComponent];
            if (!component) {
                return;
            }
            calcStyle(
                component.style,
                this.board,
                x - this.lastX,
                y - this.lastY
            );
            this.lastX = x;
            this.lastY = y;
            const data = {
                x: component.style.x,
                y: component.style.y,
            };
            this.connection.send({
                Type: 'component_move',
                Target: this.selectedComponent,
                Data: data,
            });
            this.selectedComponent = null;
        },
        onClose: function (id) {
            this.$delete(this.components, id);
            this.selectedComponent = null;
            this.moved = false;
            this.connection.send({
                Type: 'component_delete',
                Target: id,
                Data: '',
            });
        },
        onBoardMove: function () {
            Object.keys(this.components).forEach((id) => {
                calcStyle(this.components[id].style, this.board);
            });
        },
        createComponent: function (x, y) {
            const id = this.board.tool + '_' + new Date().getTime();
            const component = getComponent(this.board, x, y);
            if (!component) {
                return;
            }
            this.$set(this.components, id, component);
            const data = {
                x: component.style.x,
                y: component.style.y,
                content: component.content,
            };
            if (
                this.board.tool === '文件' ||
                this.board.tool === '从其他会议室导入文件'
            ) {
                this.components[id].content = {
                    x: component.style.x,
                    y: component.style.y,
                };
                return;
            }
            this.connection.send({
                Type: 'component',
                Target: id,
                Data: data,
            });
        },
        handleComponentCreate: function (data) {
            if (Object.keys(this.components).includes(data.Target)) {
                return;
            }
            const component = restoreComponent(data, this.board);
            this.$set(this.components, data.Target, component);
        },
        handleComponentMove: function (data) {
            if (!this.components[data.Target]) {
                return;
            }
            this.components[data.Target].style.x = parseFloat(data.Data.x);
            this.components[data.Target].style.y = parseFloat(data.Data.y);
            calcStyle(this.components[data.Target].style, this.board);
        },
        handleComponentDelete: function (data) {
            this.$delete(this.components, data.Target);
            this.selectedComponent = null;
            this.moved = false;
        },
        onShareRequest: function (data) {
            const key = '' + new Date().getTime();
            notification.info({
                key: key,
                message: data.Data.name + '发起了一个共享视角请求。',
                btn: (h) => {
                    return h(
                        'a-button',
                        {
                            props: {
                                type: 'primary',
                                size: 'small',
                            },
                            on: {
                                click: () => {
                                    notification.close(key);
                                    this.board.stage.position(data.Data.pos);
                                    this.onBoardMove();
                                },
                            },
                        },
                        '同意'
                    );
                },
            });
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
    user-select: none;
}
.toolbar {
    position: absolute;
    left: 10px;
    top: 70px;
    z-index: 2;
}
.board {
    width: 100%;
    height: 100%;
    overflow: hidden;
    background-color: var(--background);
}
.component {
    position: absolute;
    z-index: 1;
    transform-origin: 0 0 0;
}
</style>
