<template>
  <div class="glass-panel p-6 bg-charcoal-800 border border-charcoal-700 rounded-3xl space-y-6 select-none print:bg-white print:border print:border-charcoal-200 print:rounded-xl print:p-5">
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-charcoal-700/60 pb-4 print:border-charcoal-200">
      <div>
        <h3 class="text-xs font-bold text-brand-orange uppercase tracking-widest flex items-center gap-2 print:text-charcoal-900 print:text-sm">
          <span class="w-1.5 h-1.5 rounded-full bg-brand-orange print:hidden"></span>
          Ringkasan Keuangan & Pembayaran (Finance & Payment Summary)
        </h3>
        <p class="text-[10px] text-charcoal-400 font-bold tracking-wider mt-0.5 print:text-charcoal-500">
          Evaluasi Billing, Kolektibilitas Pembayaran, dan Status Invoice
        </p>
      </div>
      <span class="text-[9px] font-extrabold uppercase px-2.5 py-1 bg-amber-500/10 text-amber-400 rounded-lg print:border print:border-charcoal-200 print:text-charcoal-700 print:bg-charcoal-50">
        Finance Review
      </span>
    </div>

    <!-- Empty State -->
    <div v-if="!hasData" class="py-8 text-center text-xs font-bold text-charcoal-500 print:text-charcoal-400">
      Belum ada data keuangan untuk periode atau filter yang dipilih.
    </div>

    <div v-else class="space-y-6">
      <!-- 1. Key Financial Metrics -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 print:grid-cols-4 print:gap-3">
        <!-- Confirmed Revenue -->
        <div class="p-4 bg-charcoal-900/40 border border-charcoal-700/60 rounded-2xl print:bg-charcoal-50 print:border print:border-charcoal-200">
          <span class="text-[9px] uppercase tracking-wider text-charcoal-400 block font-bold print:text-charcoal-500">Confirmed Revenue</span>
          <span class="text-base font-black text-brand-emerald block mt-1 print:text-emerald-700">{{ formatMoney(executive.confirmed_revenue) }}</span>
          <span class="text-[8px] text-charcoal-500 font-semibold block mt-1 print:text-charcoal-400">Nilai proyek terkonfirmasi</span>
        </div>

        <!-- Received Cash -->
        <div class="p-4 bg-charcoal-900/40 border border-charcoal-700/60 rounded-2xl print:bg-charcoal-50 print:border print:border-charcoal-200">
          <span class="text-[9px] uppercase tracking-wider text-charcoal-400 block font-bold print:text-charcoal-500">Actually Received Cash</span>
          <span class="text-base font-black text-white block mt-1 print:text-charcoal-900">{{ formatMoney(executive.revenue_received) }}</span>
          <span class="text-[8px] text-charcoal-500 font-semibold block mt-1 print:text-charcoal-400">Dana masuk (approved payments)</span>
        </div>

        <!-- Collection Rate -->
        <div class="p-4 bg-charcoal-900/40 border border-charcoal-700/60 rounded-2xl print:bg-charcoal-50 print:border print:border-charcoal-200">
          <span class="text-[9px] uppercase tracking-wider text-charcoal-400 block font-bold print:text-charcoal-500">Collection Rate</span>
          <span class="text-base font-black text-sky-400 block mt-1 print:text-sky-700">{{ formatPercent(executive.collection_rate) }}</span>
          <span class="text-[8px] text-charcoal-500 font-semibold block mt-1 print:text-charcoal-400">Rasio penerimaan dana</span>
        </div>

        <!-- Outstanding Amount -->
        <div class="p-4 bg-charcoal-900/40 border border-charcoal-700/60 rounded-2xl print:bg-charcoal-50 print:border print:border-charcoal-200">
          <span class="text-[9px] uppercase tracking-wider text-charcoal-400 block font-bold print:text-charcoal-500">Outstanding Amount</span>
          <span class="text-base font-black text-rose-400 block mt-1 print:text-red-700">{{ formatMoney(executive.outstanding_amount) }}</span>
          <span class="text-[8px] text-charcoal-500 font-semibold block mt-1 print:text-charcoal-400">Sisa piutang tertagih</span>
        </div>
      </div>

      <!-- 2. Billing Status Counts -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 print:grid-cols-2 print:gap-4">
        <!-- Status summary stats -->
        <div class="space-y-3.5">
          <h4 class="text-[10px] font-black uppercase text-charcoal-400 tracking-wider print:text-charcoal-800">
            Rincian Status Pembayaran (Billing Breakdown)
          </h4>
          <div class="grid grid-cols-2 gap-3">
            <div class="p-3 bg-charcoal-900/60 border border-charcoal-800 rounded-xl flex items-center justify-between print:bg-charcoal-50 print:border-charcoal-200">
              <span class="text-[9px] font-bold text-charcoal-400 uppercase print:text-charcoal-500">Paid In Full</span>
              <span class="text-sm font-black text-white print:text-charcoal-900">{{ payment.paid_count || 0 }}</span>
            </div>
            <div class="p-3 bg-charcoal-900/60 border border-charcoal-800 rounded-xl flex items-center justify-between print:bg-charcoal-50 print:border-charcoal-200">
              <span class="text-[9px] font-bold text-charcoal-400 uppercase print:text-charcoal-500">Outstanding Invoices</span>
              <span class="text-sm font-black text-white print:text-charcoal-900">{{ payment.outstanding_count || 0 }}</span>
            </div>
            <div class="p-3 bg-charcoal-900/60 border border-charcoal-800 rounded-xl flex items-center justify-between print:bg-charcoal-50 print:border-charcoal-200">
              <span class="text-[9px] font-bold text-charcoal-400 uppercase print:text-charcoal-500">Invoice Sent</span>
              <span class="text-sm font-black text-white print:text-charcoal-900">{{ payment.invoice_sent_count || 0 }}</span>
            </div>
            <div class="p-3 bg-charcoal-900/60 border border-charcoal-800 rounded-xl flex items-center justify-between print:bg-charcoal-50 print:border-charcoal-200">
              <span class="text-[9px] font-bold text-charcoal-400 uppercase print:text-charcoal-500">Not Invoiced Yet</span>
              <span class="text-sm font-black text-white print:text-charcoal-900">{{ payment.not_invoiced_count || 0 }}</span>
            </div>
          </div>
        </div>

        <!-- Billing distribution list -->
        <div class="space-y-3.5">
          <h4 class="text-[10px] font-black uppercase text-charcoal-400 tracking-wider print:text-charcoal-800">
            Distribusi Pembayaran (Payment Status Distribution)
          </h4>
          <div class="space-y-2 border border-charcoal-700/50 p-3.5 rounded-2xl bg-charcoal-900/20 print:border-charcoal-200 print:bg-transparent">
            <div 
              v-for="(count, status) in payment.count_by_status" 
              :key="status"
              class="flex items-center justify-between text-xs font-bold"
            >
              <div class="flex items-center gap-2">
                <span :class="[
                  'w-1.5 h-1.5 rounded-full shrink-0',
                  status === 'Paid' ? 'bg-brand-emerald' : 
                  status === 'Outstanding' || status === 'Overdue' ? 'bg-rose-400' : 'bg-charcoal-400'
                ]"></span>
                <span class="text-charcoal-300 print:text-charcoal-700">{{ status }}</span>
              </div>
              <span class="text-white print:text-charcoal-900">{{ count || 0 }}</span>
            </div>
            <div v-if="!payment.count_by_status || Object.keys(payment.count_by_status).length === 0" class="text-center text-[10px] text-charcoal-500 font-bold py-2">
              Tidak ada data distribusi status pembayaran.
            </div>
          </div>
        </div>
      </div>

      <!-- Disclaimer Refinement Note -->
      <div class="flex items-start gap-2.5 p-3 bg-brand-orange/5 border border-brand-orange/20 rounded-2xl text-[10px] font-bold text-charcoal-300 print:bg-transparent print:border-none print:p-0">
        <svg class="w-4 h-4 text-brand-orange shrink-0 mt-0.5 print:hidden" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <div class="space-y-0.5">
          <span class="text-[8px] uppercase tracking-wider text-brand-orange font-black print:text-charcoal-700">Catatan Evaluasi Keuangan</span>
          <p class="leading-normal font-semibold">Nominal paid/outstanding akan diperkuat pada fase finance refinement.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  payment: {
    type: Object,
    required: true,
    default: () => ({ count_by_status: {}, paid_count: 0, outstanding_count: 0, invoice_sent_count: 0, not_invoiced_count: 0 })
  },
  executive: {
    type: Object,
    required: true,
    default: () => ({ confirmed_revenue: 0, revenue_received: 0, collection_rate: 0, outstanding_amount: 0 })
  }
})

const hasData = computed(() => {
  return props.executive && (props.executive.confirmed_revenue > 0 || props.executive.revenue_received > 0)
})

const formatMoney = (val) => {
  if (val === undefined || val === null || isNaN(val)) return 'Rp0'
  return 'Rp' + Math.round(val).toLocaleString('id-ID')
}

const formatPercent = (val) => {
  if (val === undefined || val === null || isNaN(val)) return '0,0%'
  return Number(val).toFixed(2).replace('.', ',') + '%'
}
</script>

<style scoped>
.glass-panel {
  background: rgba(26, 32, 44, 0.7);
  backdrop-filter: blur(12px);
}
</style>
