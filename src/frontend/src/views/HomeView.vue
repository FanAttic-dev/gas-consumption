<script setup lang="ts">
import { NH2, NH3, NSpace, NDivider, NPageHeader, NFlex, NButton, NText } from 'naive-ui'

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
    <n-space vertical>
      <n-page-header>
        <template #title> <n-h2 style="margin: 0">Gas Consumption Analyzer </n-h2></template>
        <template #extra>
          <n-flex align="baseline">
            <n-h3>{{ userStore.user?.name }}</n-h3>
            <n-button @click="logout" type="error" ghost>Logout </n-button>
          </n-flex>
        </template>
      </n-page-header>
      <UploadComponent></UploadComponent>
      <StatsComponent></StatsComponent>
    </n-space>
    <!-- 
      <n-flex style="width: 100%; align-items: center" justify="space-between">
        <n-h1>Gas Consumption Analyzer</n-h1>
        <n-flex>
          <n-text strong>{{ userStore.user?.name }}</n-text>
          <n-button @click="logout" type="error" ghost>Logout </n-button>
        </n-flex>
      </n-flex>
      
    </n-flex> -->
  </main>
</template>

<style>
.n-upload-trigger.n-upload-trigger--image-card .n-upload-dragger {
  padding: 24px;
}

.n-page-header {
  align-items: flex-start;
}
</style>
