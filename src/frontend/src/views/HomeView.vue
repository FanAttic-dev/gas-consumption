<script setup lang="ts">
import { NH1, NFlex } from 'naive-ui'

import UploadComponent from '@/components/UploadComponent.vue'
import StatsComponent from '@/components/StatsComponent.vue'
</script>

<template>
  <main>
    <n-flex>
      <n-h1>Gas Consumption Analyzer</n-h1>
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
