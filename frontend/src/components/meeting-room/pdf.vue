<template>
    <div class="container">
        <a-button-group>
            <a-button type="primary" @click="previousPage"
                ><a-icon type="left" />上一页</a-button
            >
            <a-button type="primary" @click="nextPage"
                >下一页<a-icon type="right"
            /></a-button>
        </a-button-group>
        <div class="page-num">{{ pageNum }}/{{ pageTotalNum }}</div>
        <import-file @importFile="getUrl" v-if="isImport"> </import-file>
        <pdf
            :page="pageNum"
            :src="url"
            @progress="loadedRatio = $event"
            @num-pages="pageTotalNum = $event"
        ></pdf>
        <input
            v-show="false"
            type="file"
            accept=".pdf"
            ref="upload"
            @change="getInput()"
        />
    </div>
</template>

<script>
import { Button, Icon } from 'ant-design-vue';
import pdf from 'vue-pdf';
import { uploadFile } from '../../requests/team';
import { defaultErrorHandler } from '../../requests/errors';
import ImportFile from './ImportFileView.vue';
export default {
    props: ['id', 'connection', 'content'],
    name: 'Pdf',
    components: {
        AButton: Button,
        AButtonGroup: Button,
        AIcon: Icon,
        pdf,
        ImportFile,
    },
    data() {
        return {
            url: '',
            pageNum: 1,
            pageTotalNum: 3,
            loadedRatio: 0,
            isImport: false,
        };
    },
    mounted: function () {
        let name = this.id.slice(0, this.id.indexOf('_'));
        if (typeof this.content !== 'string') {
            if (name === '文件') {
                this.$refs.upload.click();
            } else if (name === '从其他会议室导入文件') {
                this.isImport = true;
            }
        } else {
            this.url = this.content;
        }
    },
    methods: {
        getUrl(name) {
            this.url = '/api/files/' + name;
            this.isImport = false;
            let data = {
                x: this.content.x,
                y: this.content.y,
                content: this.url,
            };
            this.connection.send({
                Type: 'component',
                Target: this.id,
                Data: data,
            });
        },
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
        getInput() {
            const file = this.$refs.upload.files[0];
            uploadFile(file, this.$route.params.uuid)
                .then((data) => {
                    this.url = '/api/files/' + data.data;
                    let information = {
                        x: this.content.x,
                        y: this.content.y,
                        content: this.url,
                    };
                    this.connection.send({
                        Type: 'component',
                        Target: this.id,
                        Data: information,
                    });
                })
                .catch(defaultErrorHandler(uploadFile));
        },
    },
};
</script>
<style scoped>
.container {
    display: flex;
    flex-direction: column;
    background-color: #fff;
}
.page-num {
    text-align: center;
}
.ant-btn-primary {
    border-radius: 0;
}
</style>
