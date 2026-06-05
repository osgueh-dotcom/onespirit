<template>
  <div class="glass-panel p-6 bg-charcoal-800 border border-charcoal-700 rounded-3xl space-y-4 print:bg-white print:border-none print:p-0 print:rounded-none">
    <h3 class="text-xs font-bold text-brand-orange uppercase tracking-widest print:text-charcoal-800 print:text-sm">
      Catatan Evaluasi Manajemen
    </h3>
    
    <div v-if="!hasData" class="text-xs font-semibold text-charcoal-400 leading-relaxed print:text-charcoal-600">
      Belum ada data untuk menghasilkan evaluasi manajemen pada periode ini.
    </div>
    
    <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <!-- Strengths (Kekuatan) -->
      <div class="space-y-3 p-4 bg-emerald-500/5 border border-emerald-500/10 rounded-2xl print:bg-white print:border-none print:p-0">
        <h4 class="text-xs font-bold text-brand-emerald uppercase tracking-wider flex items-center gap-2 print:text-charcoal-900 print:text-sm">
          <span class="w-1.5 h-1.5 rounded-full bg-brand-emerald print:hidden"></span>
          Kekuatan / Indikasi Positif
        </h4>
        <ul class="space-y-2 text-xs font-semibold text-charcoal-200 list-disc pl-4 leading-relaxed print:text-charcoal-600">
          <li v-for="s in strengths" :key="s">{{ s }}</li>
          <li v-if="strengths.length === 0">Belum ada indikasi positif signifikan yang terdeteksi secara otomatis.</li>
        </ul>
      </div>

      <!-- Risks (Risiko) -->
      <div class="space-y-3 p-4 bg-red-500/5 border border-red-500/10 rounded-2xl print:bg-white print:border-none print:p-0">
        <h4 class="text-xs font-bold text-red-400 uppercase tracking-wider flex items-center gap-2 print:text-charcoal-900 print:text-sm">
          <span class="w-1.5 h-1.5 rounded-full bg-red-500 print:hidden"></span>
          Risiko / Bottlenecks
        </h4>
        <ul class="space-y-2 text-xs font-semibold text-charcoal-200 list-disc pl-4 leading-relaxed print:text-charcoal-600">
          <li v-for="r in risks" :key="r">{{ r }}</li>
          <li v-if="risks.length === 0">Tidak ada risiko kritis yang terdeteksi secara otomatis pada periode ini.</li>
        </ul>
      </div>

      <!-- Recommendations (Rekomendasi Tindakan) -->
      <div class="space-y-3 p-4 bg-brand-orange/5 border border-brand-orange/10 rounded-2xl print:bg-white print:border-none print:p-0">
        <h4 class="text-xs font-bold text-brand-orange uppercase tracking-wider flex items-center gap-2 print:text-charcoal-900 print:text-sm">
          <span class="w-1.5 h-1.5 rounded-full bg-brand-orange print:hidden"></span>
          Rekomendasi Tindakan
        </h4>
        <ul class="space-y-2 text-xs font-semibold text-charcoal-200 list-disc pl-4 leading-relaxed print:text-charcoal-600">
          <li v-for="a in actions" :key="a">{{ a }}</li>
          <li v-if="actions.length === 0">Semua parameter berjalan sesuai dengan standar operasional nominal.</li>
        </ul>
      </div>
    </div>

    <!-- Footnote stating these are guidelines -->
    <p class="text-[9px] text-charcoal-500 font-bold tracking-wide italic pt-1 print:text-charcoal-600">
      * Catatan ini dihasilkan secara otomatis berdasarkan data operasional dan bersifat sebagai referensi pendukung pengambilan keputusan manajemen.
    </p>
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

const targetAchievement = computed(() => props.target.achievement_rate || 0.0)
const dealRate = computed(() => props.executive.deal_rate || 0.0)
const cancelRate = computed(() => props.executive.cancel_rate || 0.0)
const confirmedRevenue = computed(() => props.executive.confirmed_revenue || 0.0)
const outstandingAmount = computed(() => props.executive.outstanding_amount || 0.0)
const dataIssues = computed(() => props.executive.total_data_quality_issues || 0)
const inquiryStageCount = computed(() => props.executive.inquiry_stage_count || 0)

const strengths = computed(() => {
  const list = []
  if (confirmedRevenue.value > 0) {
    list.push('Pipeline revenue terkonfirmasi menunjukkan aliran keuangan yang aktif.')
  }
  if (targetAchievement.value >= 100) {
    list.push('Target pencapaian tahunan berhasil ditembus secara penuh (100%+).')
  } else if (targetAchievement.value >= 60) {
    list.push('Kemajuan menuju target tahunan berjalan positif (>60% tercapai).')
  }
  if (dealRate.value >= 45) {
    list.push('Rasio konversi deal (Deal Rate) sehat dan optimum (>=45%).')
  }
  if (dataIssues.value === 0) {
    list.push('Integritas data operasional terpantau sangat baik (Nol temuan kualitas data).')
  }
  return list
})

const risks = computed(() => {
  const list = []
  if (cancelRate.value > 50) {
    list.push('Tingkat pembatalan (Cancel Rate) berada di atas batas wajar (>50%), indikasi awal kerugian prospek.')
  }
  if (outstandingAmount.value > 0) {
    list.push('Terdapat tagihan outstanding terkonfirmasi yang belum diselesaikan, memicu risiko piutang.')
  }
  if (dataIssues.value > 0) {
    list.push('Adanya temuan isu data quality dapat menghambat keakuratan evaluasi KPI staf.')
  }
  if (inquiryStageCount.value > (props.executive.total_projects * 0.6)) {
    list.push('Sebagian besar proyek menumpuk di tahap Inquiry, perlu percepatan penyusunan penawaran.')
  }
  return list
})

const actions = computed(() => {
  const list = []
  if (cancelRate.value > 30) {
    list.push('Disarankan melakukan evaluasi alasan pembatalan (cancel reason) dan review pola komunikasi penawaran.')
  }
  if (outstandingAmount.value > 0) {
    list.push('Disarankan melakukan follow-up penagihan yang lebih terstruktur bagi proyek dengan piutang outstanding.')
  }
  if (dataIssues.value > 0) {
    list.push('Disarankan melakukan perbaikan data mandiri untuk melengkapi penugasan PO/PM dan link dokumen resmi.')
  }
  if (inquiryStageCount.value > 0) {
    list.push('Segera alokasikan Program Owner (PO) untuk mengonversi antrean status Inquiry menjadi Quotation resmi.')
  }
  return list
})
</script>

<style scoped>
.glass-panel {
  background: rgba(26, 32, 44, 0.7);
  backdrop-filter: blur(12px);
}
</style>
