<template>
  <div class="glass-panel p-6 bg-charcoal-800 border border-charcoal-700 rounded-3xl flex flex-col md:flex-row items-center justify-between gap-6 select-none print:bg-white print:border print:border-charcoal-200 print:rounded-xl print:p-5">
    <div class="space-y-2 text-center md:text-left flex-1 print:text-charcoal-900">
      <h4 class="text-xs font-bold uppercase tracking-widest text-brand-orange print:text-orange-700">Annual Confirmed collections vs Target {{ target.year }}</h4>
      <p class="text-base text-white font-black print:text-charcoal-800">
        Target goal of <span class="text-brand-emerald print:text-emerald-700">{{ formatMoney(target.revenue_target) }}</span> set by One Spirit Asia executives.
      </p>
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-2 print:grid-cols-3">
        <div class="p-3 bg-charcoal-900/60 border border-charcoal-800 rounded-xl print:bg-charcoal-50 print:border print:border-charcoal-200">
          <span class="text-[9px] uppercase tracking-wider text-charcoal-400 block font-bold print:text-charcoal-500">Confirmed Revenue</span>
          <span class="text-sm font-black text-brand-emerald print:text-emerald-700">{{ formatMoney(confirmedRevenue) }}</span>
        </div>
        <div class="p-3 bg-charcoal-900/60 border border-charcoal-800 rounded-xl print:bg-charcoal-50 print:border print:border-charcoal-200">
          <span class="text-[9px] uppercase tracking-wider text-charcoal-400 block font-bold print:text-charcoal-500">Potential Pipeline</span>
          <span class="text-sm font-black text-white print:text-charcoal-900">{{ formatMoney(potentialRevenue) }}</span>
        </div>
        <div class="p-3 bg-charcoal-900/60 border border-charcoal-800 rounded-xl print:bg-charcoal-50 print:border print:border-charcoal-200">
          <span class="text-[9px] uppercase tracking-wider text-charcoal-400 block font-bold print:text-charcoal-500">Conversion Rate</span>
          <span class="text-sm font-black text-sky-400 print:text-sky-700">{{ formatPercent(conversionRate) }}</span>
        </div>
      </div>
    </div>
    
    <div class="flex flex-col items-center gap-1 shrink-0 select-none print:text-charcoal-900">
      <div class="relative w-24 h-24 flex items-center justify-center">
        <svg class="w-full h-full transform -rotate-90">
          <circle cx="48" cy="48" r="40" stroke="rgba(255,255,255,0.05)" stroke-width="8" fill="transparent" class="print:stroke-charcoal-100" />
          <circle 
            cx="48" 
            cy="48" 
            r="40" 
            stroke="#FF6B00" 
            stroke-width="8" 
            fill="transparent" 
            :stroke-dasharray="251.2"
            :stroke-dashoffset="calculateDashoffset(confirmedRevenue, target.revenue_target)"
            class="transition-all duration-500 ease-out print:stroke-orange-600"
          />
        </svg>
        <span class="absolute text-sm font-black text-white print:text-charcoal-900">
          {{ formatPercent(calculatePercentage(confirmedRevenue, target.revenue_target)) }}
        </span>
      </div>
      <span class="text-[9px] uppercase font-black text-charcoal-400 mt-1 print:text-charcoal-500">Target Achievement</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  executive: {
    type: Object,
    required: true,
    default: () => ({
      potential_revenue: 0.0,
      confirmed_revenue: 0.0,
      revenue_conversion_rate: 0.0
    })
  },
  target: {
    type: Object,
    required: true,
    default: () => ({
      year: 2025,
      revenue_target: 9200000000.0,
      achievement_rate: 0.0
    })
  }
})

const confirmedRevenue = computed(() => props.executive.confirmed_revenue || 0.0)
const potentialRevenue = computed(() => props.executive.potential_revenue || 0.0)
const conversionRate = computed(() => props.executive.revenue_conversion_rate || 0.0)

const formatMoney = (val) => {
  if (val === undefined || val === null || isNaN(val)) return 'Rp0'
  return 'Rp' + Math.round(val).toLocaleString('id-ID')
}

const formatPercent = (val) => {
  if (val === undefined || val === null || isNaN(val)) return '0,0%'
  return Number(val).toFixed(2).replace('.', ',') + '%'
}

const calculatePercentage = (part, total) => {
  if (!total || total <= 0) return 0.0
  return Math.min(100.0, (part / total) * 100.0)
}

const calculateDashoffset = (received, targetValue) => {
  if (!targetValue || targetValue <= 0) return 251.2
  const percentage = received / targetValue
  const dasharray = 251.2
  if (percentage >= 1) return 0
  return dasharray - (percentage * dasharray)
}
</script>

<style scoped>
.glass-panel {
  background: rgba(26, 32, 44, 0.7);
  backdrop-filter: blur(12px);
}
</style>
