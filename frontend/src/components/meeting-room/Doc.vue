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
import TextHandler from '../../text-cooperation/text-handler';
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
            }
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
            this.textHandler.startCompositionInput();
            this.isInputComposition = true;
        },
        endComposition: function () {
            this.textHandler.finishCompositionInput();
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
        getOps: function (value, location, length, type, data) {
            const ops = [];
            let start; // 非负数
            let insert; // 字符串
            let del; // 非正数
            let end; // 非负数

            if (type === 'insertText') {
                insert = data ? data : '\n';
                del = length - this.lastLength - insert.length;
                start = location - insert.length;
                end = length - location;
            } else if (type.startsWith('delete')) {
                insert = '';
                del = length - this.lastLength;
                start = location;
                end = length - location;
            } else if (type === 'insertFromPaste') {
                insert = this.clipboardData;
                if (insert === null || insert === '') {
                    this.textarea.value = this.lastValue;
                    return null;
                }
                del = length - this.lastLength - insert.length;
                start = location - insert.length;
                end = length - location;
            } else if (type === 'insertLineBreak') {
                insert = '\n';
                del = length - this.lastLength - insert.length;
                start = location - insert.length;
                end = length - location;
            } else if (
                type === 'insertCompositionText' ||
                type === 'insertFromComposition'
            ) {
                insert = data;
                if (insert === null || insert === '') {
                    this.textarea.value = this.lastValue;
                    return null;
                }
                del = length - this.lastLength - insert.length;
                start = location - insert.length;
                end = length - location;
            } else {
                this.textarea.value = this.lastValue;
                return null;
            }
            ops.push(start, insert, del, end);
            this.lastLength = length;
            this.lastValue = value;

            return ops;
        },
        createOperation: function (evt) {
            const textarea = this.textarea;
            const ops = this.getOps(
                this.textarea.value,
                textarea.selectionStart,
                textarea.value.length,
                evt.inputType,
                evt.data
            );
            if (ops) {
                const operation = regular(ops);
                this.textHandler.sendBuffer.push(operation);
            }
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
    background-color: var(--white);
}
</style>
