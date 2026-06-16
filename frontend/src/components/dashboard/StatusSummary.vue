<template>
  <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 select-none print:grid-cols-3 print:gap-4 print:text-charcoal-900">
    <!-- Quotation Status Summary -->
    <div class="glass-panel p-6 flex flex-col print:bg-white print:border print:border-charcoal-200 print:rounded-xl">
      <h3 class="text-xs font-bold text-main-theme tracking-widest uppercase mb-4 flex items-center gap-2 print:text-charcoal-900 print:text-sm">
        <span class="w-1.5 h-1.5 rounded-full bg-brand-orange print:hidden"></span>
        Quotation Lifecycle Status
      </h3>
      <div class="grid grid-cols-2 sm:grid-cols-3 gap-3">
        <div 
          v-for="(count, status) in quotation.count_by_status" 
          :key="status"
          class="p-3 bg-surface-theme border border-panel-theme rounded-xl print:bg-charcoal-50 print:border print:border-charcoal-200"
        >
          <span class="text-[9px] uppercase tracking-wider text-muted-theme block font-bold print:text-charcoal-500">{{ status }}</span>
          <span class="text-lg font-black text-main-theme print:text-charcoal-900">{{ count }}</span>
        </div>
      </div>
      <div class="flex items-center justify-between mt-4 pt-3 border-t border-panel-theme text-xs font-bold print:border-charcoal-200 print:text-charcoal-700">
        <span class="text-brand-emerald print:text-emerald-700">Deals Won: {{ quotation.deal_count }}</span>
        <span class="text-rose-400 print:text-red-700">Cancelled/Lost: {{ quotation.cancel_count }}</span>
      </div>
    </div>

    <!-- Program Status Summary -->
    <div class="glass-panel p-6 flex flex-col print:bg-white print:border print:border-charcoal-200 print:rounded-xl">
      <h3 class="text-xs font-bold text-main-theme tracking-widest uppercase mb-4 flex items-center gap-2 print:text-charcoal-900 print:text-sm">
        <span class="w-1.5 h-1.5 rounded-full bg-sky-400 print:hidden"></span>
        Program Operations Status
      </h3>
      <div class="grid grid-cols-2 sm:grid-cols-3 gap-3">
        <div 
          v-for="(count, status) in program.count_by_status" 
          :key="status"
          class="p-3 bg-surface-theme border border-panel-theme rounded-xl print:bg-charcoal-50 print:border print:border-charcoal-200"
        >
          <span class="text-[9px] uppercase tracking-wider text-muted-theme block font-bold print:text-charcoal-500">{{ status }}</span>
          <span class="text-lg font-black text-main-theme print:text-charcoal-900">{{ count }}</span>
        </div>
      </div>
    </div>

    <!-- Project Status Summary -->
    <div class="glass-panel p-6 flex flex-col print:bg-white print:border print:border-charcoal-200 print:rounded-xl">
      <h3 class="text-xs font-bold text-main-theme tracking-widest uppercase mb-4 flex items-center gap-2 print:text-charcoal-900 print:text-sm">
        <span class="w-1.5 h-1.5 rounded-full bg-purple-400 print:hidden"></span>
        Overall Project Status
      </h3>
      <div class="grid grid-cols-2 sm:grid-cols-3 gap-3">
        <div 
          v-for="(count, status) in project.count_by_status" 
          :key="status"
          class="p-3 bg-surface-theme border border-panel-theme rounded-xl print:bg-charcoal-50 print:border print:border-charcoal-200"
        >
          <span class="text-[9px] uppercase tracking-wider text-muted-theme block font-bold print:text-charcoal-500">{{ status }}</span>
          <span class="text-lg font-black text-main-theme print:text-charcoal-900">{{ count }}</span>
        </div>
      </div>
      <div class="flex items-center justify-between mt-4 pt-3 border-t border-panel-theme text-xs font-bold print:border-charcoal-200 print:text-charcoal-700">
        <span class="text-sky-400 print:text-sky-700">Active: {{ project.active_count }}</span>
        <span class="text-purple-400 print:text-purple-700">Reporting: {{ project.reporting_count }}</span>
        <span class="text-emerald-400 print:text-emerald-700">Closed: {{ project.closed_count }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  quotation: {
    type: Object,
    required: true,
    default: () => ({ count_by_status: {}, deal_count: 0, cancel_count: 0 })
  },
  program: {
    type: Object,
    required: true,
    default: () => ({ count_by_status: {} })
  },
  project: {
    type: Object,
    required: true,
    default: () => ({ count_by_status: {}, active_count: 0, reporting_count: 0, closed_count: 0 })
  }
})
</script>

<style scoped>
.glass-panel {
  background: rgba(26, 32, 44, 0.7);
  backdrop-filter: blur(12px);
}
</style>
