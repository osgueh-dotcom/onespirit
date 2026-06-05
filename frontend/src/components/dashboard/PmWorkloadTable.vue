<template>
  <div class="glass-panel p-6 bg-charcoal-800 border border-charcoal-700 rounded-2xl flex flex-col select-none print:bg-white print:border print:border-charcoal-200 print:rounded-xl print:p-5">
    <div class="flex items-center justify-between mb-4">
      <h3 class="text-xs font-bold text-white tracking-widest uppercase flex items-center gap-2 print:text-charcoal-900 print:text-sm">
        <span class="w-1.5 h-1.5 rounded-full bg-sky-400 print:hidden"></span>
        Review Beban Kerja Program Manager (PM)
      </h3>
    </div>
    
    <div class="overflow-x-auto custom-scrollbar">
      <table class="w-full text-left text-xs font-bold border-collapse print:text-charcoal-900">
        <thead>
          <tr class="border-b border-charcoal-700 text-charcoal-400 uppercase tracking-widest text-[9px] print:border-charcoal-200 print:text-charcoal-500">
            <th class="pb-3 pl-2">Nama</th>
            <th class="pb-3 text-center">Inisial</th>
            <th class="pb-3 text-center">Total Proyek</th>
            <th class="pb-3 text-center">Aktif</th>
            <th class="pb-3 text-center">Persiapan</th>
            <th class="pb-3 text-center">Running</th>
            <th class="pb-3 text-center">Pelaporan</th>
            <th class="pb-3 text-center pr-2">Selesai</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="data.length === 0">
            <td colspan="8" class="py-8 text-center text-charcoal-500 font-bold print:text-charcoal-400">
              Belum ada data untuk periode atau filter yang dipilih.
            </td>
          </tr>
          <tr 
            v-for="pm in data" 
            :key="pm.pm_id"
            class="border-b border-charcoal-700/60 hover:bg-charcoal-900/30 transition-all print:border-charcoal-200 print:hover:bg-transparent"
          >
            <td class="py-3.5 pl-2 text-white print:text-charcoal-900">{{ pm.pm_name }}</td>
            <td class="py-3.5 text-center">
              <span class="px-2 py-0.5 bg-charcoal-700 border border-charcoal-600 rounded text-sky-400 print:bg-charcoal-50 print:border-charcoal-200 print:text-sky-700">
                {{ pm.initial_code || '-' }}
              </span>
            </td>
            <td class="py-3.5 text-center text-white print:text-charcoal-900">{{ pm.total_projects }}</td>
            <td class="py-3.5 text-center text-amber-400 print:text-amber-700">{{ pm.active_count }}</td>
            <td class="py-3.5 text-center text-sky-400 print:text-sky-700">{{ pm.preparation_count }}</td>
            <td class="py-3.5 text-center text-brand-orange print:text-orange-700">{{ pm.running_count }}</td>
            <td class="py-3.5 text-center text-purple-400 print:text-purple-700">{{ pm.reporting_count }}</td>
            <td class="py-3.5 text-center text-brand-emerald pr-2 print:text-emerald-700">{{ pm.closed_count }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
defineProps({
  data: {
    type: Array,
    required: true,
    default: () => []
  }
})
</script>

<style scoped>
.glass-panel {
  background: rgba(26, 32, 44, 0.7);
  backdrop-filter: blur(12px);
}
</style>
