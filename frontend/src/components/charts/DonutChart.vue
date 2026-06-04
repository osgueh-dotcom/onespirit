<template>
  <div class="flex flex-col sm:flex-row items-center justify-between gap-6 p-6 bg-charcoal-800 rounded-xl border border-charcoal-700 shadow-xl">
    <!-- SVG Ring -->
    <div class="relative w-44 h-44 flex items-center justify-center flex-shrink-0">
      <svg class="w-full h-full transform -rotate-90" viewBox="0 0 200 200">
        <!-- Background circle -->
        <circle
          cx="100"
          cy="100"
          r="70"
          fill="transparent"
          stroke="#1e293b"
          stroke-width="16"
        />
        <!-- Segments -->
        <circle
          v-for="(seg, idx) in segments"
          :key="idx"
          cx="100"
          cy="100"
          r="70"
          fill="transparent"
          :stroke="seg.color"
          stroke-width="16"
          :stroke-dasharray="circumference"
          :stroke-dashoffset="seg.offset"
          stroke-linecap="round"
          class="transition-all duration-500 ease-out cursor-pointer hover:stroke-[20px]"
          @mouseenter="hoveredIndex = idx"
          @mouseleave="hoveredIndex = null"
        />
      </svg>
      <!-- Central Counter -->
      <div class="absolute flex flex-col items-center justify-center text-center">
        <span class="text-[10px] uppercase tracking-wider text-charcoal-400 font-bold">Total</span>
        <span class="text-3xl font-extrabold text-white transition-all duration-300">
          {{ hoveredIndex !== null ? segments[hoveredIndex].count : total }}
        </span>
        <span class="text-[11px] text-charcoal-300 font-semibold truncate max-w-[110px] capitalize">
          {{ hoveredIndex !== null ? segments[hoveredIndex].label : 'Projects' }}
        </span>
      </div>
    </div>

    <!-- Legend -->
    <div class="flex-1 w-full flex flex-col gap-2 max-h-48 overflow-y-auto custom-scrollbar">
      <div 
        v-for="(seg, idx) in segments" 
        :key="idx"
        class="flex items-center justify-between text-xs py-1.5 px-2 rounded-lg transition-colors duration-200 cursor-pointer"
        :class="hoveredIndex === idx ? 'bg-charcoal-700/60' : 'hover:bg-charcoal-700/30'"
        @mouseenter="hoveredIndex = idx"
        @mouseleave="hoveredIndex = null"
      >
        <div class="flex items-center gap-2">
          <span class="w-2.5 h-2.5 rounded-full flex-shrink-0" :style="{ backgroundColor: seg.color }"></span>
          <span class="font-medium capitalize text-charcoal-200">{{ seg.label }}</span>
        </div>
        <div class="flex items-center gap-3 font-semibold text-white">
          <span>{{ seg.count }}</span>
          <span class="text-[10px] text-charcoal-400">({{ seg.percentage }}%)</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  data: {
    type: Object,
    required: true,
    default: () => ({})
  }
})

const hoveredIndex = ref(null)
const circumference = 2 * Math.PI * 70 // ~439.82

const colors = {
  inquiry: '#ff9f1c',      // Energizing Orange
  quotation: '#707070',    // Slate Charcoal
  negotiation: '#3a86c8',  // Corporate Blue
  confirmed: '#2ec4b6',    // Bright Teal/Green
  preparation: '#00b4d8',  // Cyan Wave
  ongoing: '#a855f7',      // Royal Purple
  completed: '#10b981',    // Emerald Green
  canceled: '#ef233c'      // Rose Red
}

const total = computed(() => {
  return Object.values(props.data).reduce((acc, val) => acc + val, 0)
})

const segments = computed(() => {
  let accumulatedPercent = 0
  const keys = Object.keys(props.data).filter(k => props.data[k] > 0 || k === 'inquiry' || k === 'confirmed')
  
  return keys.map(key => {
    const count = props.data[key] || 0
    const pct = total.value > 0 ? (count / total.value) * 100 : 0
    const offset = circumference - (accumulatedPercent / 100) * circumference
    accumulatedPercent += pct
    return {
      label: key,
      count,
      percentage: pct.toFixed(1),
      offset,
      color: colors[key] || '#64748b'
    }
  })
})
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 2px;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 2px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.4);
}
</style>
