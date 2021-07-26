<template>
    <div class="home">
        <page-header title="This is a ant-design-vue test."></page-header>
        <guest-input
            autosize="{ minRows: 2, maxRows: 6 }"
            placeholder="请输入内容"
            v-model="input"
        ></guest-input>
        <submit-btn shape="round" size="large" @click="submitNote"
            >提交</submit-btn
        >
    </div>
</template>

<script>
// @ is an alias to /src
import { PageHeader, Input, Button } from 'ant-design-vue';

export default {
    name: 'Home',
    components: {
        PageHeader: PageHeader,
        GuestInput: Input.TextArea,
        SubmitBtn: Button,
    },
    methods: {
        submitNote: function () {
            alert('####');
        },
    },
};
</script>
