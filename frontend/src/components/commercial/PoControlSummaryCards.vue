<template>
  <div class="space-y-6">
    <!-- KPI Cards Summary -->
    <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-4 select-none">
      <div class="glass-panel p-4 border border-brand-charcoal-light/25 bg-gradient-to-tr from-brand-charcoal-dark/30 to-brand-charcoal/20">
        <p class="text-[9px] font-extrabold uppercase tracking-widest text-gray-500 mb-1">Total Proyek</p>
        <div class="flex items-baseline gap-2">
          <span class="text-xl font-black text-white">{{ summary.total_owned_projects }}</span>
          <span class="text-[9px] text-gray-400 font-bold">Proyek</span>
        </div>
      </div>

      <div class="glass-panel p-4 border border-brand-charcoal-light/25 bg-gradient-to-tr from-brand-charcoal-dark/30 to-brand-charcoal/20">
        <p class="text-[9px] font-extrabold uppercase tracking-widest text-gray-500 mb-1">Total Deal</p>
        <div class="flex items-baseline gap-2">
          <span class="text-xl font-black text-brand-emerald">{{ summary.total_deal }}</span>
          <span class="text-[9px] text-brand-emerald font-bold">Proyek</span>
        </div>
      </div>

      <div class="glass-panel p-4 border border-brand-charcoal-light/25 bg-gradient-to-tr from-brand-charcoal-dark/30 to-brand-charcoal/20">
        <p class="text-[9px] font-extrabold uppercase tracking-widest text-gray-500 mb-1">Total Batal</p>
        <div class="flex items-baseline gap-2">
          <span class="text-xl font-black text-red-400">{{ summary.total_cancel }}</span>
          <span class="text-[9px] text-red-400 font-bold">Proyek</span>
        </div>
      </div>

      <div class="glass-panel p-4 border border-brand-charcoal-light/25 bg-gradient-to-tr from-brand-charcoal-dark/30 to-brand-charcoal/20">
        <p class="text-[9px] font-extrabold uppercase tracking-widest text-gray-500 mb-1">Deal Rate</p>
        <div class="flex items-baseline gap-2">
          <span class="text-xl font-black text-indigo-400">{{ Math.round(summary.deal_rate || 0) }}%</span>
        </div>
      </div>

      <div class="glass-panel p-4 border border-brand-charcoal-light/25 bg-gradient-to-tr from-brand-charcoal-dark/30 to-brand-charcoal/20 lg:col-span-2">
        <p class="text-[9px] font-extrabold uppercase tracking-widest text-gray-500 mb-1">Potential Revenue</p>
        <div class="flex items-baseline gap-2">
          <span class="text-sm font-black text-white truncate select-all">{{ formatCurrency(summary.potential_revenue) }}</span>
        </div>
      </div>

      <div class="glass-panel p-4 border border-brand-charcoal-light/25 bg-gradient-to-tr from-brand-charcoal-dark/30 to-brand-charcoal/20 lg:col-span-2">
        <p class="text-[9px] font-extrabold uppercase tracking-widest text-gray-500 mb-1">Confirmed Revenue</p>
        <div class="flex items-baseline gap-2">
          <span class="text-sm font-black text-brand-emerald truncate select-all">{{ formatCurrency(summary.confirmed_revenue) }}</span>
        </div>
      </div>
    </div>

    <!-- Second Row KPI Summary Cards -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 select-none">
      <div class="glass-panel p-4 border border-brand-charcoal-light/25 bg-gradient-to-tr from-brand-charcoal-dark/30 to-brand-charcoal/20">
        <p class="text-[9px] font-extrabold uppercase tracking-widest text-gray-500 mb-1">Outstanding Pembayaran</p>
        <div class="flex flex-col">
          <span class="text-sm font-black text-amber-500 truncate select-all">{{ formatCurrency(summary.outstanding_payment) }}</span>
          <span class="text-[9px] text-gray-400 font-semibold mt-0.5">({{ summary.outstanding_count }} Klien)</span>
        </div>
      </div>

      <div class="glass-panel p-4 border border-brand-charcoal-light/25 bg-gradient-to-tr from-brand-charcoal-dark/30 to-brand-charcoal/20">
        <p class="text-[9px] font-extrabold uppercase tracking-widest text-gray-500 mb-1">Invoice Sent (Belum Paid)</p>
        <div class="flex items-baseline gap-2">
          <span class="text-xl font-black text-indigo-400">{{ summary.invoice_sent_count }}</span>
          <span class="text-[9px] text-indigo-400 font-bold">Tagihan</span>
        </div>
      </div>

      <div class="glass-panel p-4 border border-brand-charcoal-light/25 bg-gradient-to-tr from-brand-charcoal-dark/30 to-brand-charcoal/20">
        <p class="text-[9px] font-extrabold uppercase tracking-widest text-gray-500 mb-1">Invoice Paid (Lunas)</p>
        <div class="flex items-baseline gap-2">
          <span class="text-xl font-black text-brand-emerald">{{ summary.paid_count }}</span>
          <span class="text-[9px] text-brand-emerald font-bold">Lunas</span>
        </div>
      </div>

      <div class="glass-panel p-4 border border-brand-charcoal-light/25 bg-gradient-to-tr from-brand-charcoal-dark/30 to-brand-charcoal/20">
        <p class="text-[9px] font-extrabold uppercase tracking-widest text-gray-500 mb-1">Follow-up Diperlukan</p>
        <div class="flex items-baseline gap-2">
          <span class="text-xl font-black text-red-400">{{ summary.follow_up_needed_count }}</span>
          <span class="text-[9px] text-red-400 font-bold">Tindakan</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  summary: {
    type: Object,
    required: true
  }
})

const formatCurrency = (val) => {
  if (val === null || val === undefined) return 'Rp 0'
  return 'Rp ' + Number(val).toLocaleString('id-ID', { minimumFractionDigits: 0, maximumFractionDigits: 0 })
}
</script>

<style scoped>
.glass-panel {
  background: rgba(26, 32, 44, 0.75);
  backdrop-filter: blur(12px);
  border-radius: 1.25rem;
}
</style>
