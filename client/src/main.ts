import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { createPinia } from 'pinia';
import PrimeVue from 'primevue/config';
import '@/assets/styles.scss';
import { QuillEditor } from '@vueup/vue-quill'
import '@vueup/vue-quill/dist/vue-quill.snow.css';

import Button from 'primevue/button';
import Checkbox from 'primevue/checkbox';
import Dialog from 'primevue/dialog';
import InputText from 'primevue/inputtext';
import Toast from 'primevue/toast';
import Password from 'primevue/password';
import Menu from 'primevue/menu';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import ColumnGroup from 'primevue/columngroup';
import Row from 'primevue/row';


import { useAuthStore } from './stores/auth';
import ToastService from 'primevue/toastservice';

const app = createApp(App);
const pinia = createPinia();

app.use(router);
app.use(pinia);
app.use(PrimeVue);
app.use(ToastService);

app.component('Button', Button);
app.component('QuillEditor', QuillEditor);
app.component('Dialog', Dialog);
app.component('Toast', Toast);
app.component('InputText', InputText);
app.component('Menu', Menu);
app.component('Checkbox', Checkbox);
app.component('Password', Password);
app.component('DataTable', DataTable);
app.component('Column', Column);
app.component('ColumnGroup', ColumnGroup);
app.component('Row',Row);


console.log("init");


app.mount('#app');
