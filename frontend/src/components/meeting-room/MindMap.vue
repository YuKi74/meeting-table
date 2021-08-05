<template>
    <mindmap v-model="data" height="800"></mindmap>
</template>

<script>
import mindmap from '@hellowuxin/mindmap';

export default {
    components: { mindmap },
    // props: ['data'],
    // TODO 从服务器不断获取data
    data: () => ({
        data: [
            {
                name: '双击进行编辑',
            },
        ],
    }),
    watch: {
        data() {
            // TODO data每次更新上传一次data
        },
    },
};
</script>
<style scoped></style>
