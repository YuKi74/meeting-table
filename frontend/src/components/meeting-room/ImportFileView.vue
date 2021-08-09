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
                                        class="content"
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
                console.log(data);
                this.meetingRoom = data.data;
                for (let index in data.data) {
                    if (index === '0') {
                        this.refreshFileInformation(
                            data.data[index].uuid,
                            index
                        );
                    }
                }
                console.log(this.meetingRoom);
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
            return 'http://localhost/api' + files;
        },
        isActive(key) {
            console.log(key);
            this.refreshFileInformation(this.meetingRoom[key].uuid, key);
        },
        refreshFileInformation(uuid, index) {
            getMeetingRoomFile(uuid)
                .then((fileData) => {
                    console.log(fileData.data);
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
                .then(() => {
                    Message.success('导入成功');
                })
                .catch((data) => {
                    console.log(data);
                });
        },
    },
};
</script>
<style scoped>
.content {
    min-width: 1000px;
    min-height: 500px;
}
.fileName {
    color: rgb(126, 125, 125);
}
</style>
