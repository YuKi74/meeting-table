<template>
    <body>
        <div class="create-card">
            <card class="card" :bordered="false">
                <icon class="icon" type="team" />
                <p class="title">{{ name }}</p>
                <p class="content">
                    {{ description }}
                </p>
                <a-button type="primary" @click="attendRequest">
                    申请加入
                </a-button>
            </card>
            <a-button
                class="btn"
                type="primary"
                shape="circle"
                size="large"
                v-if="islogin"
            >
                {{ selfname[0] }}
            </a-button>
            <a-button
                class="btn"
                type="primary"
                shape="circle"
                size="large"
                v-else
            >
                登录
            </a-button>
        </div>
    </body>
</template>

<script>
import { Card, Button, Icon } from 'ant-design-vue';

export default {
    components: {
        Card,
        AButton: Button,
        Icon,
    },
    data() {
        return {
            islogin: true,
            selfname: 'name',
            name: '',
            description: '',
        };
    },
    mounted: function () {
        // TODO 获取团队信息
    },
    methods: {
        attendRequest() {
            // TODO 申请加入
        },
    },
};
</script>

<style scoped>
.card {
    width: 500px;
    background-color: var(--white);
    border-radius: var(--border-radius);
}
.create-card {
    display: flex;
    justify-content: center;
    background: var(--background);
    padding-top: 200px;
    padding-bottom: 250px;
    min-height: 100vh;
    width: 100%;
    text-align: center;
}
.title {
    color: #ffcc5f;
    font-size: 24px;
    font-weight: 900;
    margin-bottom: 10px;
    width: 100%;
    text-align: center;
}
.content {
    font-size: 16px;
    width: 100%;
    text-align: start;
}
.icon {
    color: #ffcc5f;
    width: 100%;
    height: 160px;
    font-size: 100px;
    padding: 30px;
}
.btn {
    letter-spacing: -2px;
    font-size: 16px;
    width: 50px;
    height: 50px;
    position: absolute;
    right: 30px;
    top: 30px;
}
</style>
