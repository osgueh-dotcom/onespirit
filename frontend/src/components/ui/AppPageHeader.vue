<template>
  <div class="flex flex-col md:flex-row md:items-end justify-between gap-4 select-none">
    <div>
      <p class="app-kicker">{{ eyebrow }}</p>
      <h2 class="mt-1.5 text-2xl font-black text-main-theme tracking-tight">{{ title }}</h2>
      <p v-if="subtitle" class="text-sm text-muted-theme mt-1.5 max-w-3xl leading-relaxed">
        {{ subtitle }}
      </p>
    </div>
    <div class="flex flex-wrap items-center gap-2">
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
  },
  eyebrow: {
    type: String,
    default: 'OneSpirit Workflow'
  }
})
</script>
