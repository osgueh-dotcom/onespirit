<template>
  <AppChartCard
    title="Perbandingan Revenue"
    subtitle="Membandingkan pipeline potensial, revenue terkonfirmasi, dan target tahunan."
  >
    <template #metric>
      <span class="rounded-full border border-brand-emerald/20 bg-brand-emerald/10 px-3 py-1 text-xs font-extrabold text-brand-emerald">
        {{ formatPercent(targetAchievement) }} target
      </span>
    </template>

    <div v-if="maxRevenue <= 0" class="flex flex-1 items-center justify-center text-center">
      <p class="max-w-xs text-sm font-medium text-muted-theme">Belum ada nilai revenue untuk divisualisasikan.</p>
    </div>

    <div v-else class="flex flex-1 flex-col justify-center gap-5">
      <div v-for="item in revenueItems" :key="item.label" class="space-y-2">
        <div class="flex items-end justify-between gap-3">
          <div>
            <p class="text-xs font-extrabold text-main-theme">{{ item.label }}</p>
            <p class="mt-0.5 text-[10px] font-medium text-muted-theme">{{ item.caption }}</p>
          </div>
          <p class="text-sm font-black tracking-tight" :class="item.textClass">{{ formatMoney(item.value) }}</p>
        </div>
        <div class="h-3.5 overflow-hidden rounded-full border border-slate-200 bg-slate-100">
          <div class="h-full rounded-full transition-all duration-700" :class="item.barClass" :style="{ width: `${calculatePercent(item.value)}%` }"></div>
        </div>
      </div>
    </div>
  </AppChartCard>
</template>

<script setup>
import { computed } from 'vue'
import AppChartCard from '../ui/AppChartCard.vue'

const props = defineProps({
  potentialRevenue: { type: Number, default: 0 },
  confirmedRevenue: { type: Number, default: 0 },
  targetRevenue: { type: Number, default: 0 }
})

const safePotential = computed(() => Math.max(0, Number(props.potentialRevenue) || 0))
const safeConfirmed = computed(() => Math.max(0, Number(props.confirmedRevenue) || 0))
const safeTarget = computed(() => Math.max(0, Number(props.targetRevenue) || 0))
const maxRevenue = computed(() => Math.max(safePotential.value, safeConfirmed.value, safeTarget.value))
const targetAchievement = computed(() => safeTarget.value > 0 ? Math.min(100, (safeConfirmed.value / safeTarget.value) * 100) : 0)

const revenueItems = computed(() => [
  {
    label: 'Potential Pipeline',
    caption: 'Estimasi nilai seluruh peluang',
    value: safePotential.value,
    barClass: 'bg-gradient-to-r from-brand-amber to-brand-orange',
    textClass: 'text-brand-orange'
  },
  {
    label: 'Confirmed Revenue',
    caption: 'Nilai project yang sudah deal',
    value: safeConfirmed.value,
    barClass: 'bg-brand-emerald',
    textClass: 'text-brand-emerald'
  },
  {
    label: 'Target Tahunan',
    caption: 'Pembanding pencapaian komersial',
    value: safeTarget.value,
    barClass: 'bg-brand-blue',
    textClass: 'text-brand-blue'
  }
])

const calculatePercent = (value) => maxRevenue.value > 0 ? Math.max(0, (value / maxRevenue.value) * 100) : 0
const formatMoney = (value) => `Rp${Math.round(Number(value) || 0).toLocaleString('id-ID')}`
const formatPercent = (value) => `${Number(value || 0).toFixed(1).replace('.', ',')}%`
</script>
