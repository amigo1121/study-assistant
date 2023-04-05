<script setup lang="ts">
import { defineComponent, ref } from 'vue';
import AuthService from '@/services/AuthService';
import router from '@/router';

const identifier= ref<string>('');
const password= ref<string>('');

const login = () => {
    AuthService.login({identifier: identifier.value, password: password.value}).then((response)=> {
        console.log(response);
        console.log("Logged in successfully")
        router.push({name: 'welcome'})
    }).catch((error)=>{
        console.log(error);
        console.log('Invalid credentials');
    })
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
