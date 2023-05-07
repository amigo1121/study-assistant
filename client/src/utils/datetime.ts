export function formatDate(date: string) {
  const _date = new Date(date);
  return `${_date.getFullYear()}-${_date.getMonth() + 1}-${_date.getDate()}`;
}

export function formatTime(time: string) {
  const _time = new Date(time);
  return `${_time.getHours()}:${_time.getMinutes()}`;
}

export function capitalize(str: string) {
  return str[0].toUpperCase() + str.slice(1).toLowerCase();
}

export function timeValidation(str: string) {
  const validator = /^([01][0-9]|2[0-3]):[0-5][0-9]$/;
  return validator.test(str);
}

export function getMinutesDifference(start, end) {
  const startTime = new Date(`2000-01-01T${start}:00`);
  const endTime = new Date(`2000-01-01T${end}:00`);

  // Calculate difference in minutes
  const diffMilliseconds = endTime - startTime;
  const diffMinutes = diffMilliseconds / 60000;
  return diffMinutes;
}
