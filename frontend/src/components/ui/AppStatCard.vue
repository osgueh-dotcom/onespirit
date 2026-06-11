<template>
  <div class="interactive-card p-5 relative overflow-hidden border print:bg-white print:border print:border-charcoal-200 print:rounded-xl" :class="[borderClass, bgClass]">
    <div class="absolute -top-10 -right-10 w-24 h-24 rounded-full blur-2xl opacity-10 print:hidden" :class="circleBgClass"></div>

    <p class="text-[10px] font-extrabold uppercase tracking-[0.16em] mb-2 print:text-charcoal-500" :class="mutedTextClass">
      {{ title }}
    </p>

    <h3 class="text-2xl md:text-3xl font-black text-main-theme font-sans tracking-tight print:text-charcoal-900" :class="valueTextClass">
      {{ value }}
    </h3>

    <div class="mt-3 flex flex-wrap items-center gap-1.5">
      <span v-if="badgeText" class="inline-flex text-[10px] font-bold px-2.5 py-1 rounded-lg border" :class="badgeClass">
        {{ badgeText }}
      </span>
      <span v-if="subtitle" class="text-[10px] font-bold" :class="mutedTextClass">
        {{ subtitle }}
      </span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  title: { type: String, required: true },
  value: { type: [String, Number], required: true },
  subtitle: { type: String, default: '' },
  badgeText: { type: String, default: '' },
  theme: {
    type: String,
    default: 'neutral',
    validator: (value) => ['orange', 'emerald', 'blue', 'amber', 'red', 'neutral', 'purple'].includes(value)
  }
})

const borderClass = computed(() => {
  if (props.theme === 'orange') return 'border-brand-orange/20 border-t-2 border-t-brand-orange'
  if (props.theme === 'emerald') return 'border-brand-emerald/20 border-t-2 border-t-brand-emerald'
  if (props.theme === 'blue') return 'border-brand-blue/20 border-t-2 border-t-brand-blue'
  if (props.theme === 'amber') return 'border-brand-amber/20 border-t-2 border-t-brand-amber'
  if (props.theme === 'red') return 'border-red-500/20 border-t-2 border-t-red-500'
  if (props.theme === 'purple') return 'border-purple-500/20 border-t-2 border-t-purple-500'
  return 'border-panel-theme border-t-2 border-t-slate-300'
})

const bgClass = computed(() => {
  if (props.theme === 'red') return 'bg-red-500/5'
  if (props.theme === 'amber') return 'bg-brand-amber/5'
  return ''
})

const circleBgClass = computed(() => {
  if (props.theme === 'orange') return 'bg-brand-orange'
  if (props.theme === 'emerald') return 'bg-brand-emerald'
  if (props.theme === 'blue') return 'bg-brand-blue'
  if (props.theme === 'amber') return 'bg-brand-amber'
  if (props.theme === 'red') return 'bg-red-500'
  if (props.theme === 'purple') return 'bg-purple-500'
  return 'bg-slate-500'
})

const valueTextClass = computed(() => {
  if (props.theme === 'emerald') return 'text-brand-emerald'
  if (props.theme === 'blue') return 'text-brand-blue'
  if (props.theme === 'orange') return 'text-brand-orange'
  if (props.theme === 'amber') return 'text-brand-amber'
  if (props.theme === 'red') return 'text-red-500'
  if (props.theme === 'purple') return 'text-purple-500'
  return 'text-main-theme'
})

const mutedTextClass = computed(() => 'text-muted-theme')

const badgeClass = computed(() => {
  if (props.theme === 'orange') return 'bg-brand-orange/10 text-brand-orange border-brand-orange/20'
  if (props.theme === 'emerald') return 'bg-brand-emerald/10 text-brand-emerald border-brand-emerald/20'
  if (props.theme === 'blue') return 'bg-brand-blue/10 text-brand-blue border-brand-blue/20'
  if (props.theme === 'amber') return 'bg-brand-amber/10 text-brand-amber border-brand-amber/20'
  if (props.theme === 'red') return 'bg-red-500/10 text-red-500 border-red-500/20'
  if (props.theme === 'purple') return 'bg-purple-500/10 text-purple-500 border-purple-500/20'
  return 'bg-slate-500/10 text-muted-theme border-slate-400/20'
})
</script>
