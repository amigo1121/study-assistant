<script setup lang="ts">
import { defineComponent, ref } from 'vue';
import AuthService from '@/services/AuthService';

const username= ref('');    
const email= ref('');
const password= ref('');

const register = async () => {
    try {
        const res = await AuthService.register({username: username.value, email: email.value, password: password.value});
        console.log(res);
        console.log('Registered successfully');
    } catch (error) {
        console.log(error);
        console.log('Invalid credentials');
    }
}

const test = async () => {
    try {
        const res = await AuthService.test();
        console.log(res);
        console.log('Tested successfully');
    } catch (error) {
        console.log(error);
        console.log('Invalid credentials');
    }
}

</script>
<style lang="scss" scoped>
</style>
<template>
    <h3>register</h3>
    <form>
        <input type="text" v-model="username" placeholder="username" />
        <input type="text" v-model="email" placeholder="email" />
        <input type="password" v-model="password" placeholder="password" />
        <button type="button" @click="register">Register</button>
    </form>

    <button type="button" @click="test">TEst</button>
</template>