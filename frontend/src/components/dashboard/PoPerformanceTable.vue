<template>
  <div class="glass-panel p-6 bg-charcoal-800 border border-charcoal-700 rounded-2xl flex flex-col select-none print:bg-white print:border print:border-charcoal-200 print:rounded-xl print:p-5">
    <div class="flex items-center justify-between mb-4">
      <h3 class="text-xs font-bold text-white tracking-widest uppercase flex items-center gap-2 print:text-charcoal-900 print:text-sm">
        <span class="w-1.5 h-1.5 rounded-full bg-brand-orange print:hidden"></span>
        Program Owner (PO) Performance Review
      </h3>
    </div>
    
    <div class="overflow-x-auto custom-scrollbar">
      <table class="w-full text-left text-xs font-bold border-collapse print:text-charcoal-900">
        <thead>
          <tr class="border-b border-charcoal-700 text-charcoal-400 uppercase tracking-widest text-[9px] print:border-charcoal-200 print:text-charcoal-500">
            <th class="pb-3 pl-2">Name</th>
            <th class="pb-3 text-center">Initials</th>
            <th class="pb-3 text-center">Projects</th>
            <th class="pb-3 text-center">Deals Won</th>
            <th class="pb-3 text-center">Cancelled</th>
            <th class="pb-3 text-right">Confirmed Revenue</th>
            <th class="pb-3 text-right">Avg Budget</th>
            <th class="pb-3 text-center pr-2">Closed</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="data.length === 0">
            <td colspan="8" class="py-8 text-center text-charcoal-500 font-bold print:text-charcoal-400">
              No Program Owner performance data matching filters.
            </td>
          </tr>
          <tr 
            v-for="po in data" 
            :key="po.po_id"
            class="border-b border-charcoal-700/60 hover:bg-charcoal-900/30 transition-all print:border-charcoal-200 print:hover:bg-transparent"
          >
            <td class="py-3.5 pl-2 text-white print:text-charcoal-900">{{ po.po_name }}</td>
            <td class="py-3.5 text-center">
              <span class="px-2 py-0.5 bg-charcoal-700 border border-charcoal-600 rounded text-brand-orange print:bg-charcoal-50 print:border-charcoal-200 print:text-orange-700">
                {{ po.initial_code || 'N/A' }}
              </span>
            </td>
            <td class="py-3.5 text-center text-charcoal-200 print:text-charcoal-800">{{ po.total_projects }}</td>
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
