<template>
  <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 select-none">
    <!-- Quotation Status Summary -->
    <div class="glass-panel p-6 bg-charcoal-800 border border-charcoal-700 rounded-2xl flex flex-col">
      <h3 class="text-xs font-bold text-white tracking-widest uppercase mb-4 flex items-center gap-2">
        <span class="w-1.5 h-1.5 rounded-full bg-brand-orange"></span>
        Quotation Lifecycle Status
      </h3>
      <div class="grid grid-cols-2 sm:grid-cols-3 gap-3">
        <div 
          v-for="(count, status) in quotation.count_by_status" 
          :key="status"
          class="p-3 bg-charcoal-900/60 border border-charcoal-800 rounded-xl"
        >
          <span class="text-[9px] uppercase tracking-wider text-charcoal-400 block font-bold">{{ status }}</span>
          <span class="text-lg font-black text-white">{{ count }}</span>
        </div>
      </div>
      <div class="flex items-center justify-between mt-4 pt-3 border-t border-charcoal-700/60 text-xs font-bold">
        <span class="text-brand-emerald">Deals Won: {{ quotation.deal_count }}</span>
        <span class="text-rose-400">Cancelled/Lost: {{ quotation.cancel_count }}</span>
      </div>
    </div>

    <!-- Program Status Summary -->
    <div class="glass-panel p-6 bg-charcoal-800 border border-charcoal-700 rounded-2xl flex flex-col">
      <h3 class="text-xs font-bold text-white tracking-widest uppercase mb-4 flex items-center gap-2">
        <span class="w-1.5 h-1.5 rounded-full bg-sky-400"></span>
        Program Operations Status
      </h3>
      <div class="grid grid-cols-2 sm:grid-cols-3 gap-3">
        <div 
          v-for="(count, status) in program.count_by_status" 
          :key="status"
          class="p-3 bg-charcoal-900/60 border border-charcoal-800 rounded-xl"
        >
          <span class="text-[9px] uppercase tracking-wider text-charcoal-400 block font-bold">{{ status }}</span>
          <span class="text-lg font-black text-white">{{ count }}</span>
        </div>
      </div>
    </div>

    <!-- Payment Status Summary -->
    <div class="glass-panel p-6 bg-charcoal-800 border border-charcoal-700 rounded-2xl flex flex-col">
      <h3 class="text-xs font-bold text-white tracking-widest uppercase mb-4 flex items-center gap-2">
        <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
        Finance Billing Status
      </h3>
      <div class="grid grid-cols-2 sm:grid-cols-3 gap-3">
        <div 
          v-for="(count, status) in payment.count_by_status" 
          :key="status"
          class="p-3 bg-charcoal-900/60 border border-charcoal-800 rounded-xl"
        >
          <span class="text-[9px] uppercase tracking-wider text-charcoal-400 block font-bold">{{ status }}</span>
          <span class="text-lg font-black text-white">{{ count }}</span>
        </div>
      </div>
      <div class="flex items-center justify-between mt-4 pt-3 border-t border-charcoal-700/60 text-xs font-bold">
        <span class="text-emerald-400">Fully Paid: {{ payment.paid_count }}</span>
        <span class="text-brand-orange">Outstanding Invoices: {{ payment.outstanding_count }}</span>
        <span class="text-charcoal-400">Not Invoiced: {{ payment.not_invoiced_count }}</span>
      </div>
    </div>

    <!-- Project Status Summary -->
    <div class="glass-panel p-6 bg-charcoal-800 border border-charcoal-700 rounded-2xl flex flex-col">
      <h3 class="text-xs font-bold text-white tracking-widest uppercase mb-4 flex items-center gap-2">
        <span class="w-1.5 h-1.5 rounded-full bg-purple-400"></span>
        Overall Project Status
      </h3>
      <div class="grid grid-cols-2 sm:grid-cols-3 gap-3">
        <div 
          v-for="(count, status) in project.count_by_status" 
          :key="status"
          class="p-3 bg-charcoal-900/60 border border-charcoal-800 rounded-xl"
        >
          <span class="text-[9px] uppercase tracking-wider text-charcoal-400 block font-bold">{{ status }}</span>
          <span class="text-lg font-black text-white">{{ count }}</span>
        </div>
      </div>
      <div class="flex items-center justify-between mt-4 pt-3 border-t border-charcoal-700/60 text-xs font-bold">
        <span class="text-sky-400">Active Workloads: {{ project.active_count }}</span>
        <span class="text-purple-400">In Reporting: {{ project.reporting_count }}</span>
        <span class="text-emerald-400">Closed Projects: {{ project.closed_count }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  quotation: {
    type: Object,
    required: true
  },
  program: {
    type: Object,
    required: true
  },
  payment: {
    type: Object,
    required: true
  },
  project: {
    type: Object,
    required: true
  }
})
</script>

<style scoped>
.glass-panel {
  background: rgba(26, 32, 44, 0.7);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}
</style>
