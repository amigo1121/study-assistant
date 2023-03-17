<template>
  <form class="login-form" @submit.prevent="handleSubmit">
    <h2>Login</h2>
    <div class="form-group">
      <label for="username">Username</label>
      <input type="text" id="username" v-model="username" />
    </div>
    <div class="form-group">
      <label for="password">Password</label>
      <input type="password" id="password" v-model="password" />
    </div>
    <button type="submit">Log In</button>
    <a @click="$emit('change-form', 'RegisterForm')">Register</a>
  </form>
</template>

<script>
export default {
  name: 'LoginForm',
  data() {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    async handleSubmit() {
      try {
        const response = await fetch('http://localhost/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            username: this.username,
            password: this.password
          })
        });

        if (!response.ok) {
          throw new Error('Invalid credentials');
        }
        
        console.log('Logged in');
        this.$router.push('/dashboard')       
        // Here you can add code to redirect the user to a different page
        // For example, you can use Vue Router to navigate to a new page
      } catch (error) {
        console.error(error);
        alert('Invalid credentials');
      }
    },
    reset(){
        this.username='';
        this.password='';
    }
  }
}
</script>

<style scoped>
.login-form {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 0 auto;
  max-width: 600px;
  padding: 2rem;
  background-color: var(--color-background-soft);
  border-radius: 4px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 1rem;
}

label {
  font-weight: bold;
  margin-bottom: 0.5rem;
}

input[type='text'],
input[type='password'] {
  padding: 0.5rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button[type='submit'] {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button[type='submit']:hover {
  background-color: #0069d9;
}
</style>
