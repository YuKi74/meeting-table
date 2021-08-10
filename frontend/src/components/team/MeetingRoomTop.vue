<template>
    <div class="header flex shadow main-axis-between">
        <div class="header-theme flex">
            <a-icon class="info flex cross-axis-center" type="info-circle" />
            <p class="theme">会议主题：{{ name }}</p>
        </div>
        <div class="header-button flex">
            <popover title="申请列表" trigger="click" placement="bottom">
                <template slot="content">
                    <list item-layout="horizontal" :data-source="applyList">
                        <list-item
                            slot="renderItem"
                            slot-scope="item, index"
                            :key="index"
                        >
                            <div class="flex">
                                <p class="list-name">{{ item.name }}</p>
                                <a-button class="list-btn" @click="agree">
                                    同意
                                </a-button>
                                <a-button
                                    class="list-btn"
                                    type="primary"
                                    @click="refuse"
                                >
                                    拒绝
                                </a-button>
                            </div>
                        </list-item>
                    </list>
                </template>
                <div class="notice-div">
                    <a-button class="notice-btn flex" type="link">
                        <badge :count="applyList.length" dot>
                            <a-icon class="notice" type="notification"></a-icon>
                        </badge>
                    </a-button>
                </div>
            </popover>
            <a-button
                class="invite btn"
                icon="user-add"
                type="primary"
                @click="success"
            >
                邀请
            </a-button>
            <a-button
                class="btn"
                icon="export"
                type="danger"
                @click="exitConfirm"
            >
                离开
            </a-button>
        </div>
    </div>
</template>
<script>
import {
    Button,
    Icon,
    Message,
    Modal,
    Popover,
    Badge,
    List,
} from 'ant-design-vue';
import Vue from 'vue';
Vue.use(Modal);

export default {
    props: ['name'],
    components: {
        AButton: Button,
        AIcon: Icon,
        Popover,
        Badge,
        List,
        ListItem: List.Item,
    },
    data() {
        return {
            applyList: [],
        };
    },
    methods: {
        success() {
            let input = document.createElement('input');
            input.value = window.location.href;
            document.body.appendChild(input);
            input.select();
            document.execCommand('Copy');
            document.body.removeChild(input);
            Message.success('邀请链接已复制到剪贴板');
        },
        exitConfirm() {
            Modal.confirm({
                title: '请确认是否要离开会议',
                okText: '确定',
                cancelText: '返回',
                iconType: 'exclamation-circle',
                onOk() {
                    window.location.href = '/team';
                },
            });
        },
        agree() {
            //TODO 将申请人从申请列表中删除，加入会议室成员列表
        },
        refuse() {
            Modal.confirm({
                title: '确定要拒绝此申请吗？',
                content: '点击确认后, 此申请会被拒绝',
                okText: '确认',
                cancelText: '取消',
                onOk() {
                    // TODO 将申请人从申请列表中删除
                },
            });
        },
    },
};
</script>
<style scoped>
.header {
    position: fixed;
    height: 60px;
    width: 100%;
    background-color: var(--white);
}
.header-theme {
    margin-left: 20px;
}
.info {
    width: 30px;
    height: 30px;
    font-size: 20px;
    color: var(--black);
}
.anticon {
    display: flex;
    font-style: normal;
    line-height: 0;
    text-align: center;
    text-transform: none;
    vertical-align: -0.125em;
    text-rendering: optimizeLegibility;
    -webkit-font-smoothing: antialiased;
}
.theme {
    margin: 0;
    color: var(--black);
}
.notice-div {
    padding-top: 5px;
    margin-right: 30px;
}
.notice-btn {
    padding: 0;
}
.notice {
    color: var(--black);
    font-size: 17px;
}
.notice:focus,
.notice:hover {
    color: var(--primary-color-1);
}
.btn {
    padding: 0 10px;
    margin: 0 5px;
}
.list-name {
    margin-right: 50px;
}
.list-btn {
    padding: 5px;
    width: 50px;
    font-size: 12px;
    margin: 0 2px;
}
</style>
