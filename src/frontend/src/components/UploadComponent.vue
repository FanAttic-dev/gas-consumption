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
import { computed, onMounted, ref } from 'vue'
import * as api from '@/api/api'
import { useUserStore } from '@/stores/user'
import router from '@/router'

const showModalRef = ref(false)
const previewImageUrlRef = ref('')
const uploadRef = ref<UploadInst | null>(null)

const message = useMessage()
const uploadStore = useUploadStore()
const userStore = useUserStore()

let uploadMessage: MessageReactive | null = null

async function clearImages() {
  await api.clearImages()
  await fetchImages()
  message.success('All files cleared')
}

async function handlePreview(file: UploadFileInfo) {
  const { name } = file
  const res = await api.getImage(name)
  previewImageUrlRef.value = `${api.BASE_URL}/${res.data}`
  showModalRef.value = true
}

function fileListUpdate(fileList: UploadFileInfo[]) {
  uploadStore.fileList = fileList
  // uploadStore.updateItemCount(fileList.length)
  console.log('file list update')
  console.log(fileList.length)

  const allUploaded = fileList.every((file) => file.status == 'finished')
  uploadStore.setUploadFinished(allUploaded)

  if (allUploaded) {
    uploadMessage?.destroy()
    uploadMessage = null
    message.success('All files uploaded')
    console.log('All files uploaded')
  }
}

async function fetchImages() {
  const res = await api.getAllImages()
  console.log(res.data)
  uploadStore.fileList = res.data.map((name: string, idx: number) => {
    return {
      id: name,
      name: name,
      status: 'finished'
    }
  })
}

onMounted(async () => {
  await fetchImages()
})
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
          :file-list="uploadStore.fileList"
          :headers="{
            Authorization: `Bearer ${userStore.user.token}`
          }"
          :show-preview-button="true"
          :show-remove-button="false"
          @preview="handlePreview"
          @update-file-list="fileListUpdate"
          ><n-button>Select images</n-button></n-upload
        >
      </n-scrollbar>
    </n-flex>
    <div style="width: 100; display: flex; justify-content: end">
      <n-button @click="clearImages" type="error">Clear images</n-button>
    </div>
    <n-modal v-model:show="showModalRef" preset="card" style="width: 600px" title="">
      <img :src="previewImageUrlRef" style="width: 100%" />
    </n-modal>
  </n-card>
</template>
