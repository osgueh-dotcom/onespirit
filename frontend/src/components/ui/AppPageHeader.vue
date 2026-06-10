<template>
  <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-2 select-none">
    <div>
      <h2 class="text-xl font-bold text-white tracking-wide light:text-gray-900">{{ title }}</h2>
      <p v-if="subtitle" class="text-xs text-gray-400 mt-1 light:text-gray-600">
        {{ subtitle }}
      </p>
    </div>
    <div class="flex items-center gap-2">
      <slot name="actions"></slot>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true
  },
  subtitle: {
    type: String,
    default: ''
  }
})
</script>
