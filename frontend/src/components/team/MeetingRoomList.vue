<template>
    <a-list
        :grid="{ gutter: 16, xs: 1, sm: 1, md: 2, lg: 3, xl: 4, xxl: 4 }"
        :data-source="listData"
        class="board"
    >
        <a-list-item slot="renderItem" slot-scope="item, index">
            <div v-if="item === roomAddCard">
                <div class="create" @click="addConfirm">
                    <div class="blank"></div>
                    <a-icon
                        type="plus-circle"
                        :style="plusClass"
                        class="plus"
                        @click="addConfirm"
                    />
                </div>
            </div>
            <div class="box" v-else>
                <a-card
                    :title="item.title"
                    :number="index"
                    class="card"
                    :bodyStyle="bodyStyle"
                    @click="enter"
                >
                    <a
                        slot="extra"
                        class="delete-btn"
                        href="#"
                        @click.stop="deleteComfirm"
                    >
                        删除
                    </a>
                    <div class="pic-container">
                        <img :src="item.thumbnail" class="pic" />
                    </div>
                </a-card>
            </div>
        </a-list-item>
    </a-list>
</template>
<script>
import { List, Card, Modal, Icon } from 'ant-design-vue';
import Input from './MeetingRoomCreateInput.vue';
import Vue from 'vue';
Vue.use(Modal);

export default {
    props: ['team-id'],
    components: {
        AList: List,
        AListItem: List.Item,
        ACard: Card,
        AIcon: Icon,
    },
    created: function () {
        // TODO 获取会议室列表
    },
    data() {
        return {
            plusClass: {
                color: 'var(--white)',
                fontSize: '50px',
            },
            roomAddCard: '',
            mettingRooms: [
                {
                    title: '该会议室主题',
                    thumbnail: '',
                },
            ],
            bodyStyle: {
                padding: 0,
            },
        };
    },
    computed: {
        listData: function () {
            return [this.roomAddCard].concat(this.mettingRooms);
        },
    },
    methods: {
        addConfirm() {
            const inputNode = this.$createElement(Input);
            Modal.info({
                title: '请输入会议室主题',
                content: inputNode,
                okText: '创建',
                cancelText: '返回',
                onOk() {
                    inputNode.componentInstance.confirm();
                    // TODO 在子组件Input的confirm函数中 发送创建会议室请求
                },
                onCancel() {},
            });
        },
        enter() {
            //TODO 进入对应会议室
        },
        deleteComfirm() {
            Modal.confirm({
                title: '确定要删除此会议室吗？',
                content: '点击“确认”后, 此会议室将会被删除',
                okText: '确认',
                cancelText: '取消',
                onOk() {
                    //TODO 删除相应会议室
                },
                onCancel() {},
            });
        },
    },
};
</script>
<style scoped>
.plus {
    cursor: pointer;
    height: 50px;
}
.plus:hover {
    transform: rotate(180deg);
    transition: 800ms;
}
.blank {
    height: 0;
    width: 100%;
}
.create {
    width: 100%;
    height: 250px;
    display: flex;
    justify-content: center;
    background-color: var(--primary-color-2);
    border-radius: 8px;
    box-shadow: 0 3px 20px rgb(0 0 0 / 20%);
    flex-wrap: wrap;
}
.create:hover {
    transform: translateY(-5px);
    transition: 300ms;
    cursor: pointer;
}
.pic-container {
    height: 194px;
    overflow: hidden;
    border-color: #ebebeb;
}
.pic {
    width: 100%;
}
.delete-btn {
    color: black;
    font-weight: bolder;
}
.delete-btn:hover {
    color: rgb(221, 12, 12);
}
.board {
    width: 100%;
    background-color: #fafafa;
}
.card {
    width: 100%;
    height: 250px;
    background-color: var(--white);
    border-radius: 8px;
    flex-wrap: wrap;
    box-shadow: 0 3px 20px rgb(0 0 0 / 20%);
    cursor: pointer;
    padding: 0;
    max-width: 500px;
    overflow: hidden;
}
.box {
    padding: 0;
    width: 100%;
    display: flex;
    justify-content: center;
}
.box:hover {
    transform: translateY(-5px);
    transition: 300ms;
}
</style>
