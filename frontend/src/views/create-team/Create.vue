<template>
    <body>
        <div class="create-card">
            <card :bordered="false" style="width: 500px">
                <a-button
                    id="btn"
                    type="link"
                    href="../create/list"
                    icon="plus-circle"
                    :size="size"
                />
                <p class="create-title">创建团队</p>
                <p class="create-content">
                    从这里创建团队，开始您的Meeting Table之旅
                </p>
            </card>
        </div>
    </body>
</template>

<style>
.create-card {
    display: flex;
    justify-content: center;
    background: #f1f3f8;
    padding: 200px 30px;
    height: 858px;
}
.create-title {
    font-size: 24px;
    font-weight: 900;
    margin-bottom: 10px;
}
.create-content {
    font-size: 16px;
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
<script>
import { Card, Button } from 'ant-design-vue';

export default {
    data() {
        return {
            size: 'large',
        };
    },
    components: {
        Card,
        AButton: Button,
    },
};
</script>
