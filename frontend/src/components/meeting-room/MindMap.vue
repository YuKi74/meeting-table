<template>
    <mindmap
        v-model="data"
        width="2000"
        height="2000"
        @updateNodeName="sender"
        :showUndo="false"
        :keyboard="false"
        :gps="false"
        :download="false"
        :fitView="false"
        class="mindmap"
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
        if (this.content) {
            setTimeout(() => {
                this.data = JSON.parse(JSON.stringify(this.content));
            }, 0);
        }
    },
};
</script>
<style scoped>
.mindmap {
    transform: scale(0.25, 0.25);
    transform-origin: 0 0 0;
}
</style>
