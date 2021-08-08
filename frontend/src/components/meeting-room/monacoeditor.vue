<template>
    <div
        ref="container"
        class="monaco-editor"
        :style="`height: ${height}px`"
    ></div>
</template>
<script>
import * as monaco from 'monaco-editor';
export default {
    name: 'AcMonaco',
    props: {
        opts: {
            type: Object,
            default() {
                return {};
            },
        },
        height: {
            type: Number,
            default: 300,
        },
    },
    data() {
        return {
            // 主要配置
            defaultOpts: {
                value: '', // 编辑器的值
                theme: 'vs-dark', // 编辑器主题：vs, hc-black, or vs-dark
                roundedSelection: false, // 右侧显示编辑器预览框
                autoIndent: true, // 自动缩进
            },
            // 编辑器对象
            monacoEditor: {},
        };
    },
    watch: {
        opts: {
            handler() {
                this.init();
            },
            deep: true,
        },
    },
    mounted() {
        this.init();
    },
    methods: {
        init() {
            // 初始化container的内容，销毁之前生成的编辑器
            this.$refs.container.innerHTML = '';
            // 生成编辑器配置
            let editorOptions = Object.assign(this.defaultOpts, this.opts);
            // 生成编辑器对象
            this.monacoEditor = monaco.editor.create(
                this.$refs.container,
                editorOptions
            );
            // 编辑器内容发生改变时触发
            this.monacoEditor.onDidChangeModelContent(() => {
                this.$emit('change', this.monacoEditor.getValue());
            });
        },
    },
};
</script>
<style scoped></style>
