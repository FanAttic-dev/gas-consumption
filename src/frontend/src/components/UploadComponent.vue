<script setup lang="ts">
import {
  NUpload,
  NCard,
  NModal,
  type UploadFileInfo,
  type FormInst,
  useMessage,
  type MessageReactive
} from 'naive-ui'

import { ref } from 'vue'

import * as api from '@/api/api'

const showModalRef = ref(false)
const previewImageUrlRef = ref('')
const fileListRef = ref<UploadFileInfo[]>([])
const message = useMessage()
let uploadMessage: MessageReactive | null = null

function handlePreview(file: UploadFileInfo) {
  const { name } = file
  previewImageUrlRef.value = `${api.BASE_URL}/static/uploads/${name}`
  showModalRef.value = true
}

function fileListUpdate(fileList: UploadFileInfo[]) {
  console.log('File list update:')
  fileListRef.value = fileList
  if (uploadMessage == null) {
    uploadMessage = message.loading('Uploading...', { duration: 0 })
  }
  console.log(fileList)
  const allUploaded = fileList.every((file) => file.status == 'finished')
  if (allUploaded) {
    uploadMessage?.destroy()
    uploadMessage = null
    console.log('All files uploaded')
  }
}
</script>

<template>
  <n-card title="1. Upload your photos">
    <n-upload
      accept="image/jpg"
      :multiple="true"
      :action="api.uploadUrl"
      list-type="image-card"
      :default-upload="true"
      @preview="handlePreview"
      @update-file-list="fileListUpdate"
    />
    <n-modal v-model:show="showModalRef" preset="card" style="width: 600px" title="">
      <img :src="previewImageUrlRef" style="width: 100%" />
    </n-modal>
  </n-card>
</template>
