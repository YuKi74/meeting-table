<template>
    <div class="pop">
        <popover placement="bottomLeft" arrow-point-at-center>
            <template slot="content">
                <div class="content">
                    <div class="title">
                        <p class="name">{{ name }}</p>
                        <a-button class="edit" icon="edit" @click="showModal" />
                        <modal
                            title="编辑团队信息"
                            okText="确认"
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
                                            @blur="
                                                () => {
                                                    $refs.name.onFieldBlur();
                                                }
                                            "
                                        />
                                    </form-model-item>
                                    <form-model-item
                                        label="团队简介"
                                        prop="desc"
                                    >
                                        <a-input
                                            v-model="form.desc"
                                            type="textarea"
                                            :default-value="form.desc"
                                            :autosize="{ minRows: 4 }"
                                        />
                                    </form-model-item>
                                </form-model>
                            </div>
                        </modal>
                    </div>
                    <p>{{ description }}</p>
                    <div class="share-and-dissolve">
                        <a-button type="danger" @click="success">分享</a-button>
                        <a-button
                            class="dissolve"
                            type="primary"
                            @click="showDeleteConfirm"
                            v-if="isCreater"
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
            </template>
            <a-button class="icon" type="primary" shape="circle">
                {{ name[0] }}
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
Vue.use(Modal);

export default {
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
            name: '干完这单就回家干完这单就回家干完这单就回家干完这单就回家',
            description:
                '这是一坨团队介绍这是一坨团队介绍blabla...这是一坨团队介绍这是一坨团队介绍blabla...',
            // 判断是否为创建者
            isCreater: true,
            ModalText: '',
            visible: false,
            confirmLoading: false,
            labelCol: { span: 4 },
            wrapperCol: { span: 14 },
            other: '',
            form: {
                name: '',
                desc: '',
            },
            rules: {
                name: [
                    {
                        required: true,
                        message: '请输入团队名称',
                        trigger: 'blur',
                    },
                    {
                        min: 3,
                        max: 64,
                        message: '请控制在3-64个字符以内',
                        trigger: 'blur',
                    },
                ],
                desc: [
                    {
                        required: true,
                        message: '请输入团队简介',
                        trigger: 'blur',
                    },
                    {
                        max: 255,
                        message: '请控制在255个字符以内',
                        trigger: 'blur',
                    },
                ],
            },
        };
    },
    mounted() {
        this.form.name = this.name;
        this.form.desc = this.description;
    },
    methods: {
        success() {
            let input = document.createElement('input'); // js创建一个input输入框
            input.value = 'https://antdv.com/components/modal-cn/'; // 将需要复制的文本赋值到创建的input输入框中，this.ruleForm.url这个是我要复制的内容
            document.body.appendChild(input); // 将输入框暂时创建到实例里面
            input.select(); // 选中输入框中的内容
            document.execCommand('Copy'); // 执行复制操作
            document.body.removeChild(input); // 最后删除实例中临时创建的input输入框，完成复制操作
            Message.success('分享链接已复制到剪贴板');
        },
        showDeleteConfirm() {
            let isexit = '退出';
            let dissolve = '解散后不可恢复';
            if (this.iscreater) {
                isexit = '解散';
                dissolve = '解散后不可恢复，且所有会议室文件都会丢失';
            }
            Modal.confirm({
                title: '请确认是否要' + isexit + '团队',
                content: dissolve,
                okText: '确定',
                cancelText: '取消',
                iconType: 'exclamation-circle',
            });
        },
        showModal() {
            this.visible = true;
        },
        // eslint-disable-next-line no-unused-vars
        handleOk(e) {
            // TODO 修改团队信息，删除eslint注释
        },
        handleCancel() {
            this.visible = false;
        },
    },
};
</script>

<style scoped>
.icon {
    font-size: 16px;
    width: 50px;
    height: 50px;
}
.title {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    width: 250px;
}
.edit {
    flex-shrink: 0;
}
.content {
    display: flex;
    flex-wrap: wrap;
    width: 250px;
    justify-content: center;
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
