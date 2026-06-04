<template>
  <div class="flex flex-col gap-4 p-6 bg-charcoal-800 rounded-xl border border-charcoal-700 shadow-xl w-full">
    <!-- Header / Stats -->
    <div class="flex items-center justify-between">
      <div class="flex flex-col">
        <span class="text-xs uppercase tracking-wider text-charcoal-400 font-bold">Revenue Trend</span>
        <span class="text-2xl font-extrabold text-white">
          {{ formatCurrency(totalRevenue) }}
        </span>
      </div>
      <div class="flex items-center gap-2">
        <span class="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
        <span class="text-xs text-emerald-400 font-semibold uppercase tracking-wider">6-Month Ledger</span>
      </div>
    </div>

    <!-- SVG Area Chart -->
    <div class="relative w-full h-48 mt-2">
      <svg class="w-full h-full overflow-visible" viewBox="0 0 500 180" preserveAspectRatio="none">
        <defs>
          <!-- Glowing Area Gradient -->
          <linearGradient id="areaGrad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#10b981" stop-opacity="0.45" />
            <stop offset="100%" stop-color="#10b981" stop-opacity="0.0" />
          </linearGradient>
          <!-- Line Stroke Gradient -->
          <linearGradient id="lineGrad" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stop-color="#34d399" />
            <stop offset="100%" stop-color="#10b981" />
          </linearGradient>
        </defs>

        <!-- Horizontal Grid Lines -->
        <line v-for="grid in gridLines" :key="grid" x1="0" :y1="grid" x2="500" :y2="grid" stroke="#2a3547" stroke-dasharray="4 4" stroke-width="1" />

        <!-- Filled Area Path -->
        <path :d="areaPath" fill="url(#areaGrad)" class="transition-all duration-500 ease-in-out" />

        <!-- Line Path -->
        <path :d="linePath" fill="transparent" stroke="url(#lineGrad)" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" class="transition-all duration-500 ease-in-out" />

        <!-- Interactive Points -->
        <g v-for="(pt, idx) in points" :key="idx" class="cursor-pointer group">
          <!-- Pulse Highlight on hover -->
          <circle 
            :cx="pt.x" 
            :cy="pt.y" 
            r="10" 
            fill="#10b981" 
            fill-opacity="0.15" 
            class="opacity-0 group-hover:opacity-100 transition-opacity duration-200" 
          />
          <!-- Core dot -->
          <circle 
            :cx="pt.x" 
            :cy="pt.y" 
            r="5" 
            :fill="hoveredIndex === idx ? '#34d399' : '#10b981'" 
            stroke="#1e293b" 
            stroke-width="1.5"
            class="transition-all duration-200"
            @mouseenter="hoveredIndex = idx"
            @mouseleave="hoveredIndex = null"
          />
        </g>
      </svg>

      <!-- Overlay Tooltip -->
      <div 
        v-if="hoveredIndex !== null" 
        class="absolute bg-charcoal-900 border border-charcoal-700 p-2.5 rounded-lg shadow-2xl text-xs text-white z-20 flex flex-col gap-0.5 pointer-events-none transition-all duration-200"
        :style="{ left: `${(points[hoveredIndex].x / 500) * 88}%`, top: `${Math.max(0, (points[hoveredIndex].y / 180) * 80 - 50)}px` }"
      >
        <span class="text-charcoal-400 font-bold uppercase tracking-wider">{{ data[hoveredIndex].month }}</span>
        <span class="font-extrabold text-emerald-400 text-sm">{{ formatCurrency(data[hoveredIndex].amount) }}</span>
      </div>
    </div>

    <!-- X-Axis Labels -->
    <div class="flex justify-between text-[10px] text-charcoal-400 font-bold uppercase tracking-widest px-2">
      <span v-for="item in data" :key="item.month">{{ item.month.split(' ')[0] }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  data: {
    type: Array,
    required: true,
    default: () => []
  }
})

const hoveredIndex = ref(null)

const maxAmount = computed(() => {
  if (!props.data || props.data.length === 0) return 1000
  const max = Math.max(...props.data.map(d => d.amount))
  return max === 0 ? 1000 : max * 1.15 // 15% padding
})

const totalRevenue = computed(() => {
  return props.data.reduce((acc, val) => acc + val.amount, 0)
})

const gridLines = computed(() => {
  // Return Y values for 3 gridlines
  return [45, 90, 135]
})

// Calculate SVG Points coordinates
const points = computed(() => {
  if (!props.data || props.data.length === 0) return []

  const totalPoints = props.data.length
  const stepX = 500 / (totalPoints - 1)
  const chartHeight = 180
  const topPadding = 15
  const bottomPadding = 15
  const usableHeight = chartHeight - topPadding - bottomPadding

  return props.data.map((item, idx) => {
    const x = idx * stepX
    // Scale amount to Y (where Y is inverted in SVG, 0 is top)
    const ratio = item.amount / maxAmount.value
    const y = chartHeight - bottomPadding - (ratio * usableHeight)
    return { x, y }
  })
})

// Compute the SVG line path string
const linePath = computed(() => {
  if (points.value.length === 0) return ''
  
  // Use cubic bezier control points for smooth curves
  let pathStr = `M ${points.value[0].x} ${points.value[0].y}`
  for (let i = 0; i < points.value.length - 1; i++) {
    const curr = points.value[i]
    const next = points.value[i + 1]
    
    // Control points halfway between nodes
    const cpX1 = curr.x + (next.x - curr.x) / 2
    const cpY1 = curr.y
    const cpX2 = curr.x + (next.x - curr.x) / 2
    const cpY2 = next.y
    
    pathStr += ` C ${cpX1} ${cpY1}, ${cpX2} ${cpY2}, ${next.x} ${next.y}`
  }
  return pathStr
})

// Compute the closed area path string
const areaPath = computed(() => {
  if (points.value.length === 0) return ''
  
  const lineP = linePath.value
  const lastPoint = points.value[points.value.length - 1]
  const firstPoint = points.value[0]
  
  // Close the path to the bottom edge of the SVG canvas (y=180)
  return `${lineP} L ${lastPoint.x} 180 L ${firstPoint.x} 180 Z`
})

const formatCurrency = (val) => {
  if (val >= 1e9) {
    return 'Rp ' + (val / 1e9).toFixed(2) + ' B'
  }
  if (val >= 1e6) {
    return 'Rp ' + (val / 1e6).toFixed(1) + ' M'
  }
  return 'Rp ' + val.toLocaleString('id-ID')
}
</script>
