<script setup lang="ts">
import { ref } from 'vue'
import Calendar from 'primevue/calendar';
import InputSwitch from 'primevue/inputswitch';

const startDate = ref<string>("");
const endDate = ref<string>("");
const startTime = ref<string>("");
const endTime = ref<string>("");
const title = ref<string>("");
const allDay = ref<boolean>(false);
const repeat = ref<boolean>(false);
</script>
<template>
    <h5>Create Event</h5>
    <div class="p-fluid formgrid grid">
        <div class="field col-12">
            <label for="title">Title</label>
            <InputText id="title" type="text" v-model="title" />
        </div>
        <template v-if="!allDay">
            <div class="field col-12">
                <div class="mb-1">Repeat</div>
                <InputSwitch v-model="repeat"/>
            </div>
        </template>
        <template v-if="!repeat">
            <div class="field col-12">
                <div class="mb-1">All day</div>
                <InputSwitch v-model="allDay"/>
            </div>
        </template>
        <div class="field col-6">
            <label for="startDate">From</label>
            <Calendar v-model="startDate" id="startDate" dateFormat="yy-mm-dd" showButtonBar />
        </div>
        <template v-if="allDay || repeat">
            <div class="field col-6">
                <label for="endDate">To</label>
                <Calendar v-model="endDate" id="endDate" dateFormat="yy-mm-dd" showButtonBar />
            </div>
        </template>
        <template v-if="!allDay &&!repeat">
            <div class="field col-3">
                <label for="startTime">Start at</label>
                <Calendar v-model="startTime" id="startTime" timeOnly />
            </div>
            <div class="field col-3">
                <label for="endTime">End at</label>
                <Calendar v-model="endTime" id="endTime" timeOnly />
            </div>
        </template>


    </div>
</template>
<style lang="scss" scoped></style>
