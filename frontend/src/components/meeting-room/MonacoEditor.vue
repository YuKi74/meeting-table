<template>
    <div
        ref="container"
        class="monaco-editor"
        :style="`height: ${height}px`"
    ></div>
</template>
<script>
import * as monaco from 'monaco-editor';
import TextHandler from '../../text-cooperation/text-handler';
import Operation, { regular } from '../../text-cooperation/operation';
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
        connection: {
            type: Object,
        },
        id: {
            type: String,
        },
        content: {
            type: Object,
        },
    },
    data() {
        return {
            defaultOpts: {
                value: '',
                theme: 'vs-dark',
                roundedSelection: false,
                autoIndent: true,
                unusualLineTerminators: 'off',
            },
            monacoEditor: null,

            isCompositionInput: false,
            CompositionEvtQueue: [],
            textHandler: {},
            isReadOnly: false,
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
        this.textHandler = new TextHandler(
            this.content.version,
            this.onChange,
            (data) => {
                this.connection.send({
                    Type: 'code',
                    Target: this.id,
                    Data: data,
                });
            },
            () => {
                this.isReadOnly = true;
                this.monacoEditor.updateOptions({ readOnly: true });
            }
        );
        this.connection.addMessageHandler(
            (data) => {
                return data.Type === 'code' && data.Target === this.id;
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
        this.init();
        this.textHandler.start();
    },
    destroyed: function () {
        this.textHandler.close();
    },
    methods: {
        changeModelContent: function (evt) {
            if (this.isReadOnly) {
                this.isReadOnly = false;
                this.monacoEditor.updateOptions({ readOnly: false });
                return;
            }
            if (this.isCompositionInput) {
                this.CompositionEvtQueue.push(evt);
                return;
            }

            let length = this.monacoEditor.getValue().length;
            for (let change of evt.changes) {
                length = length - change.text.length + change.rangeLength;
            }
            for (let change of evt.changes) {
                const start = change.rangeOffset;
                const insert = change.text;
                const del = change.rangeLength === 0 ? 0 : -change.rangeLength;
                const end = length + del - start;
                length += insert.length + del;

                const ops = [start, insert, del, end];
                this.textHandler.sendBuffer.push(regular(ops));
            }
        },
        compositionStart: function () {
            this.CompositionEvtQueue.length = 0;
            this.isCompositionInput = true;
            this.textHandler.startCompositionInput();
        },
        compositionEnd: function () {
            this.textHandler.finishCompositionInput();
            let length = this.monacoEditor.getValue().length;
            const firstEvt = this.CompositionEvtQueue[0];
            const lastEvt =
                this.CompositionEvtQueue[this.CompositionEvtQueue.length - 1];
            for (let i = 0; i < lastEvt.changes.length; i++) {
                length =
                    length -
                    lastEvt.changes[i].text.length +
                    firstEvt.changes[i].rangeLength;
            }
            for (let i = 0; i < lastEvt.changes.length; i++) {
                const start = firstEvt.changes[i].rangeOffset;
                const insert = lastEvt.changes[i].text;
                const del =
                    firstEvt.changes[i].rangeLength === 0
                        ? 0
                        : -firstEvt.changes[i].rangeLength;
                const end = length + del - start;
                length += insert.length + del;

                if (!insert && !del) {
                    continue;
                }

                const ops = [start, insert, del, end];
                this.textHandler.sendBuffer.push(regular(ops));
            }

            this.CompositionEvtQueue.length = 0;
            this.isCompositionInput = false;
        },
        attemptReadOnlyEdit: function () {
            const overlayMessages = document.getElementsByClassName(
                'monaco-editor-overlaymessage'
            );
            overlayMessages.forEach((overlayMessage) => {
                overlayMessage.style.display = 'none';
                overlayMessage.style.visibility = 'hidden';
            });
        },
        init() {
            let editorOptions = this.opts ? this.opts : this.defaultOpts;
            const oldValue = this.monacoEditor
                ? this.monacoEditor.getValue()
                : this.content.content;
            this.$refs.container.innerHTML = '';
            const div = document.createElement('div');
            div.style.height = '100%';
            div.style.width = '100%';
            this.$refs.container.appendChild(div);
            this.monacoEditor = monaco.editor.create(div, editorOptions);
            this.monacoEditor.setValue(oldValue);

            this.monacoEditor.onDidChangeModelContent(this.changeModelContent);
            this.monacoEditor.onDidCompositionStart(this.compositionStart);
            this.monacoEditor.onDidCompositionEnd(this.compositionEnd);
            this.monacoEditor.onDidAttemptReadOnlyEdit(
                this.attemptReadOnlyEdit
            );
        },
        onChange: function (operation) {
            const oldPosition = this.monacoEditor.getPosition();
            const oldValue = this.monacoEditor.getValue();
            let lineNumber = 1;
            let column = 1;
            let oldOffset = 0;
            for (let i = 0; i < oldValue.length; i++) {
                if (oldValue[i] === '\n') {
                    lineNumber++;
                    column = 1;
                } else {
                    column++;
                }
                if (
                    lineNumber === oldPosition.lineNumber &&
                    column === oldPosition.column
                ) {
                    oldOffset = i + 1;
                    break;
                }
            }
            const applyResult = operation.apply(oldValue, oldOffset);
            const newValue = applyResult[0];
            const newOffset = applyResult[1];
            lineNumber = 1;
            column = 1;
            for (let i = 0; i < newOffset; i++) {
                if (newValue[i] === '\n') {
                    lineNumber++;
                    column = 1;
                } else {
                    column++;
                }
            }
            this.monacoEditor.setValue(newValue);
            this.monacoEditor.setPosition({
                lineNumber,
                column,
            });
        },
    },
};
</script>
