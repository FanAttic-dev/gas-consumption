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

import { ref } from 'vue'

const showModalRef = ref(false)
const previewImageUrlRef = ref('')

function handlePreview(file: UploadFileInfo) {
  const { url } = file
  previewImageUrlRef.value = url as string
  showModalRef.value = true
}

const fileList = ref<UploadFileInfo[]>([
  {
    id: 'a',
    name: '我是上传出错的普通文件.png',
    status: 'error'
  },
  {
    id: 'b',
    name: '我是普通文本.doc',
    status: 'finished',
    type: 'text/plain'
  },
  {
    id: 'c',
    name: '我是自带url的图片.png',
    status: 'finished',
    url: 'https://07akioni.oss-cn-beijing.aliyuncs.com/07akioni.jpeg'
  },
  {
    id: 'd',
    name: '我是上传进度99%的文本.doc',
    status: 'uploading',
    percentage: 99
  }
])

const previewFileList = ref<UploadFileInfo[]>([
  {
    id: 'react',
    name: '我是react.png',
    status: 'finished',
    url: 'https://07akioni.oss-cn-beijing.aliyuncs.com/07akioni.jpeg'
  },
  {
    id: 'vue',
    name: '我是vue.png',
    status: 'finished',
    url: 'https://07akioni.oss-cn-beijing.aliyuncs.com/07akioni.jpeg'
  }
])
</script>

<template>
  <main>
    <n-card title="Upload your photos">
      <n-upload
        action="https://www.mocky.io/v2/5e4bafc63100007100d8b70f"
        :default-file-list="fileList"
        list-type="image-card"
      >
        Click to Upload
      </n-upload>
      <n-divider />
      <n-upload
        action="https://www.mocky.io/v2/5e4bafc63100007100d8b70f"
        :default-file-list="previewFileList"
        list-type="image-card"
        @preview="handlePreview"
      />
      <n-modal
        v-model:show="showModalRef"
        preset="card"
        style="width: 600px"
        title="A Cool Picture"
      >
        <img :src="previewImageUrlRef" style="width: 100%" />
      </n-modal>
    </n-card>
  </main>
</template>
