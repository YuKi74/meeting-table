<template>
    <a-list
        item-layout="horizontal"
        :data-source="data"
        class="box"
        :split="true"
    >
        <a-list-item
            class="list-item flex main-axis-between"
            slot="renderItem"
            slot-scope="item, index"
        >
            <a-list-item-meta
                :v-bind="index"
                class="description"
                :description="item.email.slice(0, 17)"
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
import { getMembers, removeMember } from '../../requests/team';
import { getUserinfo } from '../../requests/user';
import Errors, { defaultErrorHandler } from '../../requests/errors';
Vue.use(Modal);

export default {
    props: ['uuid', 'is-creator'],
    components: {
        AList: List,
        AAvatar: Avatar,
        AListItem: List.Item,
        AListItemMeta: List.Item.Meta,
        AButton: Button,
    },
    data() {
        return {
            myId: '',
            data: [],
        };
    },
    mounted() {
        this.refreshMembers();
        getUserinfo()
            .then((data) => {
                this.myId = data.data.id;
            })
            .catch(defaultErrorHandler(getUserinfo));
        this.bus.$on('aggreeApplication', () => {
            this.refreshMembers();
        });
    },
    methods: {
        refreshMembers() {
            getMembers()
                .then((data) => {
                    this.data = data.data;
                })
                .catch(defaultErrorHandler(getMembers));
        },
        isShow(id) {
            return this.isCreator && this.myId !== id;
        },
        removeConfirm(id) {
            const that = this;
            Modal.confirm({
                title: '确定要移除此成员吗？',
                content: '点击“确定”后, 此成员将被移出此团队',
                okText: '确定',
                cancelText: '取消',
                onOk() {
                    removeMember(id)
                        .then(() => {
                            Message.success('该成员已移除');
                            that.refreshMembers();
                        })
                        .catch((data) => {
                            defaultErrorHandler(removeMember)(data);
                            if (data.error === Errors.ERROR_INPUT) {
                                that.refreshMembers();
                            }
                        });
                },
            });
        },
    },
};
</script>

<style scoped>
.description {
    color: rgb(2, 2, 2);
}
.list-item {
    width: 250px;
}
.remove {
    margin: 10px;
}
.name {
    width: 150px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    font-weight: bold;
    text-align: left;
}
.box {
    overflow: auto;
    background-color: var(--white);
    width: 100%;
    padding-left: 10px;
    max-height: calc(100vh - 64px);
}
.ant-list-item-meta-avatar {
    margin-right: 5px;
}
.ant-list-item-meta-description {
    width: 150px;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
}
.avatar {
    background-color: var(--secondary-color-1);
}
</style>
