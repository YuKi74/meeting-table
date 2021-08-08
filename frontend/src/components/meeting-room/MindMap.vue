<template>
    <mindmap
        v-model="data"
        height="800"
        @updateNodeName="sender"
        :showUndo="false"
        :keyboard="false"
    ></mindmap>
</template>

<script>
import mindmap from '@hellowuxin/mindmap';

export default {
    components: { mindmap },
    props: ['content', 'connection', 'id'],
    data: () => ({
        data: [
            {
                name: '双击进行编辑',
            },
        ],
        delButton: null,
    }),
    methods: {
        receive(data) {
            this.data = data.Data;
        },
        sender() {
            this.connection.send({
                Type: 'mindmap',
                Target: this.id,
                Data: this.data,
            });
        },
    },
    mounted: function () {
        if (this.content !== '') {
            this.data = this.content;
        }
        this.delButton = document.getElementById('menu').firstChild;
        this.delButton.addEventListener('click', () => {
            this.sender();
        });

        this.connection.addMessageHandler(
            (data) => {
                return this.id === data.Target && data.Type === 'mindmap';
            },
            this.receive,
            this
        );
    },
};
</script>
<style scoped></style>
