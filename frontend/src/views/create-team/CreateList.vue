<template>
    <div class="create-card">
        <card :bordered="false" style="width: 500px">
            <p class="create-title">创建属于你的团队</p>
            <div class="create-table">
                <form-model
                    ref="ruleForm"
                    :model="form"
                    :rules="rules"
                    :label-col="labelCol"
                    :wrapper-col="wrapperCol"
                    layout="vertical"
                >
                    <form-model-item ref="name" label="团队名称" prop="name">
                        <a-input
                            v-model="form.name"
                            @blur="
                                () => {
                                    $refs.name.onFieldBlur();
                                }
                            "
                            placeholder="请输入团队名称..."
                        />
                    </form-model-item>
                    <form-model-item label="团队简介" prop="desc">
                        <a-input v-model="form.desc" type="textarea" />
                    </form-model-item>
                    <div id="create-btn">
                        <a-button type="primary" @click="onSubmit"
                            >提交</a-button
                        >
                        <a-button style="margin-left: 10px" @click="resetForm">
                            重填
                        </a-button>
                    </div>
                </form-model>
            </div>
        </card>
    </div>
</template>

<style>
.create-card {
    display: flex;
    justify-content: center;
    background: #f1f3f8;
    padding: 200px 30px;
    min-height: 100vh;
}
.create-title {
    font-size: 25px;
    font-weight: 600;
    margin: 50px 0;
    color: #ffcc5f;
    width: 100%;
    text-align: center;
}
#create-btn {
    width: 100%;
    display: flex;
    justify-content: center;
}
</style>
<script>
import { Card, FormModel, Input, Button } from 'ant-design-vue';

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
    methods: {
        onSubmit() {
            console.log(this.$refs.ruleForm);
            this.$refs.ruleForm.validate((valid) => {
                if (valid) {
                    alert('创建成功!');
                } else {
                    console.log('error submit!!');
                    return false;
                }
            });
        },
        resetForm() {
            this.$refs.ruleForm.resetFields();
        },
    },
};
</script>
