<template>
  <div class="glass-panel p-6 bg-charcoal-800 border border-charcoal-700 rounded-2xl flex flex-col select-none">
    <div class="flex items-center justify-between mb-4">
      <h3 class="text-xs font-bold text-white tracking-widest uppercase flex items-center gap-2">
        <span class="w-1.5 h-1.5 rounded-full bg-sky-400"></span>
        Program Manager (PM) Workload Balance
      </h3>
    </div>
    
    <div class="overflow-x-auto custom-scrollbar">
      <table class="w-full text-left text-xs font-bold border-collapse">
        <thead>
          <tr class="border-b border-charcoal-700 text-charcoal-400 uppercase tracking-widest text-[9px]">
            <th class="pb-3 pl-2">Name</th>
            <th class="pb-3 text-center">Initials</th>
            <th class="pb-3 text-center">Total Projects</th>
            <th class="pb-3 text-center">Active</th>
            <th class="pb-3 text-center">Preparation</th>
            <th class="pb-3 text-center">Running</th>
            <th class="pb-3 text-center">Reporting</th>
            <th class="pb-3 text-center pr-2">Closed</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="data.length === 0">
            <td colspan="8" class="py-8 text-center text-charcoal-500 font-bold">
              No Program Manager workload data matching filters.
            </td>
          </tr>
          <tr 
            v-for="pm in data" 
            :key="pm.pm_id"
            class="border-b border-charcoal-700/60 hover:bg-charcoal-900/30 transition-all"
          >
            <td class="py-3.5 pl-2 text-white">{{ pm.pm_name }}</td>
            <td class="py-3.5 text-center">
              <span class="px-2 py-0.5 bg-charcoal-700 border border-charcoal-600 rounded text-sky-400">
                {{ pm.initial_code || 'N/A' }}
              </span>
            </td>
            <td class="py-3.5 text-center text-white">{{ pm.total_projects }}</td>
            <td class="py-3.5 text-center text-amber-400">{{ pm.active_count }}</td>
            <td class="py-3.5 text-center text-sky-400">{{ pm.preparation_count }}</td>
            <td class="py-3.5 text-center text-brand-orange">{{ pm.running_count }}</td>
            <td class="py-3.5 text-center text-purple-400">{{ pm.reporting_count }}</td>
            <td class="py-3.5 text-center text-brand-emerald pr-2">{{ pm.closed_count }}</td>
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
  -webkit-backdrop-filter: blur(12px);
}
.custom-scrollbar::-webkit-scrollbar {
  height: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.15);
  border-radius: 2px;
}
</style>
