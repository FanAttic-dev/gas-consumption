<script setup lang="ts">
import { NButton, NSpin, NFlex, NCard, NImage, useMessage } from 'naive-ui'

import * as api from '@/api/api'
import { ref } from 'vue'
import axios from 'axios'
import { useUploadStore } from '@/stores/upload'

const message = useMessage()
const uploadStore = useUploadStore()
const imgRef = ref<string>()
const showSpin = ref(false)

async function processImages() {
  try {
    showSpin.value = true
    const res = await api.processImages()
    imgRef.value = `${api.BASE_URL}/${res.data}`
  } catch (err) {
    if (axios.isAxiosError(err) && err.response) {
      message.error(err.response.data)
    } else {
      console.error(err)
    }
  } finally {
    showSpin.value = false
  }
}
</script>

<template>
  <n-card title="2. Consumption statistics">
    <n-spin :show="showSpin">
      <n-flex>
        <n-button type="primary" :disabled="!uploadStore.uploadFinished" @click="processImages"
          >Analyze images</n-button
        >
        <n-image width="100%" :src="imgRef" />
      </n-flex>
    </n-spin>
  </n-card>
</template>
