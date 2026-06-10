<template>
  <div class="space-y-6">
    <!-- Cancel without reason -->
    <div class="glass-panel p-5 border border-brand-charcoal-light/20 space-y-3">
      <div class="flex items-center justify-between border-b border-brand-charcoal-light/10 pb-2">
        <h4 class="text-xs font-black text-white uppercase tracking-wider flex items-center gap-2">
          <span class="w-2 h-2 rounded-full bg-red-500"></span>
          Proyek Batal Tanpa Alasan (Cancel Reason Missing)
        </h4>
        <span v-if="commercialRisks.cancel_without_reason?.length > 0" class="text-[9px] font-bold text-red-400 bg-red-500/10 px-2 py-0.5 rounded">
          Urgensi Tinggi
        </span>
        <span v-else class="text-[9px] font-bold text-brand-emerald bg-brand-emerald/10 px-2 py-0.5 rounded">
          Aman
        </span>
      </div>
      
      <div v-if="!commercialRisks.cancel_without_reason || commercialRisks.cancel_without_reason.length === 0" class="text-xs text-gray-500 py-3 font-semibold text-center select-none">
        Aman: Tidak ada proyek batal yang kehilangan catatan alasan.
      </div>
      
      <div v-else class="overflow-x-auto">
        <table class="min-w-full text-left text-[11px]">
          <thead class="text-gray-500 text-[9px] uppercase tracking-widest font-black">
            <tr>
              <th class="py-2">Code</th>
              <th class="py-2">Program / Customer</th>
              <th class="py-2">PO / PM</th>
              <th class="py-2 text-right">Budget</th>
              <th class="py-2">Peringatan</th>
              <th class="py-2 text-right">Aksi</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-white/5 font-semibold">
            <tr v-for="rp in commercialRisks.cancel_without_reason" :key="rp.project_id" class="hover:bg-white/5">
              <td class="py-2 font-mono text-gray-400 select-all">{{ rp.project_code || '-' }}</td>
              <td class="py-2">
                <p class="text-white">{{ rp.program_name }}</p>
                <p class="text-[10px] text-gray-500">{{ rp.customer_name }}</p>
              </td>
              <td class="py-2 text-gray-400">PO: {{ rp.po_name }} • PM: {{ rp.pm_name }}</td>
              <td class="py-2 text-right text-white font-mono">{{ formatCurrency(rp.budget) }}</td>
              <td class="py-2 text-red-400 font-bold">{{ rp.reason }}</td>
              <td class="py-2 text-right">
                <router-link :to="'/projects/' + rp.project_id" class="text-[10px] text-brand-orange hover:underline font-bold">
                  Open Project
                </router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Signed deal without budget -->
    <div class="glass-panel p-5 border border-brand-charcoal-light/20 space-y-3">
      <div class="flex items-center justify-between border-b border-brand-charcoal-light/10 pb-2">
        <h4 class="text-xs font-black text-white uppercase tracking-wider flex items-center gap-2">
          <span class="w-2 h-2 rounded-full bg-red-500"></span>
          Proyek Deal Tanpa Nilai Budget (Signed &amp; Deal Rp 0)
        </h4>
        <span v-if="commercialRisks.signed_deal_without_budget?.length > 0" class="text-[9px] font-bold text-red-400 bg-red-500/10 px-2 py-0.5 rounded">
          Urgensi Tinggi
        </span>
        <span v-else class="text-[9px] font-bold text-brand-emerald bg-brand-emerald/10 px-2 py-0.5 rounded">
          Aman
        </span>
      </div>

      <div v-if="!commercialRisks.signed_deal_without_budget || commercialRisks.signed_deal_without_budget.length === 0" class="text-xs text-gray-500 py-3 font-semibold text-center select-none">
        Aman: Semua proyek Signed &amp; Deal memiliki nilai budget terisi.
      </div>

      <div v-else class="overflow-x-auto">
        <table class="min-w-full text-left text-[11px]">
          <thead class="text-gray-500 text-[9px] uppercase tracking-widest font-black">
            <tr>
              <th class="py-2">Code</th>
              <th class="py-2">Program / Customer</th>
              <th class="py-2">PO / PM</th>
              <th class="py-2 text-right">Budget</th>
              <th class="py-2">Peringatan</th>
              <th class="py-2 text-right">Aksi</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-white/5 font-semibold">
            <tr v-for="rp in commercialRisks.signed_deal_without_budget" :key="rp.project_id" class="hover:bg-white/5">
              <td class="py-2 font-mono text-gray-400 select-all">{{ rp.project_code || '-' }}</td>
              <td class="py-2">
                <p class="text-white">{{ rp.program_name }}</p>
                <p class="text-[10px] text-gray-500">{{ rp.customer_name }}</p>
              </td>
              <td class="py-2 text-gray-400">PO: {{ rp.po_name }} • PM: {{ rp.pm_name }}</td>
              <td class="py-2 text-right text-red-400 font-mono">{{ formatCurrency(rp.budget) }}</td>
              <td class="py-2 text-red-400 font-bold">{{ rp.reason }}</td>
              <td class="py-2 text-right">
                <router-link :to="'/projects/' + rp.project_id" class="text-[10px] text-brand-orange hover:underline font-bold">
                  Open Project
                </router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Outstanding Payment -->
    <div class="glass-panel p-5 border border-brand-charcoal-light/20 space-y-3">
      <div class="flex items-center justify-between border-b border-brand-charcoal-light/10 pb-2">
        <h4 class="text-xs font-black text-white uppercase tracking-wider flex items-center gap-2">
          <span class="w-2 h-2 rounded-full bg-amber-500"></span>
          Proyek dengan Status Outstanding / Overdue Payment
        </h4>
        <span v-if="commercialRisks.outstanding_payment?.length > 0" class="text-[9px] font-bold text-amber-500 bg-amber-500/10 px-2 py-0.5 rounded">
          Peringatan Keuangan
        </span>
        <span v-else class="text-[9px] font-bold text-brand-emerald bg-brand-emerald/10 px-2 py-0.5 rounded">
          Aman
        </span>
      </div>

      <div v-if="!commercialRisks.outstanding_payment || commercialRisks.outstanding_payment.length === 0" class="text-xs text-gray-500 py-3 font-semibold text-center select-none">
        Aman: Tidak ada tagihan jatuh tempo terdeteksi terlambat.
      </div>

      <div v-else class="overflow-x-auto">
        <table class="min-w-full text-left text-[11px]">
          <thead class="text-gray-500 text-[9px] uppercase tracking-widest font-black">
            <tr>
              <th class="py-2">Code</th>
              <th class="py-2">Program / Customer</th>
              <th class="py-2">PO / PM</th>
              <th class="py-2 text-right">Budget</th>
              <th class="py-2">Peringatan</th>
              <th class="py-2 text-right">Aksi</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-white/5 font-semibold">
            <tr v-for="rp in commercialRisks.outstanding_payment" :key="rp.project_id" class="hover:bg-white/5">
              <td class="py-2 font-mono text-gray-400 select-all">{{ rp.project_code || '-' }}</td>
              <td class="py-2">
                <p class="text-white">{{ rp.program_name }}</p>
                <p class="text-[10px] text-gray-500">{{ rp.customer_name }}</p>
              </td>
              <td class="py-2 text-gray-400">PO: {{ rp.po_name }} • PM: {{ rp.pm_name }}</td>
              <td class="py-2 text-right text-white font-mono">{{ formatCurrency(rp.budget) }}</td>
              <td class="py-2 text-amber-500 font-bold">{{ rp.reason }}</td>
              <td class="py-2 text-right">
                <router-link :to="'/projects/' + rp.project_id" class="text-[10px] text-brand-orange hover:underline font-bold">
                  Open Project
                </router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Invoice Sent not Paid -->
    <div class="glass-panel p-5 border border-brand-charcoal-light/20 space-y-3">
      <div class="flex items-center justify-between border-b border-brand-charcoal-light/10 pb-2">
        <h4 class="text-xs font-black text-white uppercase tracking-wider flex items-center gap-2">
          <span class="w-2 h-2 rounded-full bg-brand-blue"></span>
          Invoice Sudah Terkirim tetapi Belum Tercatat Lunas (Paid)
        </h4>
        <span v-if="commercialRisks.invoice_sent_not_paid?.length > 0" class="text-[9px] font-bold text-brand-blue bg-brand-blue/10 px-2 py-0.5 rounded">
          Penagihan Berjalan
        </span>
        <span v-else class="text-[9px] font-bold text-brand-emerald bg-brand-emerald/10 px-2 py-0.5 rounded">
          Lunas
        </span>
      </div>

      <div v-if="!commercialRisks.invoice_sent_not_paid || commercialRisks.invoice_sent_not_paid.length === 0" class="text-xs text-gray-500 py-3 font-semibold text-center select-none">
        Aman: Semua tagihan terkirim sudah lunas (Paid).
      </div>

      <div v-else class="overflow-x-auto">
        <table class="min-w-full text-left text-[11px]">
          <thead class="text-gray-500 text-[9px] uppercase tracking-widest font-black">
            <tr>
              <th class="py-2">Code</th>
              <th class="py-2">Program / Customer</th>
              <th class="py-2">PO / PM</th>
              <th class="py-2 text-right">Budget</th>
              <th class="py-2">Peringatan</th>
              <th class="py-2 text-right">Aksi</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-white/5 font-semibold">
            <tr v-for="rp in commercialRisks.invoice_sent_not_paid" :key="rp.project_id" class="hover:bg-white/5">
              <td class="py-2 font-mono text-gray-400 select-all">{{ rp.project_code || '-' }}</td>
              <td class="py-2">
                <p class="text-white">{{ rp.program_name }}</p>
                <p class="text-[10px] text-gray-500">{{ rp.customer_name }}</p>
              </td>
              <td class="py-2 text-gray-400">PO: {{ rp.po_name }} • PM: {{ rp.pm_name }}</td>
              <td class="py-2 text-right text-white font-mono">{{ formatCurrency(rp.budget) }}</td>
              <td class="py-2 text-indigo-400 font-bold">{{ rp.reason }}</td>
              <td class="py-2 text-right">
                <router-link :to="'/projects/' + rp.project_id" class="text-[10px] text-brand-orange hover:underline font-bold">
                  Open Project
                </router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Missing PO Assignment -->
    <div class="glass-panel p-5 border border-brand-charcoal-light/20 space-y-3">
      <div class="flex items-center justify-between border-b border-brand-charcoal-light/10 pb-2">
        <h4 class="text-xs font-black text-white uppercase tracking-wider flex items-center gap-2">
          <span class="w-2 h-2 rounded-full bg-amber-500"></span>
          Proyek Tanpa Penanggung Jawab Program Owner (PO)
        </h4>
      </div>

      <div v-if="!commercialRisks.missing_po || commercialRisks.missing_po.length === 0" class="text-xs text-gray-500 py-3 font-semibold text-center select-none">
        Aman: Semua proyek memiliki Program Owner (PO) penanggung jawab.
      </div>

      <div v-else class="overflow-x-auto">
        <table class="min-w-full text-left text-[11px]">
          <thead class="text-gray-500 text-[9px] uppercase tracking-widest font-black">
            <tr>
              <th class="py-2">Code</th>
              <th class="py-2">Program / Customer</th>
              <th class="py-2">PO / PM</th>
              <th class="py-2 text-right">Budget</th>
              <th class="py-2">Peringatan</th>
              <th class="py-2 text-right">Aksi</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-white/5 font-semibold">
            <tr v-for="rp in commercialRisks.missing_po" :key="rp.project_id" class="hover:bg-white/5">
              <td class="py-2 font-mono text-gray-400 select-all">{{ rp.project_code || '-' }}</td>
              <td class="py-2">
                <p class="text-white">{{ rp.program_name }}</p>
                <p class="text-[10px] text-gray-500">{{ rp.customer_name }}</p>
              </td>
              <td class="py-2 text-gray-400">PO: {{ rp.po_name }} • PM: {{ rp.pm_name }}</td>
              <td class="py-2 text-right text-white font-mono">{{ formatCurrency(rp.budget) }}</td>
              <td class="py-2 text-amber-400 font-bold">{{ rp.reason }}</td>
              <td class="py-2 text-right">
                <router-link :to="'/projects/' + rp.project_id" class="text-[10px] text-brand-orange hover:underline font-bold">
                  Open Project
                </router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Missing Lead Source -->
    <div class="glass-panel p-5 border border-brand-charcoal-light/20 space-y-3">
      <div class="flex items-center justify-between border-b border-brand-charcoal-light/10 pb-2">
        <h4 class="text-xs font-black text-white uppercase tracking-wider flex items-center gap-2">
          <span class="w-2 h-2 rounded-full bg-amber-500"></span>
          Proyek Tanpa Data Event Source / Lead Partner
        </h4>
      </div>

      <div v-if="!commercialRisks.missing_source || commercialRisks.missing_source.length === 0" class="text-xs text-gray-500 py-3 font-semibold text-center select-none">
        Aman: Semua proyek memiliki data Event Source.
      </div>

      <div v-else class="overflow-x-auto">
        <table class="min-w-full text-left text-[11px]">
          <thead class="text-gray-500 text-[9px] uppercase tracking-widest font-black">
            <tr>
              <th class="py-2">Code</th>
              <th class="py-2">Program / Customer</th>
              <th class="py-2">PO / PM</th>
              <th class="py-2 text-right">Budget</th>
              <th class="py-2">Peringatan</th>
              <th class="py-2 text-right">Aksi</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-white/5 font-semibold">
            <tr v-for="rp in commercialRisks.missing_source" :key="rp.project_id" class="hover:bg-white/5">
              <td class="py-2 font-mono text-gray-400 select-all">{{ rp.project_code || '-' }}</td>
              <td class="py-2">
                <p class="text-white">{{ rp.program_name }}</p>
                <p class="text-[10px] text-gray-500">{{ rp.customer_name }}</p>
              </td>
              <td class="py-2 text-gray-400">PO: {{ rp.po_name }} • PM: {{ rp.pm_name }}</td>
              <td class="py-2 text-right text-white font-mono">{{ formatCurrency(rp.budget) }}</td>
              <td class="py-2 text-amber-400 font-bold">{{ rp.reason }}</td>
              <td class="py-2 text-right">
                <router-link :to="'/projects/' + rp.project_id" class="text-[10px] text-brand-orange hover:underline font-bold">
                  Open Project
                </router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  commercialRisks: {
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
