export function formatDate(date: string){
    const _date = new Date(date);
    return `${_date.getFullYear()}-${_date.getMonth() + 1}-${_date.getDate()}`;
}

export function formatTime(time: string){
    const _time = new Date(time);
    return `${_time.getHours()}:${_time.getMinutes()}`;
}

export function capitalize(str: string){
    return str[0].toUpperCase() + str.slice(1).toLowerCase()
}
