<script lang="ts">
import LoginForm from '../components/LoginForm.vue'
import RegisterForm from '../components/RegisterForm.vue'

export default {
  components: {
    LoginForm,
    RegisterForm
  },
  data() {
    return {
      form: 'LoginForm'
    }
  },
  methods: {
    changeForm(name: string) {
      this.form = name
    }
  }
}
</script>

<template>
  <div class="login-page">
    <component :is="form" @change-form="changeForm"></component>
  </div>
</template>

<style>
.login-page {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100%;
}
</style>
