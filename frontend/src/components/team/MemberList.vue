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
            <a-button
                class="remove font-small"
                @click="removeConfirm"
                size="small"
                type="danger"
            >
                移除成员
            </a-button>
        </a-list-item>
    </a-list>
</template>

<script>
import { List, Avatar, Modal, Button } from 'ant-design-vue';
import Vue from 'vue';
Vue.use(Modal);

export default {
    created: function () {
        // TODO 获取用户列表
    },
    components: {
        AList: List,
        AAvatar: Avatar,
        AListItem: List.Item,
        AListItemMeta: List.Item.Meta,
        AButton: Button,
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
        removeConfirm() {
            Modal.confirm({
                title: '确定要移除此成员吗？',
                content: '点击“确认”后, 此成员将被移出此会议室',
                okText: '确认',
                cancelText: '取消',
                onOk() {
                    // TODO 将此成员移出此会议室
                },
            });
        },
    },
};
</script>

<style>
.description {
    color: rgb(2, 2, 2);
}
.remove {
    background-color: rgb(219, 215, 215);
    margin: 10px;
}
.name {
    width: 100%;
    font-weight: bold;
    font-size: 18px;
}
.box {
    background-color: var(--primary-color-2);
    width: 100%;
    border-radius: 8px;
    min-width: 300px;
    padding-left: 10px;
}
</style>
