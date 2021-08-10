<template>
    <div class="flex flex-col main-axis-center content">
        <a-icon type="warning" class="icon" />
        <h1>该页面不存在！</h1>
    </div>
</template>

<script>
import { Icon } from 'ant-design-vue';
export default {
    components: {
        AIcon: Icon,
    },
};
</script>

<style scoped>
.content {
    min-width: 100vw;
}
.icon {
    font-size: 50px;
}
</style>
