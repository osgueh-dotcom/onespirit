<template>
  <div class="glass-panel p-6 max-h-[500px] overflow-y-auto flex flex-col">
    <h3 class="text-sm font-bold text-white tracking-wider uppercase mb-5 shrink-0 select-none">Operational Activity Ledger</h3>
    
    <div class="flex-1 space-y-5 pr-1 relative pl-4 border-l border-brand-charcoal-light/25">
      <div v-if="activityLogs.length === 0" class="h-full flex items-center justify-center text-xs font-semibold text-gray-500 select-none">
        No operational activities logged.
      </div>
      <div 
        v-for="act in activityLogs" 
        :key="act.id"
        class="relative text-xs font-medium"
      >
        <!-- Timeline connector node -->
        <span class="absolute -left-6.5 top-1.5 h-3.5 w-3.5 rounded-full bg-brand-charcoal border-2 border-brand-emerald shrink-0"></span>
        
        <p class="font-extrabold text-white">
          <span class="text-brand-emerald uppercase font-bold">{{ formatAction(act.action) }}</span>
          <span v-if="act.field_name"> for field <span class="text-gray-300 italic">{{ act.field_name }}</span></span>
        </p>
        <div v-if="act.old_value || act.new_value" class="text-[11px] text-gray-400 mt-1 font-semibold">
          <span class="text-red-400">{{ act.old_value || '-' }}</span> &rarr; <span class="text-brand-emerald">{{ act.new_value || '-' }}</span>
        </div>
        <p class="text-[10px] text-gray-400 mt-0.5">
          Executor: {{ act.user?.full_name || 'System' }} | Timestamp: {{ formatDateTime(act.created_at) }}
        </p>
        <p v-if="act.notes" class="p-2.5 bg-brand-charcoal-light/10 border border-brand-charcoal-light/15 rounded-xl text-gray-300 mt-2 leading-relaxed">
          {{ act.notes }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  activityLogs: {
    type: Array,
    required: true
  }
})

const formatAction = (action) => {
  if (!action) return ''
  return action.replace(/_/g, ' ').toUpperCase()
}

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
