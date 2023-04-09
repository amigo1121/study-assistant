<template>
    <h3>register</h3>
    <form>
        <input type="text" v-model="username" placeholder="username" />
        <input type="text" v-model="email" placeholder="email" />
        <input type="password" v-model="password" placeholder="password" />
        <button type="button" @click="register">Register</button>
    </form>

    <button type="button" @click="test">Test</button>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import type { Ref } from 'vue';
import { useAuthStore } from '@/stores/auth';

const username: Ref<string> = ref('');
const email: Ref<string> = ref('');
const password: Ref<string> = ref('');
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
</script>

<style lang="scss" scoped></style>
