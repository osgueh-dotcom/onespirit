<template>
  <AppChartCard
    title="Kontribusi Source"
    subtitle="Menunjukkan source yang paling besar menghasilkan deal dan confirmed revenue."
  >
    <template #metric>
      <span class="rounded-full border border-brand-orange/20 bg-brand-orange/10 px-3 py-1 text-xs font-extrabold text-brand-orange">
        {{ items.length }} source aktif
      </span>
    </template>

    <div v-if="items.length === 0" class="flex flex-1 items-center justify-center text-center">
      <p class="max-w-sm text-sm font-medium text-muted-theme">Data source belum cukup untuk divisualisasikan.</p>
    </div>

    <div v-else class="grid flex-1 grid-cols-1 gap-x-8 gap-y-4 md:grid-cols-2">
      <div v-for="(item, index) in items" :key="item.source_type || index" class="flex flex-col justify-center space-y-2">
        <div class="flex items-end justify-between gap-3">
          <div class="min-w-0">
            <p class="truncate text-xs font-extrabold text-main-theme">{{ item.source_type || 'Belum dikategorikan' }}</p>
            <p class="mt-0.5 text-[10px] font-medium text-muted-theme">{{ item.deal_count || 0 }} deal</p>
          </div>
          <p class="shrink-0 text-xs font-black text-brand-emerald">{{ formatMoney(item.confirmed_revenue) }}</p>
        </div>
        <div class="h-2.5 overflow-hidden rounded-full bg-slate-100">
          <div
            class="h-full rounded-full bg-gradient-to-r from-brand-amber to-brand-orange transition-all duration-700"
            :style="{ width: `${item.sharePercent}%` }"
          ></div>
        </div>
      </div>
    </div>
  </AppChartCard>
</template>

<script setup>
import { computed } from 'vue'
import AppChartCard from '../ui/AppChartCard.vue'

const props = defineProps({
  sourceAnalytics: {
    type: Array,
    default: () => []
  }
})

const totalConfirmedRevenue = computed(() => props.sourceAnalytics.reduce(
  (sum, item) => sum + Math.max(0, Number(item?.confirmed_revenue) || 0),
  0
))

const items = computed(() => props.sourceAnalytics
  .map((item) => {
    const confirmedRevenue = Math.max(0, Number(item?.confirmed_revenue) || 0)
    return {
      ...item,
      confirmed_revenue: confirmedRevenue,
      sharePercent: totalConfirmedRevenue.value > 0 ? (confirmedRevenue / totalConfirmedRevenue.value) * 100 : 0
    }
  })
  .filter((item) => item.confirmed_revenue > 0)
  .sort((a, b) => b.confirmed_revenue - a.confirmed_revenue)
  .slice(0, 8))

const formatMoney = (value) => `Rp${Math.round(Number(value) || 0).toLocaleString('id-ID')}`
</script>
