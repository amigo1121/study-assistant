<script setup lang="ts">
import { defineComponent, ref } from 'vue';
import AuthService from '@/services/AuthService';

const identifier= ref('');
const password= ref('');

const login = async () => {
    try {
        const res = await AuthService.login({identifier: identifier.value, password: password.value});
        console.log(res);
        console.log('Logged in successfully');
    } catch (error) {
        console.log(error);
        console.log('Invalid credentials');
    }
}

</script>
<style lang="scss"></style>
<template>
    <h3>login</h3>
    <form>
        <input type="text" v-model="identifier" placeholder="username or email" />
        <input type="password" v-model="password" placeholder="password" />
        <button type="button" @click="login">Login</button>
    </form>
</template>