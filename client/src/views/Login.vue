<script setup lang="ts">
import { ref, defineProps, onMounted } from 'vue';
import { useRoute } from 'vue-router'
import router from '@/router';
import { useAuthStore } from '@/stores/auth';
import { useToast } from 'primevue/usetoast';
import { sessionExpireRemind } from '@/utils/sessionExpireReminder'


const identifier = ref<string>('');
const password = ref<string>('');
const isRemember = ref<boolean>(false)
const authStore = useAuthStore();
const toast = useToast();
const login = () => {
    authStore.login({ identifier: identifier.value, password: password.value }, isRemember.value).then((response) => {
        console.log(response);
        console.log("Logged in successfully")
        sessionExpireRemind(() => { toast.add({ severity: 'info', summary: "Info", detail: `Session expires in 1 minutes, you will be logged out.` }); }, () => { authStore.logout(); })
        router.push({ name: 'dashboard' })
    }).catch((error) => {
        console.log(error);
        console.log('Invalid credentials');
    })
}

onMounted(() => {
    const route = useRoute();
    const toast = useToast();
    if (route.query.sessionExpired) {
        toast.add({ severity: 'warn', summary: 'Warning', detail: 'Your session has expired, please login' });
    }
})

</script>
<template>
    <div class="surface-ground flex align-items-center justify-content-center min-h-screen min-w-screen overflow-hidden">
        <div class="flex flex-column align-items-center justify-content-center">
            <div
                style="border-radius: 56px; padding: 0.3rem; background: linear-gradient(180deg, var(--primary-color) 10%, rgba(33, 150, 243, 0) 30%)">
                <div class="w-full surface-card py-8 px-5 sm:px-8" style="border-radius: 53px">
                    <div class="text-center mb-5">
                        <span class="text-4xl font-medium">Sign in</span>
                    </div>
                    <div>
                        <label for="email1" class="block text-900 text-xl font-medium mb-2">Identifier</label>
                        <InputText id="email1" type="text" placeholder="Username of Password" class="w-full md:w-30rem mb-5"
                            style="padding: 1rem" v-model="identifier" />

                        <label for="password1" class="block text-900 font-medium text-xl mb-2">Password</label>
                        <Password id="password1" v-model="password" placeholder="Password" :toggleMask="true"
                            class="w-full mb-3" inputClass="w-full" :inputStyle="{ padding: '1rem' }" :feedback="false">
                        </Password>

                        <div class="flex align-items-center justify-content-between mb-5 gap-5">
                            <div class="flex align-items-center">
                                <Checkbox v-model="isRemember" id="rememberme1" binary class="mr-2"></Checkbox>
                                <label for="rememberme1">Remember me</label>
                            </div>
                            <router-link class="font-medium no-underline ml-2 text-right cursor-pointer"
                                style="color: var(--primary-color)" to="register">Register</router-link>
                        </div>
                        <Button label="Sign In" class="w-full p-3 text-xl" @click="login"></Button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped></style>
