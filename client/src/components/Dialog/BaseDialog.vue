<template>
        <div @click="$emit('close')">

        </div>
        <dialog open>
            <section>
                <slot></slot>
            </section>
        </dialog>
</template>

<script>

export default {
    props: {
        title: {
            type: String,
            required: false
        }
    },
    emits: ['close']
}
</script>

<style lang="scss" scoped>
div {
    position: fixed;
    top: 0;
    left: 0;
    height: 100vh;
    width: 100%;
    background-color: rgba(255, 255, 255, 0.75);
    z-index: 10;
}

dialog {
    position: fixed;
    top: 20vh;
    left: 10%;
    width: 50%;
    z-index: 100;
    border-radius: 12px;
    border: none;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.26);
    padding: 0;
    margin: 0;
    overflow: hidden;
}
section {
    padding: 1rem;
}
@media (min-width: 768px) {
    dialog {
        left: calc(50% - 20rem);
        width: 40rem;
    }
}
</style>