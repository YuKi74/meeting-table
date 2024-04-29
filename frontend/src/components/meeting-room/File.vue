<template>
    <div class="container">
        <div
            class="flex main-axis-center"
            v-show="!isChooseButtonShow && !isChooseRoom"
        >
            <a-button type="link" @click="previousPage" class="page-button"
                ><a-icon type="left"
            /></a-button>
            <div class="page-num">{{ pageNum }}/{{ pageTotalNum }}</div>
            <a-button type="link" @click="nextPage" class="page-button"
                ><a-icon type="right"
            /></a-button>
        </div>
        <a-button
            @click="showInput()"
            v-show="isChooseButtonShow"
            class="button"
            >选择文件</a-button
        >
        <import-file
            @importFile="getUrl"
            v-if="isChooseRoom"
            class="import-file"
        >
        </import-file>
        <pdf
            :page="pageNum"
            :src="url"
            @progress="loadedRatio = $event"
            @num-pages="pageTotalNum = $event"
            v-show="!isChooseButtonShow && !isChooseRoom"
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
import { Button, Icon, message } from 'ant-design-vue';
import { uploadFile } from '../../requests/team';
import { defaultErrorHandler } from '../../requests/errors';
import ImportFile from './ImportFileView.vue';
import { FILE_SIZE_LIMIT } from '../../constants/meeting-room';
import Pdf from 'vue-pdf';
export default {
    props: ['id', 'connection', 'content'],
    components: {
        AButton: Button,
        AIcon: Icon,
        ImportFile,
        Pdf,
    },
    data() {
        return {
            url: '',
            pageNum: 1,
            pageTotalNum: 3,
            loadedRatio: 0,
            isChooseButtonShow: false,
            isChooseRoom: false,
        };
    },
    mounted: function () {
        let name = this.id.slice(0, this.id.indexOf('_'));
        if (typeof this.content !== 'string') {
            if (name === '文件') {
                this.isChooseButtonShow = true;
            } else if (name === '从其他会议室导入文件') {
                this.isChooseRoom = true;
            }
        } else {
            this.url = this.content;
        }
    },
    methods: {
        getUrl(name) {
            this.isChooseRoom = false;
            this.url = '/api/files/' + name;
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
        showInput() {
            this.$refs.upload.click();
        },
        getInput() {
            const file = this.$refs.upload.files[0];
            if (file.size > FILE_SIZE_LIMIT) {
                message.info({
                    content: '上传文件过大',
                });
                return;
            }
            this.isChooseButtonShow = false;
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
.button + span {
    overflow: auto;
}
.ant-btn-primary {
    border-radius: 0;
}
.page-button {
    color: var(--black);
}
.import-file {
    overflow: auto;
}
</style>
