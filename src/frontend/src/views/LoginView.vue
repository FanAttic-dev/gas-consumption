<script setup lang="ts">
import {
  NForm,
  NPageHeader,
  NH2,
  NFormItem,
  NSpace,
  NCard,
  NButton,
  NInput,
  useMessage,
  type FormInst
} from 'naive-ui'
import { onMounted, ref } from 'vue'
import type { User } from '@/types/user'
import axios from 'axios'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()
const message = useMessage()
const formRef = ref<FormInst | null>(null)
const formValue = ref<User>({
  name: '',
  password: ''
})

const rules = {
  name: {
    required: true,
    message: 'Please enter your username',
    trigger: 'blur'
  },
  password: {
    required: true,
    message: 'Please enter your password',
    trigger: ['input', 'blur']
  }
}

async function login(e: MouseEvent) {
  e.preventDefault()

  try {
    await userStore.login(formValue.value)
  } catch (err) {
    if (axios.isAxiosError(err) && err.response) {
      message.error(err.response.data.message)
    } else {
      console.error(err)
    }
  }
}

async function register(e: MouseEvent) {
  e.preventDefault()

  try {
    await userStore.register(formValue.value)
  } catch (err) {
    if (axios.isAxiosError(err) && err.response) {
      message.error(err.response.data.message)
    } else {
      console.error(err)
    }
  }
}

onMounted(async () => {
  await userStore.autoLogin()
  if (userStore.isLoggedIn) {
    router.replace({ name: 'home' })
  }
})
</script>

<template>
  <n-space vertical>
    <n-page-header>
      <template #title> <n-h2 style="margin: 0">Gas Consumption Analyzer </n-h2></template>
    </n-page-header>
    <n-card>
      <n-form ref="formRef" :label-width="80" :model="formValue" :rules="rules">
        <n-form-item label="Username" path="name">
          <n-input v-model:value="formValue.name" placeholder="Username" />
        </n-form-item>
        <n-form-item label="Password" path="password">
          <n-input v-model:value="formValue.password" placeholder="Password" />
        </n-form-item>
        <n-form-item>
          <n-space>
            <n-button type="warning" @click="register"> Register </n-button>
            <n-button type="primary" @click="login"> Login </n-button>
          </n-space>
        </n-form-item>
      </n-form>
    </n-card>
  </n-space>
</template>
