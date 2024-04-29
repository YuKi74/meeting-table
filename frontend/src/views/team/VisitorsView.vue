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
            <user-detail class="user-detail" v-if="isLogin" />
            <a-button
                class="btn"
                type="primary"
                shape="circle"
                size="large"
                @click="login"
                v-else
            >
                登录
            </a-button>
        </div>
    </body>
</template>

<script>
import { Card, Button, Icon, Message } from 'ant-design-vue';
import { getTeaminfo, submitApplication } from '../../requests/team';
import { getUserinfo } from '../../requests/user';
import router from '../../router';
import Cookies from 'js-cookie';
import { defaultErrorHandler } from '../../requests/errors';
import UserDetail from '../../components/team/UserDetail.vue';

export default {
    props: ['uuid'],
    components: {
        Card,
        AButton: Button,
        Icon,
        UserDetail,
    },
    data() {
        return {
            isLogin: false,
            selfname: 'name',
            name: '',
            description: '',
        };
    },
    mounted: function () {
        this.isLogin = Cookies.get('token') !== undefined;
        getTeaminfo(this.uuid)
            .then((data) => {
                this.name = data.data.name;
                this.description = data.data.introduction;
            })
            .catch(defaultErrorHandler(getTeaminfo));
        getUserinfo()
            .then((data) => {
                this.selfname = data.data.name;
            })
            .catch(defaultErrorHandler(getUserinfo));
    },
    methods: {
        login() {
            router.push('/login');
        },
        attendRequest() {
            submitApplication(this.uuid)
                .then(() => {
                    Message.success('请求已发送！');
                })
                .catch(defaultErrorHandler(submitApplication));
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
    word-wrap: break-word;
}
.content {
    font-size: 16px;
    width: 100%;
    text-align: center;
    word-wrap: break-word;
}
.icon {
    color: #ffcc5f;
    width: 100%;
    height: 160px;
    font-size: 100px;
    padding: 30px;
}
.user-detail {
    position: absolute;
    right: 30px;
    top: 30px;
    width: 50px;
    height: 50px;
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
