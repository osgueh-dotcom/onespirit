<template>
  <div class="flex flex-col sm:flex-row items-center gap-6 p-6 bg-charcoal-800 rounded-xl border border-charcoal-700 shadow-xl w-full">
    <!-- SVG Vertical Funnel -->
    <div class="relative w-48 h-60 flex-shrink-0 flex items-center justify-center">
      <svg class="w-full h-full" viewBox="0 0 200 240">
        <!-- Define Gradients -->
        <defs>
          <linearGradient 
            v-for="(seg, idx) in funnelPolygons" 
            :key="'grad-' + idx"
            :id="'funnel-grad-' + idx" 
            x1="0%" y1="0%" x2="0%" y2="100%"
          >
            <stop offset="0%" :stop-color="seg.color" stop-opacity="0.9" />
            <stop offset="100%" :stop-color="seg.color" stop-opacity="0.6" />
          </linearGradient>
        </defs>

        <!-- Funnel Polygons -->
        <polygon
          v-for="(seg, idx) in funnelPolygons"
          :key="idx"
          :points="seg.points"
          :fill="`url(#funnel-grad-${idx})`"
          class="transition-all duration-300 ease-out cursor-pointer hover:filter hover:brightness-125"
          @mouseenter="hoveredIndex = idx"
          @mouseleave="hoveredIndex = null"
        />
      </svg>
    </div>

    <!-- Details and Conversion -->
    <div class="flex-1 w-full flex flex-col gap-4">
      <div 
        v-for="(seg, idx) in funnelPolygons" 
        :key="idx"
        class="flex flex-col gap-1 p-2 rounded-lg transition-colors duration-200 cursor-pointer"
        :class="hoveredIndex === idx ? 'bg-charcoal-700/60' : 'hover:bg-charcoal-700/30'"
        @mouseenter="hoveredIndex = idx"
        @mouseleave="hoveredIndex = null"
      >
        <div class="flex items-center justify-between text-xs font-semibold text-white">
          <div class="flex items-center gap-2">
            <span class="w-2.5 h-2.5 rounded-full flex-shrink-0" :style="{ backgroundColor: seg.color }"></span>
            <span class="text-charcoal-200">{{ seg.stage }}</span>
          </div>
          <span class="text-sm font-bold text-white">{{ seg.count }} Projects</span>
        </div>
        
        <!-- Conversion and Progress Bar -->
        <div class="flex items-center gap-3">
          <div class="flex-1 bg-charcoal-900 h-2.5 rounded-full overflow-hidden">
            <div 
              class="h-full rounded-full transition-all duration-700 ease-out" 
              :style="{ width: `${seg.percentage}%`, backgroundColor: seg.color }"
            ></div>
          </div>
          <span class="text-[11px] font-bold text-charcoal-300 w-12 text-right">
            {{ seg.percentage }}%
          </span>
        </div>
        
        <!-- Conversion loss indicator if applicable -->
        <span 
          v-if="idx > 0"
          class="text-[10px] text-charcoal-400 font-medium pl-4.5"
        >
          Conversion from {{ funnelPolygons[idx-1].stage }}: 
          <span class="text-emerald-400 font-semibold">
            {{ calculateSubConversion(seg.count, funnelPolygons[idx-1].count) }}%
          </span>
        </span>
      </div>
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

const colors = [
  '#ff9f1c', // Inquiry (Amber)
  '#ff7b00', // Quotation (Warm Orange)
  '#3a86c8', // Negotiation (Corp Blue)
  '#2ec4b6', // Confirmed (Teal)
  '#10b981'  // Completed (Emerald)
]

const funnelPolygons = computed(() => {
  if (!props.data || props.data.length === 0) return []

  const totalHeight = 240
  const stageCount = props.data.length
  const stageHeight = 40
  const gap = 8

  return props.data.map((item, idx) => {
    const percentage = item.percentage
    const nextItem = props.data[idx + 1]
    const nextPercentage = nextItem ? nextItem.percentage : percentage * 0.7

    // Vertical Coordinates
    const y1 = idx * (stageHeight + gap)
    const y2 = y1 + stageHeight

    // Width Calculations
    // Base width max 180, min 20 for taper aesthetics
    const w1 = Math.max(180 * (percentage / 100), 25)
    const w2 = Math.max(180 * (nextPercentage / 100), 20)

    // Center point is X=100
    const x1_left = 100 - w1 / 2
    const x1_right = 100 + w1 / 2
    const x2_left = 100 - w2 / 2
    const x2_right = 100 + w2 / 2

    // Polygon Points String
    const points = `${x1_left},${y1} ${x1_right},${y1} ${x2_right},${y2} ${x2_left},${y2}`

    return {
      stage: item.stage,
      count: item.count,
      percentage: item.percentage,
      points,
      color: colors[idx] || '#64748b'
    }
  })
})

const calculateSubConversion = (current, previous) => {
  if (!previous || previous === 0) return '0.0'
  return ((current / previous) * 100).toFixed(1)
}
</script>
