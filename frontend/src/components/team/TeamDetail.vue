<template>
    <div>
        <popover placement="bottomLeft" arrow-point-at-center>
            <div class="content flex flex-col" slot="content">
                <div class="title">
                    <p class="form-name">{{ data.name }}</p>
                    <a-button
                        class="edit"
                        icon="edit"
                        @click="showModal"
                        v-show="isCreator"
                    />
                    <modal
                        title="编辑团队信息"
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
                                    label="团队名称"
                                    prop="name"
                                >
                                    <a-input
                                        :default-value="form.name"
                                        v-model="form.name"
                                    />
                                </form-model-item>
                                <form-model-item
                                    label="团队简介"
                                    prop="introduction"
                                >
                                    <a-input
                                        v-model="form.introduction"
                                        type="textarea"
                                        :default-value="form.introduction"
                                        :autosize="{ minRows: 4 }"
                                    />
                                </form-model-item>
                            </form-model>
                        </div>
                    </modal>
                </div>
                <p class="self-cross-axis-start introduction">
                    {{ form.introduction }}
                </p>
                <div class="share-and-dissolve">
                    <a-button type="danger" @click="success">分享</a-button>
                    <a-button
                        class="dissolve"
                        type="primary"
                        @click="showDeleteConfirm"
                        v-if="isCreator"
                    >
                        解散
                    </a-button>
                    <a-button
                        class="dissolve"
                        type="primary"
                        @click="showDeleteConfirm"
                        v-else
                    >
                        退出
                    </a-button>
                </div>
            </div>
            <a-button class="icon" type="primary" shape="circle">
                {{ form.name.charAt(0) }}
            </a-button>
        </popover>
    </div>
</template>

<script>
import {
    Popover,
    Button,
    Message,
    Modal,
    FormModel,
    Input,
} from 'ant-design-vue';
import Vue from 'vue';
import {
    TEAM_NAME_MIN_LENGTH,
    TEAM_NAME_MAX_LENGTH,
    TEAM_DESCRIPTION_MAX_LENGTH,
} from '../../constants/team';
import {
    updateTeam,
    getTeaminfo,
    dissolveTeam,
    quitTeam,
} from '../../requests/team';
import { defaultErrorHandler } from '../../requests/errors';
import router from '../../router';
Vue.use(Modal);

export default {
    props: ['uuid', 'is-creator'],
    components: {
        Popover,
        AButton: Button,
        Modal,
        FormModel,
        FormModelItem: FormModel.Item,
        AInput: Input,
    },
    data: function () {
        return {
            tempStorage: '',
            visible: false,
            confirmLoading: false,
            labelCol: { span: 4 },
            wrapperCol: { span: 14 },
            data: {
                name: '',
                introduction: '',
            },
            form: {
                name: '',
                introduction: '',
            },
            rules: {
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
                        trigger: 'change',
                    },
                ],
                introduction: [
                    {
                        required: true,
                        message: '请输入团队简介',
                        trigger: 'blur',
                    },
                    {
                        max: TEAM_DESCRIPTION_MAX_LENGTH,
                        message: `请控制在${TEAM_DESCRIPTION_MAX_LENGTH}个字符以内`,
                        trigger: 'change',
                    },
                ],
            },
        };
    },
    mounted() {
        getTeaminfo(this.uuid)
            .then((data) => {
                this.data = data.data;
                this.form = JSON.parse(JSON.stringify(data.data));
            })
            .catch(defaultErrorHandler(getTeaminfo));
    },
    methods: {
        success() {
            let input = document.createElement('input');
            input.value =
                window.location.protocol +
                '//' +
                window.location.host +
                '/team/' +
                this.uuid;
            document.body.appendChild(input);
            input.select();
            document.execCommand('Copy');
            document.body.removeChild(input);
            Message.success('分享链接已复制到剪贴板');
        },
        showDeleteConfirm() {
            const that = this;
            const title = this.provideTitleAndMessage(this.isCreator).title;
            const message = this.provideTitleAndMessage(this.isCreator).message;
            Modal.confirm({
                title: title,
                content: message,
                okText: '确定',
                cancelText: '取消',
                iconType: 'exclamation-circle',
                onOk() {
                    if (that.isCreator) {
                        dissolveTeam()
                            .then(() => {
                                router.push('/team/create');
                            })
                            .catch(defaultErrorHandler(dissolveTeam));
                    } else {
                        quitTeam()
                            .then(() => {
                                router.push('/team/create');
                            })
                            .catch(defaultErrorHandler(dissolveTeam));
                    }
                },
            });
        },
        provideTitleAndMessage(creator) {
            let title = creator ? '确定要解散团队吗' : '确定要退出团队吗';
            let message = creator
                ? '解散后不可恢复，且所有会议室文件都会丢失'
                : '';
            return { title, message };
        },
        showModal() {
            this.visible = true;
            this.tempStorage = JSON.parse(JSON.stringify(this.form));
        },
        handleOk() {
            updateTeam(this.form.name, this.form.introduction)
                .then(() => {
                    Message.success('修改成功');
                    this.visible = false;
                    this.data = JSON.parse(JSON.stringify(this.form));
                })
                .catch(defaultErrorHandler(updateTeam));
        },
        handleCancel() {
            this.visible = false;
            this.form = this.tempStorage;
        },
    },
};
</script>

<style scoped>
.icon {
    font-size: 16px;
    width: 40px;
    height: 40px;
}
.title {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    width: 250px;
}
.form-name {
    width: 220px;
    word-wrap: break-word;
}
.introduction {
    width: 245px;
    word-wrap: break-word;
}
.edit {
    flex-shrink: 0;
}
.content {
    width: 250px;
}
.name {
    color: var(--black);
    font-size: 16px;
    font-weight: 900;
}
.share-and-dissolve {
    display: flex;
    justify-content: space-around;
    width: 180px;
}
.dissolve {
    margin-left: 20px;
}
</style>
