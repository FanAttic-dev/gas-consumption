<script setup lang="ts">
import {
  NButton,
  NLayout,
  NFlex,
  NLayoutHeader,
  NLayoutContent,
  NLayoutFooter,
  NUpload,
  NUploadDragger,
  NIcon,
  NCard,
  NDivider,
  NModal,
  NText,
  NForm,
  NFormItem,
  useMessage,
  type UploadFileInfo,
  type FormInst
} from 'naive-ui'

import { ArchiveOutline as ArchiveIcon } from '@vicons/ionicons5'

import { ref } from 'vue'
import * as api from '@/api/api'
import type { AxiosError } from 'axios'

const showModalRef = ref(false)
const previewImageUrlRef = ref('')
const formRef = ref<FormInst | null>(null)
const fileListRef = ref<UploadFileInfo[]>([])
const message = useMessage()

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

async function processImages() {
  try {
    await api.processImages()
  } catch (err) {
    message.error(err.response.data)
  }
}
</script>

<template>
  <main>
    <n-flex>
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

      <n-card>
        <n-button type="primary" @click="processImages">Process images</n-button>
      </n-card>
    </n-flex>
  </main>
</template>

<style>
.n-upload-trigger.n-upload-trigger--image-card .n-upload-dragger {
  padding: 24px;
}
</style>
