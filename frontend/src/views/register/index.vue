<template>
    <div class="content flex main-axis-center background">
        <card :bordered="true" class="card" :headStyle="headStyle">
            <div class="flex reg">注册</div>
            <div class="flex main-axis-center">
                <register-form :rules="rules" :model="ruleForm" ref="ruleForm">
                    <register-form-item prop="email">
                        <register-input
                            type="email"
                            placeholder="请输入邮箱"
                            class="input"
                            v-model="ruleForm.email"
                        />
                    </register-form-item>
                    <register-form-item prop="userName">
                        <register-input
                            placeholder="请输入用户名"
                            class="input"
                            v-model="ruleForm.userName"
                        />
                    </register-form-item>
                    <register-form-item prop="password">
                        <register-input
                            type="password"
                            :placeholder="passwordtext"
                            class="input"
                            v-model="ruleForm.password"
                        />
                    </register-form-item>
                    <register-form-item prop="confirmPassword">
                        <register-input
                            type="password"
                            placeholder="请确定密码"
                            class="input"
                            v-model="ruleForm.confirmPassword"
                        />
                    </register-form-item>
                    <div class="flex main-axis-around button-box">
                        <register-button
                            class="button"
                            @click="submitForm"
                            type="primary"
                        >
                            提交
                        </register-button>
                        <register-button
                            class="button"
                            @click="resetForm"
                            type="danger"
                        >
                            重置
                        </register-button>
                    </div>
                    <register-form-item>
                        <router-link to="/login" class="linkto">
                            已有账号？点击这里登录
                        </router-link>
                    </register-form-item>
                </register-form>
            </div>
        </card>
    </div>
</template>

<script>
import { FormModel, Input, Button, Card, Message } from 'ant-design-vue';
import { register } from '../../requests/user';
import {
    EMAIL_MAX_LENGTH,
    USER_NAME_MAX_LENGTH,
    PASSWORD_MIN_LENGTH,
    PASSWORD_MAX_LENGTH,
} from '../../constants/user';
import { defaultErrorHandler } from '../../requests/errors';
import router from '../../router';

export default {
    name: 'Register',
    components: {
        RegisterForm: FormModel,
        RegisterFormItem: FormModel.Item,
        RegisterInput: Input,
        RegisterButton: Button,
        Card,
    },
    data() {
        return {
            passwordtext:
                '请输入' +
                PASSWORD_MIN_LENGTH +
                '-' +
                PASSWORD_MAX_LENGTH +
                '位密码',
            ruleForm: {
                email: '',
                userName: '',
                password: '',
                confirmPassword: '',
            },
            rules: {
                email: [
                    { required: true, message: '请输入邮箱', trigger: 'blur' },
                    {
                        max: EMAIL_MAX_LENGTH,
                        message: '邮箱长度应小于' + EMAIL_MAX_LENGTH,
                        trigger: 'change',
                    },
                    {
                        type: 'email',
                        message: '邮箱格式不正确',
                        trigger: 'blur',
                    },
                ],
                userName: [
                    {
                        required: true,
                        message: '请输入用户名',
                        trigger: 'blur',
                    },
                    {
                        max: USER_NAME_MAX_LENGTH,
                        message: '姓名长度不超过' + USER_NAME_MAX_LENGTH,
                        trigger: 'blur',
                    },
                ],
                password: [
                    { required: true, message: '请输入密码', trigger: 'blur' },
                    {
                        min: PASSWORD_MIN_LENGTH,
                        message: '密码最小长度为' + PASSWORD_MIN_LENGTH + '位',
                        trigger: 'blur',
                    },
                    {
                        max: PASSWORD_MAX_LENGTH,
                        message: '密码长度最多为' + PASSWORD_MAX_LENGTH + '位',
                        trigger: 'blur',
                    },
                ],
                confirmPassword: [
                    {
                        required: true,
                        message: '请确定密码',
                        trigger: 'blur',
                    },
                    {
                        validator: (rule, value, callback) => {
                            value === this.ruleForm.password
                                ? callback()
                                : callback(new Error('两次输入不一致'));
                        },
                        trigger: 'blur',
                    },
                ],
            },
            headStyle: {
                'font-size': '30px',
                color: '#212529',
            },
        };
    },
    methods: {
        resetForm() {
            this.$refs.ruleForm.resetFields();
        },
        submitForm() {
            const form = this.ruleForm;
            this.$refs.ruleForm.validate((valid) => {
                if (valid) {
                    register(form.email, form.userName, form.password)
                        .then(() => {
                            Message.success('注册成功！正在跳转到首页');
                            router.push('/team');
                        })
                        .catch(defaultErrorHandler(register));
                }
            });
        },
    },
};
</script>

<style scoped>
.reg {
    font-size: 24px;
    justify-content: center;
    font-weight: bolder;
    margin-bottom: 20px;
}
.content {
    min-width: 100vw;
    min-height: 100vh;
    background-color: var(--background);
}
.card {
    padding-top: 30px;
    width: 500px;
    background-color: var(--white);
    border-radius: var(--border-radius);
}
.input {
    width: 360px;
    height: 32px;
    padding: 10px;
}

.button-box {
    width: 100%;
    margin: 0;
}
.button {
    width: 100px;
    margin: 20px;
}

.linkto {
    color: var(--black);
}

.linkto:hover {
    color: var(--primary-color-1);
}
</style>
