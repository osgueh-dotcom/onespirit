<template>
  <section class="app-section-card print:bg-white print:border-none print:p-0 print:shadow-none">
    <div class="grid gap-5 lg:grid-cols-[1.5fr_0.5fr]">
      <div>
        <p class="app-kicker">Executive Summary</p>
        <h3 class="mt-1.5 text-xl font-black tracking-tight text-main-theme">Sorotan periode berjalan</h3>

        <p v-if="!hasData" class="mt-4 text-sm font-medium leading-relaxed text-muted-theme">
          Belum ada data project atau inquiry untuk filter yang dipilih.
        </p>

        <p v-else class="mt-4 text-sm font-medium leading-7 text-muted-theme print:text-charcoal-800">
          One Spirit mencatat <strong class="text-brand-orange">{{ totalInquiry }} inquiry</strong> dengan
          <strong class="text-brand-emerald">{{ totalDeal }} project deal</strong>. Deal rate berada di
          <strong class="text-main-theme">{{ formatPercent(dealRate) }}</strong>, sementara cancel rate
          <strong class="text-red-500">{{ formatPercent(cancelRate) }}</strong>. Confirmed revenue mencapai
          <strong class="text-brand-emerald">{{ formatMoney(confirmedRevenue) }}</strong> atau
          <strong class="text-brand-orange">{{ formatPercent(targetAchievement) }}</strong> dari target
          {{ targetYear }}.
        </p>
      </div>

      <div class="grid grid-cols-2 gap-3 lg:grid-cols-1">
        <div class="app-subtle-panel p-4">
          <p class="text-[10px] font-extrabold uppercase tracking-wider text-muted-theme">Deal Rate</p>
          <p class="mt-1 text-2xl font-black text-brand-emerald">{{ formatPercent(dealRate) }}</p>
        </div>
        <div class="app-subtle-panel p-4">
          <p class="text-[10px] font-extrabold uppercase tracking-wider text-muted-theme">Target Achievement</p>
          <p class="mt-1 text-2xl font-black text-brand-orange">{{ formatPercent(targetAchievement) }}</p>
        </div>
      </div>
    </div>

    <div v-if="warnings.length > 0" class="mt-5 grid gap-3 md:grid-cols-2 print:hidden">
      <div v-for="warning in warnings" :key="warning.title" class="rounded-xl border border-brand-amber/25 bg-brand-amber/10 p-4">
        <p class="text-[10px] font-extrabold uppercase tracking-wider text-brand-orange">{{ warning.title }}</p>
        <p class="mt-1.5 text-xs font-medium leading-relaxed text-slate-700">{{ warning.message }}</p>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  executive: {
    type: Object,
    required: true,
    default: () => ({})
  },
  target: {
    type: Object,
    required: true,
    default: () => ({})
  }
})

const hasData = computed(() => Number(props.executive?.total_projects) > 0)
const totalInquiry = computed(() => Number(props.executive?.total_inquiry) || 0)
const totalDeal = computed(() => Number(props.executive?.total_deal) || 0)
const dealRate = computed(() => Number(props.executive?.deal_rate) || 0)
const cancelRate = computed(() => Number(props.executive?.cancel_rate) || 0)
const confirmedRevenue = computed(() => Number(props.executive?.confirmed_revenue) || 0)
const targetAchievement = computed(() => Number(props.target?.achievement_rate) || 0)
const targetYear = computed(() => props.target?.year || new Date().getFullYear())
const dataIssues = computed(() => Number(props.executive?.total_data_quality_issues) || 0)

const warnings = computed(() => {
  const items = []
  if (cancelRate.value > 30) {
    items.push({
      title: 'Cancellation perlu perhatian',
      message: `Cancel rate ${formatPercent(cancelRate.value)}. Tinjau alasan pembatalan dan kualitas follow-up.`
    })
  }
  if (dataIssues.value > 0) {
    items.push({
      title: 'Kualitas data operasional',
      message: `${dataIssues.value} isu kelengkapan data perlu diselesaikan sebelum evaluasi management.`
    })
  }
  return items
})

const formatMoney = (value) => `Rp${Math.round(Number(value) || 0).toLocaleString('id-ID')}`
const formatPercent = (value) => `${Number(value || 0).toFixed(1).replace('.', ',')}%`
</script>
