<template>
    <div>
        <team-apply-list-card
            class="card shadow text-center"
            title="申请列表"
            :bordered="true"
            :headStyle="headStyle"
            :bodyStyle="{ background: 'white' }"
        >
            <team-apply-list-list
                item-layout="horizontal"
                :data-source="this.data"
            >
                <team-apply-list-list-item
                    slot="renderItem"
                    slot-scope="item"
                    class="main-axis-center"
                >
                    <div class="full-width text-center flex main-axis-between">
                        <team-apply-list-popover
                            placement="topLeft"
                            arrow-point-at-center
                        >
                            <div slot="content" class="popover">
                                <div><span>姓名:</span> {{ item.name }}</div>
                                <div><span>邮箱:</span> {{ item.email }}</div>
                            </div>
                            <span class="text">
                                {{ item.name }}
                            </span>
                        </team-apply-list-popover>
                        <div>
                            <team-apply-list-button @click="agree">
                                同意
                            </team-apply-list-button>
                            <team-apply-list-button @click="refuse">
                                拒绝
                            </team-apply-list-button>
                        </div>
                    </div>
                </team-apply-list-list-item>
            </team-apply-list-list>
        </team-apply-list-card>
    </div>
</template>

<script>
import { Card, List, Button, Popover } from 'ant-design-vue';

export default {
    components: {
        TeamApplyListCard: Card,
        TeamApplyListList: List,
        TeamApplyListListItem: List.Item,
        TeamApplyListButton: Button,
        TeamApplyListPopover: Popover,
    },
    data() {
        return {
            data: [
                {
                    name: 'xiaomingfgdfgdfgdfgdfgdfdfgdf',
                    email: 'xiaoming@123.com',
                },
                {
                    name: '小明爸爸',
                    email: 'xiaoming@123.com',
                },
                {
                    name: '李华h',
                    email: 'lihuah@123.com',
                },
                {
                    name: 'r',
                    email: 'r@123.com',
                },
            ],
            headStyle: {
                'font-size': '20px',
                color: '#212529',
                background: '#b4c8ff',
            },
        };
    },
    method: {
        agree: function () {
            // TODO 同意申请，将此条申请消息从列表中移除
        },
        refuse: function () {
            // TODO 拒绝申请，将此条申请消息从列表中移除
        },
    },
};
</script>

<style scoped>
.card {
    height: 400px;
    overflow: auto;
}

.text {
    text-align: left;
    text-overflow: ellipsis;
    overflow: hidden;
    width: 30%;
    word-break: break-all;
    white-space: nowrap;
}

.popover {
    color: var(--black);
    width: 100%;
    height: 100%;
    text-align: left;
}

.popover > div > span {
    font-weight: bold;
}

.list-item > div > button {
    border-radius: 5px;
    margin: 0 5px;
}
</style>
