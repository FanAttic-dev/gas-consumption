<script setup lang="ts">
import HomeView from '@/views/HomeView.vue'
import { RouterLink, RouterView } from 'vue-router'
import { NMessageProvider } from 'naive-ui'
</script>

<template>
  <header>
    <!-- <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
      </nav> -->
  </header>
  <n-message-provider>
    <RouterView />
  </n-message-provider>
</template>
