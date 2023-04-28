<script lang="ts" setup>
import Calendar from 'primevue/calendar';
import moment from 'moment'
import axios from 'axios'
import { ref } from "vue"
import { useAuthStore } from '@/stores/auth';
import { API_URL } from "@/utils/config";
const authStore = useAuthStore()
const name = ref("");
const code = ref("");
const credits = ref(1);
const start = ref();
const end = ref();
const schedule = ref({
    monday: {
        apply: false,
        from: "",
        to: ""
    },
    tuesday: {
        apply: false,
        from: "",
        to: ""
    },
    wednesday: {
        apply: false,
        from: "",
        to: ""
    },
    thursday: {
        apply: false,
        from: "",
        to: ""
    },
    friday: {
        apply: false,
        from: "",
        to: ""
    }
});

const extractHour = (d: Date) => {
    return moment(d).format("HH:mm")
}

const submit = async () => {
    const inputForm = {
        name: name.value,
        credits: credits.value,
        code: code.value,
        start_date: moment(start.value).format("YYYY-MM-DD"),
        end_date: moment(end.value).format("YYYY-MM-DD"),
        schedules: (Object.entries(schedule.value)
            .filter(([key, value]) => value.apply)
            .map(([key, value]) => {
                return {
                    day: key,
                    start: extractHour(value.from),
                    end: extractHour(value.to)
                }
            }
            ))
    }
    // console.log(inputForm)

    let config = {
        headers: {
            Authorization: `Bearer ${authStore.accessToken}`,
        },
    };
    try {
        await axios.post(API_URL + "/course", inputForm, config)
    } catch (error) {
        console.log(error)
    }
}

const upper = (str) => {
    return str.charAt(0).toUpperCase() + str.slice(1)
}
</script>
<style lang="scss" scoped></style>
<template>
    <div class="p-fluid formgrid grid">
        <div class="field col-12">
            <label for="courseName">Course name</label>
            <InputText id="courseName" type="text" v-model="name" />
        </div>
        <div class="field col-6">
            <label for="courseCode">Course code</label>
            <InputText id="courseCode" type="text" v-model="code" />
        </div>

        <div class="field col-6">
            <label for="courseCredits">Credits</label>
            <InputNumber id="courseCredits" v-model="credits" inputId="minmax" :min="1" :max="5" />
        </div>


        <div class="field col-6">
            <label for="startDate">Start date</label>
            <Calendar v-model="start" id="startDate" dateFormat="yy-mm-dd" showButtonBar />
        </div>
        <div class="field col-6">
            <label for="endDate">End date</label>
            <Calendar v-model="end" id="endDate" dateFormat="yy-mm-dd" showButtonBar />
        </div>

        <div class="field col-12">
            <label for="schedule">Schedule</label>
            <div id="schedule">
                <div class="grid" v-for="(value, key) in schedule" :key="key">
                    <div class="mb-1 col-12">
                        <Checkbox v-model="value.apply" :binary="true" /> {{ upper(key) }}
                    </div>
                    <div class="field col-6" :class="{ 'p-disabled': !value.apply }">
                        <label for="startTime">From</label>
                        <Calendar v-model="value.from" id="startTime" timeOnly />
                    </div>
                    <div class="field col-6" :class="{ 'p-disabled': !value.apply }">
                        <label for="endTime">To</label>
                        <Calendar v-model="value.to" id="endTime" timeOnly />
                    </div>
                </div>
            </div>
        </div>








        <!-- <div class="field col-12">
            <div class="mb-1">All day</div>
            <InputSwitch v-model="allDay" />
        </div>
        <div class="field col-6">
            <label for="startDate">From</label>
            <Calendar v-model="startDate" id="startDate" dateFormat="yy-mm-dd" showButtonBar />
        </div>
        <div class="field col-6" v-if="!allDay">
            <label for="startTime">At</label>
            <Calendar v-model="startTime" id="startTime" timeOnly />
        </div>
        <div class="field col-6">
            <label for="endDate">To</label>
            <Calendar v-model="endDate" id="endDate" dateFormat="yy-mm-dd" showButtonBar />
        </div>
        <div class="field col-6" v-if="!allDay">
            <label for="endTime">At</label>
            <Calendar v-model="endTime" id="endTime" timeOnly />
        </div>
        <div class="col-12 mb-3" v-if="!valid">
            <InlineMessage severity="error">Wrong input</InlineMessage>
        </div> -->

        <div class="flex col-12 gap-4 flex-nowrap justify-content-end">
            <Button class="flex max-w-min" severity="info" label="Save" @click="submit" />
        </div>

    </div>
</template>
