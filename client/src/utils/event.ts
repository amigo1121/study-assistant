
import moment from 'moment';

export function getNewEvent(event: any){
  let start = moment(event.startStr);
  let end = moment(event.endStr);
  if(event.allDay){
    if(!end.isValid())
    {
      end = moment(start)
      end.add(1,"days")
    }
    start = start.format("YYYY-MM-DD")
    end = end.format("YYYY-MM-DD")
  }
  else{
    if(!end.isValid())
    {
      end = moment(start)
      end.add(1,"hours")
    }
    start = start.format()
    end = end.format()
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
