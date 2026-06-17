<template>
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 select-none">
    <!-- Total Projects -->
    <div class="interactive-card p-5 relative overflow-hidden bg-charcoal-800 border border-charcoal-700 rounded-2xl">
      <div class="absolute -top-10 -right-10 w-24 h-24 bg-brand-orange/5 rounded-full blur-2xl"></div>
      <p class="text-[10px] font-extrabold uppercase tracking-widest text-charcoal-400 mb-1">Total Pipeline Projects</p>
      <h3 class="text-3xl font-black text-white font-sans">
        {{ executive.total_projects }}
        <span class="text-xs text-charcoal-400 font-semibold">registered</span>
      </h3>
      <div class="flex items-center gap-2 mt-3 text-[10px] font-bold text-charcoal-400">
        <span class="text-brand-orange">{{ executive.total_inquiry }} Inquiry</span>
        <span>•</span>
        <span class="text-sky-400">{{ executive.total_deal }} Signed Deal</span>
      </div>
    </div>

    <!-- Deal Conversion Rate -->
    <div class="interactive-card p-5 relative overflow-hidden bg-charcoal-800 border border-charcoal-700 rounded-2xl">
      <div class="absolute -top-10 -right-10 w-24 h-24 bg-brand-emerald/5 rounded-full blur-2xl"></div>
      <p class="text-[10px] font-extrabold uppercase tracking-widest text-charcoal-400 mb-1">Deal Conversion Rate</p>
      <h3 class="text-3xl font-black text-brand-emerald font-sans">
        {{ executive.deal_rate.toFixed(1) }}%
      </h3>
      <span class="inline-flex mt-3 text-[10px] font-bold text-brand-emerald px-2.5 py-1 bg-brand-emerald/10 rounded-lg">
        {{ executive.total_deal }} Won / {{ executive.total_projects }} Total
      </span>
    </div>

    <!-- Confirmed Revenue -->
    <div class="interactive-card p-5 relative overflow-hidden bg-charcoal-800 border border-charcoal-700 rounded-2xl">
      <div class="absolute -top-10 -right-10 w-24 h-24 bg-sky-500/5 rounded-full blur-2xl"></div>
      <p class="text-[10px] font-extrabold uppercase tracking-widest text-charcoal-400 mb-1">Confirmed Revenue</p>
      <h3 class="text-2xl font-black text-sky-400 font-sans mt-0.5">
        {{ formatMoney(executive.confirmed_revenue) }}
      </h3>
      <div class="mt-3.5 text-[10px] font-bold text-charcoal-400">
        Potential: {{ formatMoney(executive.potential_revenue) }} ({{ executive.revenue_conversion_rate.toFixed(1) }}%)
      </div>
    </div>

    <!-- Average Project Value -->
    <div class="interactive-card p-5 relative overflow-hidden bg-charcoal-800 border border-charcoal-700 rounded-2xl">
      <div class="absolute -top-10 -right-10 w-24 h-24 bg-purple-500/5 rounded-full blur-2xl"></div>
      <p class="text-[10px] font-extrabold uppercase tracking-widest text-charcoal-400 mb-1">Average Project Value</p>
      <h3 class="text-2xl font-black text-purple-400 font-sans mt-0.5">
        {{ formatMoney(executive.average_project_value) }}
      </h3>
      <span class="inline-flex mt-3.5 text-[10px] font-bold text-purple-400 px-2.5 py-1 bg-purple-500/10 rounded-lg">
        Confirmed Rev / Deal
      </span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  executive: {
    type: Object,
    required: true,
    default: () => ({
      total_projects: 0,
      total_inquiry: 0,
      total_deal: 0,
      total_cancel: 0,
      deal_rate: 0.0,
      cancel_rate: 0.0,
      potential_revenue: 0.0,
      confirmed_revenue: 0.0,
      revenue_conversion_rate: 0.0,
      average_project_value: 0.0
    })
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
