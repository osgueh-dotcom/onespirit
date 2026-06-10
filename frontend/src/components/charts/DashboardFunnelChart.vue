<template>
  <div class="glass-panel p-5 bg-charcoal-800 border border-charcoal-700 rounded-2xl flex flex-col justify-between select-none min-h-[320px]">
    <div>
      <h3 class="text-xs font-extrabold uppercase tracking-widest text-brand-orange">
        Flow Inquiry ke Deal
      </h3>
      <p class="text-[10px] font-bold text-charcoal-400 mt-1 select-none">
        Menunjukkan alur inquiry menjadi project deal dan pembatalan.
      </p>
    </div>

    <div v-if="totalInquiry === 0" class="flex-1 flex flex-col items-center justify-center py-6 text-center">
      <svg class="w-12 h-12 text-charcoal-500 mb-2" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
      </svg>
      <span class="text-xs font-bold text-charcoal-400">Belum ada data flow inquiry.</span>
    </div>

    <div v-else class="flex-1 flex flex-col justify-center gap-4 mt-6">
      <!-- Funnel Bar 1: Total Inquiry -->
      <div class="space-y-1.5">
        <div class="flex items-center justify-between text-xs font-extrabold">
          <span class="text-white">1. Total Inquiry</span>
          <span class="text-brand-blue">{{ totalInquiry }} Event (100%)</span>
        </div>
        <div class="h-6 w-full bg-brand-charcoal-light/30 rounded-xl overflow-hidden border border-brand-charcoal-light/10 relative">
          <div class="h-full bg-gradient-to-r from-brand-blue/30 to-brand-blue rounded-l-xl transition-all duration-1000" :style="{ width: '100%' }"></div>
        </div>
      </div>

      <!-- Funnel Bar 2: Project Deal -->
      <div class="space-y-1.5">
        <div class="flex items-center justify-between text-xs font-extrabold">
          <span class="text-white">2. Project Deal</span>
          <span class="text-brand-emerald">{{ totalDeal }} Event ({{ formatPercent(dealRate) }})</span>
        </div>
        <div class="h-6 w-full bg-brand-charcoal-light/30 rounded-xl overflow-hidden border border-brand-charcoal-light/10 relative">
          <div 
            class="h-full bg-gradient-to-r from-brand-emerald/30 to-brand-emerald rounded-l-xl transition-all duration-1000" 
            :style="{ width: dealRate + '%' }"
          ></div>
        </div>
      </div>

      <!-- Funnel Bar 3: Cancelled Projects -->
      <div class="space-y-1.5">
        <div class="flex items-center justify-between text-xs font-extrabold">
          <span class="text-white">3. Risiko Pembatalan (Cancelled)</span>
          <span class="text-red-400">{{ totalCancel }} Event ({{ formatPercent(cancelRate) }})</span>
        </div>
        <div class="h-6 w-full bg-brand-charcoal-light/30 rounded-xl overflow-hidden border border-brand-charcoal-light/10 relative">
          <div 
            class="h-full bg-gradient-to-r from-red-500/30 to-red-500 rounded-l-xl transition-all duration-1000" 
            :style="{ width: cancelRate + '%' }"
          ></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  totalInquiry: {
    type: Number,
    default: 0
  },
  totalDeal: {
    type: Number,
    default: 0
  },
  totalCancel: {
    type: Number,
    default: 0
  }
})

const dealRate = computed(() => {
  if (props.totalInquiry <= 0) return 0
  return Math.min(100, (props.totalDeal / props.totalInquiry) * 100)
})

const cancelRate = computed(() => {
  if (props.totalInquiry <= 0) return 0
  return Math.min(100, (props.totalCancel / props.totalInquiry) * 100)
})

const formatPercent = (val) => {
  if (val === undefined || val === null || isNaN(val)) return '0,0%'
  return val.toFixed(1).replace('.', ',') + '%'
}
</script>
