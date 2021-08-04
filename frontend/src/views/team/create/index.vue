<template>
    <div>
        <div class="create-card" v-show="!isFormShow">
            <card class="card" :bordered="false">
                <a-button
                    id="btn"
                    type="link"
                    icon="plus-circle"
                    :size="size"
                    @click="showForm"
                />
                <p class="create-title">创建团队</p>
                <p class="create-content">创建团队，开始Meeting Table之旅</p>
            </card>
            <card class="card" :bordered="false">
                <a-button
                    id="btn"
                    type="link"
                    icon="form"
                    :size="size"
                    @click="showModal"
                />

                <p class="create-title">申请加入</p>
                <p class="create-content">加入已有团队，体验会议协作</p>
            </card>
        </div>
        <create-form v-show="isFormShow" />
        <modal
            v-model="visible"
            @ok="onSubmit"
            title="申请加入"
            okText="提交"
            cancelText="取消"
        >
            <form-model ref="ruleForm" :model="form" :rules="rules">
                <form-model-item ref="link" prop="link">
                    <a-input
                        v-model="form.link"
                        placeholder="请输入团队分享链接"
                    ></a-input>
                </form-model-item>
            </form-model>
        </modal>
        <modal
            v-model="formVisible"
            @ok="onsubmitForm"
            title="创建团队"
            okText="提交"
            cancelText="取消"
        >
            <form-model
                ref="ruleForm"
                :model="teamForm"
                :rules="formRules"
                layout="vertical"
            >
                <form-model-item ref="name" prop="name">
                    <a-input
                        class="input"
                        v-model="teamForm.name"
                        @blur="
                            () => {
                                $refs.name.onFieldBlur();
                            }
                        "
                        placeholder="请输入团队名称"
                    />
                </form-model-item>
                <form-model-item prop="description">
                    <a-input
                        class="input description"
                        v-model="teamForm.description"
                        type="textarea"
                        placeholder="请输入团队简介"
                    />
                </form-model-item>
            </form-model>
        </modal>
    </div>
</template>

<script>
import { Card, Button, Modal, Input, FormModel, Message } from 'ant-design-vue';
import {
    TEAM_NAME_MIN_LENGTH,
    TEAM_NAME_MAX_LENGTH,
    TEAM_DESCRIPTION_MAX_LENGTH,
} from '../../../constants/team';
import { createTeam } from '../../../requests/team';
import { defaultErrorHandler } from '../../../requests/errors';
import router from '../../../router';

export default {
    components: {
        Card,
        AButton: Button,
        Modal,
        AInput: Input,
        FormModel,
        FormModelItem: FormModel.Item,
    },
    data() {
        let handleUrl = (rule, value, callback) => {
            if (!this.isTrueUrl(value)) {
                callback(new Error('请输入正确的链接'));
            } else {
                callback();
            }
        };
        return {
            size: 'large',
            formVisible: false,
            visible: false,
            form: {
                link: '',
            },
            rules: {
                link: [
                    {
                        required: true,
                        message: '请输入链接地址',
                        trigger: 'blur',
                    },
                    { validator: handleUrl, trigger: 'blur' },
                ],
            },
            teamForm: {
                name: '',
                description: '',
            },
            formRules: {
                name: [
                    {
                        required: true,
                        message: '请输入团队名称',
                        trigger: 'blur',
                    },
                    {
                        min: TEAM_NAME_MIN_LENGTH,
                        max: TEAM_NAME_MAX_LENGTH,
                        message: `请控制在${TEAM_NAME_MIN_LENGTH}-${TEAM_NAME_MAX_LENGTH}个字符以内`,
                        trigger: 'blur',
                    },
                ],
                description: [
                    {
                        required: true,
                        message: '请输入团队简介',
                        trigger: 'blur',
                    },
                    {
                        max: TEAM_DESCRIPTION_MAX_LENGTH,
                        message: `请控制在${TEAM_DESCRIPTION_MAX_LENGTH}个字符以内`,
                        trigger: 'blur',
                    },
                ],
            },
        };
    },
    methods: {
        isTrueUrl(value) {
            let hostname = `^${window.location.hostname}`;
            let hostnameReg = RegExp(hostname);
            if (value.startsWith('http://')) {
                let hostnameIndex = value.indexOf('://') + '://'.length;
                let url = value.slice(hostnameIndex);
                return hostnameReg.test(url);
            } else return hostnameReg.test(value);
        },
        showModal() {
            this.visible = true;
        },
        showForm() {
            this.formVisible = true;
        },
        onSubmit() {
            this.$refs.ruleForm.validate((valid) => {
                if (valid) {
                    window.open(this.form.link, '_self');
                }
            });
        },
        onSubmitForm() {
            this.$refs.ruleForm.validate((valid) => {
                if (valid) {
                    createTeam(this.form.name, this.form.description)
                        .then(() => {
                            Message.success('创建成功');
                            router.push('/team');
                        })
                        .catch(defaultErrorHandler(createTeam));
                }
            });
        },
    },
};
</script>

<style scoped>
.card {
    width: 380px;
    background-color: var(--white);
    border-radius: var(--border-radius);
}
.card:hover {
    transform: translateY(-5px);
    transition: 300ms;
}
.create-card {
    display: flex;
    justify-content: space-around;
    background: #f1f3f8;
    padding: 200px 280px;
    min-height: 100vh;
    width: 100%;
    text-align: center;
}
.create-title {
    font-size: 24px;
    font-weight: 900;
    margin-bottom: 10px;
    width: 100%;
    text-align: center;
}
.create-content {
    font-size: 16px;
    width: 100%;
    text-align: center;
}
#btn {
    color: #ffcc5f;
    width: 230px;
    height: 230px;
    font-size: 100px;
    padding: 50px;
    padding-top: 70px;
    padding-bottom: 0;
}
</style>
