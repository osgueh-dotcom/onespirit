<template>
  <div class="glass-panel p-5 bg-charcoal-800 border border-charcoal-700 rounded-2xl flex flex-col justify-between select-none min-h-[320px]">
    <div>
      <h3 class="text-xs font-extrabold uppercase tracking-widest text-brand-orange">
        Perbandingan Pendapatan
      </h3>
      <p class="text-[10px] font-bold text-charcoal-400 mt-1 select-none">
        Membandingkan potensi pipeline dengan revenueaktual dan target tahunan.
      </p>
    </div>

    <div class="flex-1 flex flex-col justify-center gap-4 mt-6">
      <!-- 1. Potential Pipeline -->
      <div class="space-y-1.5">
        <div class="flex items-center justify-between text-xs font-extrabold">
          <span class="text-white">Estimasi Pipeline</span>
          <span class="text-sky-400">{{ formatMoney(potentialRevenue) }}</span>
        </div>
        <div class="h-4 w-full bg-brand-charcoal-light/30 rounded-lg overflow-hidden border border-brand-charcoal-light/10 relative">
          <div 
            class="h-full bg-gradient-to-r from-sky-500/30 to-sky-400 rounded-lg transition-all duration-1000" 
            :style="{ width: calculatePercent(potentialRevenue) + '%' }"
          ></div>
        </div>
      </div>

      <!-- 2. Confirmed Revenue -->
      <div class="space-y-1.5">
        <div class="flex items-center justify-between text-xs font-extrabold">
          <span class="text-white">Revenue Terkonfirmasi</span>
          <span class="text-brand-emerald">{{ formatMoney(confirmedRevenue) }}</span>
        </div>
        <div class="h-4 w-full bg-brand-charcoal-light/30 rounded-lg overflow-hidden border border-brand-charcoal-light/10 relative">
          <div 
            class="h-full bg-gradient-to-r from-brand-emerald/30 to-brand-emerald rounded-lg transition-all duration-1000" 
            :style="{ width: calculatePercent(confirmedRevenue) + '%' }"
          ></div>
        </div>
      </div>

      <!-- 3. Target Revenue -->
      <div class="space-y-1.5">
        <div class="flex items-center justify-between text-xs font-extrabold">
          <span class="text-white">Target Revenue (2025)</span>
          <span class="text-brand-orange">{{ formatMoney(targetRevenue) }}</span>
        </div>
        <div class="h-4 w-full bg-brand-charcoal-light/30 rounded-lg overflow-hidden border border-brand-charcoal-light/10 relative">
          <div 
            class="h-full bg-gradient-to-r from-brand-orange/30 to-brand-orange rounded-lg transition-all duration-1000" 
            :style="{ width: calculatePercent(targetRevenue) + '%' }"
          ></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  potentialRevenue: {
    type: Number,
    default: 0.0
  },
  confirmedRevenue: {
    type: Number,
    default: 0.0
  },
  targetRevenue: {
    type: Number,
    default: 9200000000.0 // Default Rp 9.2B
  }
})

const maxRevenue = computed(() => {
  const max = Math.max(props.potentialRevenue, props.confirmedRevenue, props.targetRevenue)
  return max > 0 ? max : 1.0
})

const calculatePercent = (val) => {
  return Math.max(1, (val / maxRevenue.value) * 100)
}

const formatMoney = (val) => {
  if (val === undefined || val === null || isNaN(val)) return 'Rp0'
  return 'Rp' + Math.round(val).toLocaleString('id-ID')
}
</script>
