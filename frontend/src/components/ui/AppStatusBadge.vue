<template>
  <span 
    class="px-2.5 py-1 rounded-full text-[10px] font-extrabold uppercase tracking-wider inline-block text-center select-none"
    :class="styles"
  >
    <slot>{{ status }}</slot>
  </span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  status: { type: String, required: true },
  type: { 
    type: String, 
    default: 'project',
    validator: (v) => ['project', 'quotation', 'payment', 'priority', 'readiness'].includes(v)
  }
})

const styles = computed(() => {
  const s = props.status
  const t = props.type

  if (t === 'quotation') {
    if (s === 'Signed & Deal') return 'bg-brand-emerald/15 text-brand-emerald border border-brand-emerald/20'
    if (s === 'Cancel') return 'bg-red-500/10 text-red-400 border border-red-500/20'
    if (s === 'Draft') return 'bg-gray-600/20 text-gray-400 border border-gray-600/20'
    return 'bg-amber-500/10 text-amber-500 border border-amber-500/20' // Sent, Follow Up, Revision
  }

  if (t === 'payment') {
    if (s === 'Paid' || s === 'approved' || s === 'paid') return 'bg-brand-emerald/15 text-brand-emerald border border-brand-emerald/20'
    if (['Outstanding', 'Overdue', 'rejected', 'overdue'].includes(s)) return 'bg-red-500/10 text-red-400 border border-red-500/20'
    if (s === 'Invoice Sent' || s === 'partial' || s === 'Invoice Sent') return 'bg-indigo-500/15 text-indigo-400 border border-indigo-500/20'
    return 'bg-gray-600/20 text-gray-400 border border-gray-600/20' // Not Invoiced
  }

  if (t === 'priority') {
    if (s === 'Critical' || s === 'high' || s === 'Critical') return 'bg-red-500/20 text-red-400 border border-red-500/30 font-bold'
    if (s === 'High' || s === 'medium' || s === 'High') return 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
    if (s === 'Medium' || s === 'low' || s === 'Medium') return 'bg-brand-blue/10 text-brand-blue border border-brand-blue/20'
    return 'bg-gray-600/10 text-gray-400 border border-gray-600/20'
  }

  if (t === 'readiness') {
    const score = parseFloat(s) || 0
    if (score >= 0.8 || score >= 80) return 'bg-brand-emerald/15 text-brand-emerald border border-brand-emerald/20'
    if (score >= 0.5 || score >= 50) return 'bg-yellow-500/10 text-yellow-500 border border-yellow-500/20'
    return 'bg-red-500/10 text-red-400 border border-red-500/20'
  }

  // default to project status formatting
  const confirmed = ['Confirmed', 'Preparation', 'Ready', 'Running', 'Completed', 'Reporting', 'Closed', 'Active']
  if (confirmed.includes(s)) return 'bg-brand-emerald/15 text-brand-emerald border border-brand-emerald/20'
  if (s === 'Cancel' || s === 'Canceled') return 'bg-red-500/10 text-red-400 border border-red-500/20'
  return 'bg-brand-blue/10 text-brand-blue border border-brand-blue/20' // Inquiry, Open
})
</script>
