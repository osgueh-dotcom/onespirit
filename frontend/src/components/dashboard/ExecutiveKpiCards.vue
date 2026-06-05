<template>
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5 select-none print:grid-cols-3 print:gap-4 print:text-charcoal-900">
    <!-- 1. Total Inquiry -->
    <div class="interactive-card p-5 relative overflow-hidden bg-charcoal-800 border border-charcoal-700 rounded-2xl print:bg-white print:border print:border-charcoal-200 print:rounded-xl">
      <div class="absolute -top-10 -right-10 w-24 h-24 bg-brand-orange/5 rounded-full blur-2xl print:hidden"></div>
      <p class="text-[9px] font-extrabold uppercase tracking-widest text-charcoal-400 mb-1 print:text-charcoal-500">Total Inquiry (Records)</p>
      <h3 class="text-3xl font-black text-white font-sans print:text-charcoal-900">
        {{ executive.total_inquiry || 0 }}
      </h3>
      <span class="inline-flex mt-3 text-[10px] font-bold text-brand-orange px-2.5 py-1 bg-brand-orange/10 rounded-lg print:border print:border-charcoal-200 print:text-charcoal-700 print:bg-charcoal-50">
        Incoming Events
      </span>
    </div>

    <!-- 2. Total Deal -->
    <div class="interactive-card p-5 relative overflow-hidden bg-charcoal-800 border border-charcoal-700 rounded-2xl print:bg-white print:border print:border-charcoal-200 print:rounded-xl">
      <div class="absolute -top-10 -right-10 w-24 h-24 bg-brand-emerald/5 rounded-full blur-2xl print:hidden"></div>
      <p class="text-[9px] font-extrabold uppercase tracking-widest text-charcoal-400 mb-1 print:text-charcoal-500">Total Project Deal</p>
      <h3 class="text-3xl font-black text-brand-emerald font-sans print:text-emerald-700">
        {{ executive.total_deal || 0 }}
      </h3>
      <span class="inline-flex mt-3 text-[10px] font-bold text-brand-emerald px-2.5 py-1 bg-brand-emerald/10 rounded-lg print:border print:border-charcoal-200 print:text-emerald-800 print:bg-charcoal-50">
        Signed Agreements
      </span>
    </div>

    <!-- 3. Deal Rate -->
    <div class="interactive-card p-5 relative overflow-hidden bg-charcoal-800 border border-charcoal-700 rounded-2xl print:bg-white print:border print:border-charcoal-200 print:rounded-xl">
      <div class="absolute -top-10 -right-10 w-24 h-24 bg-brand-emerald/5 rounded-full blur-2xl print:hidden"></div>
      <p class="text-[9px] font-extrabold uppercase tracking-widest text-charcoal-400 mb-1 print:text-charcoal-500">Deal Conversion Rate</p>
      <h3 class="text-3xl font-black text-brand-emerald font-sans print:text-emerald-700">
        {{ (executive.deal_rate || 0).toFixed(1) }}%
      </h3>
      <span class="inline-flex mt-3 text-[10px] font-bold text-charcoal-400 print:text-charcoal-600">
        Deal / Total inquiry
      </span>
    </div>

    <!-- 4. Cancel Rate -->
    <div class="interactive-card p-5 relative overflow-hidden bg-charcoal-800 border border-charcoal-700 rounded-2xl print:bg-white print:border print:border-charcoal-200 print:rounded-xl">
      <div class="absolute -top-10 -right-10 w-24 h-24 bg-red-500/5 rounded-full blur-2xl print:hidden"></div>
      <p class="text-[9px] font-extrabold uppercase tracking-widest text-charcoal-400 mb-1 print:text-charcoal-500">Cancellation Rate</p>
      <h3 class="text-3xl font-black text-red-400 font-sans print:text-red-700">
        {{ (executive.cancel_rate || 0).toFixed(1) }}%
      </h3>
      <span class="inline-flex mt-3 text-[10px] font-bold text-red-400 px-2.5 py-1 bg-red-500/10 rounded-lg print:border print:border-charcoal-200 print:text-red-800 print:bg-charcoal-50">
        {{ executive.total_cancel || 0 }} Cancelled
      </span>
    </div>

    <!-- 5. Potential Revenue -->
    <div class="interactive-card p-5 relative overflow-hidden bg-charcoal-800 border border-charcoal-700 rounded-2xl print:bg-white print:border print:border-charcoal-200 print:rounded-xl">
      <div class="absolute -top-10 -right-10 w-24 h-24 bg-sky-500/5 rounded-full blur-2xl print:hidden"></div>
      <p class="text-[9px] font-extrabold uppercase tracking-widest text-charcoal-400 mb-1 print:text-charcoal-500">Potential Pipeline Value</p>
      <h3 class="text-2xl font-black text-sky-400 font-sans mt-0.5 print:text-sky-700">
        {{ formatMoney(executive.potential_revenue) }}
      </h3>
      <span class="inline-flex mt-3.5 text-[10px] font-bold text-charcoal-400 print:text-charcoal-600">
        Projected Budgets Sum
      </span>
    </div>

    <!-- 6. Confirmed Revenue -->
    <div class="interactive-card p-5 relative overflow-hidden bg-charcoal-800 border border-charcoal-700 rounded-2xl print:bg-white print:border print:border-charcoal-200 print:rounded-xl">
      <div class="absolute -top-10 -right-10 w-24 h-24 bg-brand-emerald/5 rounded-full blur-2xl print:hidden"></div>
      <p class="text-[9px] font-extrabold uppercase tracking-widest text-charcoal-400 mb-1 print:text-charcoal-500">Confirmed Revenue</p>
      <h3 class="text-2xl font-black text-brand-emerald font-sans mt-0.5 print:text-emerald-700">
        {{ formatMoney(executive.confirmed_revenue) }}
      </h3>
      <span class="inline-flex mt-3.5 text-[10px] font-bold text-brand-emerald px-2.5 py-1 bg-brand-emerald/10 rounded-lg print:border print:border-charcoal-200 print:text-emerald-800 print:bg-charcoal-50">
        Signed Contract value
      </span>
    </div>

    <!-- 7. Target Achievement -->
    <div class="interactive-card p-5 relative overflow-hidden bg-charcoal-800 border border-charcoal-700 rounded-2xl print:bg-white print:border print:border-charcoal-200 print:rounded-xl">
      <div class="absolute -top-10 -right-10 w-24 h-24 bg-brand-orange/5 rounded-full blur-2xl print:hidden"></div>
      <p class="text-[9px] font-extrabold uppercase tracking-widest text-charcoal-400 mb-1 print:text-charcoal-500">Target Achievement</p>
      <h3 class="text-3xl font-black text-brand-orange font-sans print:text-orange-700">
        {{ (target.achievement_rate || 0).toFixed(1) }}%
      </h3>
      <span class="inline-flex mt-3 text-[10px] font-bold text-charcoal-400 print:text-charcoal-600">
        Target: {{ formatMoney(target.revenue_target) }}
      </span>
    </div>

    <!-- 8. Revenue Conversion Rate -->
    <div class="interactive-card p-5 relative overflow-hidden bg-charcoal-800 border border-charcoal-700 rounded-2xl print:bg-white print:border print:border-charcoal-200 print:rounded-xl">
      <div class="absolute -top-10 -right-10 w-24 h-24 bg-sky-500/5 rounded-full blur-2xl print:hidden"></div>
      <p class="text-[9px] font-extrabold uppercase tracking-widest text-charcoal-400 mb-1 print:text-charcoal-500">Revenue Conversion Rate</p>
      <h3 class="text-3xl font-black text-sky-400 font-sans print:text-sky-700">
        {{ (executive.revenue_conversion_rate || 0).toFixed(1) }}%
      </h3>
      <span class="inline-flex mt-3 text-[10px] font-bold text-charcoal-400 print:text-charcoal-600">
        Confirmed / Potential
      </span>
    </div>

    <!-- 9. Average Project Value -->
    <div class="interactive-card p-5 relative overflow-hidden bg-charcoal-800 border border-charcoal-700 rounded-2xl print:bg-white print:border print:border-charcoal-200 print:rounded-xl">
      <div class="absolute -top-10 -right-10 w-24 h-24 bg-purple-500/5 rounded-full blur-2xl print:hidden"></div>
      <p class="text-[9px] font-extrabold uppercase tracking-widest text-charcoal-400 mb-1 print:text-charcoal-500">Average Project Value</p>
      <h3 class="text-2xl font-black text-purple-400 font-sans mt-0.5 print:text-purple-700">
        {{ formatMoney(executive.average_project_value) }}
      </h3>
      <span class="inline-flex mt-3.5 text-[10px] font-bold text-purple-400 px-2.5 py-1 bg-purple-500/10 rounded-lg print:border print:border-charcoal-200 print:text-purple-800 print:bg-charcoal-50">
        Confirmed Rev / Deal
      </span>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  executive: {
    type: Object,
    required: true,
    default: () => ({})
  },
  target: {
    type: Object,
    required: true,
    default: () => ({})
  }
})

const formatMoney = (val) => {
  if (val >= 1e9) {
    return 'Rp ' + (val / 1e9).toFixed(2) + ' B'
  }
  if (val >= 1e6) {
    return 'Rp ' + (val / 1e6).toFixed(1) + ' M'
  }
  return 'Rp ' + Number(val || 0).toLocaleString('id-ID')
}
</script>

<style scoped>
.interactive-card {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.interactive-card:hover {
  transform: translateY(-4px);
  border-color: rgba(255, 107, 0, 0.35);
  box-shadow: 0 10px 20px -10px rgba(255, 107, 0, 0.15);
}
</style>
