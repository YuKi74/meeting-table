<template>
    <div class="create-card">
        <card class="card" :bordered="false" style="width: 500px">
            <p class="create-title">创建属于你的团队</p>
            <div>
                <form-model
                    ref="ruleForm"
                    :model="form"
                    :rules="rules"
                    :label-col="labelCol"
                    :wrapper-col="wrapperCol"
                    layout="vertical"
                >
                    <form-model-item ref="name" prop="name">
                        <a-input
                            class="input"
                            v-model="form.name"
                            @blur="
                                () => {
                                    $refs.name.onFieldBlur();
                                }
                            "
                            placeholder="请输入团队名称..."
                        />
                    </form-model-item>
                    <form-model-item prop="desc">
                        <a-input
                            class="input desc"
                            v-model="form.desc"
                            type="textarea"
                            placeholder="请输入团队简介..."
                        />
                    </form-model-item>
                    <div class="full-width flex main-axis-around btn">
                        <a-button
                            class="button"
                            @click="resetForm"
                            type="danger"
                        >
                            重置
                        </a-button>
                        <a-button
                            type="primary"
                            class="button"
                            @click="onSubmit"
                        >
                            提交
                        </a-button>
                    </div>
                </form-model>
            </div>
        </card>
    </div>
</template>

<script>
import { Card, FormModel, Input, Button } from 'ant-design-vue';
import {
    TEAM_NAME_MIN_LENGTH,
    TEAM_NAME_MAX_LENGTH,
    TEAM_DESCRIPTION_MAX_LENGTH,
} from '../../../constants/team';

export default {
    components: {
        Card,
        FormModel,
        FormModelItem: FormModel.Item,
        AInput: Input,
        AButton: Button,
    },
    data() {
        return {
            size: 'large',
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
                        min: TEAM_NAME_MIN_LENGTH,
                        max: TEAM_NAME_MAX_LENGTH,
                        message: `请控制在${TEAM_NAME_MIN_LENGTH}-${TEAM_NAME_MAX_LENGTH}个字符以内`,
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
                        max: TEAM_DESCRIPTION_MAX_LENGTH,
                        message: `请控制在${TEAM_DESCRIPTION_MAX_LENGTH}个字符以内`,
                        trigger: 'blur',
                    },
                ],
            },
        };
    },
    methods: {
        onSubmit() {
            this.$refs.ruleForm.validate((valid) => {
                if (valid) {
                    alert('创建成功!');
                }
            });
        },
        resetForm() {
            this.$refs.ruleForm.resetFields();
        },
    },
};
</script>

<style scoped>
.card {
    background-color: var(--white);
    border-radius: var(--border-radius);
}
.create-card {
    display: flex;
    justify-content: center;
    background: #f1f3f8;
    padding: 200px 30px;
    min-height: 100vh;
}
.create-title {
    font-size: 24px;
    font-weight: 600;
    margin: 40px 0;
    width: 100%;
    text-align: center;
}
.input {
    margin-left: 95px;
}
.btn {
    padding: 0 60px;
}
.button {
    width: 100px;
}
.desc {
    height: 100px;
}
</style>
