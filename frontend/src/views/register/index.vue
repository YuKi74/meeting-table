<template>
    <div class="content flex main-axis-center background">
        <Card
            title="注册"
            :bordered="true"
            class="shadow card"
            :headStyle="head_style"
        >
            <div class="flex main-axis-center">
                <register-form
                    layout="vertical"
                    :rules="rules"
                    :model="ruleForm"
                    ref="ruleForm"
                >
                    <register-form-item
                        has-feedback
                        label="邮箱："
                        prop="email"
                    >
                        <register-input
                            type="email"
                            placeholder="email"
                            class="input"
                            v-model="ruleForm.email"
                        />
                    </register-form-item>
                    <register-form-item
                        has-feedback
                        label="姓名："
                        prop="user_name"
                    >
                        <register-input
                            placeholder="name"
                            class="input"
                            v-model="ruleForm.user_name"
                        />
                    </register-form-item>
                    <register-form-item
                        has-feedback
                        label="密码："
                        prop="password"
                    >
                        <register-input
                            type="password"
                            placeholder="password"
                            class="input"
                            v-model="ruleForm.password"
                        />
                    </register-form-item>
                    <register-form-item
                        has-feedback
                        label="验证密码："
                        prop="comfirmpass"
                    >
                        <register-input
                            type="password"
                            placeholder="comfirm password"
                            class="input"
                            v-model="ruleForm.comfirmpass"
                        />
                    </register-form-item>
                    <register-form-item>
                        <register-button class="button" @click="resetForm">
                            重置
                        </register-button>
                        <register-button class="button" @click="submitForm">
                            提交
                        </register-button>
                    </register-form-item>
                    <register-form-item>
                        <router-link to="/login" class="linkto">
                            已有账号？点击这里登录吧
                        </router-link>
                    </register-form-item>
                </register-form>
            </div>
        </Card>
    </div>
</template>

<script>
import { FormModel, Input, Button, Card, Message } from 'ant-design-vue';
import { register } from '../../requests/user';
import Errors from '../../requests/errors';
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
            ruleForm: {
                email: '',
                user_name: '',
                password: '',
                comfirmpass: '',
            },
            rules: {
                email: [
                    { required: true, message: '请输入邮箱', trigger: 'blur' },
                    {
                        type: 'email',
                        message: '邮箱格式不正确',
                        trigger: 'blur',
                    },
                ],
                user_name: [
                    { required: true, message: '请输入姓名', trigger: 'blur' },
                    {
                        max: 32,
                        message: '姓名最长不超过32个字符',
                        trigger: 'blur',
                    },
                ],
                password: [
                    { required: true, message: '请输入密码', trigger: 'blur' },
                    { min: 6, message: '密码最小长度为6位', trigger: 'blur' },
                    { max: 64, message: '密码长度最多为64位', trigger: 'blur' },
                ],
                comfirmpass: [
                    {
                        required: true,
                        message: '请再次输入密码',
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
            head_style: {
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
                    register(form.email, form.user_name, form.password)
                        .then(() => {
                            Message.success('注册成功！正在跳转到登录界面');
                            router.push('/login');
                        })
                        .catch((data) => {
                            if (data.error === Errors.ERROR_INPUT) {
                                Message.error(data.data);
                            } else {
                                Message.error(data.error.message);
                            }
                        });
                }
            });
        },
    },
};
</script>

<style scoped>
* {
    margin: 0;
    border: 0;
    padding: 0;
}

.content {
    min-width: 100vw;
    min-height: 100vh;
}

.card {
    width: 400px;
    background-color: var(--white);
    border-radius: 10px;
}

.input {
    border: 1px var(--black) solid;
    width: 300px;
}

.button {
    width: 80px;
    background-color: var(--primary-color-2);
    margin: 20px;
    color: var(--black);
}

.linkto {
    color: var(--black);
}

.linkto:hover {
    color: var(--primary-color-1);
}
</style>
