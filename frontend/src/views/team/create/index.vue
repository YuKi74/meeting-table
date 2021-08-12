<template>
    <div class="content flex main-axis-center">
        <user-detail class="user-detail" />
        <card
            class="card card-margin-right"
            :bordered="false"
            @click="showForm"
        >
            <a-icon class="icon" type="plus-circle" />
            <p class="create-title">创建团队</p>
            <p class="create-content">创建团队，开始Meeting Table之旅</p>
        </card>
        <card class="card" :bordered="false" @click="showModal">
            <a-icon class="icon" type="form" />
            <p class="create-title">申请加入</p>
            <p class="create-content">加入已有团队，体验会议协作</p>
        </card>
        <modal
            v-model="visible"
            @ok="onSubmit"
            @cancel="onCancel"
            title="加入团队"
            okText="查看"
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
            @ok="onSubmitForm"
            @cancel="onCancelForm"
            title="创建团队"
            okText="提交"
            cancelText="取消"
        >
            <form-model
                ref="teamRuleForm"
                :model="teamForm"
                :rules="formRules"
                layout="vertical"
            >
                <form-model-item ref="name" prop="name">
                    <a-input
                        class="input"
                        v-model="teamForm.name"
                        placeholder="请输入团队名称"
                    />
                </form-model-item>
                <form-model-item prop="description">
                    <a-input
                        class="input"
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
import { Card, Icon, Modal, Input, FormModel, Message } from 'ant-design-vue';
import {
    TEAM_NAME_MIN_LENGTH,
    TEAM_NAME_MAX_LENGTH,
    TEAM_DESCRIPTION_MAX_LENGTH,
    TEAM_UUID_LENGTH,
} from '../../../constants/team';
import { createTeam, getTeaminfo } from '../../../requests/team';
import Errors, { defaultErrorHandler } from '../../../requests/errors';
import router from '../../../router';
import UserDetail from '../../../components/team/UserDetail.vue';

export default {
    components: {
        Card,
        AIcon: Icon,
        Modal,
        AInput: Input,
        FormModel,
        FormModelItem: FormModel.Item,
        UserDetail,
    },
    data() {
        let handleUrl = (rule, value, callback) => {
            if (!this.isTrueUrl(value)) {
                callback(new Error('请输入正确的团队链接'));
            } else {
                callback();
            }
        };
        return {
            temporaryForm: '',
            temporaryTeam: '',
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
            let hostname = `^${window.location.hostname}/team/`;
            let hostnameReg = RegExp(hostname);
            if (value.startsWith('http://')) {
                let hostnameIndex = value.indexOf('://') + '://'.length;
                let url = value.slice(hostnameIndex);
                if (hostnameReg.test(url)) {
                    const uuid = this.form.link.slice(
                        this.form.link.indexOf('/team/') + '/team/'.length,
                        this.form.link.length
                    );
                    if (uuid.length < TEAM_UUID_LENGTH) {
                        return false;
                    }
                    return true;
                }
            } else return hostnameReg.test(value);
        },
        showModal() {
            this.visible = true;
            this.temporaryForm = JSON.parse(JSON.stringify(this.form));
        },
        showForm() {
            this.formVisible = true;
            this.temporaryTeam = JSON.parse(JSON.stringify(this.teamForm));
        },
        onSubmit() {
            this.$refs.ruleForm.validate((valid) => {
                if (valid) {
                    const uuid = this.form.link.slice(
                        this.form.link.indexOf('/team/') + '/team/'.length,
                        this.form.link.length
                    );
                    getTeaminfo(uuid)
                        .then(() => {
                            this.$router.push('/team/' + uuid);
                        })
                        .catch((data) => {
                            if (data.error === Errors.ERROR_INPUT) {
                                Message.error('请输入正确的团队链接');
                            } else {
                                defaultErrorHandler(getTeaminfo)(data);
                            }
                        });
                }
            });
        },
        onCancel() {
            this.visible = false;
            this.form = this.temporaryForm;
        },
        onSubmitForm() {
            this.$refs.teamRuleForm.validate((valid) => {
                if (valid) {
                    createTeam(this.teamForm.name, this.teamForm.description)
                        .then(() => {
                            Message.success('创建成功');
                            router.push('/team');
                        })
                        .catch(defaultErrorHandler(createTeam));
                }
            });
        },
        onCancelForm() {
            this.formVisible = false;
            this.teamForm = this.temporaryTeam;
        },
    },
};
</script>

<style scoped>
.user-detail {
    width: 50px;
    height: 50px;
    position: fixed;
    top: 40px;
    right: 40px;
}
.content {
    background-color: var(--background);
    min-width: 100vw;
    min-height: 100vh;
}
.card {
    width: 380px;
    height: 430px;
    background-color: var(--white);
    border-radius: var(--border-radius);
    display: flex;
    flex-direction: column;
    align-items: center;
}
.card:hover {
    cursor: pointer;
    transform: translateY(-5px);
    transition: 300ms;
}
.card-margin-right {
    margin-right: 50px;
}
.create-title {
    font-size: 24px;
    font-weight: 900;
    margin-bottom: 10px;
    text-align: center;
}
.create-content {
    font-size: 16px;
    text-align: center;
}
.icon {
    color: var(--primary-color-1);
    font-size: 100px;
    height: 230px;
    min-width: 230px;
    display: flex;
    justify-content: center;
    align-items: center;
}
.input {
    width: 472px;
}
</style>
