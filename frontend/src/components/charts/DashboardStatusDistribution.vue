<template>
  <AppChartCard
    title="Distribusi Status Project"
    subtitle="Memperlihatkan konsentrasi project pada setiap tahap operasional."
  >
    <template #metric>
      <span class="rounded-full border border-brand-orange/20 bg-brand-orange/10 px-3 py-1 text-xs font-extrabold text-brand-orange">
        {{ totalProjects }} project
      </span>
    </template>

    <div v-if="totalProjects === 0" class="flex flex-1 items-center justify-center text-center">
      <p class="max-w-xs text-sm font-medium text-muted-theme">Belum ada data status project untuk periode ini.</p>
    </div>

    <div v-else class="flex flex-1 flex-col justify-center space-y-3 overflow-y-auto pr-1">
      <div v-for="item in statusItems" :key="item.statusKey" class="space-y-1.5">
        <div class="flex items-center justify-between gap-3 text-xs">
          <div class="flex min-w-0 items-center gap-2">
            <span class="h-2 w-2 shrink-0 rounded-full" :class="item.colorClass"></span>
            <span class="truncate font-extrabold text-main-theme">{{ item.label }}</span>
          </div>
          <span class="shrink-0 font-bold text-muted-theme">{{ item.count }} | {{ formatPercent(item.percent) }}</span>
        </div>
        <div class="h-2 overflow-hidden rounded-full bg-slate-100">
          <div class="h-full rounded-full transition-all duration-700" :class="item.colorClass" :style="{ width: `${item.percent}%` }"></div>
        </div>
      </div>
    </div>
  </AppChartCard>
</template>

<script setup>
import { computed } from 'vue'
import AppChartCard from '../ui/AppChartCard.vue'

const props = defineProps({
  statusCounts: {
    type: Object,
    default: () => ({})
  }
})

const statusLabels = {
  inquiry: { label: 'Inquiry', colorClass: 'bg-brand-amber' },
  quotation: { label: 'Penawaran', colorClass: 'bg-brand-orange' },
  negotiation: { label: 'Negosiasi', colorClass: 'bg-yellow-500' },
  confirmed: { label: 'Terkonfirmasi', colorClass: 'bg-brand-emerald-dark' },
  preparation: { label: 'Persiapan', colorClass: 'bg-brand-blue' },
  ongoing: { label: 'Berjalan', colorClass: 'bg-sky-500' },
  running: { label: 'Berjalan', colorClass: 'bg-sky-500' },
  completed: { label: 'Selesai', colorClass: 'bg-brand-emerald' },
  canceled: { label: 'Dibatalkan', colorClass: 'bg-red-500' },
  cancel: { label: 'Dibatalkan', colorClass: 'bg-red-500' },
  closed: { label: 'Ditutup', colorClass: 'bg-slate-500' },
  reporting: { label: 'Pelaporan', colorClass: 'bg-violet-500' },
  active: { label: 'Aktif', colorClass: 'bg-brand-blue' },
  open: { label: 'Open', colorClass: 'bg-brand-amber' }
}

const normalizedCounts = computed(() => props.statusCounts || {})
const totalProjects = computed(() => Object.values(normalizedCounts.value).reduce((sum, value) => sum + (Number(value) || 0), 0))

const statusItems = computed(() => Object.entries(normalizedCounts.value)
  .map(([key, value]) => {
    const count = Math.max(0, Number(value) || 0)
    const config = statusLabels[key.toLowerCase()] || { label: key, colorClass: 'bg-slate-400' }
    return {
      statusKey: key,
      label: config.label,
      colorClass: config.colorClass,
      count,
      percent: totalProjects.value > 0 ? (count / totalProjects.value) * 100 : 0
    }
  })
  .filter((item) => item.count > 0)
  .sort((a, b) => b.count - a.count))

const formatPercent = (value) => `${Number(value || 0).toFixed(1).replace('.', ',')}%`
</script>
