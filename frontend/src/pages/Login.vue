<template>
  <div class="h-screen flex items-center justify-center">
    <div class="w-full max-w-md p-6 border-2 rounded">
      <div class="flex justify-center p-5 mt-0">
        <Avatar
          :shape="'square'"
          image="/assets/go1_vendor/image/logo.svg"
          label="EY"
          size="2xl"
        />
      </div>
      <h1 class="text-center text-3xl font-semibold text-gray-900 mb-4">
        Login to Go1 Vendor
      </h1>
      <form class="flex flex-col space-y-2 w-full" @submit.prevent="submit">
        <Input
          v-model="email"
          required
          name="email"
          type="text"
          placeholder="johndoe@email.com"
          label="User ID"
        />
        <div class="relative">
          <Input
            v-model="password"
            required
            name="password"
            :type="showPassword ? 'text' : 'password'"
            placeholder="••••••"
            label="Password"
          />
          <FeatherIcon
            :name="showPassword ? 'eye' : 'eye-off'"
            @click="togglePasswordVisibility"
            class="absolute h-4 right-3 top-2/3 transform -translate-y-1/3 cursor-pointer text-gray-600"
          />
        </div>
        <Button
          :loading="session.login.loading"
          variant="solid"
          style="margin-top: 24px"
          >Login</Button
        >
        <ErrorMessage :message="errorMessage" v-if="errorMessage" />
      </form>
      <!-- <div class="flex justify-center items-center mt-4">
        <span class="text-sm text-gray-600">Don't have an account?</span>
        <Button
          variant="ghost"
          theme="gray"
          size="sm"
          label="Signup"
          :loading="false"
          :disabled="false"
          @click="openCreate"
          class="ml-2"
        >
          Signup
        </Button>
      </div> -->
    </div>
  </div>
</template>
<script lang="ts" setup>
import { ref } from 'vue'
import { session } from '../data/session'
import {
  Avatar,
  Button,
  Input,
  createResource,
  ErrorMessage,
  FeatherIcon,
} from 'frappe-ui'
import { useRouter } from 'vue-router'

const router = useRouter()

const email = ref('')
const showPassword = ref(false)
const password = ref('')
const errorMessage = ref<string>('')

const openCreate = async () => {
  try {
    console.log('Navigating to Signup page')
    await router.push({ name: 'Register' })
  } catch (error) {
    console.error('Navigation error:', error)
  }
}

const submit = async () => {
  session.login.Loading = true;
  errorMessage.value = '';
  
  try {
    if (email.value.toLowerCase() === 'administrator') {
      await session.login.submit({
        email: email.value,
        password: password.value,
      });
      return;
    }

    const loginResource = createResource({
      url: 'go1_vendor.apidata.check_supplier',
      method: 'GET',
      params: { email: email.value },
    });

    const response = await loginResource.fetch();
    console.log('data', response);

    if (response.status === "success") {      
      await session.login.submit({
        email: email.value,
        password: password.value,
      });
    } else {     
      errorMessage.value = "Email not found in Supplier portal users.";      
    }
  } catch (error) {
    console.log('Error during login:', error);
  } finally {
    session.login.Loading = false;
  }
};

function togglePasswordVisibility() {
  showPassword.value = !showPassword.value
}
</script>
