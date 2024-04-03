import { defineStore } from 'pinia'
import type { UploadFileInfo } from 'naive-ui'

export const useUploadStore = defineStore('upload', {
  state: () => {
    return {
      uploadFinished: false,
      fileList: [] as UploadFileInfo[]
    }
  },
  actions: {
    setUploadFinished(status: boolean) {
      this.uploadFinished = status
    }
  },
  getters: {
    enoughImagesUploaded: (state) => state.fileList.length > 20
  }
})
