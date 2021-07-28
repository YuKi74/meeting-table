<template>
    <body>
        <div class="create-card">
            <card :bordered="false" style="width: 500px">
                <icon id="icon" type="team" />
                <p class="create-title">{{ name }}</p>
                <p class="create-content">
                    {{ description }}
                </p>
                <a-button type="primary" @click="AttendRequest"
                    >申请加入</a-button
                >
            </card>
            <a-button
                id="btn"
                type="primary"
                shape="circle"
                size="large"
                v-if="islogin"
            >
                {{ selfname[0] }}
            </a-button>
            <a-button
                id="btn"
                type="primary"
                shape="circle"
                size="large"
                v-else
            >
                登录
            </a-button>
        </div>
    </body>
</template>

<script>
import { Card, Button, Icon } from 'ant-design-vue';

export default {
    components: {
        Card,
        AButton: Button,
        Icon,
    },
    data() {
        return {
            islogin: true,
            selfname: 'xxxx',
            name: '干完这单就回家',
            description:
                '这是一坨团队介绍这是一坨团队介绍blabla...这是一坨团队介绍这是一坨团队介绍blabla...',
        };
    },
    mounted: function () {},
    methods: {
        AttendRequest() {
            // todo
            //申请加入按钮操作
        },
    },
};
</script>

<style>
.create-card {
    display: flex;
    justify-content: center;
    background: #f1f3f8;
    padding-top: 200px;
    padding-bottom: 250px;
    min-height: 100vh;
    width: 100%;
    text-align: center;
}
.create-title {
    color: #ffcc5f;
    font-size: 24px;
    font-weight: 900;
    margin-bottom: 10px;
    width: 100%;
    text-align: center;
}
.create-content {
    font-size: 16px;
    width: 100%;
    text-align: start;
}
#icon {
    color: #ffcc5f;
    width: 100%;
    height: 160px;
    font-size: 100px;
    padding: 30px;
}
#btn {
    letter-spacing: -2px;
    font-size: 16px;
    width: 50px;
    height: 50px;
    position: absolute;
    right: 30px;
    top: 30px;
}
</style>
