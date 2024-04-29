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
        <a-textarea
            :rows="1"
            v-model="value"
            @pressEnter="enter"
            class="input"
        />
    </div>
</template>
<script>
import { Input, Spin } from 'ant-design-vue';
import { TIME_INTERVAL } from '../../constants/meeting-room';
import { getUserinfo } from '../../requests/user';
import { defaultErrorHandler } from '../../requests/errors';
export default {
    props: ['connection', 'id', 'content'],
    components: {
        ATextarea: Input,
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
        this.messages = JSON.parse(JSON.stringify(this.content));
        getUserinfo()
            .then((user) => {
                this.userId = user.data.id;
                this.userName = user.data.name;
                this.connection.addMessageHandler(
                    (data) => {
                        return this.id === data.Target && data.Type === 'im';
                    },
                    this.receive,
                    this
                );
            })
            .catch(defaultErrorHandler(getUserinfo));
    },
    computed: {
        messagesLength() {
            return this.messages.length;
        },
    },
    methods: {
        enter(e) {
            e.preventDefault();
            if (this.value === '') {
                return;
            }
            let message = {
                message: this.value,
                name: this.userName,
                id: this.userId,
            };
            this.commitList.push(message);
            this.value = '';
            setTimeout(() => {
                this.$refs.msgboard.scrollTop =
                    this.$refs.msgboard.scrollHeight;
            }, 1);
            this.connection.send({
                Type: 'im',
                Target: this.id,
                Data: message,
            });
        },
        receive(data) {
            this.isPop = true;
            this.setPopContent(data.Data.id === this.userId);
            this.messages.push(data.Data);
            setTimeout(() => {
                this.$refs.msgboard.scrollTop =
                    this.$refs.msgboard.scrollHeight;
            }, 1);
            setTimeout(() => {
                this.isPop = false;
            }, TIME_INTERVAL);
        },
        setPopContent(isOwn) {
            if (isOwn) {
                this.commitList.shift();
                this.popContent = '消息发送成功';
            } else {
                this.popContent = '您有新的消息';
            }
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
    background-color: var(--white);
}
.msgboard {
    width: 100%;
    height: 100%;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    padding-top: 3px;
}
.msg-container-left {
    display: flex;
    flex-direction: column;
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
    margin-top: 0;
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
    margin-top: 0;
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
    border-color: transparent;
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
.input {
    background-color: var(--white);
}
</style>
