<template>
    <div class="header flex shadow main-axis-between">
        <div class="header-theme flex">
            <a-icon class="info flex cross-axis-center" type="info-circle" />
            <p class="theme">会议主题：{{ name }}</p>
        </div>
        <div class="header-button flex">
            <a-button
                class="invite btn"
                icon="eye"
                type="primary"
                @click="$emit('share-view')"
            >
                共享视角
            </a-button>
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
import { Button, Icon, Message, Modal } from 'ant-design-vue';
import Vue from 'vue';
Vue.use(Modal);

export default {
    props: ['name'],
    components: {
        AButton: Button,
        AIcon: Icon,
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
                title: '请确定是否要离开会议',
                okText: '确定',
                cancelText: '返回',
                iconType: 'exclamation-circle',
                onOk() {
                    window.location.href = '/team';
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
    padding-right: 5px;
}
.header-theme {
    margin-left: 10px;
}
.info {
    padding-top: 4.5px;
    width: 30px;
    height: 30px;
    font-size: 20px;
    color: var(--black);
}
.theme {
    margin: 0;
    color: var(--black);
}

.btn {
    padding: 0 10px;
    margin: 0 5px;
}
</style>
