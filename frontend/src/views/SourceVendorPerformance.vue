<template>
  <div class="space-y-6">
    <!-- Header -->
    <AppPageHeader 
      title="Source & Vendor Performance Center" 
      subtitle="Analisis komprehensif performa lead source, kontribusi vendor partner, alokasi Program Owner, dan audit kualitas data komersial."
    >
      <template #actions>
        <button 
          @click="fetchPerformanceData"
          class="px-4 py-2 rounded-xl bg-brand-charcoal border border-brand-charcoal-light/35 hover:border-brand-orange/40 text-xs font-bold text-gray-300 hover:text-white transition-all flex items-center gap-2"
        >
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
          </svg>
          Refresh Analisis
        </button>
      </template>
    </AppPageHeader>

    <!-- Filters Bar -->
    <div class="glass-panel p-4 border border-brand-charcoal-light/20">
      <div class="flex flex-wrap items-center gap-4 text-xs">
        <!-- Date From -->
        <div class="flex flex-col gap-1">
          <label class="text-gray-400 font-bold select-none">Dari Tanggal</label>
          <input 
            type="date" 
            v-model="filters.date_from" 
            @change="fetchPerformanceData"
            class="bg-brand-charcoal-dark border border-brand-charcoal-light/30 rounded-xl px-3 py-1.5 text-white outline-none focus:border-brand-orange/50 transition-all font-mono"
          />
        </div>

        <!-- Date To -->
        <div class="flex flex-col gap-1">
          <label class="text-gray-400 font-bold select-none">Sampai Tanggal</label>
          <input 
            type="date" 
            v-model="filters.date_to" 
            @change="fetchPerformanceData"
            class="bg-brand-charcoal-dark border border-brand-charcoal-light/30 rounded-xl px-3 py-1.5 text-white outline-none focus:border-brand-orange/50 transition-all font-mono"
          />
        </div>

        <!-- Program Owner -->
        <div class="flex flex-col gap-1">
          <label class="text-gray-400 font-bold select-none">Program Owner (PO)</label>
          <select 
            v-model="filters.po_id" 
            @change="fetchPerformanceData"
            class="bg-brand-charcoal-dark border border-brand-charcoal-light/30 rounded-xl px-3 py-1.5 text-white outline-none focus:border-brand-orange/50 transition-all cursor-pointer font-bold"
          >
            <option value="">Semua PO</option>
            <option v-for="u in users" :key="u.id" :value="u.id">
              {{ u.full_name }} ({{ u.initial_code || u.email.split('@')[0].toUpperCase().slice(0, 3) }})
            </option>
          </select>
        </div>

        <!-- Checkboxes -->
        <div class="flex items-center gap-4 mt-4 select-none">
          <label class="inline-flex items-center gap-2 text-gray-300 font-bold cursor-pointer hover:text-white transition-colors">
            <input 
              type="checkbox" 
              v-model="filters.include_closed" 
              @change="fetchPerformanceData"
              class="rounded border-brand-charcoal-light bg-brand-charcoal text-brand-orange focus:ring-brand-orange/50"
            />
            Sertakan Closed
          </label>
          <label class="inline-flex items-center gap-2 text-gray-300 font-bold cursor-pointer hover:text-white transition-colors">
            <input 
              type="checkbox" 
              v-model="filters.include_canceled" 
              @change="fetchPerformanceData"
              class="rounded border-brand-charcoal-light bg-brand-charcoal text-brand-orange focus:ring-brand-orange/50"
            />
            Sertakan Batal
          </label>
        </div>

        <!-- Reset Button -->
        <button 
          @click="resetFilters"
          class="ml-auto px-4 py-2 mt-4 rounded-xl bg-red-500/10 hover:bg-red-500/25 border border-red-500/20 text-red-400 hover:text-white font-bold transition-all"
        >
          Reset Filter
        </button>
      </div>
    </div>

    <!-- Error State -->
    <AppErrorState 
      v-if="error" 
      title="Gagal Memuat Source & Vendor Performance" 
      :message="error" 
      @retry="fetchPerformanceData" 
    />

    <!-- Loading State -->
    <AppLoadingState v-else-if="loading" message="Memuat metrik analisis source & vendor..." />

    <!-- Main Dashboard Content -->
    <div v-else class="space-y-6">
      <!-- KPI Cards Summary Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 select-none animate-fade-in">
        <AppStatCard 
          title="Total Sources" 
          :value="summary.total_sources" 
          subtitle="Kategori Lead Source" 
          theme="blue" 
        />
        <AppStatCard 
          title="Total Vendors" 
          :value="summary.total_vendors" 
          subtitle="Vendor Partner" 
          theme="amber" 
        />
        <AppStatCard 
          title="Proyek Dianalisis" 
          :value="summary.total_projects_analyzed" 
          subtitle="Event Project Terdaftar" 
          theme="orange" 
        />
        <AppStatCard 
          title="Estimasi Revenue" 
          :value="formatCurrency(summary.total_potential_revenue)" 
          subtitle="Potential Revenue" 
          theme="neutral" 
        />
        <AppStatCard 
          title="Revenue Terkonfirmasi" 
          :value="formatCurrency(summary.total_confirmed_revenue)" 
          subtitle="Confirmed Revenue" 
          theme="emerald" 
        />
        <AppStatCard 
          title="Outstanding Pembayaran" 
          :value="formatCurrency(summary.total_outstanding_payment)" 
          subtitle="Belum Melunasi" 
          theme="red" 
        />
        <AppStatCard 
          title="Rata-rata Konversi" 
          :value="`${Math.round(summary.average_conversion_rate)}%`" 
          subtitle="Rasio Deal Opportunity" 
          theme="emerald" 
        />
        <AppStatCard 
          title="Risiko Komersial" 
          :value="summary.commercial_risk_count" 
          subtitle="Peringatan Audit Data" 
          theme="purple" 
        />
      </div>

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

      <!-- TAB 1: Source Performance -->
      <div v-show="activeTab === 'sources'" class="space-y-4">
        <div class="glass-panel p-5 border border-brand-charcoal-light/20 space-y-4">
          <h3 class="text-sm font-bold text-white uppercase tracking-wider">Performa Sumber Project (Lead Source Performance)</h3>
          
          <!-- Desktop Table View -->
          <div class="hidden lg:block overflow-x-auto">
            <table class="min-w-full text-left text-xs divide-y divide-brand-charcoal-light/10">
              <thead class="bg-brand-charcoal-dark/30 text-[9px] font-extrabold uppercase tracking-widest text-gray-500 select-none">
                <tr>
                  <th class="px-4 py-3">Lead Source</th>
                  <th class="px-4 py-3 text-center">Total Projects</th>
                  <th class="px-4 py-3 text-center">Active</th>
                  <th class="px-4 py-3 text-center">Confirmed</th>
                  <th class="px-4 py-3 text-center">Pending Q</th>
                  <th class="px-4 py-3 text-center">Canceled</th>
                  <th class="px-4 py-3 text-right">Potential Revenue</th>
                  <th class="px-4 py-3 text-right">Confirmed Revenue</th>
                  <th class="px-4 py-3 text-right">Outstanding Payment</th>
                  <th class="px-4 py-3 text-center">Conversion</th>
                  <th class="px-4 py-3 text-center">Risk Count</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-brand-charcoal-light/5 font-medium">
                <tr v-if="sourcePerformance.length === 0">
                  <td colspan="11" class="px-4 py-8 text-center text-gray-500 font-semibold">
                    Tidak ada data performa source untuk filter ini.
                  </td>
                </tr>
                <tr 
                  v-for="s in sourcePerformance" 
                  :key="s.source_type"
                  class="hover:bg-white/5 transition-colors"
                >
                  <td class="px-4 py-3 whitespace-nowrap font-bold text-white select-all">
                    {{ s.source_type }}
                  </td>
                  <td class="px-4 py-3 text-center text-gray-300 font-mono font-bold">{{ s.total_projects }}</td>
                  <td class="px-4 py-3 text-center text-indigo-400 font-bold">{{ s.active_projects }}</td>
                  <td class="px-4 py-3 text-center text-brand-emerald font-bold">{{ s.confirmed_projects }}</td>
                  <td class="px-4 py-3 text-center text-amber-500 font-bold">{{ s.pending_quotation_projects }}</td>
                  <td class="px-4 py-3 text-center text-red-400 font-bold">{{ s.cancelled_projects }}</td>
                  <td class="px-4 py-3 text-right font-mono text-gray-300">{{ formatCurrency(s.potential_revenue) }}</td>
                  <td class="px-4 py-3 text-right font-mono text-brand-emerald font-bold">{{ formatCurrency(s.confirmed_revenue) }}</td>
                  <td class="px-4 py-3 text-right font-mono" :class="s.outstanding_payment > 0 ? 'text-red-400 font-bold' : 'text-gray-400'">
                    {{ formatCurrency(s.outstanding_payment) }}
                  </td>
                  <td class="px-4 py-3 text-center font-bold text-brand-emerald font-mono">
                    {{ Math.round(s.conversion_rate) }}%
                  </td>
                  <td class="px-4 py-3 text-center">
                    <span 
                      v-if="s.commercial_risk > 0" 
                      class="px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 text-[10px] font-black"
                    >
                      {{ s.commercial_risk }} Risk
                    </span>
                    <span v-else class="text-brand-emerald font-semibold">-</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Mobile Card List -->
          <div class="block lg:hidden space-y-4">
            <div v-if="sourcePerformance.length === 0" class="py-6 text-center text-xs text-gray-500 font-semibold">
              Tidak ada data performa source untuk filter ini.
            </div>
            <div 
              v-for="s in sourcePerformance" 
              :key="s.source_type"
              class="bg-brand-charcoal/60 border border-brand-charcoal-light/20 p-4 rounded-2xl space-y-3 animate-fade-in"
            >
              <div class="flex items-center justify-between border-b border-brand-charcoal-light/10 pb-2">
                <span class="text-white font-bold select-none text-xs">{{ s.source_type }}</span>
                <span class="text-brand-emerald font-bold font-mono text-xs">{{ Math.round(s.conversion_rate) }}% Deal Rate</span>
              </div>
              <div class="grid grid-cols-2 gap-2 bg-black/20 p-2.5 rounded-xl border border-white/5 text-[11px] font-semibold">
                <div>
                  <p class="text-gray-500 text-[9px] uppercase tracking-wider">Total Proyek</p>
                  <p class="text-white font-bold">{{ s.total_projects }} Proyek</p>
                  <p class="text-[9px] text-gray-400 mt-0.5">Active: {{ s.active_projects }} • Deal: {{ s.confirmed_projects }}</p>
                </div>
                <div>
                  <p class="text-gray-500 text-[9px] uppercase tracking-wider">Status Keuangan</p>
                  <p class="text-brand-emerald font-mono font-bold">Confirmed: {{ formatCurrency(s.confirmed_revenue) }}</p>
                  <p class="text-red-400 font-mono text-[10px]">Outstanding: {{ formatCurrency(s.outstanding_payment) }}</p>
                </div>
              </div>
              <div class="flex justify-between items-center text-[10px] text-gray-400">
                <span>Potential: <b class="text-white font-mono">{{ formatCurrency(s.potential_revenue) }}</b></span>
                <span v-if="s.commercial_risk > 0" class="px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 text-[9px] font-bold">
                  {{ s.commercial_risk }} Risk
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- TAB 2: Vendor Performance -->
      <div v-show="activeTab === 'vendors'" class="space-y-4">
        <div class="glass-panel p-5 border border-brand-charcoal-light/20 space-y-4">
          <div class="flex items-center justify-between">
            <h3 class="text-sm font-bold text-white uppercase tracking-wider">Performa Vendor Partner (Vendor Performance)</h3>
            <span class="text-[10px] font-black text-gray-400 uppercase bg-brand-charcoal-light/20 px-2 py-0.5 rounded select-none">Kualitas Data</span>
          </div>

          <!-- Empty state description / limitation warning -->
          <div class="bg-amber-500/5 border border-amber-500/10 rounded-xl p-4 text-xs text-amber-400 space-y-1">
            <p class="font-bold">Data Vendor Masih Terbatas:</p>
            <p class="leading-relaxed">
              Analisis performa vendor saat ini didasarkan pada pencatatan field tekstual vendor_name di dalam entitas EventSource.
              Jika data vendor terstruktur belum lengkap, sistem akan menampilkan data apa adanya.
            </p>
          </div>

          <!-- Desktop Table View -->
          <div class="hidden lg:block overflow-x-auto">
            <table class="min-w-full text-left text-xs divide-y divide-brand-charcoal-light/10">
              <thead class="bg-brand-charcoal-dark/30 text-[9px] font-extrabold uppercase tracking-widest text-gray-500 select-none">
                <tr>
                  <th class="px-4 py-3">Nama Vendor Partner</th>
                  <th class="px-4 py-3 text-center">Total Projects</th>
                  <th class="px-4 py-3 text-center">Active</th>
                  <th class="px-4 py-3 text-center">Confirmed</th>
                  <th class="px-4 py-3 text-center">Canceled</th>
                  <th class="px-4 py-3 text-right">Potential Revenue</th>
                  <th class="px-4 py-3 text-right">Confirmed Revenue</th>
                  <th class="px-4 py-3 text-right">Average Value</th>
                  <th class="px-4 py-3 text-center">Usage Frequency</th>
                  <th class="px-4 py-3 text-center">Risk Count</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-brand-charcoal-light/5 font-medium">
                <tr v-if="vendorPerformance.length === 0">
                  <td colspan="10" class="px-4 py-8 text-center text-gray-500 font-semibold">
                    Tidak ada data performa vendor partner.
                  </td>
                </tr>
                <tr 
                  v-for="v in vendorPerformance" 
                  :key="v.vendor_name"
                  class="hover:bg-white/5 transition-colors"
                >
                  <td class="px-4 py-3 whitespace-nowrap font-bold text-white select-all">
                    {{ v.vendor_name }}
                  </td>
                  <td class="px-4 py-3 text-center text-gray-300 font-mono font-bold">{{ v.total_projects }}</td>
                  <td class="px-4 py-3 text-center text-indigo-400 font-bold">{{ v.active_projects }}</td>
                  <td class="px-4 py-3 text-center text-brand-emerald font-bold">{{ v.confirmed_projects }}</td>
                  <td class="px-4 py-3 text-center text-red-400 font-bold">{{ v.cancelled_projects }}</td>
                  <td class="px-4 py-3 text-right font-mono text-gray-300">{{ formatCurrency(v.potential_revenue) }}</td>
                  <td class="px-4 py-3 text-right font-mono text-brand-emerald font-bold">{{ formatCurrency(v.confirmed_revenue) }}</td>
                  <td class="px-4 py-3 text-right font-mono text-gray-400">{{ formatCurrency(v.average_project_value) }}</td>
                  <td class="px-4 py-3 text-center font-bold text-white font-mono">
                    {{ v.usage_frequency }}x
                  </td>
                  <td class="px-4 py-3 text-center">
                    <span 
                      v-if="v.risk_count > 0" 
                      class="px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 text-[10px] font-black"
                    >
                      {{ v.risk_count }} Risk
                    </span>
                    <span v-else class="text-brand-emerald font-semibold">-</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Mobile Card List -->
          <div class="block lg:hidden space-y-4">
            <div v-if="vendorPerformance.length === 0" class="py-6 text-center text-xs text-gray-500 font-semibold">
              Tidak ada data performa vendor partner.
            </div>
            <div 
              v-for="v in vendorPerformance" 
              :key="v.vendor_name"
              class="bg-brand-charcoal/60 border border-brand-charcoal-light/20 p-4 rounded-2xl space-y-3 animate-fade-in"
            >
              <div class="flex items-center justify-between border-b border-brand-charcoal-light/10 pb-2">
                <span class="text-white font-bold select-none text-xs">{{ v.vendor_name }}</span>
                <span class="px-2 py-0.5 rounded text-[10px] bg-indigo-500/10 text-indigo-400 font-mono">Dipakai {{ v.usage_frequency }}x</span>
              </div>
              <div class="grid grid-cols-2 gap-2 bg-black/20 p-2.5 rounded-xl border border-white/5 text-[11px] font-semibold">
                <div>
                  <p class="text-gray-500 text-[9px] uppercase tracking-wider">Total Proyek</p>
                  <p class="text-white font-bold">{{ v.total_projects }} Proyek</p>
                  <p class="text-[9px] text-gray-400 mt-0.5">Active: {{ v.active_projects }} • Deal: {{ v.confirmed_projects }}</p>
                </div>
                <div>
                  <p class="text-gray-500 text-[9px] uppercase tracking-wider">Pendapatan Vendor</p>
                  <p class="text-brand-emerald font-mono font-bold">Confirmed: {{ formatCurrency(v.confirmed_revenue) }}</p>
                  <p class="text-gray-400 font-mono text-[10px]">Avg Value: {{ formatCurrency(v.average_project_value) }}</p>
                </div>
              </div>
              <div class="flex justify-between items-center text-[10px] text-gray-400">
                <span>Potential: <b class="text-white font-mono">{{ formatCurrency(v.potential_revenue) }}</b></span>
                <span v-if="v.risk_count > 0" class="px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 text-[9px] font-bold">
                  {{ v.risk_count }} Risk
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- TAB 3: PO + Source Performance -->
      <div v-show="activeTab === 'po_sources'" class="space-y-4">
        <div class="glass-panel p-5 border border-brand-charcoal-light/20 space-y-4">
          <h3 class="text-sm font-bold text-white uppercase tracking-wider">Distribusi Alokasi PO & Event Source</h3>
          
          <!-- Desktop Table View -->
          <div class="hidden lg:block overflow-x-auto">
            <table class="min-w-full text-left text-xs divide-y divide-brand-charcoal-light/10">
              <thead class="bg-brand-charcoal-dark/30 text-[9px] font-extrabold uppercase tracking-widest text-gray-500 select-none">
                <tr>
                  <th class="px-4 py-3">Program Owner (PO)</th>
                  <th class="px-4 py-3">Lead Source Type</th>
                  <th class="px-4 py-3 text-center">Total Projects</th>
                  <th class="px-4 py-3 text-center">Confirmed Deals</th>
                  <th class="px-4 py-3 text-center">Pending Quotations</th>
                  <th class="px-4 py-3 text-right">Potential Revenue</th>
                  <th class="px-4 py-3 text-right">Confirmed Revenue</th>
                  <th class="px-4 py-3 text-center">Follow-up Load</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-brand-charcoal-light/5 font-medium">
                <tr v-if="poSourcePerformance.length === 0">
                  <td colspan="8" class="px-4 py-8 text-center text-gray-500 font-semibold">
                    Tidak ada data alokasi PO dan lead source.
                  </td>
                </tr>
                <tr 
                  v-for="(p, index) in poSourcePerformance" 
                  :key="index"
                  class="hover:bg-white/5 transition-colors"
                >
                  <td class="px-4 py-3 whitespace-nowrap font-bold text-white select-all">
                    {{ p.po_name }}
                  </td>
                  <td class="px-4 py-3 text-gray-300 font-semibold">{{ p.source_type }}</td>
                  <td class="px-4 py-3 text-center text-gray-300 font-mono font-bold">{{ p.total_projects }}</td>
                  <td class="px-4 py-3 text-center text-brand-emerald font-bold">{{ p.confirmed_projects }}</td>
                  <td class="px-4 py-3 text-center text-amber-500 font-bold">{{ p.pending_projects }}</td>
                  <td class="px-4 py-3 text-right font-mono text-gray-300">{{ formatCurrency(p.potential_revenue) }}</td>
                  <td class="px-4 py-3 text-right font-mono text-brand-emerald font-bold">{{ formatCurrency(p.confirmed_revenue) }}</td>
                  <td class="px-4 py-3 text-center">
                    <span 
                      v-if="p.follow_up_needed > 0" 
                      class="px-2 py-0.5 rounded bg-red-500/10 text-red-400 text-[10px] font-black"
                    >
                      {{ p.follow_up_needed }} F-Up
                    </span>
                    <span v-else class="text-brand-emerald font-semibold">-</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Mobile Card List -->
          <div class="block lg:hidden space-y-4">
            <div v-if="poSourcePerformance.length === 0" class="py-6 text-center text-xs text-gray-500 font-semibold">
              Tidak ada data alokasi PO dan lead source.
            </div>
            <div 
              v-for="(p, index) in poSourcePerformance" 
              :key="index"
              class="bg-brand-charcoal/60 border border-brand-charcoal-light/20 p-4 rounded-2xl space-y-3 animate-fade-in"
            >
              <div class="flex items-center justify-between border-b border-brand-charcoal-light/10 pb-2">
                <span class="text-white font-bold select-none text-xs">{{ p.po_name }}</span>
                <span class="text-gray-400 text-[11px] font-semibold">{{ p.source_type }}</span>
              </div>
              <div class="grid grid-cols-2 gap-2 bg-black/20 p-2.5 rounded-xl border border-white/5 text-[11px] font-semibold">
                <div>
                  <p class="text-gray-500 text-[9px] uppercase tracking-wider">Total Proyek</p>
                  <p class="text-white font-bold">{{ p.total_projects }} Proyek</p>
                  <p class="text-[9px] text-gray-400 mt-0.5">Confirmed: {{ p.confirmed_projects }} • Pending: {{ p.pending_projects }}</p>
                </div>
                <div>
                  <p class="text-gray-500 text-[9px] uppercase tracking-wider">Estimasi Revenue</p>
                  <p class="text-brand-emerald font-mono font-bold">Confirmed: {{ formatCurrency(p.confirmed_revenue) }}</p>
                  <p class="text-gray-400 font-mono text-[10px]">Potential: {{ formatCurrency(p.potential_revenue) }}</p>
                </div>
              </div>
              <div class="flex justify-end">
                <span v-if="p.follow_up_needed > 0" class="px-2 py-0.5 rounded bg-red-500/10 text-red-400 text-[9px] font-bold">
                  {{ p.follow_up_needed }} F-Up Needed
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Risk Alerts & Data Quality Panels -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Left: Risk Alerts -->
        <div class="glass-panel p-5 border border-brand-charcoal-light/20 space-y-4">
          <h3 class="text-sm font-bold text-white uppercase tracking-wider">Source dengan Risiko Tinggi (Risk Alerts)</h3>
          <div v-if="riskAlerts.length === 0" class="h-32 flex flex-col items-center justify-center text-gray-500">
            <svg class="w-8 h-8 text-brand-emerald/40 mb-2" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span class="text-xs font-semibold text-gray-400">Tidak ada alert risiko komersial terdeteksi.</span>
          </div>
          <div v-else class="space-y-3 max-h-72 overflow-y-auto pr-2">
            <div 
              v-for="(alert, index) in riskAlerts" 
              :key="index"
              class="p-3 rounded-xl border flex gap-3 items-start transition-all"
              :class="getAlertClass(alert.level)"
            >
              <div class="mt-0.5 font-black uppercase text-[8px] px-1.5 py-0.5 rounded" :class="getAlertBadgeClass(alert.level)">
                {{ alert.level }}
              </div>
              <div class="flex-1 text-xs">
                <p class="text-white font-bold leading-normal">{{ alert.message }}</p>
                <p class="text-[10px] text-gray-400 mt-1 uppercase font-semibold tracking-wider">Kategori: {{ alert.category }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Right: Data Quality Report -->
        <div class="glass-panel p-5 border border-brand-charcoal-light/20 space-y-4">
          <h3 class="text-sm font-bold text-white uppercase tracking-wider">Audit Kualitas Data (Data Quality)</h3>
          <div class="grid grid-cols-2 gap-4">
            <div class="bg-black/20 p-4 rounded-xl border border-white/5 text-center">
              <p class="text-[9px] font-black text-gray-500 uppercase tracking-widest mb-1">Missing Lead Source Mapping</p>
              <p class="text-2xl font-black text-white" :class="dataQuality.missing_source_count > 0 ? 'text-amber-400' : 'text-brand-emerald'">
                {{ dataQuality.missing_source_count }}
              </p>
              <span class="text-[8px] text-gray-400 block mt-1">Proyek tanpa Event Source</span>
            </div>

            <div class="bg-black/20 p-4 rounded-xl border border-white/5 text-center">
              <p class="text-[9px] font-black text-gray-500 uppercase tracking-widest mb-1">Missing Vendor Partners</p>
              <p class="text-2xl font-black text-white" :class="dataQuality.missing_vendor_count > 0 ? 'text-amber-400' : 'text-brand-emerald'">
                {{ dataQuality.missing_vendor_count }}
              </p>
              <span class="text-[8px] text-gray-400 block mt-1">Vendor name kosong / -</span>
            </div>
          </div>

          <div class="bg-brand-charcoal-dark/40 rounded-xl p-4 border border-white/5 text-xs text-gray-400 space-y-2">
            <div class="flex items-center gap-2 font-bold text-white">
              <svg class="w-4 h-4 text-indigo-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M11.25 11.25l.041-.02a.75.75 0 111.083 1.083l-.04.02m-.041 0a.75.75 0 001.083 1.083l.04-.02m-1.083-1.083A.75.75 0 0011.25 11.25zm.041-.02l.041-.02a.75.75 0 10-1.083-1.083l-.04.02m1.083 1.083a.75.75 0 00-1.083-1.083l-.04.02" />
              </svg>
              Sistem Fallback & Catatan Teknis:
            </div>
            <ul class="list-disc pl-4 space-y-1 leading-relaxed text-[11px] font-medium">
              <li v-for="(note, index) in dataQuality.notes" :key="index">{{ note }}</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

// Shared UI components
import AppPageHeader from '../components/ui/AppPageHeader.vue'
import AppStatCard from '../components/ui/AppStatCard.vue'
import AppLoadingState from '../components/ui/AppLoadingState.vue'
import AppErrorState from '../components/ui/AppErrorState.vue'

const users = ref([])
const loading = ref(true)
const error = ref(null)
const activeTab = ref('sources')

const filters = ref({
  po_id: '',
  date_from: '',
  date_to: '',
  include_closed: false,
  include_canceled: false
})

const summary = ref({
  total_sources: 0,
  total_vendors: 0,
  total_projects_analyzed: 0,
  total_potential_revenue: 0.0,
  total_confirmed_revenue: 0.0,
  total_outstanding_payment: 0.0,
  average_conversion_rate: 0.0,
  commercial_risk_count: 0
})

const sourcePerformance = ref([])
const vendorPerformance = ref([])
const poSourcePerformance = ref([])
const riskAlerts = ref([])
const dataQuality = ref({
  missing_source_count: 0,
  missing_vendor_count: 0,
  limited_vendor_data: true,
  notes: []
})

const tabs = computed(() => [
  { id: 'sources', name: 'Kinerja Lead Source', count: sourcePerformance.value.length },
  { id: 'vendors', name: 'Kinerja Vendor Partner', count: vendorPerformance.value.length },
  { id: 'po_sources', name: 'Alokasi PO & Source', count: poSourcePerformance.value.length }
])

const fetchUsers = async () => {
  try {
    const res = await axios.get('/api/v1/auth/users')
    users.value = res.value || res.data || []
  } catch (err) {
    console.error('Failed to load users for filters', err)
  }
}

const fetchPerformanceData = async () => {
  loading.value = true
  error.value = null
  try {
    const params = {
      include_closed: filters.value.include_closed,
      include_canceled: filters.value.include_canceled
    }
    if (filters.value.po_id) params.po_id = filters.value.po_id
    if (filters.value.date_from) params.date_from = filters.value.date_from
    if (filters.value.date_to) params.date_to = filters.value.date_to

    const res = await axios.get('/api/v1/dashboard/source-vendor-performance', { params })
    const d = res.data

    summary.value = d.summary
    sourcePerformance.value = d.source_performance || []
    vendorPerformance.value = d.vendor_performance || []
    poSourcePerformance.value = d.po_source_performance || []
    riskAlerts.value = d.risk_alerts || []
    dataQuality.value = d.data_quality || {
      missing_source_count: 0,
      missing_vendor_count: 0,
      limited_vendor_data: true,
      notes: []
    }
  } catch (err) {
    console.error('Failed to load performance analytics', err)
    error.value = err.response?.data?.detail?.message || err.response?.data?.detail || 'Gagal memuat data Source & Vendor Performance.'
  } finally {
    loading.value = false
  }
}

const resetFilters = () => {
  filters.value = {
    po_id: '',
    date_from: '',
    date_to: '',
    include_closed: false,
    include_canceled: false
  }
  fetchPerformanceData()
}

onMounted(() => {
  fetchUsers()
  fetchPerformanceData()
})

// Formatting helpers
const formatCurrency = (val) => {
  if (val === null || val === undefined) return 'Rp 0'
  return 'Rp ' + Number(val).toLocaleString('id-ID', { minimumFractionDigits: 0, maximumFractionDigits: 0 })
}

// Styling classes for Risk Alerts
const getAlertClass = (level) => {
  if (level === 'Critical') return 'bg-red-500/5 border-red-500/20 text-red-300'
  if (level === 'High') return 'bg-orange-500/5 border-orange-500/20 text-orange-300'
  if (level === 'Medium') return 'bg-amber-500/5 border-amber-500/20 text-amber-300'
  return 'bg-blue-500/5 border-blue-500/10 text-blue-300'
}

const getAlertBadgeClass = (level) => {
  if (level === 'Critical') return 'bg-red-500/20 text-red-400 border border-red-500/30'
  if (level === 'High') return 'bg-orange-500/20 text-orange-400 border border-orange-500/30'
  if (level === 'Medium') return 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
  return 'bg-blue-500/20 text-blue-400 border border-blue-500/30'
}
</script>

<style scoped>
.glass-panel {
  background: rgba(26, 32, 44, 0.75);
  backdrop-filter: blur(12px);
  border-radius: 1.25rem;
}
</style>
