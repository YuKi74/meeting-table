<template>
    <div
        @mouseenter="isHover = true"
        @mouseleave="isHover = false"
        ref="container"
        class="content"
    >
        <div
            :class="{ show: isHover, shadow: isHover, header: true }"
            @mousedown="onMouseDown"
        >
            <div class="close" @click="$emit('close', id)" />
            <div class="bar" />
        </div>
        <component
            :is="component"
            :connection="connection"
            :id="id"
            :content="content"
            class="component shadow"
        />
    </div>
</template>

<script>
export default {
    props: ['component', 'id', 'connection', 'content'],
    data() {
        return {
            isHover: false,
            isDown: false,
        };
    },
    mounted: function () {
        this.$refs.container.addEventListener('wheel', (e) => {
            if (e.ctrlKey) {
                e.preventDefault();
            }
        });
    },
    methods: {
        onMouseDown: function (event) {
            const x = event.clientX;
            const y = event.clientY;
            this.$emit('mousedown', this.id, x, y);
        },
    },
};
</script>

<style scoped>
.content {
    overflow: auto;
}
.header {
    position: relative;
    width: 100%;
    height: 20px;
    background-color: var(--white);
    border-top-right-radius: 8px;
    border-top-left-radius: 8px;
    cursor: move;
    display: flex;
    justify-content: center;
    align-items: center;
    opacity: 0;
}
.close {
    position: absolute;
    left: 8px;
    top: 5px;
    background-color: rgb(240, 106, 94);
    width: 10px;
    height: 10px;
    border-radius: 5px;
}
.close:hover {
    cursor: default;
    background-color: red;
}
.bar {
    width: 30%;
    height: 6px;
    border-radius: 3px;
    background-color: var(--black);
}
@keyframes appear {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}
.show {
    animation: appear 300ms;
    opacity: 1;
}
.component {
    height: calc(100% - 20px);
}
</style>
