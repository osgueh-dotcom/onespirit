<template>
  <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 select-none print:grid-cols-2 print:gap-4 print:text-charcoal-900">
    <!-- Event Source Breakdown -->
    <div class="glass-panel p-6 flex flex-col h-[350px] print:bg-white print:border print:border-charcoal-200 print:rounded-xl print:h-auto print:p-5">
      <h3 class="text-xs font-bold text-main-theme tracking-widest uppercase mb-4 flex items-center gap-2 print:text-charcoal-900 print:text-sm">
        <span class="w-1.5 h-1.5 rounded-full bg-brand-orange print:hidden"></span>
        Analitik Sumber Event (Event Source Analytics)
      </h3>
      <div class="flex-1 overflow-y-auto space-y-4 pr-1 custom-scrollbar print:overflow-visible print:h-auto">
        <div v-if="sources.length === 0" class="text-center py-12 text-muted-theme font-bold print:text-charcoal-400">
          Belum ada data untuk periode atau filter yang dipilih.
        </div>
        <div 
          v-for="src in sources" 
          :key="src.source_type"
          class="space-y-1.5"
        >
          <div class="flex justify-between text-xs font-bold print:text-charcoal-950">
            <span class="text-soft-theme print:text-charcoal-800">{{ src.source_type }} ({{ src.total_projects }} Proj)</span>
            <span class="text-main-theme print:text-charcoal-900">Confirmed: {{ formatMoney(src.confirmed_revenue) }}</span>
          </div>
          <div class="h-2 w-full bg-surface-theme rounded-full overflow-hidden print:bg-charcoal-100">
            <div 
              class="h-full bg-brand-orange transition-all duration-300 print:bg-orange-600"
              :style="`width: ${calculatePercentage(src.confirmed_revenue, totalConfirmedRevenue)}%`"
            ></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Customer Category Breakdown -->
    <div class="glass-panel p-6 flex flex-col h-[350px] print:bg-white print:border print:border-charcoal-200 print:rounded-xl print:h-auto print:p-5">
      <h3 class="text-xs font-bold text-main-theme tracking-widest uppercase mb-4 flex items-center gap-2 print:text-charcoal-900 print:text-sm">
        <span class="w-1.5 h-1.5 rounded-full bg-sky-400 print:hidden"></span>
        Rasio Kategori Pelanggan (Customer Category Shares)
      </h3>
      <div class="flex-1 overflow-y-auto space-y-4 pr-1 custom-scrollbar print:overflow-visible print:h-auto">
        <div v-if="customers.length === 0" class="text-center py-12 text-muted-theme font-bold print:text-charcoal-400">
          Belum ada data untuk periode atau filter yang dipilih.
        </div>
        <div 
          v-for="cust in customers" 
          :key="cust.customer_category"
          class="space-y-1.5"
        >
          <div class="flex justify-between text-xs font-bold print:text-charcoal-950">
            <span class="text-soft-theme print:text-charcoal-800">{{ cust.customer_category }} ({{ cust.total_projects }} Proj)</span>
            <span class="text-main-theme print:text-charcoal-900">Confirmed: {{ formatMoney(cust.confirmed_revenue) }}</span>
          </div>
          <div class="h-2 w-full bg-surface-theme rounded-full overflow-hidden print:bg-charcoal-100">
            <div 
              class="h-full bg-sky-400 transition-all duration-300 print:bg-sky-600"
              :style="`width: ${calculatePercentage(cust.confirmed_revenue, totalConfirmedRevenue)}%`"
            ></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Event Category Breakdown -->
    <div class="glass-panel p-6 flex flex-col h-[350px] print:bg-white print:border print:border-charcoal-200 print:rounded-xl print:h-auto print:p-5">
      <h3 class="text-xs font-bold text-main-theme tracking-widest uppercase mb-4 flex items-center gap-2 print:text-charcoal-900 print:text-sm">
        <span class="w-1.5 h-1.5 rounded-full bg-purple-400 print:hidden"></span>
        Analitik Kategori Event (Event Category Breakdown)
      </h3>
      <div class="flex-1 overflow-y-auto space-y-4 pr-1 custom-scrollbar print:overflow-visible print:h-auto">
        <div v-if="eventCategories.length === 0" class="text-center py-12 text-muted-theme font-bold print:text-charcoal-400">
          Belum ada data untuk periode atau filter yang dipilih.
        </div>
        <div 
          v-for="ev in eventCategories" 
          :key="ev.event_category"
          class="space-y-1.5"
        >
          <div class="flex justify-between text-xs font-bold print:text-charcoal-950">
            <span class="text-soft-theme print:text-charcoal-800">{{ ev.event_category }} ({{ ev.total_projects }} Proj)</span>
            <span class="text-main-theme print:text-charcoal-900">{{ formatMoney(ev.confirmed_revenue) }}</span>
          </div>
          <div class="h-2 w-full bg-surface-theme rounded-full overflow-hidden print:bg-charcoal-100">
            <div 
              class="h-full bg-purple-400 transition-all duration-300 print:bg-purple-600"
              :style="`width: ${calculatePercentage(ev.confirmed_revenue, totalConfirmedRevenue)}%`"
            ></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Program Type Breakdown -->
    <div class="glass-panel p-6 flex flex-col h-[350px] print:bg-white print:border print:border-charcoal-200 print:rounded-xl print:h-auto print:p-5">
      <h3 class="text-xs font-bold text-main-theme tracking-widest uppercase mb-4 flex items-center gap-2 print:text-charcoal-900 print:text-sm">
        <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 print:hidden"></span>
        Analitik Tipe Program (Program Type Analytics)
      </h3>
      <div class="flex-1 overflow-y-auto space-y-4 pr-1 custom-scrollbar print:overflow-visible print:h-auto">
        <div v-if="programTypes.length === 0" class="text-center py-12 text-muted-theme font-bold print:text-charcoal-400">
          Belum ada data untuk periode atau filter yang dipilih.
        </div>
        <div 
          v-for="prog in programTypes" 
          :key="prog.program_type"
          class="space-y-1.5"
        >
          <div class="flex justify-between text-xs font-bold print:text-charcoal-950">
            <span class="text-soft-theme print:text-charcoal-800">{{ prog.program_type }} ({{ prog.total_projects }} Proj)</span>
            <span class="text-main-theme print:text-charcoal-900">{{ formatMoney(prog.confirmed_revenue) }}</span>
          </div>
          <div class="h-2 w-full bg-surface-theme rounded-full overflow-hidden print:bg-charcoal-100">
            <div 
              class="h-full bg-emerald-400 transition-all duration-300 print:bg-emerald-600"
              :style="`width: ${calculatePercentage(prog.confirmed_revenue, totalConfirmedRevenue)}%`"
            ></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  sources: {
    type: Array,
    required: true,
    default: () => []
  },
  customers: {
    type: Array,
    required: true,
    default: () => []
  },
  eventCategories: {
    type: Array,
    required: true,
    default: () => []
  },
  programTypes: {
    type: Array,
    required: true,
    default: () => []
  }
})

const totalConfirmedRevenue = computed(() => {
  return props.sources.reduce((acc, src) => acc + (src.confirmed_revenue || 0.0), 0.0)
})

const formatMoney = (val) => {
  if (val === undefined || val === null || isNaN(val)) return 'Rp0'
  return 'Rp' + Math.round(val).toLocaleString('id-ID')
}

const calculatePercentage = (part, total) => {
  if (!total || total <= 0) return 0
  return Math.round((part / total) * 100)
}
</script>

<style scoped>
.glass-panel {
  background: rgba(26, 32, 44, 0.7);
  backdrop-filter: blur(12px);
}
</style>
