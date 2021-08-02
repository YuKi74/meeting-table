<template>
    <div class="back">
        <div class="left-board">
            <a-tooltip
                placement="right"
                v-for="(tool, index) in toolList"
                :key="'tool' + index"
            >
                <template slot="title"> {{ tool.name }} </template>
                <div class="box" @click="chooseTool(tool)">
                    <a-icon
                        :type="tool.icon"
                        :class="{
                            icon: true,
                            clicked: currentTool.name === tool.name,
                        }"
                        class="font-size-20"
                    />
                </div>
            </a-tooltip>
            <a-icon type="minus" class="separate font-size-25" />
            <a-tooltip
                placement="right"
                v-for="(tool, index) in specialToolList"
                :key="'specilTool' + index"
            >
                <template slot="title"> {{ tool.name }} </template>
                <div class="box" @click="chooseTool(tool)">
                    <a-icon
                        :type="tool.icon"
                        :class="{
                            icon: true,
                            clicked: currentTool.name === tool.name,
                        }"
                        class="font-size-20"
                    />
                </div>
            </a-tooltip>
        </div>
        <div class="right-board" v-show="currentTool.name === '设置'">
            <a-tooltip
                placement="right"
                v-for="(style, index) in styleList"
                :key="'style' + index"
            >
                <template slot="title"> {{ style.name }} </template>
                <div class="box" @click="chooseStyle(style)">
                    <a-icon
                        :type="style.icon"
                        :class="{
                            icon: true,
                            clicked: currentStyle.name === style.name,
                        }"
                        class="font-size-20"
                    />
                </div>
            </a-tooltip>
            <div class="color-board" v-show="currentStyle.name === '线色'">
                <div
                    class="color-box"
                    v-for="(strokeColor, index) in colorList"
                    :key="'strokeColor' + index"
                >
                    <a-icon
                        v-if="strokeColor.color === 'transparent'"
                        type="pushpin"
                        :class="{
                            clicked:
                                currentStrokeColor.color === strokeColor.color,
                        }"
                        class="color-button font-size-22 black-text"
                        @click="chooseStrokeColor(strokeColor)"
                    />
                    <a-icon
                        v-else
                        type="pushpin"
                        theme="filled"
                        :style="strokeColor"
                        :class="{
                            clicked:
                                currentStrokeColor.color === strokeColor.color,
                        }"
                        class="color-button font-size-22"
                        @click="chooseStrokeColor(strokeColor)"
                    />
                </div>
            </div>
            <div class="color-board" v-show="currentStyle.name === '填充色'">
                <div
                    class="color-box"
                    v-for="(fillColor, index) in colorList"
                    :key="'fillColor' + index"
                >
                    <a-icon
                        v-if="fillColor.color === 'transparent'"
                        type="pushpin"
                        :class="{
                            clicked: currentFillColor.color === fillColor.color,
                        }"
                        class="color-button font-size-22 black-text"
                        @click="chooseFillColor(fillColor)"
                    />
                    <a-icon
                        v-else
                        type="pushpin"
                        theme="filled"
                        :style="fillColor"
                        :class="{
                            clicked: currentFillColor.color === fillColor.color,
                        }"
                        class="color-button font-size-22"
                        @click="chooseFillColor(fillColor)"
                    />
                </div>
            </div>
            <div class="slider" v-show="currentStyle.name === '线宽'">
                <a-slider
                    vertical
                    v-model="strokeWidth"
                    :max="STROKE_MAX_WIDTH"
                    :min="STROKE_MIN_WIDTH"
                    :step="STROKE_WIDTH_STEP"
                />
            </div>
            <div class="color-board" v-show="currentStyle.name === '文本颜色'">
                <div
                    class="color-box"
                    v-for="(textColor, index) in colorList"
                    :key="'textColor' + index"
                >
                    <a-icon
                        v-if="textColor.color === 'transparent'"
                        type="pushpin"
                        :class="{
                            clicked: currentTextColor.color === textColor.color,
                        }"
                        class="color-button font-size-22 black-text"
                        @click="chooseTextColor(textColor)"
                    />
                    <a-icon
                        v-else
                        type="pushpin"
                        theme="filled"
                        :style="textColor"
                        :class="{
                            clicked: currentTextColor.color === textColor.color,
                        }"
                        class="color-button font-size-22"
                        @click="chooseTextColor(textColor)"
                    />
                </div>
            </div>
            <div class="slider" v-show="currentStyle.name === '字号'">
                <a-slider
                    ref="slider"
                    vertical
                    v-model="fontSize"
                    :max="FONT_MAX_SIZE"
                    :min="FONT_MIN_SIZE"
                    :step="FONT_SIZE_STEP"
                />
            </div>
        </div>
    </div>
</template>

