<script setup lang="ts">
import { NUpload, NCard, NModal, type UploadFileInfo, type FormInst } from 'naive-ui'

import { ref } from 'vue'

import * as api from '@/api/api'

const showModalRef = ref(false)
const previewImageUrlRef = ref('')
const fileListRef = ref<UploadFileInfo[]>([])

function handlePreview(file: UploadFileInfo) {
  const { name } = file
  previewImageUrlRef.value = `${api.BASE_URL}/uploads/${name}`
  showModalRef.value = true
}

function beforeUpload(options: { file: UploadFileInfo; fileList: Array<UploadFileInfo> }) {
  console.log(`Before Upload`)
  // console.log(options.file)
  return true
}

function afterUpload(options: { file: UploadFileInfo; event?: Event }) {
  console.log('After upload')
}

function fileListUpdate(fileList: UploadFileInfo[]) {
  fileListRef.value = fileList
  // console.log(fileList)
  // console.log(`FileListUpdate ${fileListRef.value.length}`)
}
</script>

<template>
  <n-card title="Upload your photos">
    <n-upload
      accept="image/jpg"
      :multiple="true"
      :action="api.uploadUrl"
      list-type="image-card"
      :default-upload="true"
      @preview="handlePreview"
      @before-upload="beforeUpload"
      @finish="afterUpload"
      @update-file-list="fileListUpdate"
    />
    <n-modal v-model:show="showModalRef" preset="card" style="width: 600px" title="">
      <img :src="previewImageUrlRef" style="width: 100%" />
    </n-modal>
  </n-card>
</template>
