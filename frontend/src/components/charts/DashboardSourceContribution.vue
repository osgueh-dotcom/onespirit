<template>
  <div class="glass-panel p-5 bg-charcoal-800 border border-charcoal-700 rounded-2xl flex flex-col justify-between select-none min-h-[320px]">
    <div>
      <h3 class="text-xs font-extrabold uppercase tracking-widest text-brand-orange">
        Kontribusi Source
      </h3>
      <p class="text-[10px] font-bold text-charcoal-400 mt-1 select-none">
        Menampilkan kontribusi revenue dari berbagai sumber referensi proyek.
      </p>
    </div>

    <div v-if="items.length === 0" class="flex-1 flex flex-col items-center justify-center py-6 text-center">
      <svg class="w-12 h-12 text-charcoal-500 mb-2" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 13.5h3.86a2.25 2.25 0 012.008 1.24l.885 1.77a2.25 2.25 0 002.007 1.24h1.98a2.25 2.25 0 002.007-1.24l.885-1.77a2.25 2.25 0 012.007-1.24h3.86m-18 0h18" />
      </svg>
      <span class="text-xs font-bold text-charcoal-400">Data source belum cukup untuk divisualisasikan.</span>
    </div>

    <div v-else class="flex-1 space-y-3 mt-4 overflow-y-auto max-h-[200px] pr-1">
      <div v-for="item in items" :key="item.source_type" class="space-y-1">
        <div class="flex items-center justify-between text-[11px] font-extrabold">
          <span class="text-white">{{ item.source_type || 'Unknown' }}</span>
          <span class="text-brand-emerald font-mono">{{ formatMoney(item.confirmed_revenue) }} ({{ item.deal_count }} Deal)</span>
        </div>
        <div class="h-2 w-full bg-brand-charcoal-light/20 rounded-md overflow-hidden relative border border-brand-charcoal-light/5">
          <div 
            class="h-full bg-brand-blue rounded-md transition-all duration-700" 
            :style="{ width: item.sharePercent + '%' }"
          ></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  sourceAnalytics: {
    type: Array,
    default: () => []
  }
})

const totalConfirmedRevenue = computed(() => {
  return props.sourceAnalytics.reduce((sum, item) => sum + (item.confirmed_revenue || 0), 0)
})

const items = computed(() => {
  const maxRev = Math.max(1, totalConfirmedRevenue.value)
  const list = props.sourceAnalytics.map(item => {
    const rev = item.confirmed_revenue || 0
    return {
      ...item,
      sharePercent: (rev / maxRev) * 100
    }
  })
  
  // Filter out zero revenue sources and sort by confirmed revenue descending
  return list.filter(i => i.confirmed_revenue > 0).sort((a, b) => b.confirmed_revenue - a.confirmed_revenue)
})

const formatMoney = (val) => {
  if (val === undefined || val === null || isNaN(val)) return 'Rp0'
  return 'Rp' + Math.round(val).toLocaleString('id-ID')
}
</script>
