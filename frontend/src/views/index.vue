<template>
    <div class="whole-page">
        <div class="header flex main-axis-between">
            <div class="logo flex">Meeting-Table</div>
            <div class="right-top" v-if="!isOn">
                <div class="login flex" @click="login">登录</div>
                <div class="register flex" @click="register">注册</div>
            </div>
            <div class="right-top info flex" v-if="isOn" @click="toTeam">
                <a-avatar
                    shape="square"
                    icon="user"
                    size="large"
                    style="background: var(--secondary-color-1)"
                />
                <div class="box">
                    <div class="id">{{ name }}</div>
                    <div class="tip">您已登录，点击进入</div>
                </div>
            </div>
        </div>
        <div class="body">
            <div class="left">
                <a-icon class="message-icon" type="message" />
                <div class="title">
                    随时随地与你的团队<br />一起创造价值，激发潜能
                </div>
                <div class="introduce">
                    一款好用的 针对数字化产品的 全在线可视化 协作工具<br />轻量便捷、
                    多人协作 帮助将分布式团队随时随地 聚集一处，<br />让每一个人都潜能无限
                </div>
                <a-icon class="chart-icon" type="pie-chart" />
            </div>
            <div class="right flex">
                <img class="picture" src="../assets/table-picture.png" alt="" />
            </div>
        </div>
    </div>
</template>
<script>
import { Icon, Avatar } from 'ant-design-vue';
import { getUserinfo } from '../requests/user';
import Cookies from 'js-cookie';
import router from '../router';

export default {
    components: {
        AIcon: Icon,
        AAvatar: Avatar,
    },
    data: function () {
        return {
            isOn: false,
            name: 'userid',
        };
    },
    mounted() {
        if (!Cookies.get('token')) {
            this.isOn = false;
        } else {
            getUserinfo().then((data) => {
                this.name = data.data.name;
                this.isOn = true;
            });
        }
    },
    methods: {
        login: function () {
            router.push('/login');
        },
        register: function () {
            router.push('/register');
        },
        toTeam: function () {
            router.push('/team');
        },
    },
};
</script>
<style scoped>
.id {
    font-size: 18px;
    font-weight: bold;
    width: 130px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.tip {
    font-size: 10px;
    margin-left: 10px;
    color: var(--black);
}
.box {
    flex-direction: column;
    margin-left: 10px;
}
.login {
    font-size: 18px;
    font-weight: bold;
    width: 36px;
}
.login:hover {
    cursor: pointer;
    transform: scale3d(1.05, 1.05, 1);
    color: var(--black);
}
.register {
    margin-left: 20px;
    font-size: 18px;
    font-weight: bold;
    width: 36px;
}
.register:hover {
    cursor: pointer;
    transform: scale3d(1.05, 1.05, 1);
    color: var(--black);
}
.right-top {
    width: 200px;
    height: 70px;
    display: flex;
}
.right-top:hover {
    cursor: pointer;
}
.picture {
    text-align: center;
    width: 100%;
}
.chart-icon {
    font-size: 500px;
    color: #5b8ee70e;
    float: left;
    transform: translate(-100px, 0);
}
.message-icon {
    font-size: 200px;
    color: var(--secondary-color-2);
    transform: rotate(-30deg);
    float: right;
}
.title {
    margin-top: 240px;
    font-size: 40px;
    font-weight: bolder;
    text-align: center;
    margin-left: 25%;
    color: var(--black);
}
.introduce {
    margin-top: 25px;
    margin-left: 27%;
    font-size: 15px;
    text-align: center;
    width: 70%;
}
.body {
    display: flex;
    height: calc(100vh - 70px);
    overflow: hidden;
}
.left {
    width: 40%;
}
.right {
    padding-bottom: 90px;
    width: 60%;
    display: flex;
    justify-content: center;
}
.logo {
    margin-left: 100px;
    font-size: 25px;
    font-family: fantasy;
    text-align: center;
    height: 100%;
    color: var(--black);
    width: 160px;
    white-space: nowrap;
}
.whole-page {
    background: linear-gradient(var(--secondary-color-2), var(--white));
    width: 100%;
    height: 100vh;
}
.header {
    height: 70px;
    width: 100%;
    display: flex;
}
</style>
