

export const INITIAL_EVENTS = [
  {
    id: createEventId(),
    title: 'All-day event',
    start: todayStr
  },
  {
    id: createEventId(),
    title: 'Timed event',
    start: todayStr + 'T12:00:00',
    end: todayStr + 'T20:00:00'
  }
]

export function createEventId() {
  return String(eventGuid++)
}

export function getDay(date: string){
  return date.replace(/T.*$/, '')
}

export function getNewEvent(event: any){
  let start = event.startStr;
  let end = event.endStr;
  if(event.allDay){
    start = getDay(start)
    end = getDay(end)
  }
  let owner_id = event.owner_id? event.owner_id: null

  return {
    title: event.title,
    start,
    end,
    owner_id,
    id: event.id
  }
}
