<template>
  <div class="app-section-card p-8 md:p-10 text-center space-y-4 select-none print:text-charcoal-400">
    <div class="flex flex-col items-center justify-center gap-3">
      <!-- Simple Search/Document Folder Icon -->
      <svg class="w-12 h-12 text-gray-500" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 13.5h3.86a2.25 2.25 0 012.008 1.24l.885 1.77a2.25 2.25 0 002.007 1.24h1.98a2.25 2.25 0 002.007-1.24l.885-1.77a2.25 2.25 0 012.007-1.24h3.86m-18 0h18M2.25 13.5l1.626-5.69a2.25 2.25 0 012.163-1.61h11.922a2.25 2.25 0 012.163 1.61l1.627 5.69m-18 0v7.5A2.25 2.25 0 004.5 21h15a2.25 2.25 0 002.25-2.25v-7.5" />
      </svg>
      <h4 class="text-base font-extrabold text-main-theme">{{ title }}</h4>
      <p class="text-sm text-muted-theme font-medium max-w-md mx-auto leading-relaxed">
        {{ message }}
      </p>
    </div>
    <div v-if="$slots.actions" class="pt-2">
      <slot name="actions"></slot>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    default: 'Belum Ada Data'
  },
  message: {
    type: String,
    default: 'Data kosong atau tidak ditemukan untuk filter ini.'
  }
})
</script>
