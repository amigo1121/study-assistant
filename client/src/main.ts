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
const app = createApp(App);
const pinia = createPinia();

app.use(router);
app.use(pinia);
app.use(PrimeVue);
app.component('QuillEditor', QuillEditor);
app.component('Dialog', Dialog);



app.mount('#app');
