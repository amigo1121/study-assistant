import moment from "moment";
import { useAuthStore } from "@/stores/auth";
export function sessionExpireRemind(setNotification, setLogout) {
  const authStore = useAuthStore();
  let expiredTime = localStorage.getItem("loginTime");
  if (authStore.refreshToken) {
    expiredTime = moment(expiredTime).add(7, "days");
  } else {
    expiredTime = moment(expiredTime).add(15, "minutes");
  }
  if (expiredTime.isValid()) {
    let currentTime = moment();
    let diffSecond = expiredTime.diff(currentTime, "seconds");

    // setTimeout(()=>{authStore.logout();},120*1000)
    setTimeout(setLogout, diffSecond * 1000);

    // setTimeout(()=>{toast.add({severity: 'info', summary: "Info", detail: `Session expires in 1 minutes, you will be loged out.`});},(120-60)*1000)
    setTimeout(setNotification, (diffSecond - 60) * 1000);
  }
}

export default sessionExpireRemind;
