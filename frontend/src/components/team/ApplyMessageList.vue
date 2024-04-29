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
                                <div>
                                    <span>姓名:</span> {{ item.applicant_name }}
                                </div>
                                <div>
                                    <span>邮箱:</span>
                                    {{ item.applicant_email }}
                                </div>
                            </div>
                            <span class="text">
                                {{ item.applicant_name }}
                            </span>
                        </team-apply-list-popover>
                        <div>
                            <team-apply-list-button @click="agree(item.id)">
                                同意
                            </team-apply-list-button>
                            <team-apply-list-button @click="refuse(item.id)">
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
import { Card, List, Button, Popover, Message } from 'ant-design-vue';
import { getApplyList, handleApplication } from '../../requests/team';
import { defaultErrorHandler } from '../../requests/errors';

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
            isAggree: true,
            data: [],
            headStyle: {
                'font-size': '20px',
                color: '#212529',
                background: '#b4c8ff',
            },
        };
    },
    mounted() {
        this.refreshApplyList();
        this.bus.$on('refresh', () => {
            this.refreshApplyList();
        });
    },
    methods: {
        refreshApplyList() {
            getApplyList()
                .then((data) => {
                    this.data = data.data;
                })
                .catch(defaultErrorHandler(getApplyList));
        },
        handleCheckButton(id, isAdmit) {
            const that = this;
            handleApplication(id, isAdmit)
                .then(() => {
                    if (isAdmit) {
                        Message.success('申请已同意');
                        this.bus.$emit('aggreeApplication');
                    } else {
                        Message.success('申请已拒绝');
                    }
                    that.refreshApplyList();
                })
                .catch(defaultErrorHandler(handleApplication));
        },
        agree(id) {
            this.handleCheckButton(id, true);
        },
        refuse(id) {
            this.handleCheckButton(id, false);
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
