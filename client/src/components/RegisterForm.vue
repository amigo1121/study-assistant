<template>
  <form class="register-form" @submit.prevent="handleSubmit">
    <h2>Register</h2>
    <div class="form-group">
      <label for="username">Username</label>
      <input type="text" id="username" v-model="username" />
    </div>
    <div class="form-group">
      <label for="email">Email</label>
      <input type="email" id="email" v-model="email" />
    </div>
    <div class="form-group">
      <label for="password">Password</label>
      <input type="password" id="password" v-model="password" />
    </div>
    <div class="form-group">
      <label for="password2">Re-enter Password</label>
      <input type="password" id="password2" v-model="password2" />
    </div>
    <button type="submit">Register</button>
    <a @click="$emit('change-form', 'LoginForm')">Login</a>

  </form>
</template>

<script lang="ts">
export default {
  name: 'RegisterForm',
  data() {
    return {
      username: '',
      email: '',
      password: '',
      password2: ''
    };
  },
  methods: {
    async handleSubmit() {
      if (this.password !== this.password2) {
        alert('Passwords do not match');
        return;
      }
      
      try {
        const response = await fetch('http://localhost/users', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            username: this.username,
            email: this.email,
            password: this.password
          })
        });
        
        console.log(response)
        if (!response.ok) {
          throw new Error('Error registering user');
        }
        
        console.log('User registered');
        this.reset()
      } catch (error) {
        console.error(error);
        alert('Error registering user');
      }
    },
    reset(){
        this.username=''
        this.email=''
        this.password=''
        this.password2=''
    }
  }
}
</script>

<style scoped>
.register-form {
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
input[type='email'],
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
