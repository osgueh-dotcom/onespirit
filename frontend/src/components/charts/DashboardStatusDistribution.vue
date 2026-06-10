<template>
  <div class="glass-panel p-5 bg-charcoal-800 border border-charcoal-700 rounded-2xl flex flex-col justify-between select-none min-h-[320px]">
    <div>
      <h3 class="text-xs font-extrabold uppercase tracking-widest text-brand-orange">
        Komposisi Status Project
      </h3>
      <p class="text-[10px] font-bold text-charcoal-400 mt-1 select-none">
        Menampilkan persebaran status project saat ini.
      </p>
    </div>

    <div v-if="totalProjects === 0" class="flex-1 flex flex-col items-center justify-center py-6 text-center">
      <svg class="w-12 h-12 text-charcoal-500 mb-2" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
      </svg>
      <span class="text-xs font-bold text-charcoal-400">Belum ada data status project.</span>
    </div>

    <div v-else class="flex-1 space-y-2.5 mt-4 overflow-y-auto max-h-[200px] pr-1">
      <div v-for="item in statusItems" :key="item.statusKey" class="space-y-1">
        <div class="flex items-center justify-between text-[11px] font-extrabold">
          <span class="text-white">{{ item.label }}</span>
          <span class="text-charcoal-400 font-mono">{{ item.count }} ({{ formatPercent(item.percent) }})</span>
        </div>
        <div class="h-2 w-full bg-brand-charcoal-light/20 rounded-md overflow-hidden relative border border-brand-charcoal-light/5">
          <div 
            class="h-full bg-brand-orange rounded-md transition-all duration-700" 
            :style="{ width: item.percent + '%' }"
            :class="item.colorClass"
          ></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  statusCounts: {
    type: Object,
    default: () => ({})
  }
})

const statusLabels = {
  inquiry: { label: 'Inquiry', colorClass: 'bg-brand-blue' },
  quotation: { label: 'Penawaran', colorClass: 'bg-brand-blue-light' },
  negotiation: { label: 'Negosiasi', colorClass: 'bg-amber-500' },
  confirmed: { label: 'Terkonfirmasi (Confirmed)', colorClass: 'bg-brand-emerald-dark' },
  preparation: { label: 'Persiapan', colorClass: 'bg-brand-emerald' },
  ongoing: { label: 'Berjalan (Running)', colorClass: 'bg-brand-orange-light' },
  completed: { label: 'Selesai (Completed)', colorClass: 'bg-brand-emerald-light' },
  canceled: { label: 'Dibatalkan (Canceled)', colorClass: 'bg-red-500' },
  closed: { label: 'Ditutup (Closed)', colorClass: 'bg-charcoal-500' }
}

const totalProjects = computed(() => {
  return Object.values(props.statusCounts).reduce((a, b) => a + b, 0)
})

const statusItems = computed(() => {
  const list = []
  const max = totalProjects.value > 0 ? totalProjects.value : 1
  
  for (const [key, config] of Object.entries(statusLabels)) {
    const count = props.statusCounts[key] || 0
    if (count > 0) {
      list.push({
        statusKey: key,
        label: config.label,
        colorClass: config.colorClass,
        count: count,
        percent: (count / max) * 100
      })
    }
  }
  
  // Sort by count descending
  return list.sort((a, b) => b.count - a.count)
})

const formatPercent = (val) => {
  if (val === undefined || val === null || isNaN(val)) return '0,0%'
  return val.toFixed(1).replace('.', ',') + '%'
}
</script>
