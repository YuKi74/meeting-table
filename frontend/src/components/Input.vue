<template>
    <a-form-model :model="form" :rules="rules" ref="form">
        <a-form-model-item prop="content">
            <a-input
                class="input"
                v-model="form.content"
                placeholder="请输入主题"
            />
        </a-form-model-item>
    </a-form-model>
</template>
<script>
import { Input, FormModel, Message } from 'ant-design-vue';

export default {
    components: {
        AInput: Input,
        AFormModel: FormModel,
        AFormModelItem: FormModel.Item,
    },
    data() {
        return {
            form: {
                content: '',
            },
            rules: {
                content: [
                    {
                        required: true,
                        message: '请输入创建会议室的主题',
                        trigger: 'blur',
                    },
                    {
                        max: 64,
                        message: '主题长度应小于64',
                        trigger: 'change',
                    },
                ],
            },
        };
    },
    methods: {
        confirm() {
            this.$refs.form.validate((valid) => {
                if (valid) {
                    Message.success('创建成功');

                    return true;
                } else {
                    Message.error('主题长度应小于64');

                    return false;
                }
            });
        },
    },
};
</script>
<style>
.input {
    width: 85%;
}
</style>