<script>
import { Icon, Tooltip, Slider } from 'ant-design-vue';
import {
    STROKE_MIN_WIDTH,
    STROKE_MAX_WIDTH,
    STROKE_WIDTH_STEP,
    FONT_MIN_SIZE,
    FONT_MAX_SIZE,
    FONT_SIZE_STEP,
} from '../../constants/meeting-room';

export default {
    components: {
        AIcon: Icon,
        ATooltip: Tooltip,
        ASlider: Slider,
    },
    mounted: function () {
        // 修改ant-design中slider的默认样式
        const slidersTrack =
            document.getElementsByClassName('ant-slider-track');
        for (let i = 0; i < slidersTrack.length; i++) {
            const slider = slidersTrack[i];
            slider.style.backgroundColor = 'gray';
        }
        const slidersHandle =
            document.getElementsByClassName('ant-slider-handle');
        for (let i = 0; i < slidersHandle.length; i++) {
            const slider = slidersHandle[i];
            slider.style.border = 'solid 2px gray';
        }
    },
    data: () => {
        return {
            toolList: [
                {
                    name: '移动',
                    icon: 'drag',
                },
                {
                    name: '画笔',
                    icon: 'edit',
                },
                {
                    name: '直线',
                    icon: 'line',
                },
                {
                    name: '矩形',
                    icon: 'border',
                },
                {
                    name: '椭圆',
                    icon: 'loading-3-quarters',
                },
                {
                    name: '文本框',
                    icon: 'file-text',
                },
                {
                    name: '设置',
                    icon: 'setting',
                },
            ],
            specialToolList: [
                {
                    name: '聊天框',
                    icon: 'message',
                },
                {
                    name: '创意纸',
                    icon: 'reconciliation',
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
                {
                    name: '从其他会议室导入文件',
                    icon: 'file-search',
                },
            ],
            styleList: [
                {
                    name: '线色',
                    icon: 'highlight',
                },
                {
                    name: '填充色',
                    icon: 'bg-colors',
                },
                {
                    name: '线宽',
                    icon: 'bold',
                },
                {
                    name: '文本颜色',
                    icon: 'font-colors',
                },
                {
                    name: '字号',
                    icon: 'font-size',
                },
            ],
            colorList: [
                {
                    color: 'transparent',
                },
                {
                    color: 'white',
                },
                {
                    color: 'black',
                },
                {
                    color: 'red',
                },
                {
                    color: 'grey',
                },
                {
                    color: 'lightskyblue',
                },
                {
                    color: 'green',
                },
                {
                    color: 'purple',
                },
                {
                    color: 'orange',
                },
            ],
            currentTool: { name: '移动', icon: 'drag' },
            currentStyle: { name: '聊天框', icon: 'message' },
            currentStrokeColor: { color: 'black' },
            currentFillColor: { color: 'black' },
            strokeWidth: 5,
            currentTextColor: { color: 'black' },
            fontSize: 36,
            STROKE_MIN_WIDTH,
            STROKE_MAX_WIDTH,
            STROKE_WIDTH_STEP,
            FONT_MIN_SIZE,
            FONT_MAX_SIZE,
            FONT_SIZE_STEP,
        };
    },
    methods: {
        chooseTool(tool) {
            this.currentTool = tool;
        },
        chooseStyle(style) {
            this.currentStyle = style;
        },
        chooseStrokeColor(color) {
            this.currentStrokeColor = color;
        },
        chooseFillColor(color) {
            this.currentFillColor = color;
        },
        chooseTextColor(color) {
            this.currentTextColor = color;
        },
    },
};
</script>
<style scope>
.slider {
    display: inline-block;
    margin-top: 20px;
    height: 200px;
    margin-left: 2px;
}
.color-button:hover {
    transform: scale3d(1.3, 1.3, 10);
    cursor: pointer;
}
.color-box {
    width: 28px;
    height: 28px;
    background-color: rgb(245, 243, 240);
}
.color-board {
    display: flex;
    margin-top: 17px;
    width: 100px;
    height: 100px;
    padding: 8px;
    background-color: rgb(245, 243, 240);
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: center;
    border-radius: 6px;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 8%);
    border: none;
}
.right-board {
    margin-left: 5px;
    margin-top: 40px;
    width: 48px;
    height: 208px;
    padding: 8px;
    background-color: #ffffff;
    flex-direction: column;
    justify-content: center;
    border-radius: 6px;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 8%);
    border: none;
}
.back {
    display: flex;
}
.separate {
    margin-left: 3px;
    color: rgb(223, 223, 223);
}
.left-board {
    width: 48px;
    height: 555px;
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

.font-size-20 {
    font-size: 20px;
}
.font-size-22 {
    font-size: 22px;
}
.font-size-25 {
    font-size: 25px;
}
</style>
