<template>
  <AppChartCard
    title="Alur Inquiry ke Deal"
    subtitle="Membaca pergerakan inquiry menjadi project deal serta risiko pembatalan."
  >
    <template #metric>
      <span class="rounded-full border border-brand-emerald/20 bg-brand-emerald/10 px-3 py-1 text-xs font-extrabold text-brand-emerald">
        {{ formatPercent(dealRate) }} deal
      </span>
    </template>

    <div v-if="safeInquiry === 0" class="flex flex-1 items-center justify-center text-center">
      <p class="max-w-xs text-sm font-medium text-muted-theme">Belum ada data inquiry untuk periode yang dipilih.</p>
    </div>

    <div v-else class="flex flex-1 flex-col justify-center gap-5">
      <div v-for="item in funnelItems" :key="item.label" class="space-y-2">
        <div class="flex items-end justify-between gap-4">
          <div>
            <p class="text-xs font-extrabold text-main-theme">{{ item.label }}</p>
            <p class="mt-0.5 text-[11px] font-medium text-muted-theme">{{ item.caption }}</p>
          </div>
          <div class="text-right">
            <p class="text-lg font-black tracking-tight" :class="item.textClass">{{ item.value }}</p>
            <p class="text-[10px] font-bold text-muted-theme">{{ formatPercent(item.percent) }}</p>
          </div>
        </div>
        <div class="h-3.5 w-full overflow-hidden rounded-full bg-slate-100 border border-slate-200">
          <div class="h-full rounded-full transition-all duration-700" :class="item.barClass" :style="{ width: `${item.percent}%` }"></div>
        </div>
      </div>
    </div>
  </AppChartCard>
</template>

<script setup>
import { computed } from 'vue'
import AppChartCard from '../ui/AppChartCard.vue'

const props = defineProps({
  totalInquiry: { type: Number, default: 0 },
  totalDeal: { type: Number, default: 0 },
  totalCancel: { type: Number, default: 0 }
})

const safeInquiry = computed(() => Math.max(0, Number(props.totalInquiry) || 0))
const safeDeal = computed(() => Math.max(0, Number(props.totalDeal) || 0))
const safeCancel = computed(() => Math.max(0, Number(props.totalCancel) || 0))

const dealRate = computed(() => safeInquiry.value > 0 ? Math.min(100, (safeDeal.value / safeInquiry.value) * 100) : 0)
const cancelRate = computed(() => safeInquiry.value > 0 ? Math.min(100, (safeCancel.value / safeInquiry.value) * 100) : 0)

const funnelItems = computed(() => [
  {
    label: 'Total Inquiry',
    caption: 'Seluruh peluang yang masuk',
    value: safeInquiry.value,
    percent: 100,
    barClass: 'bg-gradient-to-r from-brand-amber to-brand-orange',
    textClass: 'text-brand-orange'
  },
  {
    label: 'Project Deal',
    caption: 'Inquiry yang berhasil dikonfirmasi',
    value: safeDeal.value,
    percent: dealRate.value,
    barClass: 'bg-brand-emerald',
    textClass: 'text-brand-emerald'
  },
  {
    label: 'Dibatalkan',
    caption: 'Inquiry atau project yang berhenti',
    value: safeCancel.value,
    percent: cancelRate.value,
    barClass: 'bg-red-500',
    textClass: 'text-red-500'
  }
])

const formatPercent = (value) => `${Number(value || 0).toFixed(1).replace('.', ',')}%`
</script>
