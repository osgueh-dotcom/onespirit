<template>
  <div class="glass-panel p-6 bg-charcoal-800 border border-charcoal-700 rounded-3xl flex flex-col md:flex-row items-center justify-between gap-6 select-none">
    <div class="space-y-2 text-center md:text-left flex-1">
      <h4 class="text-xs font-bold uppercase tracking-widest text-brand-orange">Annual Confirmed collections vs Target 2025</h4>
      <p class="text-base text-white font-black">
        Target goal of <span class="text-brand-emerald">Rp 9,200,000,000</span> set by One Spirit Asia executives.
      </p>
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-2">
        <div class="p-3 bg-charcoal-900/60 border border-charcoal-800 rounded-xl">
          <span class="text-[9px] uppercase tracking-wider text-charcoal-400 block font-bold">Confirmed Cash</span>
          <span class="text-sm font-black text-brand-emerald">{{ formatMoney(confirmedRevenue) }}</span>
        </div>
        <div class="p-3 bg-charcoal-900/60 border border-charcoal-800 rounded-xl">
          <span class="text-[9px] uppercase tracking-wider text-charcoal-400 block font-bold">Potential Pipeline</span>
          <span class="text-sm font-black text-white">{{ formatMoney(potentialRevenue) }}</span>
        </div>
        <div class="p-3 bg-charcoal-900/60 border border-charcoal-800 rounded-xl">
          <span class="text-[9px] uppercase tracking-wider text-charcoal-400 block font-bold">Conversion Rate</span>
          <span class="text-sm font-black text-sky-400">{{ conversionRate.toFixed(1) }}%</span>
        </div>
      </div>
    </div>
    
    <div class="flex flex-col items-center gap-1 shrink-0 select-none">
      <div class="relative w-24 h-24 flex items-center justify-center">
        <svg class="w-full h-full transform -rotate-90">
          <circle cx="48" cy="48" r="40" stroke="rgba(255,255,255,0.05)" stroke-width="8" fill="transparent" />
          <circle 
            cx="48" 
            cy="48" 
            r="40" 
            stroke="#FF6B00" 
            stroke-width="8" 
            fill="transparent" 
            :stroke-dasharray="251.2"
            :stroke-dashoffset="calculateDashoffset(confirmedRevenue, 9200000000)"
            class="transition-all duration-500 ease-out"
          />
        </svg>
        <span class="absolute text-sm font-black text-white">
          {{ calculatePercentage(confirmedRevenue, 9200000000) }}%
        </span>
      </div>
      <span class="text-[9px] uppercase font-black text-charcoal-400 mt-1">Target Achievement</span>
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
  }
})

const confirmedRevenue = computed(() => props.executive.confirmed_revenue || 0.0)
const potentialRevenue = computed(() => props.executive.potential_revenue || 0.0)
const conversionRate = computed(() => props.executive.revenue_conversion_rate || 0.0)

const formatMoney = (val) => {
  if (val >= 1e9) {
    return 'Rp ' + (val / 1e9).toFixed(2) + ' B'
  }
  if (val >= 1e6) {
    return 'Rp ' + (val / 1e6).toFixed(1) + ' M'
  }
  return 'Rp ' + Number(val || 0).toLocaleString('id-ID')
}

const calculatePercentage = (part, total) => {
  if (!total || total <= 0) return 0
  return Math.min(100, Math.round((part / total) * 100))
}

const calculateDashoffset = (received, target) => {
  const percentage = received / target
  const dasharray = 251.2
  if (percentage >= 1) return 0
  return dasharray - (percentage * dasharray)
}
</script>

<style scoped>
.glass-panel {
  background: rgba(26, 32, 44, 0.7);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}
</style>
