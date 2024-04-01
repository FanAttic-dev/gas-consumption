<script setup lang="ts">
import {
  NUpload,
  NCard,
  NFlex,
  NScrollbar,
  NModal,
  NButton,
  type UploadFileInfo,
  type FormInst,
  useMessage,
  type MessageReactive,
  type UploadInst
} from 'naive-ui'

import { useUploadStore } from '@/stores/upload'
import { computed, ref } from 'vue'
import * as api from '@/api/api'

const showModalRef = ref(false)
const previewImageUrlRef = ref('')
const uploadRef = ref<UploadInst | null>(null)
const fileListRef = ref<UploadFileInfo[]>([])
const fileListCount = computed(() => fileListRef.value.length)
const isEmpty = computed(() => fileListCount.value == 0)

const message = useMessage()
const uploadStore = useUploadStore()

let uploadMessage: MessageReactive | null = null

function handlePreview(file: UploadFileInfo) {
  const { name } = file
  previewImageUrlRef.value = `${api.BASE_URL}/static/uploads/${name}`
  showModalRef.value = true
}

function fileListUpdate(fileList: UploadFileInfo[]) {
  fileListRef.value = fileList

  const allUploaded = fileList.every((file) => file.status == 'finished')
  uploadStore.setUploadFinished(allUploaded)

  if (allUploaded) {
    uploadMessage?.destroy()
    uploadMessage = null
    message.success('All files uploaded')
    console.log('All files uploaded')
  }
}

function submit() {
  if (uploadMessage == null) {
    uploadMessage = message.loading('Uploading...', { duration: 0 })
  }
  setTimeout(() => uploadRef.value?.submit(), 500)
}
</script>

<template>
  <n-card title="1. Upload your images">
    <n-flex>
      <n-scrollbar style="max-height: 50vh">
        <n-upload
          ref="uploadRef"
          accept="image/jpg"
          :multiple="true"
          :action="api.uploadUrl"
          :default-upload="false"
          :show-preview-button="true"
          @preview="handlePreview"
          @update-file-list="fileListUpdate"
          ><n-button v-show="!uploadStore.uploadFinished">Select images</n-button></n-upload
        >
      </n-scrollbar>
      <n-button
        v-show="!uploadStore.uploadFinished"
        type="primary"
        :disabled="isEmpty"
        @click="submit"
        >Upload {{ fileListCount }} images</n-button
      >
    </n-flex>
    <n-modal v-model:show="showModalRef" preset="card" style="width: 600px" title="">
      <img :src="previewImageUrlRef" style="width: 100%" />
    </n-modal>
  </n-card>
</template>
