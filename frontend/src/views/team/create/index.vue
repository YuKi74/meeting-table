<template>
    <div>
        <div class="create-card" v-show="!isFormShow">
            <card :bordered="false" style="width: 500px">
                <a-button
                    id="btn"
                    type="link"
                    icon="plus-circle"
                    :size="size"
                    @click="isFormShow = true"
                />
                <p class="create-title">创建团队</p>
                <p class="create-content">
                    从这里创建团队，开始您的Meeting Table之旅
                </p>
            </card>
        </div>
        <create-form v-show="isFormShow" />
    </div>
</template>

<script>
import { Card, Button } from 'ant-design-vue';
import CreateForm from './TeamCreateFormView.vue';

export default {
    data() {
        return {
            size: 'large',
            isFormShow: false,
        };
    },
    components: {
        Card,
        AButton: Button,
        CreateForm,
    },
};
</script>

<style scoped>
.create-card {
    display: flex;
    justify-content: center;
    background: #f1f3f8;
    padding: 200px 30px;
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
