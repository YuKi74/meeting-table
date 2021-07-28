<template>
    <a-list item-layout="horizontal" :data-source="data" class="box">
        <a-list-item slot="renderItem" slot-scope="item, index">
            <a-list-item-meta
                :v-bind="index"
                class="description"
                :description="item.email"
            >
                <div class="name" slot="title">{{ item.nickname }}</div>
                <a-avatar :size="40" slot="avatar" icon="user" class="avatar" />
            </a-list-item-meta>
            <div class="remove" @click="remove_confirm">移除成员</div>
        </a-list-item>
    </a-list>
</template>
<script>
import { List, Avatar, Modal } from 'ant-design-vue';
export default {
    created: function () {
        // TODO 获取用户列表
    },
    components: {
        AList: List,
        AAvatar: Avatar,
        AListItem: List.Item,
        AListItemMeta: List.Item.Meta,
    },
    data() {
        return {
            data: [
                {
                    nickname: '',
                    email: '',
                },
            ],
        };
    },
    methods: {
        remove_confirm() {
            Modal.confirm({
                title: '确定要移除此成员吗？',
                content: '点击“确认”后, 此成员将被移出此会议室',
                okText: '确认',
                cancelText: '取消',
                onOk() {
                    // TODO 将此成员移出此会议室
                },
                onCancel() {},
            });
        },
    },
};
</script>
<style>
.avatar {
    background-color: #498d4ffb;
}
.description {
    color: rgb(2, 2, 2);
}
.remove {
    background-color: rgba(221, 221, 221, 0.486);
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 10%);
    padding-left: 4px;
    padding-right: 4px;
    padding-top: 2px;
    padding-bottom: 2px;
    border-radius: 20px;
    font-size: 8px;
    color: rgb(6, 51, 17);
    margin-right: 20px;
    font-weight: 100;
    cursor: pointer;
}
.remove:hover {
    color: red;
    transform: scale(1.1, 1.1);
    transition: 500ms;
}
.name {
    width: 100%;
    font-weight: bold;
    font-size: 18px;
}
.box {
    background-color: #82ca88fb;
    width: 100%;
    border-radius: 8px;
    min-width: 300px;
    padding-left: 10px;
}
</style>
