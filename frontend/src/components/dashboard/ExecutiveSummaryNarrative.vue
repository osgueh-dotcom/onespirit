<template>
  <div class="glass-panel p-6 bg-charcoal-800 border border-charcoal-700 rounded-3xl space-y-3 print:bg-white print:border-none print:p-0 print:rounded-none">
    <h3 class="text-xs font-bold text-brand-orange uppercase tracking-widest print:text-charcoal-800 print:text-sm">
      Executive Summary Narrative
    </h3>
    
    <div v-if="!hasData" class="text-xs font-semibold text-charcoal-400 leading-relaxed print:text-charcoal-600">
      Belum ada data proyek atau inquiry yang tercatat untuk filter periode yang dipilih. Silakan sesuaikan filter pencarian Anda.
    </div>
    
    <div v-else class="space-y-4">
      <p class="text-sm font-semibold text-white leading-relaxed print:text-charcoal-800">
        Pada periode ini, PT. One Spirit Asia mencatat sebanyak <span class="text-brand-orange print:text-charcoal-900 font-extrabold">{{ totalInquiry }}</span> record inquiry masuk dengan total <span class="text-brand-emerald print:text-charcoal-900 font-extrabold">{{ totalDeal }}</span> project deal yang berhasil ditandatangani. Tingkat pencapaian deal (Deal Rate) tercatat di angka <span class="text-white print:text-charcoal-900 font-extrabold">{{ dealRate.toFixed(1) }}%</span>, sedangkan tingkat pembatalan (Cancel Rate) berada pada angka <span class="text-white print:text-charcoal-900 font-extrabold">{{ cancelRate.toFixed(1) }}%</span>. Confirmed revenue (nilai proyek yang disepakati) saat ini mencapai <span class="text-brand-emerald print:text-charcoal-900 font-extrabold">{{ formatMoney(confirmedRevenue) }}</span>, yang menyumbang sekitar <span class="text-brand-orange print:text-charcoal-900 font-extrabold">{{ targetAchievement.toFixed(1) }}%</span> dari target tahunan Rp 9.2 Miliar yang dicanangkan oleh direksi untuk tahun {{ targetYear }}. 
      </p>

      <!-- Warnings/Issues Alert blocks -->
      <div v-if="warnings.length > 0" class="space-y-2.5 print:hidden">
        <div 
          v-for="warning in warnings" 
          :key="warning.message"
          class="flex items-start gap-2.5 p-3 bg-brand-orange/5 border border-brand-orange/20 rounded-2xl text-xs"
        >
          <svg class="w-4 h-4 text-brand-orange mt-0.5 shrink-0" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          <div class="space-y-0.5">
            <span class="text-[9px] uppercase font-black text-brand-orange tracking-wider">{{ warning.title }}</span>
            <p class="text-charcoal-200 font-semibold leading-normal">{{ warning.message }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
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

const hasData = computed(() => {
  return props.executive && props.executive.total_projects > 0
})

const totalInquiry = computed(() => props.executive.total_inquiry || 0)
const totalDeal = computed(() => props.executive.total_deal || 0)
const dealRate = computed(() => props.executive.deal_rate || 0.0)
const cancelRate = computed(() => props.executive.cancel_rate || 0.0)
const confirmedRevenue = computed(() => props.executive.confirmed_revenue || 0.0)
const targetAchievement = computed(() => props.target.achievement_rate || 0.0)
const targetYear = computed(() => props.target.year || 2025)
const dataIssues = computed(() => props.executive.total_data_quality_issues || 0)

const warnings = computed(() => {
  const list = []
  if (cancelRate.value > 30) {
    list.push({
      title: 'Tingkat Pembatalan Tinggi',
      message: `Persentase pembatalan proyek (Cancel Rate: ${cancelRate.value.toFixed(1)}%) terpantau cukup tinggi pada periode ini. Disarankan melakukan tinjauan mendalam atas alasan pembatalan (cancel reason) proyek.`
    })
  }
  if (dataIssues.value > 0) {
    list.push({
      title: 'Kualitas Data Operasional',
      message: `Terdapat ${dataIssues.value} isu ketidaklengkapan data yang terdeteksi di database. Disarankan untuk segera melengkapi data penugasan PO/PM, Customer, anggaran (budget), maupun dokumen drive pendukung sebelum rapat evaluasi.`
    })
  }
  return list
})

const formatMoney = (val) => {
  if (val >= 1e9) {
    return 'Rp ' + (val / 1e9).toFixed(2) + ' B'
  }
  if (val >= 1e6) {
    return 'Rp ' + (val / 1e6).toFixed(1) + ' M'
  }
  return 'Rp ' + Number(val || 0).toLocaleString('id-ID')
}
</script>

<style scoped>
.glass-panel {
  background: rgba(26, 32, 44, 0.7);
  backdrop-filter: blur(12px);
}
</style>
