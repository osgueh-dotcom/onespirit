<template>
  <section>
    <div class="mb-4 flex flex-col gap-1 sm:flex-row sm:items-end sm:justify-between">
      <div>
        <p class="app-kicker">KPI Utama</p>
        <h3 class="mt-1 text-lg font-black tracking-tight text-main-theme">Kinerja bisnis dalam satu pandangan</h3>
      </div>
      <p class="text-xs font-medium text-muted-theme">Nilai mengikuti filter dashboard aktif.</p>
    </div>

    <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-3 print:grid-cols-3">
      <AppStatCard title="Total Inquiry" :value="executive.total_inquiry || 0" subtitle="Peluang masuk" theme="orange" />
      <AppStatCard title="Total Project Deal" :value="executive.total_deal || 0" subtitle="Project terkonfirmasi" theme="emerald" />
      <AppStatCard title="Deal Conversion Rate" :value="formatPercent(executive.deal_rate)" subtitle="Deal terhadap inquiry" theme="emerald" />
      <AppStatCard title="Cancellation Rate" :value="formatPercent(executive.cancel_rate)" :subtitle="`${executive.total_cancel || 0} dibatalkan`" theme="red" />
      <AppStatCard title="Potential Pipeline" :value="formatMoney(executive.potential_revenue)" subtitle="Estimasi nilai peluang" theme="amber" />
      <AppStatCard title="Confirmed Revenue" :value="formatMoney(executive.confirmed_revenue)" subtitle="Nilai project deal" theme="emerald" />
      <AppStatCard title="Target Achievement" :value="formatPercent(target.achievement_rate)" :subtitle="`Target ${formatMoney(target.revenue_target)}`" theme="orange" />
      <AppStatCard title="Revenue Conversion" :value="formatPercent(executive.revenue_conversion_rate)" subtitle="Confirmed terhadap pipeline" theme="blue" />
      <AppStatCard title="Average Project Value" :value="formatMoney(executive.average_project_value)" subtitle="Rata-rata nilai deal" theme="purple" />
    </div>
  </section>
</template>

<script setup>
import AppStatCard from '../ui/AppStatCard.vue'

defineProps({
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

const formatMoney = (value) => `Rp${Math.round(Number(value) || 0).toLocaleString('id-ID')}`
const formatPercent = (value) => `${Number(value || 0).toFixed(1).replace('.', ',')}%`
</script>
