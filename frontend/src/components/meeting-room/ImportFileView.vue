<template>
    <div>
        <collapse
            v-model="activeKey"
            :bordered="false"
            @change="isActive"
            accordion
        >
            <collapse-panel
                :header="item.name"
                v-for="item in meetingRoom"
                :key="item.index"
            >
                <a-list item-layout="horizontal" :data-source="item.fileList">
                    <a-list-item slot="renderItem" slot-scope="listItem">
                        <popover placement="right">
                            <template slot="content">
                                <div class="content">
                                    <embed
                                        class="pdf"
                                        :src="getUrl(listItem.files)"
                                    />
                                </div>
                            </template>
                            <a-button type="link" class="fileName">
                                {{ listItem.name }}
                            </a-button>
                        </popover>
                        <a-button
                            type="primary"
                            @click="
                                importFile(listItem.meetingRoom, listItem.id)
                            "
                        >
                            导入
                        </a-button>
                    </a-list-item>
                </a-list>
            </collapse-panel>
        </collapse>
    </div>
</template>

<script>
import { Collapse, List, Button, Message, Popover } from 'ant-design-vue';
import {
    getMeetingRooms,
    getMeetingRoomFile,
    importOtherMeetingRoomFile,
} from '../../requests/meeting-room';
import { defaultErrorHandler } from '../../requests/errors';
export default {
    components: {
        Collapse,
        CollapsePanel: Collapse.Panel,
        AList: List,
        AListItem: List.Item,
        AButton: Button,
        Popover,
    },
    mounted() {
        getMeetingRooms()
            .then((data) => {
                this.meetingRoom = data.data;
                for (let index in data.data) {
                    if (index === '0') {
                        this.refreshFileInformation(
                            data.data[index].uuid,
                            index
                        );
                    }
                }
            })
            .catch(defaultErrorHandler(getMeetingRooms));
    },
    data() {
        return {
            text: `A solds across the world.`,
            activeKey: ['0'],
            meetingRoom: [],
        };
    },
    methods: {
        getUrl(files) {
            return '/api' + files;
        },
        isActive(key) {
            this.refreshFileInformation(this.meetingRoom[key].uuid, key);
        },
        refreshFileInformation(uuid, index) {
            getMeetingRoomFile(uuid)
                .then((fileData) => {
                    this.$set(
                        this.meetingRoom[index],
                        'fileList',
                        fileData.data
                    );
                })
                .catch(defaultErrorHandler(getMeetingRoomFile));
        },
        importFile(roomId, recordId) {
            importOtherMeetingRoomFile(roomId, recordId)
                .then((data) => {
                    Message.success('导入成功');
                    this.$emit('importFile', data.data);
                })
                .catch(defaultErrorHandler(importOtherMeetingRoomFile));
        },
    },
};
</script>
<style scoped>
.content {
    width: 200px;
    height: 300px;
}
.pdf {
    height: 100%;
    width: 100%;
}
.fileName {
    color: rgb(126, 125, 125);
}
</style>
