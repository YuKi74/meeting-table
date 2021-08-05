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
import { TEAM_NAME_MAX_LENGTH } from '../../constants/team';
import { defaultErrorHandler } from '../../requests/errors';
import { createMeetingRoom } from '../../requests/meeting-room';

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
                        max: TEAM_NAME_MAX_LENGTH,
                        message: `主题长度应小于${TEAM_NAME_MAX_LENGTH}`,
                        trigger: 'change',
                    },
                ],
            },
        };
    },
    methods: {
        confirm(onSuccess) {
            this.$refs.form.validate((valid) => {
                if (this.confirmHintMessage(valid)) {
                    createMeetingRoom(this.form.content)
                        .then(() => {
                            Message.success('创建成功');
                            onSuccess();
                        })
                        .catch(defaultErrorHandler(createMeetingRoom));
                }
            });
        },
        confirmHintMessage(isChecked) {
            if (isChecked) {
                return true;
            } else {
                if (this.form.content === '') {
                    Message.error('请输入创建会议室的主题');
                } else {
                    Message.error(`主题长度应小于${TEAM_NAME_MAX_LENGTH}`);
                }
                return false;
            }
        },
    },
};
</script>

<style>
.input {
    width: 85%;
}
</style>
