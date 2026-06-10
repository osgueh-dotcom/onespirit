<template>
  <div class="space-y-6">
    <!-- Header -->
    <AppPageHeader 
      title="PO Control Center" 
      subtitle="Pusat kontrol komersial untuk membantu Program Owner memantau quotation, deal/cancel, revenue, source, outstanding, dan prioritas follow-up."
    >
      <template #actions>
        <button 
          @click="fetchControlCenterData"
          class="px-4 py-2 rounded-xl bg-brand-charcoal border border-brand-charcoal-light/35 hover:border-brand-orange/40 text-xs font-bold text-gray-300 hover:text-white transition-all flex items-center gap-2"
        >
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
          </svg>
          Refresh Data
        </button>
      </template>
    </AppPageHeader>

    <!-- Filters Bar -->
    <PoControlFilters :users="users" @change="handleFilterChange" />

    <!-- Error State -->
    <AppErrorState 
      v-if="error" 
      title="Gagal Memuat PO Control Center" 
      :message="error" 
      @retry="fetchControlCenterData" 
    />

    <!-- Loading State -->
    <AppLoadingState v-else-if="loading" message="Mengompilasi data PO Control Center..." />

    <!-- Main Content -->
    <div v-else class="space-y-6 animate-fade-in">
      <!-- KPI Cards Summary -->
      <PoControlSummaryCards :summary="summary" />

      <!-- Tab Buttons -->
      <div class="flex border-b border-brand-charcoal-light/25 select-none overflow-x-auto">
        <button 
          v-for="tab in tabs" 
          :key="tab.id"
          @click="activeTab = tab.id"
          class="px-5 py-3 text-xs font-bold transition-all border-b-2 outline-none flex items-center gap-2 whitespace-nowrap"
          :class="activeTab === tab.id ? 'border-brand-orange text-white bg-white/5' : 'border-transparent text-gray-400 hover:text-white'"
        >
          {{ tab.name }}
          <span 
            v-if="tab.count !== undefined" 
            class="px-1.5 py-0.5 rounded-full text-[9px] font-black"
            :class="activeTab === tab.id ? 'bg-brand-orange text-black' : 'bg-brand-charcoal-light/30 text-gray-400'"
          >
            {{ tab.count }}
          </span>
        </button>
      </div>

      <!-- TAB 1: Follow-up Priorities -->
      <div v-show="activeTab === 'priority'" class="space-y-4">
        <FollowUpPriorityList :priorities="followUpPriorities" />
      </div>

      <!-- TAB 2: Owned Projects List -->
      <div v-show="activeTab === 'projects'" class="space-y-6">
        <div class="glass-panel p-5 border border-brand-charcoal-light/20 space-y-4">
          <h3 class="text-sm font-bold text-white uppercase tracking-wider">Daftar Proyek di Bawah PO</h3>
          
          <!-- Desktop Table View -->
          <div class="hidden md:block overflow-x-auto">
            <table class="min-w-full text-left text-xs divide-y divide-brand-charcoal-light/10">
              <thead class="bg-brand-charcoal-dark/30 text-[9px] font-extrabold uppercase tracking-widest text-gray-500 select-none">
                <tr>
                  <th class="px-4 py-3">Code</th>
                  <th class="px-4 py-3">Customer / Program</th>
                  <th class="px-4 py-3">Lead Source</th>
                  <th class="px-4 py-3">PO / PM</th>
                  <th class="px-4 py-3 text-center">Status Q / P / Payment</th>
                  <th class="px-4 py-3 text-right">Budget</th>
                  <th class="px-4 py-3">Rekomendasi Aksi PO</th>
                  <th class="px-4 py-3 text-right">Navigasi</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-brand-charcoal-light/5 font-medium">
                <tr v-if="ownedProjects.length === 0">
                  <td colspan="8" class="px-4 py-8 text-center text-gray-500 font-semibold">
                    Tidak ada proyek PO untuk filter ini.
                  </td>
                </tr>
                <tr 
                  v-for="p in ownedProjects" 
                  :key="p.project_id"
                  class="hover:bg-white/5 transition-colors"
                >
                  <td class="px-4 py-3 whitespace-nowrap font-mono font-bold text-gray-400 select-all">
                    {{ p.project_code || '-' }}
                  </td>
                  <td class="px-4 py-3">
                    <p class="text-white font-bold leading-tight">{{ p.customer_name }}</p>
                    <p class="text-[10px] text-gray-500 font-semibold mt-0.5">{{ p.event_date_start ? formatDate(p.event_date_start) : '-' }}</p>
                  </td>
                  <td class="px-4 py-3 whitespace-nowrap">
                    <p class="text-gray-200 font-bold select-none text-[10px]">{{ p.source_type }}</p>
                    <p class="text-[9px] text-gray-500 leading-none mt-0.5">{{ p.vendor_name }} • {{ p.sales_name }}</p>
                  </td>
                  <td class="px-4 py-3 whitespace-nowrap font-semibold">
                    <p class="text-gray-300">PO: {{ p.po_name }}</p>
                    <p class="text-[10px] text-gray-500">PM: {{ p.pm_name }}</p>
                  </td>
                  <td class="px-4 py-3 whitespace-nowrap">
                    <div class="flex flex-col gap-1 items-center">
                      <span class="px-2 py-0.5 rounded text-[8px] font-black uppercase text-center w-20 block" :class="getQuotationStatusClass(p.quotation_status)">
                        Q: {{ p.quotation_status }}
                      </span>
                      <span class="px-2 py-0.5 rounded text-[8px] font-black uppercase text-center w-20 block" :class="getProgramStatusClass(p.program_status)">
                        P: {{ p.program_status }}
                      </span>
                      <span class="px-2 py-0.5 rounded text-[8px] font-black uppercase text-center w-20 block" :class="getPaymentStatusClass(p.payment_status)">
                        PAY: {{ p.payment_status }}
                      </span>
                    </div>
                  </td>
                  <td class="px-4 py-3 text-right whitespace-nowrap text-white font-bold font-mono select-all">
                    {{ formatCurrency(p.budget) }}
                  </td>
                  <td class="px-4 py-3 text-gray-200 font-bold leading-relaxed max-w-xs">
                    {{ p.recommended_action }}
                  </td>
                  <td class="px-4 py-3 text-right">
                    <router-link 
                      :to="'/projects/' + p.project_id"
                      class="px-2.5 py-1 text-[10px] font-bold text-brand-orange bg-brand-orange/10 hover:bg-brand-orange/20 rounded transition-all"
                    >
                      Buka
                    </router-link>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Mobile Card List -->
          <div class="block md:hidden space-y-4">
            <div v-if="ownedProjects.length === 0" class="py-6 text-center text-xs text-gray-500 font-semibold">
              Tidak ada proyek PO untuk filter ini.
            </div>
            <div 
              v-for="p in ownedProjects" 
              :key="p.project_id"
              class="bg-brand-charcoal/60 border border-brand-charcoal-light/20 p-4 rounded-2xl space-y-3 animate-fade-in"
            >
              <div class="flex items-center justify-between border-b border-brand-charcoal-light/10 pb-2">
                <span class="font-mono text-[10px] font-bold text-gray-400">{{ p.project_code || 'OSA-EVENT' }}</span>
                <span class="text-brand-emerald font-bold font-mono">{{ formatCurrency(p.budget) }}</span>
              </div>
              <div>
                <h4 class="font-bold text-white text-sm">{{ p.customer_name }}</h4>
                <p class="text-xs text-gray-400 mt-0.5">Event: {{ p.event_date_start ? formatDate(p.event_date_start) : '-' }}</p>
              </div>
              <div class="grid grid-cols-2 gap-2 bg-black/20 p-2.5 rounded-xl border border-white/5 text-[11px] font-semibold">
                <div>
                  <p class="text-gray-500 text-[9px] uppercase tracking-wider">Lead Source</p>
                  <p class="text-white truncate">{{ p.source_type }}</p>
                  <p class="text-[9px] text-gray-400 truncate">{{ p.vendor_name }}</p>
                </div>
                <div>
                  <p class="text-gray-500 text-[9px] uppercase tracking-wider">PO / PM</p>
                  <p class="text-white truncate">PO: {{ p.po_name }}</p>
                  <p class="text-gray-400 truncate text-[10px]">PM: {{ p.pm_name }}</p>
                </div>
              </div>
              <div class="flex flex-wrap gap-1.5 justify-start">
                <span class="px-2 py-0.5 rounded text-[8px] font-black uppercase text-center" :class="getQuotationStatusClass(p.quotation_status)">
                  Q: {{ p.quotation_status }}
                </span>
                <span class="px-2 py-0.5 rounded text-[8px] font-black uppercase text-center" :class="getProgramStatusClass(p.program_status)">
                  P: {{ p.program_status }}
                </span>
                <span class="px-2 py-0.5 rounded text-[8px] font-black uppercase text-center" :class="getPaymentStatusClass(p.payment_status)">
                  PAY: {{ p.payment_status }}
                </span>
              </div>
              <div class="bg-brand-orange/5 border border-brand-orange/10 p-2.5 rounded-xl text-[11px] text-gray-200">
                <p class="text-[8px] font-black text-brand-orange uppercase tracking-wider mb-1 select-none">Rekomendasi Aksi PO:</p>
                <p class="font-bold leading-normal">{{ p.recommended_action }}</p>
              </div>
              <div class="flex justify-end pt-1">
                <router-link 
                  :to="'/projects/' + p.project_id"
                  class="px-3 py-1.5 rounded bg-brand-orange/10 hover:bg-brand-orange/20 text-brand-orange font-bold text-[10px] transition-all"
                >
                  Buka Proyek →
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- TAB 3: Commercial Performance & Leads -->
      <div v-show="activeTab === 'kinerja'" class="space-y-6">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <!-- Left: Quotation & Revenue Breakdown -->
          <div class="space-y-6">
            <!-- Quotation Summary -->
            <div class="glass-panel p-5 border border-brand-charcoal-light/20 space-y-4">
              <h3 class="text-sm font-bold text-white uppercase tracking-wider">Struktur Status Penawaran (Quotation)</h3>
              <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
                <div class="bg-black/20 p-3 rounded-xl border border-white/5 text-center">
                  <p class="text-[9px] font-black text-gray-500 uppercase tracking-widest mb-1">Draft</p>
                  <p class="text-lg font-black text-gray-300">{{ quotationSummary.draft_count }}</p>
                </div>
                <div class="bg-black/20 p-3 rounded-xl border border-white/5 text-center">
                  <p class="text-[9px] font-black text-indigo-400 uppercase tracking-widest mb-1">Sent</p>
                  <p class="text-lg font-black text-indigo-300">{{ quotationSummary.sent_count }}</p>
                </div>
                <div class="bg-black/20 p-3 rounded-xl border border-white/5 text-center">
                  <p class="text-[9px] font-black text-amber-500 uppercase tracking-widest mb-1">Follow Up</p>
                  <p class="text-lg font-black text-amber-400">{{ quotationSummary.follow_up_count }}</p>
                </div>
                <div class="bg-black/20 p-3 rounded-xl border border-white/5 text-center">
                  <p class="text-[9px] font-black text-purple-400 uppercase tracking-widest mb-1">Revision</p>
                  <p class="text-lg font-black text-purple-300">{{ quotationSummary.revision_count }}</p>
                </div>
                <div class="bg-black/20 p-3 rounded-xl border border-white/5 text-center bg-brand-emerald/5 border-brand-emerald/10">
                  <p class="text-[9px] font-black text-brand-emerald uppercase tracking-widest mb-1">Signed & Deal</p>
                  <p class="text-lg font-black text-brand-emerald">{{ quotationSummary.signed_deal_count }}</p>
                </div>
                <div class="bg-black/20 p-3 rounded-xl border border-white/5 text-center bg-red-500/5 border-red-500/10">
                  <p class="text-[9px] font-black text-red-400 uppercase tracking-widest mb-1">Cancel</p>
                  <p class="text-lg font-black text-red-400">{{ quotationSummary.cancel_count }}</p>
                </div>
              </div>
            </div>

            <!-- Revenue Summary -->
            <div class="glass-panel p-5 border border-brand-charcoal-light/20 space-y-4">
              <h3 class="text-sm font-bold text-white uppercase tracking-wider">Statistik Nilai Proyek & Konversi</h3>
              <div class="grid grid-cols-2 gap-4">
                <div class="bg-black/20 p-3 rounded-xl border border-white/5">
                  <p class="text-[9px] font-black text-gray-500 uppercase tracking-widest mb-0.5">Rata-rata Nilai Proyek Potensial</p>
                  <p class="text-sm font-black text-white">{{ formatCurrency(revenueSummary.average_project_value) }}</p>
                  <span class="text-[8px] text-gray-400 font-semibold block mt-0.5">Average value of all owned project opportunities.</span>
                </div>
                <div class="bg-black/20 p-3 rounded-xl border border-white/5">
                  <p class="text-[9px] font-black text-gray-500 uppercase tracking-widest mb-0.5">Tingkat Konversi Pendapatan</p>
                  <p class="text-sm font-black text-brand-emerald">{{ Math.round(revenueSummary.revenue_conversion_rate || 0) }}%</p>
                </div>
                <div class="bg-black/20 p-3 rounded-xl border border-white/5">
                  <p class="text-[9px] font-black text-gray-500 uppercase tracking-widest mb-0.5">Nilai Proyek Tertinggi</p>
                  <p class="text-sm font-black text-indigo-400">{{ formatCurrency(revenueSummary.highest_project_value) }}</p>
                </div>
                <div class="bg-black/20 p-3 rounded-xl border border-white/5">
                  <p class="text-[9px] font-black text-gray-500 uppercase tracking-widest mb-0.5">Nilai Proyek Terendah</p>
                  <p class="text-sm font-black text-gray-400">{{ formatCurrency(revenueSummary.lowest_project_value) }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Right: PO Performance Table -->
          <div class="glass-panel p-5 border border-brand-charcoal-light/20 space-y-4">
            <h3 class="text-sm font-bold text-white uppercase tracking-wider">Beban Kerja & Kinerja Komersial PO</h3>
            
            <!-- Desktop Table View -->
            <div class="hidden md:block overflow-x-auto">
              <table class="min-w-full text-left text-xs divide-y divide-brand-charcoal-light/10">
                <thead class="bg-brand-charcoal-dark/30 text-[9px] font-extrabold uppercase tracking-widest text-gray-500 select-none">
                  <tr>
                    <th class="px-3 py-2.5">PO</th>
                    <th class="px-3 py-2.5 text-center">Total Proyek</th>
                    <th class="px-3 py-2.5 text-center">Deal Rate</th>
                    <th class="px-3 py-2.5 text-right">Confirmed Rev</th>
                    <th class="px-3 py-2.5 text-center">Risk / Overdue</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-brand-charcoal-light/5 font-medium">
                  <tr v-if="poPerformance.length === 0">
                    <td colspan="5" class="px-3 py-6 text-center text-gray-500 font-semibold">
                      Belum ada beban kerja PO komersial tercatat.
                    </td>
                  </tr>
                  <tr v-for="po in poPerformance" :key="po.po_id" class="hover:bg-white/5 transition-colors">
                    <td class="px-3 py-2.5">
                      <div class="flex items-center gap-2 select-none">
                        <div class="w-6 h-6 rounded-lg bg-indigo-500/10 text-indigo-400 font-bold flex items-center justify-center text-[8px]">
                          {{ po.initial_code }}
                        </div>
                        <span class="text-white font-bold">{{ po.po_name }}</span>
                      </div>
                    </td>
                    <td class="px-3 py-2.5 text-center text-white font-bold">{{ po.total_projects }}</td>
                    <td class="px-3 py-2.5 text-center text-indigo-400 font-bold">{{ Math.round(po.deal_rate) }}%</td>
                    <td class="px-3 py-2.5 text-right text-brand-emerald font-mono font-bold">{{ formatCurrency(po.confirmed_revenue) }}</td>
                    <td class="px-3 py-2.5 text-center">
                      <span class="px-1.5 py-0.5 rounded text-[8px] font-bold" :class="po.outstanding_count > 0 ? 'bg-amber-500/10 text-amber-400' : 'bg-brand-emerald/10 text-brand-emerald'">
                        {{ po.outstanding_count }} Risk / {{ po.follow_up_needed_count }} F-Up
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Mobile Card List for PO Workload & Commercial Performance -->
            <div class="block md:hidden space-y-4">
              <div v-if="poPerformance.length === 0" class="py-6 text-center text-xs text-gray-500 font-semibold">
                Belum ada beban kerja PO komersial tercatat.
              </div>
              <div 
                v-for="po in poPerformance" 
                :key="po.po_id"
                class="bg-brand-charcoal/60 border border-brand-charcoal-light/20 p-4 rounded-2xl space-y-3 animate-fade-in"
              >
                <div class="flex items-center justify-between border-b border-brand-charcoal-light/10 pb-2">
                  <div class="flex items-center gap-2">
                    <div class="w-6 h-6 rounded-lg bg-indigo-500/10 text-indigo-400 font-bold flex items-center justify-center text-[8px]">
                      {{ po.initial_code }}
                    </div>
                    <span class="text-white font-bold">{{ po.po_name }}</span>
                  </div>
                  <span class="text-brand-emerald font-bold font-mono">{{ formatCurrency(po.confirmed_revenue) }}</span>
                </div>
                <div class="grid grid-cols-3 gap-2 bg-black/20 p-2.5 rounded-xl border border-white/5 text-[11px] font-semibold text-center">
                  <div>
                    <p class="text-gray-500 text-[9px] uppercase tracking-wider">Total Proyek</p>
                    <p class="text-white">{{ po.total_projects }}</p>
                  </div>
                  <div>
                    <p class="text-indigo-400 text-[9px] uppercase tracking-wider">Deal Rate</p>
                    <p class="text-white">{{ Math.round(po.deal_rate) }}%</p>
                  </div>
                  <div>
                    <p class="text-amber-500 text-[9px] uppercase tracking-wider">Risk / F-Up</p>
                    <p class="text-white text-[10px]">{{ po.outstanding_count }} / {{ po.follow_up_needed_count }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Source Contribution Table -->
        <div class="glass-panel p-5 border border-brand-charcoal-light/20 space-y-4">
          <h3 class="text-sm font-bold text-white uppercase tracking-wider">Kontribusi Lead Source & Vendor Partner</h3>
          
          <!-- Desktop Table View -->
          <div class="hidden md:block overflow-x-auto">
            <table class="min-w-full text-left text-xs divide-y divide-brand-charcoal-light/10">
              <thead class="bg-brand-charcoal-dark/30 text-[9px] font-extrabold uppercase tracking-widest text-gray-500 select-none">
                <tr>
                  <th class="px-4 py-3">Source Type</th>
                  <th class="px-4 py-3">Nama Vendor Partner</th>
                  <th class="px-4 py-3">Sales External</th>
                  <th class="px-4 py-3 text-center">Total Proyek</th>
                  <th class="px-4 py-3 text-center">Deal (Signed)</th>
                  <th class="px-4 py-3 text-center">Batal</th>
                  <th class="px-4 py-3 text-right">Potential Revenue</th>
                  <th class="px-4 py-3 text-right">Confirmed Revenue</th>
                  <th class="px-4 py-3 text-right">Rata-rata Nilai</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-brand-charcoal-light/5 font-medium">
                <tr v-if="sourceContribution.length === 0">
                  <td colspan="9" class="px-4 py-8 text-center text-gray-500 font-semibold">
                    Belum ada data kontribusi lead partner.
                  </td>
                </tr>
                <tr v-for="(sc, index) in sourceContribution" :key="index" class="hover:bg-white/5 transition-colors">
                  <td class="px-4 py-3 whitespace-nowrap text-white font-bold select-none">{{ sc.source_type }}</td>
                  <td class="px-4 py-3 text-gray-300 font-bold select-all">{{ sc.vendor_name }}</td>
                  <td class="px-4 py-3 text-gray-400 font-semibold select-all">{{ sc.sales_name }}</td>
                  <td class="px-4 py-3 text-center text-white font-black">{{ sc.total_projects }}</td>
                  <td class="px-4 py-3 text-center text-brand-emerald font-bold">{{ sc.deal_count }}</td>
                  <td class="px-4 py-3 text-center text-red-400 font-bold">{{ sc.cancel_count }}</td>
                  <td class="px-4 py-3 text-right font-mono font-bold text-gray-300">{{ formatCurrency(sc.potential_revenue) }}</td>
                  <td class="px-4 py-3 text-right font-mono font-bold text-brand-emerald">{{ formatCurrency(sc.confirmed_revenue) }}</td>
                  <td class="px-4 py-3 text-right font-mono text-gray-400">{{ formatCurrency(sc.average_project_value) }}</td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Mobile Card List for Lead Source Contribution -->
          <div class="block md:hidden space-y-4">
            <div v-if="sourceContribution.length === 0" class="py-6 text-center text-xs text-gray-500 font-semibold">
              Belum ada data kontribusi lead partner.
            </div>
            <div 
              v-for="(sc, index) in sourceContribution" 
              :key="index"
              class="bg-brand-charcoal/60 border border-brand-charcoal-light/20 p-4 rounded-2xl space-y-3 animate-fade-in"
            >
              <div class="flex items-center justify-between border-b border-brand-charcoal-light/10 pb-2">
                <span class="text-white font-bold select-none text-xs">{{ sc.source_type }}</span>
                <span class="text-brand-emerald font-bold font-mono text-xs">{{ formatCurrency(sc.confirmed_revenue) }}</span>
              </div>
              <div>
                <h4 class="font-bold text-gray-200 text-xs">{{ sc.vendor_name }}</h4>
                <p class="text-[10px] text-gray-500 mt-0.5">Sales: {{ sc.sales_name || '-' }}</p>
              </div>
              <div class="grid grid-cols-3 gap-2 bg-black/20 p-2.5 rounded-xl border border-white/5 text-[10px] font-semibold text-center">
                <div>
                  <p class="text-gray-500 text-[8px] uppercase tracking-wider">Proyek</p>
                  <p class="text-white">{{ sc.total_projects }} ({{ sc.deal_count }} Deal)</p>
                </div>
                <div>
                  <p class="text-red-400 text-[8px] uppercase tracking-wider">Batal</p>
                  <p class="text-white">{{ sc.cancel_count }}</p>
                </div>
                <div>
                  <p class="text-gray-400 text-[8px] uppercase tracking-wider">Avg Value</p>
                  <p class="text-white">{{ formatCurrency(sc.average_project_value) }}</p>
                </div>
              </div>
              <div class="text-[10px] text-gray-400 text-right">
                Potential: <span class="text-white font-mono font-bold">{{ formatCurrency(sc.potential_revenue) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- TAB 4: Commercial Risks exceptions -->
      <div v-show="activeTab === 'risiko'" class="space-y-6">
        <CommercialRisksPanel :commercial-risks="commercialRisks" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

// Shared UI Components
import AppPageHeader from '../components/ui/AppPageHeader.vue'
import AppLoadingState from '../components/ui/AppLoadingState.vue'
import AppErrorState from '../components/ui/AppErrorState.vue'

// Local Components
import PoControlSummaryCards from '../components/commercial/PoControlSummaryCards.vue'
import PoControlFilters from '../components/commercial/PoControlFilters.vue'
import FollowUpPriorityList from '../components/commercial/FollowUpPriorityList.vue'
import CommercialRisksPanel from '../components/commercial/CommercialRisksPanel.vue'

const users = ref([])
const summary = ref({
  total_owned_projects: 0,
  total_deal: 0,
  total_cancel: 0,
  deal_rate: 0,
  cancel_rate: 0,
  potential_revenue: 0,
  confirmed_revenue: 0,
  average_project_value: 0,
  outstanding_count: 0,
  invoice_sent_count: 0,
  paid_count: 0,
  follow_up_needed_count: 0,
  active_projects: 0,
  pending_quotation_projects: 0,
  follow_up_needed_projects: 0,
  cancelled_projects: 0,
  outstanding_payment: 0.0,
  commercial_risk_count: 0
})

const quotationSummary = ref({
  draft_count: 0,
  sent_count: 0,
  follow_up_count: 0,
  revision_count: 0,
  signed_deal_count: 0,
  cancel_count: 0
})

const revenueSummary = ref({
  potential_revenue: 0,
  confirmed_revenue: 0,
  revenue_conversion_rate: 0,
  average_project_value: 0,
  highest_project_value: 0,
  lowest_project_value: 0
})

const followUpPriorities = ref([])
const ownedProjects = ref([])
const poPerformance = ref([])
const sourceContribution = ref([])
const commercialRisks = ref({
  cancel_without_reason: [],
  signed_deal_without_budget: [],
  outstanding_payment: [],
  invoice_sent_not_paid: [],
  missing_po: [],
  missing_source: []
})

const loading = ref(true)
const error = ref(null)
const activeTab = ref('priority')

// Filters state
const appliedFilters = ref({
  event_window: 'all',
  include_closed: false,
  include_canceled: false
})

const handleFilterChange = (newFilters) => {
  appliedFilters.value = newFilters
  fetchControlCenterData()
}

const totalRisksCount = computed(() => {
  const r = commercialRisks.value
  if (!r) return 0
  return (r.cancel_without_reason?.length || 0) +
         (r.signed_deal_without_budget?.length || 0) +
         (r.outstanding_payment?.length || 0) +
         (r.invoice_sent_not_paid?.length || 0) +
         (r.missing_po?.length || 0) +
         (r.missing_source?.length || 0)
})

const tabs = computed(() => [
  { id: 'priority', name: 'Prioritas Follow-up', count: followUpPriorities.value.length },
  { id: 'projects', name: 'Daftar Proyek PO', count: ownedProjects.value.length },
  { id: 'kinerja', name: 'Kinerja Komersial' },
  { id: 'risiko', name: 'Risiko Komersial', count: totalRisksCount.value }
])

const fetchUsers = async () => {
  try {
    const res = await axios.get('/api/v1/auth/users')
    users.value = res.data
  } catch (err) {
    console.error('Failed to load users for PO filters', err)
  }
}

const fetchControlCenterData = async () => {
  loading.value = true
  error.value = null
  try {
    const params = {
      event_window: appliedFilters.value.event_window,
      include_closed: appliedFilters.value.include_closed,
      include_canceled: appliedFilters.value.include_canceled
    }
    if (appliedFilters.value.po_id) params.po_id = appliedFilters.value.po_id
    if (appliedFilters.value.pm_id) params.pm_id = appliedFilters.value.pm_id
    if (appliedFilters.value.source_type) params.source_type = appliedFilters.value.source_type
    if (appliedFilters.value.customer_category) params.customer_category = appliedFilters.value.customer_category
    if (appliedFilters.value.quotation_status) params.quotation_status = appliedFilters.value.quotation_status
    if (appliedFilters.value.program_status) params.program_status = appliedFilters.value.program_status
    if (appliedFilters.value.payment_status) params.payment_status = appliedFilters.value.payment_status
    if (appliedFilters.value.project_status) params.project_status = appliedFilters.value.project_status
    if (appliedFilters.value.date_from) params.date_from = appliedFilters.value.date_from
    if (appliedFilters.value.date_to) params.date_to = appliedFilters.value.date_to

    const res = await axios.get('/api/v1/dashboard/po-control-center', { params })
    
    summary.value = res.data.summary
    quotationSummary.value = res.data.quotation_summary
    revenueSummary.value = res.data.revenue_summary
    followUpPriorities.value = res.data.follow_up_priorities
    ownedProjects.value = res.data.owned_projects
    poPerformance.value = res.data.po_performance
    sourceContribution.value = res.data.source_contribution
    commercialRisks.value = res.data.commercial_risks
  } catch (err) {
    console.error('Failed to load PO dashboard data', err)
    error.value = err.response?.data?.detail?.message || err.response?.data?.detail || 'Gagal memuat data PO Control Center.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchUsers()
  fetchControlCenterData()
})

// Formatting helpers
const formatDate = (val) => {
  if (!val) return '-'
  return new Date(val).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

const formatCurrency = (val) => {
  if (val === null || val === undefined) return 'Rp 0'
  return 'Rp ' + Number(val).toLocaleString('id-ID', { minimumFractionDigits: 0, maximumFractionDigits: 0 })
}

// Status Badges class helpers
const getQuotationStatusClass = (status) => {
  if (status === 'Signed & Deal') return 'bg-brand-emerald/15 text-brand-emerald border border-brand-emerald/20'
  if (status === 'Cancel') return 'bg-red-500/10 text-red-400 border border-red-500/20'
  if (status === 'Draft') return 'bg-gray-600/20 text-gray-400 border border-gray-600/20'
  return 'bg-amber-500/10 text-amber-500 border border-amber-500/20'
}

const getProgramStatusClass = (status) => {
  const success = ['Confirmed', 'Ready', 'Running', 'Completed', 'Reporting', 'Closed']
  if (success.includes(status)) return 'bg-brand-emerald/15 text-brand-emerald border border-brand-emerald/20'
  if (status === 'Cancel') return 'bg-red-500/10 text-red-400 border border-red-500/20'
  return 'bg-brand-blue/10 text-brand-blue border border-brand-blue/20'
}

const getPaymentStatusClass = (status) => {
  if (status === 'Paid') return 'bg-brand-emerald/15 text-brand-emerald border border-brand-emerald/20'
  if (['Outstanding', 'Overdue'].includes(status)) return 'bg-red-500/10 text-red-400 border border-red-500/20'
  if (status === 'Invoice Sent') return 'bg-indigo-500/15 text-indigo-400 border border-indigo-500/20'
  return 'bg-gray-600/20 text-gray-400 border border-gray-600/20'
}
</script>

<style scoped>
.glass-panel {
  background: rgba(26, 32, 44, 0.75);
  backdrop-filter: blur(12px);
  border-radius: 1.25rem;
}
</style>
