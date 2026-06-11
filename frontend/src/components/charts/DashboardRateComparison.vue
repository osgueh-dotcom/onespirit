<template>
  <AppChartCard
    title="Deal vs Cancel"
    subtitle="Perbandingan cepat antara rasio konversi dan pembatalan."
  >
    <template #metric>
      <span class="rounded-full border border-brand-blue/20 bg-brand-blue/10 px-3 py-1 text-xs font-extrabold text-brand-blue">
        {{ rateGapLabel }}
      </span>
    </template>

    <div class="grid flex-1 grid-cols-2 items-center gap-4">
      <div v-for="gauge in gauges" :key="gauge.label" class="flex flex-col items-center text-center">
        <div class="relative flex h-28 w-28 items-center justify-center sm:h-32 sm:w-32">
          <svg class="h-full w-full -rotate-90" viewBox="0 0 100 100" role="img" :aria-label="`${gauge.label} ${formatPercent(gauge.value)}`">
            <circle cx="50" cy="50" r="40" fill="transparent" class="stroke-slate-100" stroke-width="9" />
            <circle
              cx="50"
              cy="50"
              r="40"
              fill="transparent"
              :class="gauge.strokeClass"
              stroke-width="9"
              stroke-dasharray="251.2"
              :stroke-dashoffset="calculateOffset(gauge.value)"
              stroke-linecap="round"
              class="transition-all duration-700"
            />
          </svg>
          <div class="absolute flex flex-col items-center">
            <span class="text-xl font-black tracking-tight" :class="gauge.textClass">{{ formatPercent(gauge.value) }}</span>
            <span class="mt-0.5 text-[9px] font-extrabold uppercase tracking-wider text-muted-theme">{{ gauge.shortLabel }}</span>
          </div>
        </div>
        <p class="mt-3 text-xs font-extrabold text-main-theme">{{ gauge.label }}</p>
        <p class="mt-1 text-[10px] font-medium text-muted-theme">{{ gauge.caption }}</p>
      </div>
    </div>
  </AppChartCard>
</template>

<script setup>
import { computed } from 'vue'
import AppChartCard from '../ui/AppChartCard.vue'

const props = defineProps({
  dealRate: { type: Number, default: 0 },
  cancelRate: { type: Number, default: 0 }
})

const safeDealRate = computed(() => Math.max(0, Math.min(100, Number(props.dealRate) || 0)))
const safeCancelRate = computed(() => Math.max(0, Math.min(100, Number(props.cancelRate) || 0)))

const gauges = computed(() => [
  {
    label: 'Tingkat Deal',
    shortLabel: 'Deal',
    caption: 'Inquiry berhasil dikonversi',
    value: safeDealRate.value,
    strokeClass: 'stroke-brand-emerald',
    textClass: 'text-brand-emerald'
  },
  {
    label: 'Tingkat Cancel',
    shortLabel: 'Cancel',
    caption: 'Peluang berhenti atau batal',
    value: safeCancelRate.value,
    strokeClass: 'stroke-red-500',
    textClass: 'text-red-500'
  }
])

const rateGapLabel = computed(() => {
  const gap = safeDealRate.value - safeCancelRate.value
  return `${Math.abs(gap).toFixed(1).replace('.', ',')} pt ${gap >= 0 ? 'positif' : 'negatif'}`
})

const calculateOffset = (rate) => 251.2 - (251.2 * rate) / 100
const formatPercent = (value) => `${Number(value || 0).toFixed(1).replace('.', ',')}%`
</script>
