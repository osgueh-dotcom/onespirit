<template>
  <div class="glass-panel p-6 bg-charcoal-800 border border-charcoal-700 rounded-2xl flex flex-col select-none">
    <div class="flex items-center justify-between mb-4 border-b border-charcoal-700 pb-3">
      <div class="flex flex-col">
        <h3 class="text-xs font-bold text-white tracking-widest uppercase flex items-center gap-2">
          <span class="w-1.5 h-1.5 rounded-full bg-brand-orange animate-pulse"></span>
          Operational Data Quality & Integrity Audits
        </h3>
        <span class="text-[9px] text-charcoal-400 font-semibold mt-0.5">Identifies workflow and mapping inconsistencies in active records</span>
      </div>
      <div 
        class="text-[10px] uppercase font-black px-2.5 py-1 rounded"
        :class="hasIssues ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20' : 'bg-brand-emerald/10 text-brand-emerald border border-brand-emerald/20'"
      >
        {{ hasIssues ? 'Inconsistencies Detected' : 'Data Integrity Nominal' }}
      </div>
    </div>

    <!-- Perfect Data Quality State -->
    <div 
      v-if="!hasIssues" 
      class="py-12 flex flex-col items-center justify-center text-center gap-3 bg-charcoal-900/40 border border-charcoal-800 rounded-xl"
    >
      <div class="w-10 h-10 rounded-full bg-brand-emerald/15 flex items-center justify-center text-brand-emerald">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="3" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
        </svg>
      </div>
      <div>
        <p class="text-xs text-white font-bold">100% Data Integrity Score</p>
        <p class="text-[10px] text-charcoal-400 font-semibold mt-0.5">No missing owners, invalid budgets, or untagged sources found.</p>
      </div>
    </div>

    <!-- Issues Checklist Grid -->
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
      <!-- Missing PO -->
      <div 
        class="p-4 rounded-xl border flex flex-col bg-charcoal-900/40"
        :class="quality.missing_po > 0 ? 'border-amber-500/30' : 'border-charcoal-800'"
      >
        <div class="flex items-center justify-between mb-1.5">
          <span class="text-[9px] uppercase tracking-wider font-black" :class="quality.missing_po > 0 ? 'text-amber-400' : 'text-charcoal-400'">Missing PO</span>
          <span 
            v-if="quality.missing_po > 0"
            class="text-[10px] bg-amber-500/10 text-amber-400 border border-amber-500/20 px-1.5 py-0.5 rounded font-black font-sans"
          >
            {{ quality.missing_po }}
          </span>
          <svg v-else class="w-4 h-4 text-brand-emerald" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <p class="text-[10px] text-charcoal-300 font-semibold leading-normal">
          Active projects that do not have a Program Owner assigned.
        </p>
      </div>

      <!-- Missing PM -->
      <div 
        class="p-4 rounded-xl border flex flex-col bg-charcoal-900/40"
        :class="quality.missing_pm > 0 ? 'border-amber-500/30' : 'border-charcoal-800'"
      >
        <div class="flex items-center justify-between mb-1.5">
          <span class="text-[9px] uppercase tracking-wider font-black" :class="quality.missing_pm > 0 ? 'text-amber-400' : 'text-charcoal-400'">Missing PM</span>
          <span 
            v-if="quality.missing_pm > 0"
            class="text-[10px] bg-amber-500/10 text-amber-400 border border-amber-500/20 px-1.5 py-0.5 rounded font-black font-sans"
          >
            {{ quality.missing_pm }}
          </span>
          <svg v-else class="w-4 h-4 text-brand-emerald" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <p class="text-[10px] text-charcoal-300 font-semibold leading-normal">
          Active projects that do not have a Program Manager assigned.
        </p>
      </div>

      <!-- Missing Customer -->
      <div 
        class="p-4 rounded-xl border flex flex-col bg-charcoal-900/40"
        :class="quality.missing_customer > 0 ? 'border-red-500/30' : 'border-charcoal-800'"
      >
        <div class="flex items-center justify-between mb-1.5">
          <span class="text-[9px] uppercase tracking-wider font-black" :class="quality.missing_customer > 0 ? 'text-red-400' : 'text-charcoal-400'">Missing Customer</span>
          <span 
            v-if="quality.missing_customer > 0"
            class="text-[10px] bg-red-500/10 text-red-400 border border-red-500/20 px-1.5 py-0.5 rounded font-black font-sans"
          >
            {{ quality.missing_customer }}
          </span>
          <svg v-else class="w-4 h-4 text-brand-emerald" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <p class="text-[10px] text-charcoal-300 font-semibold leading-normal">
          Projects without any associated client or partner profile.
        </p>
      </div>

      <!-- Missing Budget -->
      <div 
        class="p-4 rounded-xl border flex flex-col bg-charcoal-900/40"
        :class="quality.missing_budget > 0 ? 'border-amber-500/30' : 'border-charcoal-800'"
      >
        <div class="flex items-center justify-between mb-1.5">
          <span class="text-[9px] uppercase tracking-wider font-black" :class="quality.missing_budget > 0 ? 'text-amber-400' : 'text-charcoal-400'">Missing Budget</span>
          <span 
            v-if="quality.missing_budget > 0"
            class="text-[10px] bg-amber-500/10 text-amber-400 border border-amber-500/20 px-1.5 py-0.5 rounded font-black font-sans"
          >
            {{ quality.missing_budget }}
          </span>
          <svg v-else class="w-4 h-4 text-brand-emerald" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <p class="text-[10px] text-charcoal-300 font-semibold leading-normal">
          Active or signed projects with no budget allocated or budget <= 0.
        </p>
      </div>

      <!-- Cancel without Reason -->
      <div 
        class="p-4 rounded-xl border flex flex-col bg-charcoal-900/40"
        :class="quality.cancel_without_reason > 0 ? 'border-amber-500/30' : 'border-charcoal-800'"
      >
        <div class="flex items-center justify-between mb-1.5">
          <span class="text-[9px] uppercase tracking-wider font-black" :class="quality.cancel_without_reason > 0 ? 'text-amber-400' : 'text-charcoal-400'">Cancel w/o Reason</span>
          <span 
            v-if="quality.cancel_without_reason > 0"
            class="text-[10px] bg-amber-500/10 text-amber-400 border border-amber-500/20 px-1.5 py-0.5 rounded font-black font-sans"
          >
            {{ quality.cancel_without_reason }}
          </span>
          <svg v-else class="w-4 h-4 text-brand-emerald" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <p class="text-[10px] text-charcoal-300 font-semibold leading-normal">
          Canceled quotations with empty cancellation notes.
        </p>
      </div>

      <!-- Closed Not Paid -->
      <div 
        class="p-4 rounded-xl border flex flex-col bg-charcoal-900/40"
        :class="quality.closed_not_paid > 0 ? 'border-red-500/30' : 'border-charcoal-800'"
      >
        <div class="flex items-center justify-between mb-1.5">
          <span class="text-[9px] uppercase tracking-wider font-black" :class="quality.closed_not_paid > 0 ? 'text-red-400' : 'text-charcoal-400'">Closed Not Paid</span>
          <span 
            v-if="quality.closed_not_paid > 0"
            class="text-[10px] bg-red-500/10 text-red-400 border border-red-500/20 px-1.5 py-0.5 rounded font-black font-sans"
          >
            {{ quality.closed_not_paid }}
          </span>
          <svg v-else class="w-4 h-4 text-brand-emerald" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <p class="text-[10px] text-charcoal-300 font-semibold leading-normal">
          Projects marked Closed but payment is not marked Paid.
        </p>
      </div>

      <!-- Documentation Missing -->
      <div 
        class="p-4 rounded-xl border flex flex-col bg-charcoal-900/40"
        :class="quality.documentation_missing > 0 ? 'border-amber-500/30' : 'border-charcoal-800'"
      >
        <div class="flex items-center justify-between mb-1.5">
          <span class="text-[9px] uppercase tracking-wider font-black" :class="quality.documentation_missing > 0 ? 'text-amber-400' : 'text-charcoal-400'">No Documents</span>
          <span 
            v-if="quality.documentation_missing > 0"
            class="text-[10px] bg-amber-500/10 text-amber-400 border border-amber-500/20 px-1.5 py-0.5 rounded font-black font-sans"
          >
            {{ quality.documentation_missing }}
          </span>
          <svg v-else class="w-4 h-4 text-brand-emerald" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <p class="text-[10px] text-charcoal-300 font-semibold leading-normal">
          Projects with no Google Drive assets or contracts linked.
        </p>
      </div>

      <!-- Unknown Event Source -->
      <div 
        class="p-4 rounded-xl border flex flex-col bg-charcoal-900/40"
        :class="quality.unknown_source > 0 ? 'border-amber-500/30' : 'border-charcoal-800'"
      >
        <div class="flex items-center justify-between mb-1.5">
          <span class="text-[9px] uppercase tracking-wider font-black" :class="quality.unknown_source > 0 ? 'text-amber-400' : 'text-charcoal-400'">Unknown Source</span>
          <span 
            v-if="quality.unknown_source > 0"
            class="text-[10px] bg-amber-500/10 text-amber-400 border border-amber-500/20 px-1.5 py-0.5 rounded font-black font-sans"
          >
            {{ quality.unknown_source }}
          </span>
          <svg v-else class="w-4 h-4 text-brand-emerald" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <p class="text-[10px] text-charcoal-300 font-semibold leading-normal">
          Projects with no source, or type set to Other or Unknown.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  quality: {
    type: Object,
    required: true,
    default: () => ({
      missing_po: 0,
      missing_pm: 0,
      missing_customer: 0,
      missing_budget: 0,
      cancel_without_reason: 0,
      closed_not_paid: 0,
      documentation_missing: 0,
      unknown_source: 0
    })
  }
})

const hasIssues = computed(() => {
  const q = props.quality
  return (
    q.missing_po > 0 ||
    q.missing_pm > 0 ||
    q.missing_customer > 0 ||
    q.missing_budget > 0 ||
    q.cancel_without_reason > 0 ||
    q.closed_not_paid > 0 ||
    q.documentation_missing > 0 ||
    q.unknown_source > 0
  )
})
</script>

<style scoped>
.glass-panel {
  background: rgba(26, 32, 44, 0.7);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}
</style>
