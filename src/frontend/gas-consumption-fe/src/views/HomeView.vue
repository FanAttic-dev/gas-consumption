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
  type UploadFileInfo
} from 'naive-ui'

import { ArchiveOutline as ArchiveIcon } from '@vicons/ionicons5'

import { ref } from 'vue'

const showModalRef = ref(false)
const previewImageUrlRef = ref('')

function handlePreview(file: UploadFileInfo) {
  const { url } = file
  previewImageUrlRef.value = url as string
  showModalRef.value = true
}

function beforeUpload(options: { file: UploadFileInfo; fileList: Array<UploadFileInfo> }) {
  console.log(`Before Upload`)
  console.log(options.file)
  return true
}

function fileListUpdate(fileList: UploadFileInfo[]) {
  console.log(`FileListUpdate ${fileList.length}`)
}
</script>

<template>
  <main>
    <n-card title="Upload your photos">
      <n-upload
        accept="image/*"
        :multiple="true"
        :max="50"
        action=""
        list-type="image-card"
        @preview="handlePreview"
        @before-upload="beforeUpload"
        @update-file-list="fileListUpdate"
      />
      <n-modal v-model:show="showModalRef" preset="card" style="width: 600px" title="">
        <img :src="previewImageUrlRef" style="width: 100%" />
      </n-modal>
    </n-card>
  </main>
</template>

<style>
.n-upload-trigger.n-upload-trigger--image-card .n-upload-dragger {
  padding: 24px;
}
</style>
