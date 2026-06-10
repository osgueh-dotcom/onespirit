<template>
  <div class="glass-panel p-5 bg-charcoal-800 border border-charcoal-700 rounded-2xl flex flex-col justify-between select-none min-h-[320px]">
    <div>
      <h3 class="text-xs font-extrabold uppercase tracking-widest text-brand-orange">
        Perbandingan Deal dan Cancel
      </h3>
      <p class="text-[10px] font-bold text-charcoal-400 mt-1 select-none">
        Membandingkan tingkat keberhasilan deal dan pembatalan proyek.
      </p>
    </div>

    <div class="flex-1 grid grid-cols-2 gap-4 mt-6 items-center">
      <!-- 1. Deal Rate Circular Gauge -->
      <div class="flex flex-col items-center text-center space-y-2">
        <div class="relative w-28 h-28 flex items-center justify-center">
          <svg class="w-full h-full transform -rotate-95" viewBox="0 0 100 100">
            <!-- Background track circle -->
            <circle 
              cx="50" cy="50" r="40" 
              fill="transparent" 
              class="stroke-brand-charcoal-light/30" 
              stroke-width="8"
            />
            <!-- Animated deal fill circle -->
            <circle 
              cx="50" cy="50" r="40" 
              fill="transparent" 
              class="stroke-brand-emerald" 
              stroke-width="8" 
              stroke-dasharray="251.2"
              :stroke-dashoffset="calculateOffset(dealRate)"
              stroke-linecap="round"
              style="transition: stroke-dashoffset 1.5s ease-in-out;"
            />
          </svg>
          <div class="absolute flex flex-col items-center justify-center">
            <span class="text-xl font-black text-brand-emerald">{{ formatPercent(dealRate) }}</span>
            <span class="text-[8px] uppercase tracking-wider font-extrabold text-charcoal-400">Deal Rate</span>
          </div>
        </div>
        <span class="text-[10px] font-bold text-white select-none">Tingkat Deal</span>
      </div>

      <!-- 2. Cancel Rate Circular Gauge -->
      <div class="flex flex-col items-center text-center space-y-2">
        <div class="relative w-28 h-28 flex items-center justify-center">
          <svg class="w-full h-full transform -rotate-95" viewBox="0 0 100 100">
            <!-- Background track circle -->
            <circle 
              cx="50" cy="50" r="40" 
              fill="transparent" 
              class="stroke-brand-charcoal-light/30" 
              stroke-width="8"
            />
            <!-- Animated cancel fill circle -->
            <circle 
              cx="50" cy="50" r="40" 
              fill="transparent" 
              class="stroke-red-500" 
              stroke-width="8" 
              stroke-dasharray="251.2"
              :stroke-dashoffset="calculateOffset(cancelRate)"
              stroke-linecap="round"
              style="transition: stroke-dashoffset 1.5s ease-in-out;"
            />
          </svg>
          <div class="absolute flex flex-col items-center justify-center">
            <span class="text-xl font-black text-red-400">{{ formatPercent(cancelRate) }}</span>
            <span class="text-[8px] uppercase tracking-wider font-extrabold text-charcoal-400">Cancel Rate</span>
          </div>
        </div>
        <span class="text-[10px] font-bold text-white select-none">Tingkat Cancel</span>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  dealRate: {
    type: Number,
    default: 0.0
  },
  cancelRate: {
    type: Number,
    default: 0.0
  }
})

// Circular circumference is 2 * pi * r = 2 * 3.14159 * 40 = 251.2
const calculateOffset = (rate) => {
  const boundedRate = Math.max(0, Math.min(100, rate))
  return 251.2 - (251.2 * boundedRate) / 100
}

const formatPercent = (val) => {
  if (val === undefined || val === null || isNaN(val)) return '0,0%'
  return Number(val).toFixed(1).replace('.', ',') + '%'
}
</script>
