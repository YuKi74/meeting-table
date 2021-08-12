<template>
    <div>
        <popover placement="bottomRight">
            <template slot="content">
                <div class="content">
                    <div class="title flex main-axis-around">
                        <div>
                            <div class="name">{{ showList.name }}</div>
                            <div>{{ showList.email }}</div>
                        </div>
                        <a-button class="edit" icon="edit" @click="showModal" />
                        <modal
                            title="个人信息"
                            okText="保存"
                            cancelText="取消"
                            :visible="visible"
                            :confirm-loading="confirmLoading"
                            @ok="handleOk"
                            @cancel="handleCancel"
                        >
                            <div class="create-table">
                                <form-model
                                    ref="ruleForm"
                                    :model="form"
                                    :rules="rules"
                                    :label-col="labelCol"
                                    :wrapper-col="wrapperCol"
                                    layout="vertical"
                                >
                                    <form-model-item
                                        ref="name"
                                        label="用户名"
                                        prop="name"
                                    >
                                        <a-input
                                            :default-value="form.name"
                                            v-model="form.name"
                                        />
                                    </form-model-item>
                                    <form-model-item
                                        label="密码"
                                        prop="password"
                                    >
                                        <a-input
                                            type="password"
                                            :default-value="form.password"
                                            class="input"
                                            v-model="form.password"
                                        />
                                    </form-model-item>
                                </form-model>
                            </div>
                        </modal>
                    </div>
                    <div class="logout">
                        <a-button
                            class="dissolve"
                            type="primary"
                            icon="export"
                            @click="showDeleteConfirm"
                        >
                            退出登录
                        </a-button>
                    </div>
                </div>
            </template>
            <a-button class="icon" :type="buttonType" shape="circle">
                {{ form.name[0] }}
            </a-button>
        </popover>
    </div>
</template>

<script>
import {
    Popover,
    Button,
    Modal,
    FormModel,
    Input,
    Message,
} from 'ant-design-vue';
import Vue from 'vue';
import {
    USER_NAME_MAX_LENGTH,
    PASSWORD_MIN_LENGTH,
    PASSWORD_MAX_LENGTH,
} from '../../constants/user';
import { updateUser, getUserinfo } from '../../requests/user';
import { defaultErrorHandler } from '../../requests/errors';
import Cookies from 'js-cookie';
import router from '../../router';

Vue.use(Modal);

export default {
    props: {
        buttonType: {
            default: 'primary',
        },
    },
    components: {
        Popover,
        AButton: Button,
        Modal,
        FormModel,
        FormModelItem: FormModel.Item,
        AInput: Input,
    },
    data() {
        return {
            tempStorage: '',
            visible: false,
            confirmLoading: false,
            labelCol: { span: 4 },
            wrapperCol: { span: 14 },
            showList: {},
            form: {
                name: '',
                password: '',
                email: '',
            },
            rules: {
                name: [
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
            },
        };
    },
    mounted() {
        getUserinfo()
            .then((data) => {
                this.showList = JSON.parse(JSON.stringify(data.data));
                this.form = data.data;
            })
            .catch(defaultErrorHandler(getUserinfo));
    },
    methods: {
        showDeleteConfirm() {
            let title = '确定要退出登录吗';
            Modal.confirm({
                title: title,
                okText: '确定',
                cancelText: '取消',
                iconType: 'exclamation-circle',
                onOk() {
                    Cookies.remove('token');
                    router.push('/login');
                },
            });
        },
        showModal() {
            this.visible = true;
            this.tempStorage = JSON.parse(JSON.stringify(this.form));
        },
        handleOk() {
            updateUser(this.form.name, this.form.password)
                .then(() => {
                    Message.success('修改成功');
                    this.showList = JSON.parse(JSON.stringify(this.form));
                    this.visible = false;
                })
                .catch(defaultErrorHandler(updateUser));
        },
        handleCancel() {
            this.visible = false;
            this.form = this.tempStorage;
        },
    },
};
</script>

<style scoped>
.logout {
    margin: 10px 0;
}
.icon {
    height: 100%;
    width: 100%;
    display: block;
}
.name {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.email {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.edit {
    margin-left: 10px;
}
</style>
