<template>
    <div class="surface-ground flex align-items-center justify-content-center min-h-screen min-w-screen overflow-hidden">
        <div class="flex flex-column align-items-center justify-content-center">
            <div
                style="border-radius: 56px; padding: 0.3rem; background: linear-gradient(180deg, var(--primary-color) 10%, rgba(33, 150, 243, 0) 30%)">
                <div class="w-full surface-card py-8 px-5 sm:px-8" style="border-radius: 53px">
                    <div class="text-center mb-5">
                        <span class="text-4xl font-medium">Sign up</span>
                    </div>
                    <div>
                        <label for="username" class="block text-900 text-xl font-medium mb-2">Username</label>
                        <InputText id="username" type="text" placeholder="Username" class="w-full md:w-30rem mb-3"
                            style="padding: 1rem" v-model="username" />
                        <label for="email" class="block text-900 text-xl font-medium mb-2">Email</label>
                        <InputText id="email" type="text" placeholder="Email" class="w-full md:w-30rem mb-3"
                            style="padding: 1rem" v-model="email" />
                        <label for="password1" class="block text-900 font-medium text-xl mb-2">Password</label>
                        <Password id="password1" v-model="password" placeholder="Password" :toggleMask="true"
                            :feedback="false" class="w-full mb-3" inputClass="w-full" :inputStyle="{ padding: '1rem' }">
                        </Password>
                        <label for="password2" class="block text-900 font-medium text-xl mb-2">Confirm Password</label>
                        <Password id="password2" v-model="confirmPassword" placeholder="Confirm Password" :toggleMask="true"
                            :feedback="false" class="w-full mb-3" inputClass="w-full" :inputStyle="{ padding: '1rem' }">
                        </Password>
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
import { ref } from 'vue';
import type { Ref } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useToast } from "primevue/usetoast";

const username: Ref<string> = ref('');
const email: Ref<string> = ref('');
const password: Ref<string> = ref('');
const confirmPassword: Ref<string> = ref('');
const authStore = useAuthStore();

const register = async () => {
    try {
        const res = await authStore.register({ username: username.value, email: email.value, password: password.value });
        console.log(res);
        console.log('Registered successfully');
    } catch (error) {
        console.log(error);
        console.log('Invalid credentials');
    }
};



const toast = useToast();
</script>

<style lang="scss" scoped>
</style>
