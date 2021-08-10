<template>
    <body>
        <div class="content flex main-axis-center">
            <card class="card" :bordered="false">
                <icon class="icon" type="calendar" />
                <p class="title">{{ name }}</p>
                <div class="attend flex main-axis-center">
                    <a-button type="primary" @click="showModal">
                        申请进入
                    </a-button>
                </div>
            </card>
            <modal
                v-model="visible"
                @ok="onSubmit"
                title="申请进入会议室"
                okText="提交"
                cancelText="取消"
            >
                <form-model ref="ruleForm" :model="form" :rules="rules">
                    <form-model-item ref="extendName" prop="extendName">
                        <a-input
                            v-model="form.extendName"
                            placeholder="请输入您的入会名称"
                        ></a-input>
                    </form-model-item>
                </form-model>
            </modal>
        </div>
    </body>
</template>

<script>
import {
    Card,
    Button,
    Icon,
    Modal,
    FormModel,
    Message,
    Input,
} from 'ant-design-vue';
import { VISITOR_NAME_MAX_LENGTH } from '../../constants/meeting-room';
import router from '../../router';
import Cookies from 'js-cookie';

export default {
    components: {
        Card,
        AButton: Button,
        Icon,
        Modal,
        FormModel,
        FormModelItem: FormModel.Item,
        AInput: Input,
    },
    data() {
        return {
            isLogin: '',
            name: '',
            description: '',
            visible: false,
            form: {
                extendName: '',
            },
            rules: {
                extendName: [
                    {
                        required: true,
                        message: '请输入入会名称',
                        trigger: 'blur',
                    },
                    {
                        max: VISITOR_NAME_MAX_LENGTH,
                        message: '名称长度不超过' + VISITOR_NAME_MAX_LENGTH,
                        trigger: 'blur',
                    },
                ],
            },
        };
    },
    mounted: function () {
        this.isLogin = Cookies.get('token') !== undefined;
    },
    methods: {
        login() {
            router.push('/login');
        },
        showModal() {
            this.visible = true;
        },
        onSubmit() {
            this.$refs.ruleForm.validate((valid) => {
                if (valid) {
                    Message.success('已提交申请');
                    this.visible = false;
                }
            });
        },
    },
};
</script>

<style scoped>
.card {
    height: 430px;
    width: 500px;
    background-color: var(--white);
    border-radius: var(--border-radius);
    display: flex;
    flex-direction: column;
    align-items: center;
}

.title {
    color: var(--secondary-color-2);
    font-size: 24px;
    font-weight: 900;
    margin-bottom: 10px;
    width: 100%;
    min-height: 50px;
    text-align: center;
}
.content {
    background-color: var(--background);
    min-width: 100vw;
    min-height: 100vh;
}
.icon {
    color: var(--secondary-color-2);
    width: 100%;
    height: 190px;
    font-size: 120px;
    padding-top: 40px;
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
.user-detail {
    position: absolute;
    right: 30px;
    top: 30px;
}
.attend {
    width: 100%;
}
</style>
