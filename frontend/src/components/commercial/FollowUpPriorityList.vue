<template>
  <div class="glass-panel p-5 border border-brand-charcoal-light/20 space-y-4">
    <div class="flex items-center justify-between">
      <h3 class="text-sm font-bold text-white uppercase tracking-wider">Prioritas Tindakan Follow-up</h3>
      <span class="text-[10px] font-bold text-gray-400 bg-brand-charcoal-light/20 px-2 py-0.5 rounded">
        Aksi komersial mendesak berdasarkan sisa hari event, nilai budget, dan resiko pembayaran
      </span>
    </div>

    <div v-if="priorities.length === 0" class="py-12 text-center text-xs text-gray-500 font-semibold">
      Tidak ada prioritas follow-up terdeteksi. Semua quotation dan penagihan terpantau aman.
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div 
        v-for="(act, idx) in priorities" 
        :key="idx"
        class="p-4 rounded-2xl border flex flex-col justify-between gap-3 text-xs group"
        :class="getPrioClass(act.priority_level)"
      >
        <div>
          <div class="flex items-center justify-between border-b border-brand-charcoal-light/10 pb-2 mb-2 select-none">
            <span class="font-bold font-mono tracking-wider">{{ act.project_code || 'UNCODED' }}</span>
            <span class="px-2 py-0.5 rounded text-[8px] font-black uppercase" :class="getPrioBadgeClass(act.priority_level)">
              {{ act.priority_level }}
            </span>
          </div>
          <h4 class="font-bold text-white text-sm mb-1 leading-snug group-hover:text-brand-orange transition-colors">
            {{ act.program_name }}
          </h4>
          <p class="text-gray-400 font-semibold text-[10px] mb-1">Klien: {{ act.customer_name }} • Budget: {{ formatCurrency(act.budget) }}</p>
          <p class="text-gray-300 font-semibold text-[11px] mb-2">{{ act.reason }}</p>
          
          <div class="bg-black/20 p-2.5 rounded-xl border border-white/5 space-y-1">
            <p class="text-[9px] font-black text-brand-orange uppercase tracking-wider select-none">Rekomendasi Aksi:</p>
            <p class="text-white font-bold leading-normal">{{ act.recommended_action }}</p>
          </div>
        </div>
        <div class="pt-2 flex justify-end">
          <router-link 
            :to="'/projects/' + act.project_id"
            class="px-3 py-1.5 rounded bg-white/10 hover:bg-white/20 text-white font-bold text-[10px] transition-all"
          >
            Buka Proyek →
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  priorities: {
    type: Array,
    required: true
  }
})

// Formatting helpers
const formatCurrency = (val) => {
  if (val === null || val === undefined) return 'Rp 0'
  return 'Rp ' + Number(val).toLocaleString('id-ID', { minimumFractionDigits: 0, maximumFractionDigits: 0 })
}

// Priority Action class helpers
const getPrioClass = (prio) => {
  if (prio === 'Critical') return 'bg-red-500/10 border-red-500/30 text-white shadow-lg shadow-red-500/5'
  if (prio === 'High') return 'bg-amber-500/10 border-amber-500/30 text-white'
  if (prio === 'Medium') return 'bg-brand-blue/10 border-brand-blue/30 text-white'
  return 'bg-brand-charcoal/40 border-brand-charcoal-light/20 text-gray-400'
}

const getPrioBadgeClass = (prio) => {
  if (prio === 'Critical') return 'bg-red-500 text-white'
  if (prio === 'High') return 'bg-amber-500 text-black'
  if (prio === 'Medium') return 'bg-brand-blue text-white'
  return 'bg-gray-600 text-white'
}
</script>

<style scoped>
.glass-panel {
  background: rgba(26, 32, 44, 0.75);
  backdrop-filter: blur(12px);
  border-radius: 1.25rem;
}
</style>
