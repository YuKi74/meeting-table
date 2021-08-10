<template>
    <div>
        <textarea
            class="text"
            ref="text"
            @compositionstart="startComposition"
            @compositionend="endComposition"
            @paste="getClipboardData"
            @input="getChange"
        ></textarea>
    </div>
</template>

<script>
import Operation, { regular } from '../../text-cooperation/operation';
import TextHandler from '../../text-cooperation/handler';
export default {
    props: ['connection', 'content', 'id'],
    name: 'doc',
    data() {
        return {
            textarea: null,
            lastLength: 0,
            clipboardData: '',
            lastEvt: null,
            lastValue: '',
            isInputComposition: false, // 中文输入中，隔绝服务器
            textHandler: {},
        };
    },
    mounted: function () {
        this.textarea = this.$refs.text;
        this.setText(this.content.content);
        this.textHandler = new TextHandler(
            parseInt(this.content.version),
            this.applyChange,
            (data) => {
                this.connection.send({
                    Type: 'text',
                    Target: this.id,
                    Data: data,
                });
            },
            () => {}
        );
        this.connection.addMessageHandler(
            (data) => {
                return data.Target === this.id && data.Type === 'text';
            },
            (data) => {
                const operation = data.Data;
                this.textHandler.receiveBuffer.push(
                    new Operation(
                        operation.BaseLength,
                        operation.TargetLength,
                        operation.Ops
                    )
                );
            },
            this
        );
        this.textHandler.start();
    },
    methods: {
        startComposition: function () {
            this.isInputComposition = true;
        },
        endComposition: function () {
            this.isInputComposition = false;
            this.createOperation(this.lastEvt);
        },
        getClipboardData: function () {
            const clipboard = event.clipboardData || window.clipboardData;
            this.clipboardData = clipboard.getData('text');
        },
        getChange: function (evt) {
            this.lastEvt = evt;
            if (this.isInputComposition) {
                return;
            }
            this.createOperation(evt);
        },
        setText: function (content) {
            this.textarea.value = content;
            this.lastLength = this.textarea.value.length;
            this.lastValue = this.textarea.value;
        },
        createOperation: function (evt) {
            const textarea = this.textarea;
            const ops = [];
            const location = textarea.selectionStart;
            const length = textarea.value.length;
            let start; // 非负数
            let insert; // 字符串
            let del; // 非正数
            let end; // 非负数

            if (evt.inputType === 'insertText') {
                insert = evt.data ? evt.data : '\n';
                del = length - this.lastLength - insert.length;
                start = location - insert.length;
                end = length - location;
            } else if (evt.inputType.startsWith('delete')) {
                insert = '';
                del = length - this.lastLength;
                start = location;
                end = length - location;
            } else if (evt.inputType === 'insertFromPaste') {
                insert = this.clipboardData;
                if (insert === null || insert === '') {
                    this.textarea.value = this.lastValue;
                    return;
                }
                del = length - this.lastLength - insert.length;
                start = location - insert.length;
                end = length - location;
            } else if (evt.inputType === 'insertLineBreak') {
                insert = '\n';
                del = length - this.lastLength - insert.length;
                start = location - insert.length;
                end = length - location;
            } else if (
                evt.inputType === 'insertCompositionText' ||
                evt.inputType === 'insertFromComposition'
            ) {
                insert = evt.data;
                if (insert === null || insert === '') {
                    this.textarea.value = this.lastValue;
                    return;
                }
                del = length - this.lastLength - insert.length;
                start = location - insert.length;
                end = length - location;
            } else {
                this.textarea.value = this.lastValue;
                return;
            }
            ops.push(start, insert, del, end);
            this.lastLength = length;
            this.lastValue = this.textarea.value;
            const operation = regular(ops);
            this.textHandler.sendBuffer.push(operation);
        },
        applyChange: function (operation) {
            const oldOffset = this.textarea.selectionStart;
            const applyResult = operation.apply(this.textarea.value, oldOffset);
            this.setText(applyResult[0]);
            const newOffset = applyResult[1];
            this.textarea.setSelectionRange(newOffset, newOffset);
        },
    },
};
</script>

<style scoped>
.text {
    width: 100%;
    height: 100%;
    resize: none;
    border: none;
}
</style>
