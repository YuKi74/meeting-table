<template>
    <div class="login">
        <div class="card">
            <div class="tip">登录</div>
            <form-model :model="form" :rules="rules" ref="form">
                <form-model-item prop="email">
                    <guest-input
                        placeholder="请输入邮箱"
                        v-model="form.email"
                    />
                </form-model-item>
                <div class="blank-space"></div>
                <form-model-item prop="password">
                    <password-input
                        placeholder="请输入密码"
                        v-model="form.password"
                        :visibilityToggle="true"
                        @keyup.enter="submitLogin"
                    />
                </form-model-item>
                <div class="blank-space"></div>
                <form-model-item>
                    <submit-btn
                        class="button"
                        :disabled="form.password === ''"
                        @click="submitLogin"
                    >
                        立即进入
                    </submit-btn>
                </form-model-item>
                <form-model-item>
                    <router-link to="/register" class="linkto">
                        还没有账号？点击这里注册
                    </router-link>
                </form-model-item>
            </form-model>
        </div>
    </div>
</template>

<script>
import { Input, Button, FormModel, Message } from 'ant-design-vue';
import { login } from '../../requests/user';
import {
    EMAIL_MAX_LENGTH,
    PASSWORD_MIN_LENGTH,
    PASSWORD_MAX_LENGTH,
} from '../../constants/user';
import { defaultErrorHandler } from '../../requests/errors';
import Cookies from 'js-cookie';
import router from '../../router';

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
                email: '',
                password: '',
            },
            rules: {
                email: [
                    {
                        required: true,
                        message: '请输入邮箱',
                        trigger: 'blur',
                    },
                    {
                        max: EMAIL_MAX_LENGTH,
                        message: `邮箱长度应小于${EMAIL_MAX_LENGTH}`,
                        trigger: 'change',
                    },
                    {
                        type: 'email',
                        message: '邮箱格式不正确',
                        trigger: 'blur',
                    },
                ],
                password: [
                    { required: true, message: '请输入密码', trigger: 'blur' },
                    {
                        min: PASSWORD_MIN_LENGTH,
                        max: PASSWORD_MAX_LENGTH,
                        message: `密码长度应在${PASSWORD_MIN_LENGTH}-${PASSWORD_MAX_LENGTH}位之间`,
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
        submitLogin: function () {
            const form = this.form;
            this.$refs.form.validate((valid) => {
                if (valid) {
                    login(form.email, form.password)
                        .then((data) => {
                            Cookies.set('token', data.data.token);
                            Message.success('登录成功');
                            router.push('/team');
                        })
                        .catch(defaultErrorHandler(login));
                }
            });
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
    background-color: var(--primary-color-1);
    color: var(--black);
    height: 40px;
    width: 100%;
}
.blank-space {
    height: 20px;
}
.tip {
    text-align: center;
    font-size: 24px;
    justify-content: center;
    margin-bottom: 30px;
    font-weight: bolder;
}
.login {
    height: 100vh;
    width: 100vw;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: var(--background);
}
.card {
    width: 500px;
    padding: 64px 64px 40px;
    border-radius: var(--border-radius);
    background-color: var(--white);
    display: flex;
    flex-direction: column;
    position: relative;
}
.linkto {
    color: var(--black);
}

.linkto:hover {
    color: var(--primary-color-1);
}
</style>
