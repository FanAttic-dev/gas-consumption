<script setup lang="ts">
import {
  NButton,
  NLayout,
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
  type UploadFileInfo,
  type FormInst
} from 'naive-ui'

import { ArchiveOutline as ArchiveIcon } from '@vicons/ionicons5'

import { ref } from 'vue'

const showModalRef = ref(false)
const previewImageUrlRef = ref('')
const formRef = ref<FormInst | null>(null)
const fileListRef = ref<UploadFileInfo[]>([])

function handlePreview(file: UploadFileInfo) {
  const { url } = file
  previewImageUrlRef.value = url as string
  showModalRef.value = true
}

function beforeUpload(options: { file: UploadFileInfo; fileList: Array<UploadFileInfo> }) {
  console.log(`Before Upload`)
  // console.log(options.file)
  return true
}

function fileListUpdate(fileList: UploadFileInfo[]) {
  fileListRef.value = fileList
  console.log(fileList)
  console.log(`FileListUpdate ${fileListRef.value.length}`)
}

function handleSubmit(e: MouseEvent) {
  e.preventDefault()
  console.log(`Submit ${fileListRef.value.length} items`)
  // TODO: submit
}
</script>

<template>
  <main>
    <n-card title="Upload your photos">
      <n-form method="POST" enctype="multipart/form-data" ref="formRef">
        <n-form-item>
          <n-upload
            accept="image/*"
            :multiple="true"
            :max="50"
            list-type="image-card"
            @preview="handlePreview"
            @before-upload="beforeUpload"
            @update-file-list="fileListUpdate"
          />
          <n-modal v-model:show="showModalRef" preset="card" style="width: 600px" title="">
            <img :src="previewImageUrlRef" style="width: 100%" />
          </n-modal>
        </n-form-item>
        <div style="display: flex; justify-content: flex-end">
          <n-button @click="handleSubmit" round type="primary">Submit</n-button>
        </div>
      </n-form>
    </n-card>
  </main>
</template>

<style>
.n-upload-trigger.n-upload-trigger--image-card .n-upload-dragger {
  padding: 24px;
}
</style>
