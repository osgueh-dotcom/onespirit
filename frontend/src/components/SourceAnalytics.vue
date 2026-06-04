<template>
  <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 select-none">
    <!-- Event Source Breakdown -->
    <div class="glass-panel p-6 bg-charcoal-800 border border-charcoal-700 rounded-2xl flex flex-col h-[350px]">
      <h3 class="text-xs font-bold text-white tracking-widest uppercase mb-4 flex items-center gap-2">
        <span class="w-1.5 h-1.5 rounded-full bg-brand-orange"></span>
        Event Source Analytics
      </h3>
      <div class="flex-1 overflow-y-auto space-y-4 pr-1 custom-scrollbar">
        <div v-if="sources.length === 0" class="text-center py-12 text-charcoal-500 font-bold">
          No Event Source data available.
        </div>
        <div 
          v-for="src in sources" 
          :key="src.source_type"
          class="space-y-1.5"
        >
          <div class="flex justify-between text-xs font-bold">
            <span class="text-charcoal-200">{{ src.source_type }} ({{ src.total_projects }} Proj)</span>
            <span class="text-white">Confirmed: {{ formatMoney(src.confirmed_revenue) }}</span>
          </div>
          <div class="h-2 w-full bg-charcoal-900 rounded-full overflow-hidden">
            <div 
              class="h-full bg-brand-orange transition-all duration-300"
              :style="`width: ${calculatePercentage(src.confirmed_revenue, totalConfirmedRevenue)}%`"
            ></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Customer Category Breakdown -->
    <div class="glass-panel p-6 bg-charcoal-800 border border-charcoal-700 rounded-2xl flex flex-col h-[350px]">
      <h3 class="text-xs font-bold text-white tracking-widest uppercase mb-4 flex items-center gap-2">
        <span class="w-1.5 h-1.5 rounded-full bg-sky-400"></span>
        Customer Category Shares
      </h3>
      <div class="flex-1 overflow-y-auto space-y-4 pr-1 custom-scrollbar">
        <div v-if="customers.length === 0" class="text-center py-12 text-charcoal-500 font-bold">
          No Customer Category data available.
        </div>
        <div 
          v-for="cust in customers" 
          :key="cust.customer_category"
          class="space-y-1.5"
        >
          <div class="flex justify-between text-xs font-bold">
            <span class="text-charcoal-200">{{ cust.customer_category }} ({{ cust.total_projects }} Proj)</span>
            <span class="text-white">Confirmed: {{ formatMoney(cust.confirmed_revenue) }}</span>
          </div>
          <div class="h-2 w-full bg-charcoal-900 rounded-full overflow-hidden">
            <div 
              class="h-full bg-sky-400 transition-all duration-300"
              :style="`width: ${calculatePercentage(cust.confirmed_revenue, totalConfirmedRevenue)}%`"
            ></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Event Category Breakdown -->
    <div class="glass-panel p-6 bg-charcoal-800 border border-charcoal-700 rounded-2xl flex flex-col h-[350px]">
      <h3 class="text-xs font-bold text-white tracking-widest uppercase mb-4 flex items-center gap-2">
        <span class="w-1.5 h-1.5 rounded-full bg-purple-400"></span>
        Event Category Breakdown
      </h3>
      <div class="flex-1 overflow-y-auto space-y-4 pr-1 custom-scrollbar">
        <div v-if="eventCategories.length === 0" class="text-center py-12 text-charcoal-500 font-bold">
          No Event Category data available.
        </div>
        <div 
          v-for="ev in eventCategories" 
          :key="ev.event_category"
          class="space-y-1.5"
        >
          <div class="flex justify-between text-xs font-bold">
            <span class="text-charcoal-200">{{ ev.event_category }} ({{ ev.total_projects }} Proj)</span>
            <span class="text-white">{{ formatMoney(ev.confirmed_revenue) }}</span>
          </div>
          <div class="h-2 w-full bg-charcoal-900 rounded-full overflow-hidden">
            <div 
              class="h-full bg-purple-400 transition-all duration-300"
              :style="`width: ${calculatePercentage(ev.confirmed_revenue, totalConfirmedRevenue)}%`"
            ></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Program Type Breakdown -->
    <div class="glass-panel p-6 bg-charcoal-800 border border-charcoal-700 rounded-2xl flex flex-col h-[350px]">
      <h3 class="text-xs font-bold text-white tracking-widest uppercase mb-4 flex items-center gap-2">
        <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
        Program Type Analytics
      </h3>
      <div class="flex-1 overflow-y-auto space-y-4 pr-1 custom-scrollbar">
        <div v-if="programTypes.length === 0" class="text-center py-12 text-charcoal-500 font-bold">
          No Program Type data available.
        </div>
        <div 
          v-for="prog in programTypes" 
          :key="prog.program_type"
          class="space-y-1.5"
        >
          <div class="flex justify-between text-xs font-bold">
            <span class="text-charcoal-200">{{ prog.program_type }} ({{ prog.total_projects }} Proj)</span>
            <span class="text-white">{{ formatMoney(prog.confirmed_revenue) }}</span>
          </div>
          <div class="h-2 w-full bg-charcoal-900 rounded-full overflow-hidden">
            <div 
              class="h-full bg-emerald-400 transition-all duration-300"
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
  if (val >= 1e9) {
    return 'Rp ' + (val / 1e9).toFixed(2) + ' B'
  }
  if (val >= 1e6) {
    return 'Rp ' + (val / 1e6).toFixed(1) + ' M'
  }
  return 'Rp ' + Number(val || 0).toLocaleString('id-ID')
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
  -webkit-backdrop-filter: blur(12px);
}
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.15);
  border-radius: 2px;
}
</style>
