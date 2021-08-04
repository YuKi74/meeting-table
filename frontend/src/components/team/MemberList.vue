<template>
    <a-list
        item-layout="horizontal"
        :data-source="data"
        class="box flex main-axis-between"
    >
        <a-list-item slot="renderItem" slot-scope="item, index">
            <a-list-item-meta
                :v-bind="index"
                class="description"
                :description="item.email"
            >
                <div class="name font-normall" slot="title">
                    {{ item.name }}
                </div>
                <a-avatar :size="30" slot="avatar" icon="user" class="avatar" />
            </a-list-item-meta>

            <a-button
                class="remove font-small"
                @click="removeConfirm(item.id)"
                size="small"
                type="primary"
                v-show="isShow(item.id)"
            >
                移除
            </a-button>
        </a-list-item>
    </a-list>
</template>

<script>
import { List, Avatar, Modal, Button, Message } from 'ant-design-vue';
import Vue from 'vue';
import { getMembers } from '../../requests/team';
import { getTeaminfo, removeMember } from '../../requests/team';
import { getUserinfo } from '../../requests/user';
import { defaultErrorHandler } from '../../requests/errors';
Vue.use(Modal);

export default {
    props: ['uuid'],
    components: {
        AList: List,
        AAvatar: Avatar,
        AListItem: List.Item,
        AListItemMeta: List.Item.Meta,
        AButton: Button,
    },
    data() {
        return {
            isCreator: '',
            myId: '',
            data: [],
        };
    },
    mounted() {
        //获取团队成员信息
        getMembers()
            .then((data) => {
                this.data = data.data;
            })
            .catch(defaultErrorHandler(getMembers));
        //获取团队信息
        getTeaminfo(this.uuid)
            .then((data) => {
                this.isCreator = data.data.is_creator;
            })
            .catch(defaultErrorHandler(getTeaminfo));
        //获取用户信息
        getUserinfo()
            .then((data) => {
                this.myId = data.data.id;
            })
            .catch(defaultErrorHandler(getUserinfo));
    },
    methods: {
        isShow(id) {
            return this.isCreator && this.myId !== id;
        },
        removeConfirm(id) {
            Modal.confirm({
                title: '确定要移除此成员吗？',
                content: '点击“确认”后, 此成员将被移出此会议室',
                okText: '确认',
                cancelText: '取消',
                onOk() {
                    removeMember(id)
                        .then(() => {
                            Message.success('该成员已移除');
                        })
                        .catch(defaultErrorHandler(removeMember));
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
    margin: 10px;
}
.name {
    width: 100%;
    font-weight: bold;
    text-align: left;
}
.box {
    overflow: auto;
    background-color: var(--white);
    width: 100%;
    border-radius: 8px;
    min-width: 250px;
    padding-left: 10px;
    max-height: 600px;
}
.ant-list-item-meta-avatar {
    margin-right: 5px;
}
.avatar {
    background-color: var(--secondary-color-1);
}
</style>
