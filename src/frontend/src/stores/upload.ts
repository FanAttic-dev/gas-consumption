import { defineStore } from 'pinia'
import type { UploadFileInfo } from 'naive-ui'

export const useUploadStore = defineStore('upload', {
  state: () => {
    return {
      uploadFinished: true,
      fileList: [] as UploadFileInfo[]
    }
  },
  actions: {
    setUploadFinished(status: boolean) {
      this.uploadFinished = status
    }
  },
  getters: {}
})
