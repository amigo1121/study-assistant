<script lang="ts" setup>
import { ref, defineEmits } from 'vue'
import {useToast} from 'primevue/usetoast'
const props = defineProps({
    coursecode:{
        type: String,
        required: true
    }
})
const menuRef = ref()
const toast = useToast()
const emits = defineEmits(['detail','drop'])
const items = ref(
    [
        {
            label: 'Options',
            items: [
                {
                    label: 'Detail',
                    command: () => {
                        emits('detail',props.coursecode)
                    }
                },
                {
                    label: 'Drop course',
                    command: () => {
                        emits('drop',props.coursecode)
                    }
                }
            ]
        }]
)
function toggleMenu(event) {
    menuRef.value.toggle(event)
}

</script>
<style lang="scss" scoped></style>
<template>
    <Button icon="pi pi-user" severity="info" text rounded aria-label="User" @click="toggleMenu" />
    <Menu :model="items" popup ref="menuRef"></Menu>
</template>
