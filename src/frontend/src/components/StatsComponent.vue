<script setup lang="ts">
import { NButton, NFlex, NCard, NImage, useMessage } from 'naive-ui'

import * as api from '@/api/api'
import { ref } from 'vue'

const message = useMessage()
const imgRef = ref<string>()

async function processImages() {
  try {
    const res = await api.processImages()
    console.log(res.data)
    imgRef.value = `${api.BASE_URL}/${res.data}`
  } catch (err) {
    message.error(err.response.data)
  }
}
</script>

<template>
  <n-card>
    <n-flex>
      <n-button type="primary" @click="processImages">Process images</n-button>
      <n-image width="100%" :src="imgRef" />
    </n-flex>
  </n-card>
</template>
