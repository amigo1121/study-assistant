import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { createPinia } from 'pinia';
import PrimeVue from 'primevue/config';
import '@/assets/styles.scss';
import { QuillEditor } from '@vueup/vue-quill'
import '@vueup/vue-quill/dist/vue-quill.snow.css';
import Dialog from 'primevue/dialog';
import { useAuthStore } from './stores/auth';
import Toast from 'primevue/toast';
import ToastService from 'primevue/toastservice';
const app = createApp(App);
const pinia = createPinia();

app.use(router);
app.use(pinia);
app.use(PrimeVue);
app.use(ToastService);
app.component('QuillEditor', QuillEditor);
app.component('Dialog', Dialog);
app.component('Toast', Toast);
console.log("init");


app.mount('#app');
