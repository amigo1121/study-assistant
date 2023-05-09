import { defineStore } from "pinia";
import { ref } from "vue";

export const useTimer = defineStore("timer", () => {
  const studyTime = ref(30);
  const shortBreak = ref(5);
  const longBreak = ref(15);
  const counter = ref(0);
  const minutes = ref(0);
  const seconds = ref(0);
  const intervalId = ref(null);
  const isPaused = ref(false);
  const mode = ref("study");
  const started = ref(false);
  // set timer base on mode: study or break
  const startTimer = () => {
    started.value = true;
    prerun();
    startInterval();
  };

  const startInterval = () => {
    intervalId.value = setInterval(() => {
      if (seconds.value === 0) {
        if (minutes.value === 0) {
          clearInterval(intervalId.value);
          intervalId.value = null;
          counter.value += 1;
          if (mode.value === "study") {
            const takeBreak = confirm(
              "You have studied for 30 minutes, let's take a break"
            );
            if (takeBreak) {
              mode.value = "break";
            } else {
              counter.value += 1;
            }
          } else {
            alert("Break time is over, let's get back to work");
            mode.value = "study";
          }
          prerun();
          startTimer();
        } else {
          minutes.value--;
          seconds.value = 59;
        }
      } else {
        seconds.value--;
      }
    }, 1000);
  };

  const pauseTimer = () => {
    isPaused.value = true;
    if (intervalId.value) {
      clearInterval(intervalId.value);
      intervalId.value = null;
    }
  };

  const resumeTimer = () => {
    isPaused.value = false;
    if (!intervalId.value) startInterval();
  };

  const resetTimer = () => {
    pauseTimer();
    mode.value = "study";
    seconds.value = 0;
    minutes.value = studyTime.value;
    counter.value = 0;
    isPaused.value = false;
    started.value = false;
  };

  const prerun = () => {
    seconds.value = 0;
    switch (mode.value) {
      case "study":
        minutes.value = studyTime.value;
        break;
      case "break":
        if (counter.value % 2 === 1) {
          if ((counter.value + 1) % 8 === 0) {
            minutes.value = longBreak.value;
          } else {
            minutes.value = shortBreak.value;
          }
        }
        break;
    }
  };

  return {
    started,
    intervalId,
    studyTime,
    shortBreak,
    longBreak,
    mode,
    counter,
    minutes,
    seconds,
    startTimer,
    startInterval,
    resumeTimer,
    isPaused,
    pauseTimer,
    resetTimer,
    prerun,
  };
});
