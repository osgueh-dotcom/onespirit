<template>
  <div class="p-6 bg-gradient-to-r from-brand-charcoal to-brand-charcoal-light/45 border border-brand-charcoal-light/35 rounded-3xl relative overflow-hidden select-none flex flex-col md:flex-row md:items-center justify-between gap-6 print:bg-white print:border-none print:p-0 print:rounded-none">
    <div class="absolute top-0 right-0 -mt-8 -mr-8 w-48 h-48 bg-brand-orange/5 rounded-full blur-3xl pointer-events-none print:hidden"></div>
    
    <div class="space-y-1">
      <h2 class="text-2xl font-black text-white tracking-wide print:text-charcoal-900 print:text-3xl">Executive Dashboard</h2>
      <p class="text-xs text-brand-orange font-bold flex items-center gap-1.5 print:text-charcoal-500 print:text-sm">
        <span class="h-1.5 w-1.5 rounded-full bg-brand-emerald animate-ping print:hidden"></span>
        One Spirit Workflow & Business Analytics
      </p>
      
      <!-- Printed Active Filter context info block -->
      <p class="text-[10px] text-charcoal-400 font-semibold pt-1 hidden print:block">
        Filter Periode: {{ getFilterSummary() }} | Diunduh pada: {{ timestamp }}
      </p>
    </div>

    <div class="flex items-center gap-4 self-start md:self-auto print:hidden">
      <!-- Last updated block -->
      <div class="bg-charcoal-800/80 border border-charcoal-700/80 py-2 px-4 rounded-2xl flex items-center gap-3">
        <span class="w-2 h-2 rounded-full bg-brand-emerald animate-pulse"></span>
        <div class="flex flex-col">
          <span class="text-[9px] uppercase tracking-wider text-charcoal-400 font-bold">Last Sync</span>
          <span class="text-xs font-bold text-white">{{ timestamp }}</span>
        </div>
      </div>
      
      <!-- Print/Save Report action button -->
      <button 
        @click="$emit('print')"
        class="py-3 px-5 bg-brand-orange hover:bg-brand-orange-light text-white text-xs font-black uppercase tracking-wider rounded-2xl flex items-center gap-2 transition-all duration-300 hover:scale-[1.02] active:scale-[0.98] shadow-lg shadow-brand-orange/20"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M6.72 13.829c-.24.03-.48.062-.72.096m.72-.096a42.415 42.415 0 0110.56 0m-10.56 0L6.34 18m10.94-4.171c.24.03.48.062.72.096m-.72-.096L17.66 18m0 0l.229 2.523a1.125 1.125 0 01-1.12 1.227H7.231c-.662 0-1.18-.568-1.12-1.227L6.34 18m11.318-4.171a3 3 0 000-5.658L17.67 5.83a2.25 2.25 0 00-1.979-1.956 41.302 41.302 0 00-7.382 0 2.25 2.25 0 00-1.98 1.956L6.33 8.172a3 3 0 000 5.658m11.318-4.17h.008v.008H17.67V8.172zm-11.336 0H6.33v.008h.008V8.17z" />
        </svg>
        Print / Save Report
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({
  filters: {
    type: Object,
    required: true,
    default: () => ({})
  }
})

const emit = defineEmits(['print'])
const timestamp = ref('')

const updateTimestamp = () => {
  const now = new Date()
  timestamp.value = now.toLocaleTimeString('id-ID', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  }) + ' (' + now.toLocaleDateString('id-ID', {
    day: 'numeric',
    month: 'short',
    year: 'numeric'
  }) + ')'
}

const getFilterSummary = () => {
  const parts = []
  if (props.filters.year) parts.push(`Tahun ${props.filters.year}`)
  if (props.filters.month) {
    const monthName = new Date(2000, props.filters.month - 1).toLocaleString('id-ID', { month: 'long' })
    parts.push(monthName)
  }
  if (props.filters.date_from && props.filters.date_to) {
    parts.push(`${props.filters.date_from} s.d. ${props.filters.date_to}`)
  } else if (props.filters.date_from) {
    parts.push(`Mulai ${props.filters.date_from}`)
  } else if (props.filters.date_to) {
    parts.push(`Hingga ${props.filters.date_to}`)
  }
  if (props.filters.po_id) parts.push("Filtered by PO")
  if (props.filters.pm_id) parts.push("Filtered by PM")
  if (props.filters.source_type) parts.push(`Source: ${props.filters.source_type}`)
  if (props.filters.customer_category) parts.push(`Customer: ${props.filters.customer_category}`)
  
  return parts.length > 0 ? parts.join(', ') : 'Semua Periode / No Filter'
}

onMounted(() => {
  updateTimestamp()
  setInterval(updateTimestamp, 60000)
})
</script>

<style scoped>
@media print {
  .p-6 {
    padding: 0 !important;
  }
}
</style>
