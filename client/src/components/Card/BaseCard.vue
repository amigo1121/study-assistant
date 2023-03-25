<template>
    <div class="base-card">
        <slot></slot>
    </div>
</template>
<style scoped lang="scss">
.base-card {
    background-color: #f4f5f7;
    border: 1px solid #dfe1e6;
    border-radius: 3px;
    box-shadow: 0 1px 0 rgba(9, 30, 66, 0.25);
    font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Noto Sans, Ubuntu,
        Cantarell, Helvetica Neue, sans-serif;
    width: fit-content;

    &:hover {
        box-shadow: 0 0 0 1px rgba(9, 30, 66, 0.25), 0 1px 3px rgba(9, 30, 66, 0.25);
    }
}
</style>
  