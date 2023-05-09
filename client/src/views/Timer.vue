<script lang="ts" setup>
import { useTimer } from "@/stores/timer";
const timer = useTimer();
</script>

<style scoped>
.pomodoro-timer {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.timer-display {
  font-size: 48px;
  font-weight: bold;
  margin: 20px 0;
}

.timer-controls button {
  margin-right: 10px;
}
</style>

<template>
  <div class="pomodoro-timer">
    <h1>Pomodoro Timer</h1>
    <div class="timer-display">
      {{ timer.minutes }}:{{ timer.seconds < 10 ? "0" : "" }}{{ timer.seconds }}
    </div>
    <div class="timer-controls">
      <Button @click="timer.startTimer" :class="{ 'p-disabled': timer.started }"
        >Start</Button
      >
      <Button
        @click="timer.pauseTimer"
        :class="{ 'p-disabled': !timer.intervalId }"
        >Pause</Button
      >
      <Button @click="timer.resumeTimer" v-if="timer.isPaused">Resume</Button>
      <Button @click="timer.resetTimer">Reset</Button>
    </div>
    <!-- <Button @click="resPermit">Ask for notification permission</Button> -->
  </div>
</template>
