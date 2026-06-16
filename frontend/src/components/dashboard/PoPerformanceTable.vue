<template>
  <div class="glass-panel p-6 flex flex-col select-none print:bg-white print:border print:border-charcoal-200 print:rounded-xl print:p-5">
    <div class="flex items-center justify-between mb-4">
      <h3 class="text-xs font-bold text-main-theme tracking-widest uppercase flex items-center gap-2 print:text-charcoal-900 print:text-sm">
        <span class="w-1.5 h-1.5 rounded-full bg-brand-orange print:hidden"></span>
        Review Performa Program Owner (PO)
      </h3>
    </div>
    
    <div class="overflow-x-auto custom-scrollbar">
      <table class="w-full text-left text-xs font-bold border-collapse print:text-charcoal-900">
        <thead>
          <tr class="border-b border-panel-theme text-muted-theme uppercase tracking-widest text-[9px] print:border-charcoal-200 print:text-charcoal-500">
            <th class="pb-3 pl-2">Nama</th>
            <th class="pb-3 text-center">Inisial</th>
            <th class="pb-3 text-center">Total Proyek</th>
            <th class="pb-3 text-center">Deal</th>
            <th class="pb-3 text-center">Batal</th>
            <th class="pb-3 text-right">Confirmed Revenue</th>
            <th class="pb-3 text-right">Rata-rata Anggaran</th>
            <th class="pb-3 text-center pr-2">Selesai</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="data.length === 0">
            <td colspan="8" class="py-8 text-center text-muted-theme font-bold print:text-charcoal-400">
              Belum ada data untuk periode atau filter yang dipilih.
            </td>
          </tr>
          <tr 
            v-for="po in data" 
            :key="po.po_id"
            class="app-table-row border-b border-panel-theme print:border-charcoal-200 print:hover:bg-transparent"
          >
            <td class="py-3.5 pl-2 text-main-theme print:text-charcoal-900">{{ po.po_name }}</td>
            <td class="py-3.5 text-center">
              <span class="px-2 py-0.5 bg-surface-theme border border-panel-theme rounded text-brand-orange print:bg-charcoal-50 print:border-charcoal-200 print:text-orange-700">
                {{ po.initial_code || '-' }}
              </span>
            </td>
            <td class="py-3.5 text-center text-soft-theme print:text-charcoal-800">{{ po.total_projects }}</td>
            <td class="py-3.5 text-center text-brand-emerald print:text-emerald-700">{{ po.deal_count }}</td>
            <td class="py-3.5 text-center text-rose-400 print:text-red-700">{{ po.cancel_count }}</td>
            <td class="py-3.5 text-right text-brand-emerald font-sans print:text-emerald-700">{{ formatMoney(po.confirmed_revenue) }}</td>
            <td class="py-3.5 text-right text-sky-400 font-sans print:text-sky-700">{{ formatMoney(po.average_budget) }}</td>
            <td class="py-3.5 text-center text-purple-400 pr-2 print:text-purple-700">{{ po.closed_count }}</td>
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

const formatMoney = (val) => {
  if (val === undefined || val === null || isNaN(val)) return 'Rp0'
  return 'Rp' + Math.round(val).toLocaleString('id-ID')
}
</script>

<style scoped>
.glass-panel {
  background: rgba(26, 32, 44, 0.7);
  backdrop-filter: blur(12px);
}
</style>
