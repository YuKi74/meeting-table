<template>
    <div class="container">
        <a-button-group>
            <a-button type="primary" @click="previousPage"
                ><a-icon type="left" />上一页</a-button
            >
            <a-button type="primary" @click="nextPage"
                ><a-icon type="right" />下一页</a-button
            >
        </a-button-group>
        <div class="page-num">{{ pageNum }}/{{ pageTotalNum }}</div>
        <pdf
            :page="pageNum"
            :src="url"
            @progress="loadedRatio = $event"
            @num-pages="pageTotalNum = $event"
        ></pdf>
    </div>
</template>

<script>
import { Button, Icon } from 'ant-design-vue';
import pdf from 'vue-pdf';
export default {
    name: 'Pdf',
    components: {
        AButton: Button,
        AButtonGroup: Button,
        AIcon: Icon,
        pdf,
    },
    data() {
        return {
            url: '',
            pageNum: 1,
            pageTotalNum: 3,
            loadedRatio: 0,
        };
    },
    methods: {
        previousPage() {
            let page = this.pageNum;
            page = page > 1 ? page - 1 : this.pageTotalNum;
            this.pageNum = page;
        },
        nextPage() {
            let page = this.pageNum;
            page = page < this.pageTotalNum ? page + 1 : 1;
            this.pageNum = page;
        },
    },
};
</script>
<style scoped>
.container {
    display: flex;
    flex-direction: column;
}
.page-num {
    text-align: center;
}
</style>
