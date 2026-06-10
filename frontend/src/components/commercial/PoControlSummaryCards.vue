<template>
  <div class="space-y-6">
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 select-none">
      <AppStatCard 
        title="Total Proyek" 
        :value="summary.total_owned_projects" 
        subtitle="Proyek Terdaftar" 
        theme="neutral" 
      />
      <AppStatCard 
        title="Total Deal" 
        :value="summary.total_deal" 
        subtitle="Signed & Deal" 
        theme="emerald" 
      />
      <AppStatCard 
        title="Total Batal" 
        :value="summary.total_cancel" 
        subtitle="Batal (Cancelled)" 
        theme="red" 
      />
      <AppStatCard 
        title="Deal Rate" 
        :value="`${Math.round(summary.deal_rate || 0)}%`" 
        subtitle="Rasio Keberhasilan Deal" 
        theme="blue" 
      />
      <AppStatCard 
        title="Estimasi Revenue" 
        :value="formatCurrency(summary.potential_revenue)" 
        subtitle="Potential Revenue (Kotor)" 
        theme="amber" 
      />
      <AppStatCard 
        title="Revenue Terkonfirmasi" 
        :value="formatCurrency(summary.confirmed_revenue)" 
        subtitle="Confirmed Revenue (Pasti)" 
        theme="emerald" 
      />
      <AppStatCard 
        title="Pembayaran Belum Lunas" 
        :value="formatCurrency(summary.outstanding_payment)" 
        :subtitle="`${summary.outstanding_count} Klien Belum Melunasi`" 
        theme="red" 
      />
      <AppStatCard 
        title="Quotation Menunggu Follow-up" 
        :value="summary.follow_up_needed_count" 
        subtitle="Tindakan Diperlukan" 
        theme="orange" 
      />
    </div>
  </div>
</template>

<script setup>
import AppStatCard from '../ui/AppStatCard.vue'

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
