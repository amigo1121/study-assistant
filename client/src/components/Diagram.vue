
<template>
    <Chart type="doughnut" :data="chartData" :options="chartOptions" class="max-w-24rem m-auto" />
</template>

<script setup>
import { ref, onMounted} from "vue";
import Chart from 'primevue/chart';

const props = defineProps(['data'])

onMounted(() => {
chartData.value = setChartData();
});

const chartData = ref();
const chartOptions = ref({
plugins: {
    legend: {
        labels: {
            usePointStyle: true
        }
    }
}
});

const setChartData = () => {
const documentStyle = getComputedStyle(document.body);

return {
    labels: ['Low', 'Medium', 'High'],
    datasets: [
        {
            data: props.data,
            backgroundColor: [documentStyle.getPropertyValue('--green-500'), documentStyle.getPropertyValue('--yellow-500'), documentStyle.getPropertyValue('--red-500')],
            hoverBackgroundColor: [documentStyle.getPropertyValue('--green-400'), documentStyle.getPropertyValue('--yellow-400'), documentStyle.getPropertyValue('--red-400')]
        }
    ]
};
};
</script>
