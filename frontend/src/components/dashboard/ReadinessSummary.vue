<template>
  <div class="glass-panel p-6 bg-charcoal-800 border border-charcoal-700 rounded-2xl select-none print:bg-white print:border print:border-charcoal-200 print:rounded-xl print:p-5">
    <h3 class="text-xs font-bold text-white tracking-widest uppercase flex items-center gap-2 mb-5 print:text-charcoal-900 print:text-sm">
      <span class="w-1.5 h-1.5 rounded-full bg-brand-orange print:hidden"></span>
      Ringkasan Kesiapan Operasional Event (Readiness Summary)
    </h3>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
      <!-- 1. Average Readiness Score -->
      <div class="bg-charcoal-900/40 border border-charcoal-700/60 p-4 rounded-xl flex flex-col justify-between print:bg-transparent print:border-charcoal-200">
        <div>
          <p class="text-[9px] font-extrabold uppercase tracking-widest text-charcoal-400 mb-1">Rata-Rata Kesiapan</p>
          <h4 class="text-2xl font-black text-brand-orange">{{ formatPercent(summary.average_readiness_score) }}</h4>
        </div>
        <p class="text-[10px] text-charcoal-400 mt-2 font-medium">Skor kumulatif seluruh proyek</p>
      </div>

      <!-- 2. Ready vs Not Ready -->
      <div class="bg-charcoal-900/40 border border-charcoal-700/60 p-4 rounded-xl flex flex-col justify-between print:bg-transparent print:border-charcoal-200">
        <div>
          <p class="text-[9px] font-extrabold uppercase tracking-widest text-charcoal-400 mb-1">Status Kesiapan Proyek</p>
          <div class="flex items-center gap-4 mt-1">
            <div>
              <p class="text-xs font-bold text-brand-emerald">Ready</p>
              <h4 class="text-lg font-black text-white">{{ summary.projects_ready_count || 0 }}</h4>
            </div>
            <div class="border-l border-charcoal-700/60 pl-4 h-8 print:border-charcoal-200"></div>
            <div>
              <p class="text-xs font-bold text-red-400">Belum Ready</p>
              <h4 class="text-lg font-black text-white">{{ summary.projects_not_ready_count || 0 }}</h4>
            </div>
          </div>
        </div>
        <p class="text-[10px] text-charcoal-400 mt-2 font-medium">Batas aman kesiapan: >= 80%</p>
      </div>

      <!-- 3. Upcoming & Overdue Events -->
      <div class="bg-charcoal-900/40 border border-charcoal-700/60 p-4 rounded-xl flex flex-col justify-between print:bg-transparent print:border-charcoal-200">
        <div>
          <p class="text-[9px] font-extrabold uppercase tracking-widest text-charcoal-400 mb-1">Timeline & Urgensi Event</p>
          <div class="flex items-center gap-4 mt-1">
            <div>
              <p class="text-xs font-bold text-brand-blue">Upcoming (7H)</p>
              <h4 class="text-lg font-black text-white">{{ summary.upcoming_events_7_days || 0 }}</h4>
            </div>
            <div class="border-l border-charcoal-700/60 pl-4 h-8 print:border-charcoal-200"></div>
            <div>
              <p class="text-xs font-bold text-red-400">Terlambat (Overdue)</p>
              <h4 class="text-lg font-black text-white">{{ summary.overdue_events || 0 }}</h4>
            </div>
          </div>
        </div>
        <p class="text-[10px] text-charcoal-400 mt-2 font-medium">Event lewat jadwal & belum closed</p>
      </div>

      <!-- 4. Operational Checklist Issues -->
      <div class="bg-charcoal-900/40 border border-charcoal-700/60 p-4 rounded-xl flex flex-col justify-between print:bg-transparent print:border-charcoal-200">
        <div>
          <p class="text-[9px] font-extrabold uppercase tracking-widest text-charcoal-400 mb-1">Defisit Dokumen & Revisi</p>
          <div class="flex items-center gap-4 mt-1">
            <div>
              <p class="text-xs font-bold text-red-400">Overdue Inst</p>
              <h4 class="text-lg font-black text-white">{{ summary.total_overdue_instruments || 0 }}</h4>
            </div>
            <div class="border-l border-charcoal-700/60 pl-4 h-8 print:border-charcoal-200"></div>
            <div>
              <p class="text-xs font-bold text-rose-400">Butuh Revisi</p>
              <h4 class="text-lg font-black text-white">{{ summary.total_need_revision_instruments || 0 }}</h4>
            </div>
          </div>
        </div>
        <p class="text-[10px] text-charcoal-400 mt-2 font-medium">Instrumen checklist bermasalah</p>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  summary: {
    type: Object,
    required: true,
    default: () => ({
      projects_ready_count: 0,
      projects_not_ready_count: 0,
      average_readiness_score: 0.0,
      upcoming_events_7_days: 0,
      overdue_events: 0,
      events_missing_readiness_items: 0,
      total_overdue_instruments: 0,
      total_need_revision_instruments: 0
    })
  }
})

const formatPercent = (val) => {
  if (val === undefined || val === null || isNaN(val)) return '0%'
  return Math.round(val) + '%'
}
</script>

<style scoped>
.glass-panel {
  background: rgba(26, 32, 44, 0.7);
  backdrop-filter: blur(12px);
}
</style>
