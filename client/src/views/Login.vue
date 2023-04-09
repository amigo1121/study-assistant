<script setup lang="ts">
import { defineComponent, ref } from 'vue';
import router from '@/router';
import { useAuthStore } from '@/stores/auth';

const identifier= ref<string>('');
const password= ref<string>('');
const  authStore = useAuthStore();

const login = () => {
    authStore.login({identifier: identifier.value, password: password.value}).then((response)=> {
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
