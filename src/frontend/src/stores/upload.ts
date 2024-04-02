import { defineStore } from 'pinia'

export const useUploadStore = defineStore('upload', {
  state: () => {
    return {
      uploadFinished: false
    }
  },
  actions: {
    setUploadFinished(status: boolean) {
      this.uploadFinished = status
    }
  }
})
