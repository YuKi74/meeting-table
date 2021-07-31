<template>
    <div class="board">
        <a-tooltip
            placement="right"
            v-for="(tool, index) in tools"
            :key="index"
        >
            <template slot="title"> {{ tool.name }} </template>
            <div class="box" @click="onClick(index)">
                <a-icon
                    :type="tool.icon"
                    :class="{
                        icon: true,
                        clicked: currentTool === index,
                    }"
                    style="font-size: 20px"
                />
            </div>
        </a-tooltip>
        <a-icon type="minus" style="font-size: 25px" class="separate" />
        <a-tooltip
            placement="right"
            v-for="(tool, index) in specialTools"
            :key="index"
        >
            <template slot="title"> {{ tool.name }} </template>
            <div class="box" @click="specialToolsOnClick(index)">
                <a-icon
                    :type="tool.icon"
                    :class="{
                        icon: true,
                        clicked: currentTool === index + gap,
                    }"
                    style="font-size: 20px"
                />
            </div>
        </a-tooltip>
    </div>
</template>

<script>
import { Icon, Tooltip } from 'ant-design-vue';

export default {
    components: {
        AIcon: Icon,
        ATooltip: Tooltip,
    },
    data: () => {
        return {
            tools: [
                {
                    name: '移动',
                    icon: 'drag',
                },
                {
                    name: '画笔',
                    icon: 'highlight',
                },
                {
                    name: '直线',
                    icon: 'line',
                },
                {
                    name: '曲线',
                    icon: 'loading-3-quarters',
                },
                {
                    name: '矩形',
                    icon: 'border',
                },
                {
                    name: '椭圆',
                    icon: 'trademark',
                },
                {
                    name: '文本框',
                    icon: 'font-colors',
                },
            ],
            specialTools: [
                {
                    name: '创意纸',
                    icon: 'reconciliation',
                },
                {
                    name: '聊天框',
                    icon: 'message',
                },
                {
                    name: '代码块',
                    icon: 'code',
                },
                {
                    name: '思维导图',
                    icon: 'apartment',
                },
                {
                    name: '文件',
                    icon: 'file-add',
                },
            ],
            currentTool: 0,
        };
    },
    computed: {
        gap: function () {
            return this.tools.length;
        },
    },
    methods: {
        onClick(index) {
            this.currentTool = index;
        },
        specialToolsOnClick(index) {
            this.currentTool = index + this.gap;
        },
    },
};
</script>
<style scope>
.separate {
    margin-left: 3px;
    color: rgb(223, 223, 223);
}
.board {
    width: 48px;
    height: 515px;
    padding: 8px;
    background-color: #ffffff;
    flex-direction: column;
    justify-content: center;
    border-radius: 6px;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 8%);
    border: none;
}
.box {
    width: 32px;
    height: 32px;
    margin-bottom: 8px;
    justify-content: center;
    border-radius: 6px;
}
.icon {
    width: 32px;
    height: 32px;
    background-color: #ffffff;
    border-radius: 6px;
    padding: 6px;
}
.icon:hover,
.clicked {
    cursor: pointer;
    background-color: rgb(223, 223, 223);
    transition: 500ms;
    transform: scale3d(1.1, 1.1, 2);
}
</style>
