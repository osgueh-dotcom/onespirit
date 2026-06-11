<template>
  <section class="app-chart-card flex min-h-[320px] flex-col print:bg-white print:border print:border-slate-200 print:shadow-none">
    <header class="flex flex-col gap-1 border-b border-panel-theme pb-4">
      <div class="flex flex-wrap items-start justify-between gap-3">
        <div>
          <p class="app-kicker">{{ eyebrow }}</p>
          <h3 class="mt-1 text-base font-extrabold tracking-tight text-main-theme">{{ title }}</h3>
        </div>
        <slot name="metric"></slot>
      </div>
      <p v-if="subtitle" class="app-section-copy max-w-2xl">{{ subtitle }}</p>
    </header>

    <div class="flex flex-1 flex-col pt-5">
      <slot></slot>
    </div>
  </section>
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
    default: 'Visual Analytics'
  }
})
</script>
