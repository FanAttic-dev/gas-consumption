<script setup lang="ts">
import { NH1, NFlex, NButton } from 'naive-ui'

import UploadComponent from '@/components/UploadComponent.vue'
import StatsComponent from '@/components/StatsComponent.vue'
import { useUserStore } from '@/stores/user'
import { onMounted } from 'vue'
import { useUploadStore } from '@/stores/upload'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const uploadStore = useUploadStore()
const router = useRouter()

function logout(e: MouseEvent) {
  e.preventDefault()

  userStore.logout()
  router.replace({ name: 'login' })
}

onMounted(async () => {
  uploadStore.$reset()
  await userStore.autoLogin()
})
</script>

<template>
  <main>
    <n-flex>
      <n-flex style="width: 100%" justify="space-between">
        <n-h1>Gas Consumption Analyzer</n-h1>
        <n-button @click="logout" type="error" ghost>Logout </n-button>
      </n-flex>
      <UploadComponent></UploadComponent>
      <StatsComponent></StatsComponent>
    </n-flex>
  </main>
</template>

<style>
.n-upload-trigger.n-upload-trigger--image-card .n-upload-dragger {
  padding: 24px;
}
</style>
