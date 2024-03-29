<script setup lang="ts">
import HomeView from '@/views/HomeView.vue'
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <!-- <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
      </nav> -->
  </header>

  <RouterView />
</template>
