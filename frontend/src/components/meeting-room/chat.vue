<template>
    <div class="container">
        <p class="header">聊天室</p>
        <div class="msgboard" ref="msgboard">
            <div
                v-for="(item, index) in messages"
                :key="index"
                :class="[
                    item.id !== userId
                        ? 'self-cross-axis-start'
                        : 'self-cross-axis-end',
                ]"
            >
                <div class="msg-container-left" v-show="item.id !== userId">
                    <div>
                        <p class="title">{{ item.name }}</p>
                    </div>
                    <div class="chat-left">
                        <div class="fill-left"></div>
                        <p>{{ item.message }}</p>
                    </div>
                </div>
                <div class="msg-container-right" v-show="item.id === userId">
                    <div class="chat-right">
                        <div class="fill-right"></div>
                        <p>{{ item.message }}</p>
                    </div>
                </div>
            </div>
            <div
                v-for="(item, index) in commitList"
                :key="index + messagesLength"
                class="self-cross-axis-end"
            >
                <div class="msg-container-right">
                    <div>
                        <a-spin class="loading"> </a-spin>
                    </div>
                    <div class="chat-right">
                        <div class="fill-right"></div>
                        <p>{{ item.message }}</p>
                    </div>
                </div>
            </div>
        </div>
        <p v-if="isPop">{{ popContent }}</p>
        <a-textarea id="input" :rows="1" v-model="value" @pressEnter="enter" />
    </div>
</template>
<script>
import { Input, Spin } from 'ant-design-vue';
import { TIME_INTERVAL } from '../../constants/meeting-room';
export default {
    components: {
        ATextarea: Input.TextArea,
        ASpin: Spin,
    },
    data() {
        return {
            messages: [],
            popContent: '您有新消息',
            isPop: false,
            commitList: [],
            userName: '',
            userId: null,
            value: '',
        };
    },
    mounted: function () {
        // TODO  加载时获取用户名和id
    },
    computed: {
        messagesLength() {
            return this.messages.length;
        },
    },
    watch: {
        messages: function (val) {
            this.isPop = true;
            if (val[val.length - 1] === this.commitList[0]) {
                this.commitList.shift();
                this.popContent = '消息发送成功';
            } else {
                this.popContent = '您有新的消息';
            }
            setTimeout(() => {
                this.isPop = false;
            }, TIME_INTERVAL);
        },
    },
    methods: {
        enter(e) {
            e.preventDefault();
            let message = {
                message: this.value,
                name: this.userName,
                id: this.userId,
            };
            this.$emit('update-input', message);
            this.commitList.push(message);
            this.value = '';
            setTimeout(() => {
                this.$refs.msgboard.scrollTop =
                    this.$refs.msgboard.scrollHeight;
            }, 1);
        },
    },
};
</script>
<style scoped>
* {
    margin: 0;
    padding: 0;
}
.container {
    display: flex;
    flex-direction: column;
    align-items: center;
    border: 5px solid var(--secondary-color-1);
}
.msgboard {
    width: 100%;
    height: 400px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
}
.msg-container-left {
    display: flex;
    align-items: center;
    justify-content: flex-start;
}
.msg-container-right {
    display: flex;
    align-items: center;
    justify-content: flex-end;
}
.chat-left {
    position: relative;
    border: 2px solid;
    border-color: var(--primary-color-2);
    border-radius: 5px;
    width: 80%;
    display: inline-block;
    word-break: break-all;
    padding: 10px;
    margin: 20px;
    background-color: var(--primary-color-2);
}
.chat-right {
    position: relative;
    border: 2px solid;
    border-color: var(--secondary-color-2);
    border-radius: 5px;
    width: 80%;
    display: inline-block;
    word-break: break-all;
    padding: 10px;
    margin: 20px;
    background-color: var(--secondary-color-2);
}
.fill-left {
    position: absolute;
    top: 15px;
    border-width: 10px;
    border-style: solid;
    left: -20px;
    border-color: transparent var(--primary-color-2) transparent transparent;
}
.fill-right {
    position: absolute;
    top: 15px;
    border-width: 10px;
    border-style: solid;
    right: -20px;
    border-color: transparent transparent transparent var(--secondary-color-2);
}
.title {
    white-space: nowrap;
    margin: 5px;
}
.header {
    font-size: larger;
    border-bottom: 5px solid var(--secondary-color-1);
    color: var(--black);
}
</style>
