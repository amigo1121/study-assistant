<template>
    <div class="surface-ground flex align-items-center justify-content-center min-h-screen min-w-screen overflow-hidden">
        <div class="flex flex-column align-items-center justify-content-center w-full sm:w-min">
            <div class="w-full"
                style="border-radius: 56px; padding: 0.3rem; background: linear-gradient(180deg, var(--primary-color) 10%, rgba(33, 150, 243, 0) 30%)">
                <div class="w-full surface-card py-8 px-5 sm:px-8" style="border-radius: 53px">
                    <div class="text-center mb-5">
                        <span class="text-4xl font-medium">Sign up</span>
                    </div>
                    <div>
                        <div class="field">
                            <label for="username" class="block text-900 text-xl font-medium mb-2">Username</label>
                            <InputText id="username" type="text" placeholder="Username" class="md:w-30rem sm:w-25rem w-full"
                                style="padding: 1rem" v-model="username" :class="{ 'p-invalid': error.username || !registerSuccessful}" />
                            <div class="error-msg" v-if="error.username">Username is invalid</div>
                        </div>
                        <div class="field">
                            <label for="email" class="block text-900 text-xl font-medium ">Email</label>
                            <InputText id="email" type="text" placeholder="Email" class="w-full " style="padding: 1rem"
                                v-model="email" :class="{ 'p-invalid': error.email || !registerSuccessful}" />
                            <div class="error-msg" v-if="error.email">Email is invalid</div>
                        </div>

                        <div class="field">
                            <label for="password1" class="block text-900 font-medium text-xl">Password</label>
                            <Password id="password1" v-model="password" placeholder="Password" :toggleMask="true"
                                :feedback="false" class="w-full" inputClass="w-full" :inputStyle="{ padding: '1rem' }"
                                :class="{ 'p-invalid': error.password || !registerSuccessful}">
                            </Password>
                            <div class="error-msg" v-if="error.password">Password is invalid</div>
                        </div>
                        <div class="field">
                            <label for="password2" class="block text-900 font-medium text-xl">Confirm Password</label>
                            <Password id="password2" v-model="confirmPassword" placeholder="Confirm Password"
                                :toggleMask="true" :feedback="false" class="w-full" inputClass="w-full"
                                :inputStyle="{ padding: '1rem' }" :class="{ 'p-invalid': error.confirmPassword || !registerSuccessful}">
                            </Password>
                            <div class="error-msg" v-if="error.confirmPassword">Confirm password is invalid</div>
                        </div>

                        <Button label="Sign up" class="w-full p-3 text-xl mt-2" @click="register"></Button>
                        <div class="w-100 flex align-items-center justify-content-center mt-3">
                            <router-link to="login" class="font-medium no-underline ml-2 text-right cursor-pointer"
                                style="color: var(--primary-color)">Already have a account? Log in</router-link>
                        </div>
                    </div>

                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import type { Ref } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useToast } from "primevue/usetoast";
import router from '@/router'
const username: Ref<string> = ref('');
const email: Ref<string> = ref('');
const password: Ref<string> = ref('');
const confirmPassword: Ref<string> = ref('');
const authStore = useAuthStore();
const registerSuccessful = ref<boolean>(true)
const error = reactive({
    username: false,
    email: false,
    password: false,
    confirmPassword: false
})

const register = async () => {
    if (validate())
        try {
            const res = await authStore.register({ username: username.value, email: email.value, password: password.value });
            console.log(res);
            console.log('Registered successfully');
            registerSuccessful.value = true
            router.push({ name: 'login', query: {status: 'registered'} });
        } catch (error) {
            registerSuccessful.value = false
            toast.add({severity: 'error', summary: 'Error', detail: 'User already exists', life: 2000})
            console.log(error);
            console.log('Invalid credentials');
        }
};

function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

const validate = () => {
    error.username = username.value === ""
    error.email = !validateEmail(email.value)
    error.password = password.value === ""
    error.confirmPassword = (confirmPassword.value === "" || confirmPassword.value !== password.value)

    return !(error.username || error.email || error.password || error.confirmPassword);
}


const toast = useToast();
</script>

<style lang="scss" scoped>
.error-msg {
    color: var(--red-500);
    background-color: var(--red-100);
    padding: 0.5rem 1rem;
    border-radius: 3px;
}

.field {
    margin-bottom: 1rem;
}
</style>
