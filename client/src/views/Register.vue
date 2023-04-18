<template>
    <div class="container">
        <Card id="card">
            <template #title> <div class="flex justify-content-center text-4xl">
                Sign Up
            </div>
        </template>
            <template #content>
                <label for="username" class="block text-900 text-xl font-medium mb-2">Username</label>
                <InputText id="username" type="text" placeholder="Username" class="w-full md:w-30rem mb-3"
                    style="padding: 1rem" v-model="username" />
                <label for="email" class="block text-900 text-xl font-medium mb-2">Email</label>
                <InputText id="email" type="text" placeholder="Email" class="w-full md:w-30rem mb-3" style="padding: 1rem"
                    v-model="email" />
                <label for="password1" class="block text-900 font-medium text-xl mb-2">Password</label>
                <Password id="password1" v-model="password" placeholder="Password" :toggleMask="true" :feedback="false"
                    class="w-full mb-3" inputClass="w-full" :inputStyle="{padding:'1rem'}"></Password>
                <label for="password2" class="block text-900 font-medium text-xl mb-2">Confirm Password</label>
                <Password id="password2" v-model="confirmPassword" placeholder="Confirm Password" :toggleMask="true"
                    :feedback="false" class="w-full mb-3" inputClass="w-full" :inputStyle="{padding:'1rem'}"></Password>
                <Button label="Sign up" class="w-full p-3 text-xl mt-2" @click="register"></Button>
                <div class="w-100 flex align-items-center justify-content-center mt-3">
                    <router-link to="login" class="font-medium no-underline ml-2 text-right cursor-pointer"
                        style="color: var(--primary-color)">Already have a account? Log in</router-link>
                </div>
            </template>
        </Card>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import type { Ref } from 'vue';
import { useAuthStore } from '@/stores/auth';
import Card from 'primevue/card';
import InputText from 'primevue/inputtext';
import Password from 'primevue/password';
import Button from 'primevue/button';
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
.p-card {
    padding: 20px;
    max-width: 500px;
    position: absolute;
    margin: auto;
    inset: 0;
    height: fit-content;
}

.p-card-title {
    text-align: center;
}

.input-container {
    margin-bottom: 2rem;
}

.p-inputtext {
    width: 100%;
}
</style>
