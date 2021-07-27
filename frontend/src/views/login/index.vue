<template>
    <div class="login">
        <div class="card">
            <div class="tip">登录</div>
            <form-model :model="form" :rules="rules" ref="form">
                <form-model-item prop="id">
                    <guest-input
                        placeholder="请输入邮箱"
                        v-model="form.id"
                        class="input"
                    >
                    </guest-input>
                </form-model-item>
                <div class="blank-space"></div>
                <form-model-item prop="password">
                    <password-input
                        placeholder="请输入密码"
                        v-model="form.password"
                        :visibilityToggle="true"
                        class="input"
                    >
                    </password-input>
                </form-model-item>
                <div class="blank-space"></div>
                <form-model-item>
                    <submit-btn class="button" :disabled="form.password === ''"
                        >立即进入</submit-btn
                    >
                </form-model-item>
                <div class="blank-space"></div>
                <div class="blank-space"></div>
                <div class="blank-space"></div>
                <form-model-item>
                    <div class="to-register">
                        还没有账号？
                        <span @click="register">去注册</span>
                    </div>
                </form-model-item>
            </form-model>
        </div>
    </div>
</template>

<script>
import { Input, Button, FormModel } from 'ant-design-vue';

export default {
    name: 'Home',
    components: {
        GuestInput: Input,
        SubmitBtn: Button,
        PasswordInput: Input.Password,
        FormModel: FormModel,
        FormModelItem: FormModel.Item,
    },
    data: () => {
        return {
            form: {
                userid: '',
                password: '',
            },
            rules: {
                id: [
                    {
                        required: true,
                        message: '请输入邮箱',
                        trigger: 'blur',
                    },
                    {
                        max: 50,
                        message: '邮箱长度应小于50',
                        trigger: 'change',
                    },
                ],
                password: [
                    { required: true, message: '请输入密码', trigger: 'blur' },
                    {
                        min: 6,
                        max: 64,
                        message: '密码长度应在6-64位之间',
                        trigger: 'change',
                    },
                ],
            },
        };
    },
    methods: {
        register: function () {
            this.$router.push('/register');
        },
    },
};
</script>

<style scoped>
.to-register {
    text-align: right;
}
.to-register span {
    text-decoration: underline;
    cursor: pointer;
}
.button {
    background-color: black;
    color: white;
    height: 40px;
    width: 100%;
}
.blank-space {
    height: 20px;
}
.input {
    height: 40px;
}
div {
    text-align: center;
}
.tip {
    font-size: 24px;
    justify-content: center;
    margin-bottom: 30px;
    font-weight: bolder;
    color: black;
}
.login {
    height: 100vh;
    width: 100vw;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #dde1ea;
}
.card {
    width: 500px;
    padding: 64px 64px 40px;
    border-radius: 1.5rem;
    background-color: #f5f6f9;
    display: flex;
    flex-direction: column;
    position: relative;
}
</style>
