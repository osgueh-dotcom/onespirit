<template>
  <div class="glass-panel p-6 max-h-[500px] overflow-y-auto flex flex-col">
    <h3 class="text-sm font-bold text-white tracking-wider uppercase mb-5 shrink-0 select-none">Workflow Audit Trail (Status Timeline)</h3>
    
    <div class="flex-1 space-y-5 pr-1 relative pl-4 border-l border-brand-charcoal-light/25">
      <div v-if="logs.length === 0" class="h-full flex items-center justify-center text-xs font-semibold text-gray-500 select-none">
        No status timeline shifts logged.
      </div>
      <div 
        v-for="log in logs" 
        :key="log.id"
        class="relative text-xs font-medium"
      >
        <!-- Timeline connector node -->
        <span class="absolute -left-6.5 top-1.5 h-3.5 w-3.5 rounded-full bg-brand-charcoal border-2 border-brand-orange shrink-0"></span>
        
        <p class="font-extrabold text-white">
          <span class="text-brand-orange uppercase font-bold">[{{ log.status_type || 'program_status' }}]</span>: 
          Shifted from 
          <span class="text-gray-400 lowercase italic">{{ log.old_status || log.from_status || '-' }}</span> to 
          <span class="text-brand-orange uppercase font-bold">{{ log.new_status || log.to_status }}</span>
        </p>
        <p class="text-[10px] text-gray-400 mt-0.5">
          Changed by: {{ log.changed_by_user?.full_name || log.changed_by?.full_name || 'System' }} | Timestamp: {{ formatDateTime(log.created_at) }}
        </p>
        <p v-if="log.notes" class="p-2.5 bg-brand-charcoal-light/10 border border-brand-charcoal-light/15 rounded-xl text-gray-300 mt-2 leading-relaxed">
          {{ log.notes }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  logs: {
    type: Array,
    required: true
  }
})

const formatDateTime = (val) => {
  if (!val) return '-'
  return new Date(val).toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>
