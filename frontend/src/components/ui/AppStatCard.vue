<template>
  <div 
    class="interactive-card p-5 relative overflow-hidden bg-charcoal-800 border rounded-2xl print:bg-white print:border print:border-charcoal-200 print:rounded-xl"
    :class="[
      borderClass,
      bgClass
    ]"
  >
    <div class="absolute -top-10 -right-10 w-24 h-24 rounded-full blur-2xl opacity-10 print:hidden" :class="circleBgClass"></div>
    
    <p class="text-[9px] font-extrabold uppercase tracking-widest text-gray-400 mb-1 print:text-charcoal-500" :class="mutedTextClass">
      {{ title }}
    </p>
    
    <h3 class="text-3xl font-black text-white font-sans mt-0.5 print:text-charcoal-900" :class="valueTextClass">
      {{ value }}
    </h3>
    
    <div class="mt-3 flex items-center gap-1.5">
      <span 
        v-if="badgeText"
        class="inline-flex text-[10px] font-bold px-2 py-0.5 rounded-lg border"
        :class="badgeClass"
      >
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
    validator: (v) => ['orange', 'emerald', 'blue', 'amber', 'red', 'neutral', 'purple'].includes(v)
  }
})

const borderClass = computed(() => {
  if (props.theme === 'orange') return 'border-brand-orange/20 border-l-4 border-l-brand-orange'
  if (props.theme === 'emerald') return 'border-brand-emerald/20 border-l-4 border-l-brand-emerald'
  if (props.theme === 'blue') return 'border-brand-blue/20 border-l-4 border-l-brand-blue'
  if (props.theme === 'amber') return 'border-yellow-500/20 border-l-4 border-l-yellow-500'
  if (props.theme === 'red') return 'border-red-500/20 border-l-4 border-l-red-500'
  if (props.theme === 'purple') return 'border-purple-500/20 border-l-4 border-l-purple-500'
  return 'border-brand-charcoal-light/30 border-l-4 border-l-gray-400'
})

const bgClass = computed(() => {
  if (props.theme === 'red') return 'bg-red-500/5'
  if (props.theme === 'amber') return 'bg-yellow-500/5'
  return 'bg-brand-charcoal/40'
})

const circleBgClass = computed(() => {
  if (props.theme === 'orange') return 'bg-brand-orange'
  if (props.theme === 'emerald') return 'bg-brand-emerald'
  if (props.theme === 'blue') return 'bg-brand-blue'
  if (props.theme === 'amber') return 'bg-yellow-500'
  if (props.theme === 'red') return 'bg-red-500'
  if (props.theme === 'purple') return 'bg-purple-500'
  return 'bg-gray-500'
})

const valueTextClass = computed(() => {
  if (props.theme === 'emerald') return 'text-brand-emerald'
  if (props.theme === 'blue') return 'text-brand-blue'
  if (props.theme === 'orange') return 'text-brand-orange'
  if (props.theme === 'amber') return 'text-yellow-500'
  if (props.theme === 'red') return 'text-red-400'
  if (props.theme === 'purple') return 'text-purple-400'
  return 'text-white'
})

const mutedTextClass = computed(() => {
  return 'text-gray-400 light:text-gray-600'
})

const badgeClass = computed(() => {
  if (props.theme === 'orange') return 'bg-brand-orange/10 text-brand-orange border-brand-orange/20'
  if (props.theme === 'emerald') return 'bg-brand-emerald/10 text-brand-emerald border-brand-emerald/20'
  if (props.theme === 'blue') return 'bg-brand-blue/10 text-brand-blue border-brand-blue/20'
  if (props.theme === 'amber') return 'bg-yellow-500/10 text-yellow-500 border-yellow-500/20'
  if (props.theme === 'red') return 'bg-red-500/10 text-red-400 border-red-500/20'
  if (props.theme === 'purple') return 'bg-purple-500/10 text-purple-400 border-purple-500/20'
  return 'bg-brand-charcoal-light/10 text-gray-400 border-brand-charcoal-light/20'
})
</script>
