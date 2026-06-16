<template>
  <div class="glass-panel p-6 flex flex-col select-none print:bg-white print:border print:border-charcoal-200 print:rounded-xl print:p-5 print:text-charcoal-900">
    <div class="flex items-center justify-between mb-4 border-b border-panel-theme pb-3 print:border-charcoal-200">
      <div class="flex flex-col">
        <h3 class="text-xs font-bold text-white tracking-widest uppercase flex items-center gap-2 print:text-charcoal-900 print:text-sm">
          <span class="w-1.5 h-1.5 rounded-full bg-brand-orange animate-pulse print:hidden"></span>
          Review Kualitas Data Operasional (Data Quality Review)
        </h3>
        <span class="text-[9px] text-muted-theme font-semibold mt-0.5 print:text-charcoal-500">Identifikasi inkonsistensi alur kerja dan pemetaan data</span>
      </div>
      <div 
        class="text-[10px] uppercase font-black px-2.5 py-1 rounded print:border"
        :class="hasIssues ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20 print:bg-charcoal-50 print:border-charcoal-350 print:text-charcoal-700' : 'bg-brand-emerald/10 text-brand-emerald border border-brand-emerald/20 print:bg-charcoal-50 print:border-charcoal-300 print:text-emerald-700'"
      >
        {{ hasIssues ? 'Terdeteksi Inkonsistensi' : 'Kualitas Data Nominal' }}
      </div>
    </div>

    <!-- Explanation paragraph on why data quality matters -->
    <p class="text-xs text-soft-theme font-semibold leading-relaxed mb-4 print:text-charcoal-600">
      * Akurasi dan kelengkapan data operasional sangat penting untuk memastikan keandalan laporan eksekutif. Ketidaksesuaian data dapat memicu bias dalam penilaian kinerja Program Owner/Manager (PO/PM), menghambat rekonsiliasi keuangan, serta mengganggu keakuratan proyeksi pipeline bisnis.
    </p>

    <!-- Perfect Data Quality State -->
    <div 
      v-if="!hasIssues" 
      class="py-12 flex flex-col items-center justify-center text-center gap-3 bg-surface-theme border border-panel-theme rounded-xl print:bg-charcoal-50 print:border-charcoal-200"
    >
      <div class="w-10 h-10 rounded-full bg-brand-emerald/15 flex items-center justify-center text-brand-emerald">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="3" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
        </svg>
      </div>
      <div>
        <p class="text-xs text-white font-bold print:text-charcoal-900">Skor Kualitas Data 100%</p>
        <p class="text-[10px] text-muted-theme font-semibold mt-0.5 print:text-charcoal-500">Tidak ada data penugasan, anggaran, atau sumber event yang terdeteksi tidak lengkap.</p>
      </div>
    </div>

    <!-- Issues Checklist Grid -->
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4 print:grid-cols-2">
      <!-- Missing PO -->
      <div 
        class="p-4 rounded-xl border flex flex-col bg-surface-theme print:bg-charcoal-50 print:border-charcoal-200"
        :class="quality.missing_po > 0 ? 'border-amber-500/30' : 'border-panel-theme'"
      >
        <div class="flex items-center justify-between mb-1.5">
          <span class="text-[9px] uppercase tracking-wider font-black" :class="quality.missing_po > 0 ? 'text-amber-400 print:text-orange-700' : 'text-muted-theme print:text-charcoal-500'">PO Belum Ditunjuk</span>
          <span 
            v-if="quality.missing_po > 0"
            class="text-[10px] bg-amber-500/10 text-amber-400 border border-amber-500/20 px-1.5 py-0.5 rounded font-black font-sans print:border-charcoal-250 print:text-charcoal-700"
          >
            {{ quality.missing_po }}
          </span>
          <svg v-else class="w-4 h-4 text-brand-emerald" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <p class="text-[10px] text-soft-theme font-semibold leading-normal print:text-charcoal-600">
          Proyek aktif yang belum memiliki penugasan Program Owner.
        </p>
      </div>

      <!-- Missing PM -->
      <div 
        class="p-4 rounded-xl border flex flex-col bg-surface-theme print:bg-charcoal-50 print:border-charcoal-200"
        :class="quality.missing_pm > 0 ? 'border-amber-500/30' : 'border-panel-theme'"
      >
        <div class="flex items-center justify-between mb-1.5">
          <span class="text-[9px] uppercase tracking-wider font-black" :class="quality.missing_pm > 0 ? 'text-amber-400 print:text-orange-700' : 'text-muted-theme print:text-charcoal-500'">PM Belum Ditunjuk</span>
          <span 
            v-if="quality.missing_pm > 0"
            class="text-[10px] bg-amber-500/10 text-amber-400 border border-amber-500/20 px-1.5 py-0.5 rounded font-black font-sans print:border-charcoal-250 print:text-charcoal-700"
          >
            {{ quality.missing_pm }}
          </span>
          <svg v-else class="w-4 h-4 text-brand-emerald" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <p class="text-[10px] text-soft-theme font-semibold leading-normal print:text-charcoal-600">
          Proyek aktif yang belum memiliki penugasan Program Manager.
        </p>
      </div>

      <!-- Missing Customer -->
      <div 
        class="p-4 rounded-xl border flex flex-col bg-surface-theme print:bg-charcoal-50 print:border-charcoal-200"
        :class="quality.missing_customer > 0 ? 'border-red-500/30' : 'border-panel-theme'"
      >
        <div class="flex items-center justify-between mb-1.5">
          <span class="text-[9px] uppercase tracking-wider font-black" :class="quality.missing_customer > 0 ? 'text-red-400 print:text-red-700' : 'text-muted-theme print:text-charcoal-500'">Pelanggan Kosong</span>
          <span 
            v-if="quality.missing_customer > 0"
            class="text-[10px] bg-red-500/10 text-red-400 border border-red-500/20 px-1.5 py-0.5 rounded font-black font-sans print:border-charcoal-250 print:text-charcoal-700"
          >
            {{ quality.missing_customer }}
          </span>
          <svg v-else class="w-4 h-4 text-brand-emerald" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <p class="text-[10px] text-soft-theme font-semibold leading-normal print:text-charcoal-600">
          Proyek yang belum terhubung dengan profil pelanggan/klien.
        </p>
      </div>

      <!-- Missing Budget -->
      <div 
        class="p-4 rounded-xl border flex flex-col bg-surface-theme print:bg-charcoal-50 print:border-charcoal-200"
        :class="quality.missing_budget > 0 ? 'border-amber-500/30' : 'border-panel-theme'"
      >
        <div class="flex items-center justify-between mb-1.5">
          <span class="text-[9px] uppercase tracking-wider font-black" :class="quality.missing_budget > 0 ? 'text-amber-400 print:text-orange-700' : 'text-muted-theme print:text-charcoal-500'">Anggaran Kosong</span>
          <span 
            v-if="quality.missing_budget > 0"
            class="text-[10px] bg-amber-500/10 text-amber-400 border border-amber-500/20 px-1.5 py-0.5 rounded font-black font-sans print:border-charcoal-250 print:text-charcoal-700"
          >
            {{ quality.missing_budget }}
          </span>
          <svg v-else class="w-4 h-4 text-brand-emerald" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <p class="text-[10px] text-soft-theme font-semibold leading-normal print:text-charcoal-600">
          Proyek aktif yang nilai anggarannya kosong atau bernilai nol.
        </p>
      </div>

      <!-- Cancel without Reason -->
      <div 
        class="p-4 rounded-xl border flex flex-col bg-surface-theme print:bg-charcoal-50 print:border-charcoal-200"
        :class="quality.cancel_without_reason > 0 ? 'border-amber-500/30' : 'border-panel-theme'"
      >
        <div class="flex items-center justify-between mb-1.5">
          <span class="text-[9px] uppercase tracking-wider font-black" :class="quality.cancel_without_reason > 0 ? 'text-amber-400 print:text-orange-700' : 'text-muted-theme print:text-charcoal-500'">Batal Tanpa Alasan</span>
          <span 
            v-if="quality.cancel_without_reason > 0"
            class="text-[10px] bg-amber-500/10 text-amber-400 border border-amber-500/20 px-1.5 py-0.5 rounded font-black font-sans print:border-charcoal-250 print:text-charcoal-700"
          >
            {{ quality.cancel_without_reason }}
          </span>
          <svg v-else class="w-4 h-4 text-brand-emerald" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <p class="text-[10px] text-soft-theme font-semibold leading-normal print:text-charcoal-600">
          Proyek batal dengan kolom alasan pembatalan (cancel reason) kosong.
        </p>
      </div>

      <!-- Closed Not Paid -->
      <div 
        class="p-4 rounded-xl border flex flex-col bg-surface-theme print:bg-charcoal-50 print:border-charcoal-200"
        :class="quality.closed_not_paid > 0 ? 'border-red-500/30' : 'border-panel-theme'"
      >
        <div class="flex items-center justify-between mb-1.5">
          <span class="text-[9px] uppercase tracking-wider font-black" :class="quality.closed_not_paid > 0 ? 'text-red-400 print:text-red-700' : 'text-muted-theme print:text-charcoal-500'">Closed Belum Lunas</span>
          <span 
            v-if="quality.closed_not_paid > 0"
            class="text-[10px] bg-red-500/10 text-red-400 border border-red-500/20 px-1.5 py-0.5 rounded font-black font-sans print:border-charcoal-250 print:text-charcoal-700"
          >
            {{ quality.closed_not_paid }}
          </span>
          <svg v-else class="w-4 h-4 text-brand-emerald" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <p class="text-[10px] text-soft-theme font-semibold leading-normal print:text-charcoal-600">
          Proyek berstatus Closed tetapi pembayarannya belum berstatus Paid.
        </p>
      </div>

      <!-- Documentation Missing -->
      <div 
        class="p-4 rounded-xl border flex flex-col bg-surface-theme print:bg-charcoal-50 print:border-charcoal-200"
        :class="quality.documentation_missing > 0 ? 'border-amber-500/30' : 'border-panel-theme'"
      >
        <div class="flex items-center justify-between mb-1.5">
          <span class="text-[9px] uppercase tracking-wider font-black" :class="quality.documentation_missing > 0 ? 'text-amber-400 print:text-orange-700' : 'text-muted-theme print:text-charcoal-500'">Dokumen Kosong</span>
          <span 
            v-if="quality.documentation_missing > 0"
            class="text-[10px] bg-amber-500/10 text-amber-400 border border-amber-500/20 px-1.5 py-0.5 rounded font-black font-sans print:border-charcoal-250 print:text-charcoal-700"
          >
            {{ quality.documentation_missing }}
          </span>
          <svg v-else class="w-4 h-4 text-brand-emerald" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <p class="text-[10px] text-soft-theme font-semibold leading-normal print:text-charcoal-600">
          Proyek aktif tanpa tautan Google Drive dokumen pendukung.
        </p>
      </div>

      <!-- Unknown Event Source -->
      <div 
        class="p-4 rounded-xl border flex flex-col bg-surface-theme print:bg-charcoal-50 print:border-charcoal-200"
        :class="quality.unknown_source > 0 ? 'border-amber-500/30' : 'border-panel-theme'"
      >
        <div class="flex items-center justify-between mb-1.5">
          <span class="text-[9px] uppercase tracking-wider font-black" :class="quality.unknown_source > 0 ? 'text-amber-400 print:text-orange-700' : 'text-muted-theme print:text-charcoal-500'">Sumber Tidak Jelas</span>
          <span 
            v-if="quality.unknown_source > 0"
            class="text-[10px] bg-amber-500/10 text-amber-400 border border-amber-500/20 px-1.5 py-0.5 rounded font-black font-sans print:border-charcoal-250 print:text-charcoal-700"
          >
            {{ quality.unknown_source }}
          </span>
          <svg v-else class="w-4 h-4 text-brand-emerald" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <p class="text-[10px] text-soft-theme font-semibold leading-normal print:text-charcoal-600">
          Proyek dengan sumber event kosong atau berkategori Other/Unknown.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  quality: {
    type: Object,
    required: true,
    default: () => ({
      missing_po: 0,
      missing_pm: 0,
      missing_customer: 0,
      missing_budget: 0,
      cancel_without_reason: 0,
      closed_not_paid: 0,
      documentation_missing: 0,
      unknown_source: 0
    })
  }
})

const hasIssues = computed(() => {
  const q = props.quality
  return (
    q.missing_po > 0 ||
    q.missing_pm > 0 ||
    q.missing_customer > 0 ||
    q.missing_budget > 0 ||
    q.cancel_without_reason > 0 ||
    q.closed_not_paid > 0 ||
    q.documentation_missing > 0 ||
    q.unknown_source > 0
  )
})
</script>

<style scoped>
.glass-panel {
  background: rgba(26, 32, 44, 0.7);
  backdrop-filter: blur(12px);
}
</style>
