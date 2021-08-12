<template>
    <a-list
        :grid="{ gutter: 16, xs: 1, sm: 1, md: 2, lg: 3, xl: 4, xxl: 4 }"
        :data-source="listData"
        class="board"
    >
        <a-list-item slot="renderItem" slot-scope="item, index">
            <div class="box" v-if="item === roomAddCard">
                <div class="create flex main-axis-center" @click="addConfirm">
                    <a-icon
                        type="plus-circle"
                        :style="plusClass"
                        class="plus"
                        @click.stop="addConfirm"
                    />
                </div>
            </div>
            <div class="box" v-else>
                <a-card
                    :title="item.name"
                    :number="index"
                    class="card"
                    :bodyStyle="bodyStyle"
                    @click="enter(item.uuid)"
                >
                    <a
                        slot="extra"
                        class="delete-btn"
                        href="#"
                        @click.stop="deleteComfirm(item.id)"
                    >
                        删除
                    </a>
                    <div class="pic-container flex main-axis-center">
                        <a-icon
                            type="calendar"
                            theme="twoTone"
                            two-tone-color="#b4c8ff"
                            class="icon"
                        />
                    </div>
                </a-card>
            </div>
        </a-list-item>
    </a-list>
</template>
<script>
import { List, Card, Modal, Icon, Message } from 'ant-design-vue';
import Input from './MeetingRoomCreateInput.vue';
import { defaultErrorHandler } from '../../requests/errors';
import {
    getMeetingRooms,
    deleteMeetingRoom,
} from '../../requests/meeting-room';
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
    data() {
        return {
            plusClass: {
                color: 'var(--white)',
                fontSize: '50px',
            },
            roomAddCard: '',
            meetingRooms: [],
            bodyStyle: {
                padding: 0,
            },
        };
    },
    computed: {
        listData: function () {
            return [this.roomAddCard].concat(this.meetingRooms);
        },
    },
    mounted() {
        this.refreshMeetingRooms();
    },
    methods: {
        refreshMeetingRooms() {
            getMeetingRooms()
                .then((data) => {
                    this.meetingRooms = data.data;
                })
                .catch(defaultErrorHandler(getMeetingRooms));
        },
        addConfirm() {
            const inputNode = this.$createElement(Input);
            const that = this;
            Modal.confirm({
                title: '请输入会议室主题',
                content: inputNode,
                okText: '创建',
                cancelText: '返回',
                onOk() {
                    inputNode.componentInstance.confirm(() => {
                        that.refreshMeetingRooms();
                    });
                },
            });
        },
        enter(uuid) {
            window.location.href = `/meeting-room/${uuid}`;
        },
        deleteComfirm(id) {
            const that = this;
            Modal.confirm({
                title: '确定要删除此会议室吗？',
                content: '点击“确定”后, 此会议室将会被删除',
                okText: '确定',
                cancelText: '取消',
                onOk() {
                    deleteMeetingRoom(id)
                        .then(() => {
                            Message.success('删除成功');
                            that.refreshMeetingRooms();
                        })
                        .catch(defaultErrorHandler(deleteMeetingRoom));
                },
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
    background-color: var(--primary-color-2);
    border-radius: 8px;
    max-width: 500px;
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
}
.card {
    width: 100%;
    height: 250px;
    background-color: var(--white);
    border-radius: 8px;
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
.icon {
    font-size: 100px;
}
</style>
