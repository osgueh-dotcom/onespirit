<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 select-none">
      <div>
        <h2 class="text-xl font-bold text-white tracking-wide">PO Control Center</h2>
        <p class="text-xs text-gray-400 mt-1">
          Pusat kontrol komersial untuk membantu Program Owner memantau quotation, deal/cancel, revenue, source, outstanding, dan prioritas follow-up.
        </p>
      </div>
      <div class="flex items-center gap-2">
        <button 
          @click="fetchControlCenterData"
          class="px-4 py-2 rounded-xl bg-brand-charcoal border border-brand-charcoal-light/35 hover:border-brand-orange/40 text-xs font-bold text-gray-300 hover:text-white transition-all flex items-center gap-2"
        >
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
          </svg>
          Refresh Data
        </button>
      </div>
    </div>

    <!-- Filters Bar -->
    <div class="glass-panel p-5 border border-brand-charcoal-light/30 space-y-4 select-none">
      <div class="flex items-center justify-between border-b border-brand-charcoal-light/15 pb-2">
        <span class="text-[10px] font-black uppercase tracking-wider text-gray-400">Filter Komersial</span>
        <button @click="resetFilters" class="text-[10px] font-bold text-brand-orange hover:underline">
          Reset Filter ✕
        </button>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4">
        <!-- Filter PO -->
        <div>
          <label class="block text-[9px] font-extrabold uppercase tracking-widest text-gray-500 mb-1.5">Program Owner (PO)</label>
          <select 
            v-model="filterPo" 
            @change="fetchControlCenterData"
            class="w-full px-3 py-2 rounded-lg bg-brand-charcoal-dark border border-brand-charcoal-light/45 hover:border-brand-orange/30 text-[11px] font-semibold text-gray-300 outline-none transition-all"
          >
            <option value="">Semua PO</option>
            <option v-for="u in users" :key="u.id" :value="u.id">{{ u.full_name }}</option>
          </select>
        </div>

        <!-- Filter PM -->
        <div>
          <label class="block text-[9px] font-extrabold uppercase tracking-widest text-gray-500 mb-1.5">Program Manager (PM)</label>
          <select 
            v-model="filterPm" 
            @change="fetchControlCenterData"
            class="w-full px-3 py-2 rounded-lg bg-brand-charcoal-dark border border-brand-charcoal-light/45 hover:border-brand-orange/30 text-[11px] font-semibold text-gray-300 outline-none transition-all"
          >
            <option value="">Semua PM</option>
            <option v-for="u in users" :key="u.id" :value="u.id">{{ u.full_name }}</option>
          </select>
        </div>

        <!-- Source Type -->
        <div>
          <label class="block text-[9px] font-extrabold uppercase tracking-widest text-gray-500 mb-1.5">Source Type</label>
          <select 
            v-model="filterSourceType" 
            @change="fetchControlCenterData"
            class="w-full px-3 py-2 rounded-lg bg-brand-charcoal-dark border border-brand-charcoal-light/45 hover:border-brand-orange/30 text-[11px] font-semibold text-gray-300 outline-none transition-all"
          >
            <option value="">Semua Source</option>
            <option value="Hotel">Hotel</option>
            <option value="Direct">Direct</option>
            <option value="Repeater">Repeater</option>
            <option value="Partner">Partner</option>
            <option value="Instagram">Instagram</option>
            <option value="Web">Web</option>
            <option value="Other">Other</option>
          </select>
        </div>

        <!-- Customer Category -->
        <div>
          <label class="block text-[9px] font-extrabold uppercase tracking-widest text-gray-500 mb-1.5">Kategori Klien</label>
          <select 
            v-model="filterCustomerCategory" 
            @change="fetchControlCenterData"
            class="w-full px-3 py-2 rounded-lg bg-brand-charcoal-dark border border-brand-charcoal-light/45 hover:border-brand-orange/30 text-[11px] font-semibold text-gray-300 outline-none transition-all"
          >
            <option value="">Semua Kategori</option>
            <option value="Corporate">Corporate</option>
            <option value="Agency">Agency</option>
            <option value="Partner">Partner</option>
            <option value="Government">Government</option>
            <option value="Other">Other</option>
          </select>
        </div>

        <!-- Date Range From -->
        <div>
          <label class="block text-[9px] font-extrabold uppercase tracking-widest text-gray-500 mb-1.5">Dari Tanggal</label>
          <input 
            v-model="filterDateFrom" 
            type="date"
            @change="fetchControlCenterData"
            class="w-full px-3 py-2 rounded-lg bg-brand-charcoal-dark border border-brand-charcoal-light/45 hover:border-brand-orange/30 text-[11px] font-semibold text-gray-300 outline-none transition-all"
          />
        </div>

        <!-- Date Range To -->
        <div>
          <label class="block text-[9px] font-extrabold uppercase tracking-widest text-gray-500 mb-1.5">Sampai Tanggal</label>
          <input 
            v-model="filterDateTo" 
            type="date"
            @change="fetchControlCenterData"
            class="w-full px-3 py-2 rounded-lg bg-brand-charcoal-dark border border-brand-charcoal-light/45 hover:border-brand-orange/30 text-[11px] font-semibold text-gray-300 outline-none transition-all"
          />
        </div>
      </div>

      <!-- Second Row of Filters -->
      <div class="grid grid-cols-1 md:grid-cols-4 lg:grid-cols-6 gap-4 border-t border-brand-charcoal-light/10 pt-4">
        <!-- Quotation Status -->
        <div>
          <label class="block text-[9px] font-extrabold uppercase tracking-widest text-gray-500 mb-1.5">Status Quotation</label>
          <select 
            v-model="filterQuotationStatus" 
            @change="fetchControlCenterData"
            class="w-full px-3 py-2 rounded-lg bg-brand-charcoal-dark border border-brand-charcoal-light/45 hover:border-brand-orange/30 text-[11px] font-semibold text-gray-300 outline-none transition-all"
          >
            <option value="">Semua Quotation</option>
            <option value="Draft">Draft</option>
            <option value="Sent">Sent</option>
            <option value="Follow Up">Follow Up</option>
            <option value="Revision">Revision</option>
            <option value="Signed & Deal">Signed & Deal</option>
            <option value="Cancel">Cancel</option>
          </select>
        </div>

        <!-- Program Status -->
        <div>
          <label class="block text-[9px] font-extrabold uppercase tracking-widest text-gray-500 mb-1.5">Status Program</label>
          <select 
            v-model="filterProgramStatus" 
            @change="fetchControlCenterData"
            class="w-full px-3 py-2 rounded-lg bg-brand-charcoal-dark border border-brand-charcoal-light/45 hover:border-brand-orange/30 text-[11px] font-semibold text-gray-300 outline-none transition-all"
          >
            <option value="">Semua Program</option>
            <option value="Inquiry">Inquiry</option>
            <option value="Confirmed">Confirmed</option>
            <option value="Preparation">Preparation</option>
            <option value="Ready">Ready</option>
            <option value="Running">Running</option>
            <option value="Completed">Completed</option>
            <option value="Reporting">Reporting</option>
            <option value="Closed">Closed</option>
            <option value="Cancel">Cancel</option>
          </select>
        </div>

        <!-- Payment Status -->
        <div>
          <label class="block text-[9px] font-extrabold uppercase tracking-widest text-gray-500 mb-1.5">Status Pembayaran</label>
          <select 
            v-model="filterPaymentStatus" 
            @change="fetchControlCenterData"
            class="w-full px-3 py-2 rounded-lg bg-brand-charcoal-dark border border-brand-charcoal-light/45 hover:border-brand-orange/30 text-[11px] font-semibold text-gray-300 outline-none transition-all"
          >
            <option value="">Semua Pembayaran</option>
            <option value="Not Invoiced">Not Invoiced</option>
            <option value="Invoice Sent">Invoice Sent</option>
            <option value="Partial Paid">Partial Paid</option>
            <option value="Paid">Paid</option>
            <option value="Outstanding">Outstanding</option>
            <option value="Overdue">Overdue</option>
          </select>
        </div>

        <!-- Event Window -->
        <div>
          <label class="block text-[9px] font-extrabold uppercase tracking-widest text-gray-500 mb-1.5">Event Window</label>
          <select 
            v-model="filterEventWindow" 
            @change="fetchControlCenterData"
            class="w-full px-3 py-2 rounded-lg bg-brand-charcoal-dark border border-brand-charcoal-light/45 hover:border-brand-orange/30 text-[11px] font-semibold text-gray-300 outline-none transition-all"
          >
            <option value="all">Semua Jadwal</option>
            <option value="today">Hari Ini</option>
            <option value="next_7_days">7 Hari ke Depan</option>
            <option value="next_14_days">14 Hari ke Depan</option>
            <option value="this_month">Bulan Ini</option>
            <option value="overdue">Terlambat (Overdue)</option>
          </select>
        </div>

        <!-- Checkboxes -->
        <div class="md:col-span-2 flex items-center gap-4 pt-4 select-none">
          <label class="flex items-center gap-2 text-[10px] font-bold text-gray-400 hover:text-white cursor-pointer transition-colors">
            <input 
              v-model="filterIncludeClosed" 
              type="checkbox" 
              @change="fetchControlCenterData"
              class="rounded bg-brand-charcoal border-brand-charcoal-light/40 text-brand-orange focus:ring-0"
            />
            Closed Project
          </label>
          <label class="flex items-center gap-2 text-[10px] font-bold text-gray-400 hover:text-white cursor-pointer transition-colors">
            <input 
              v-model="filterIncludeCanceled" 
              type="checkbox" 
              @change="fetchControlCenterData"
              class="rounded bg-brand-charcoal border-brand-charcoal-light/40 text-brand-orange focus:ring-0"
            />
            Batal (Canceled)
          </label>
        </div>
      </div>
    </div>

    <!-- Error State -->
    <div v-if="error" class="glass-panel p-8 border border-red-500/20 text-center space-y-3">
      <p class="text-sm font-bold text-red-400">{{ error }}</p>
      <button 
        @click="fetchControlCenterData"
        class="px-4 py-2 bg-red-500/10 text-red-400 hover:bg-red-500/20 rounded-xl text-xs font-bold transition-all border border-red-500/20"
      >
        Coba Lagi
      </button>
    </div>

    <!-- Loading State -->
    <div v-else-if="loading" class="h-64 flex flex-col items-center justify-center gap-3">
      <svg class="animate-spin h-6 w-6 text-brand-orange" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
      <span class="text-xs text-gray-400 font-semibold">Mengompilasi data PO Control Center...</span>
    </div>

    <!-- Main Content -->
    <div v-else class="space-y-6">
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
          <div class="flex items-baseline gap-2">
            <span class="text-xl font-black text-amber-500">{{ summary.outstanding_count }}</span>
            <span class="text-[9px] text-amber-500 font-bold">Klien</span>
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

      <!-- Tab Buttons -->
      <div class="flex border-b border-brand-charcoal-light/25 select-none">
        <button 
          v-for="tab in tabs" 
          :key="tab.id"
          @click="activeTab = tab.id"
          class="px-5 py-3 text-xs font-bold transition-all border-b-2 outline-none flex items-center gap-2"
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
        <div class="glass-panel p-5 border border-brand-charcoal-light/20 space-y-4">
          <div class="flex items-center justify-between">
            <h3 class="text-sm font-bold text-white uppercase tracking-wider">Prioritas Tindakan Follow-up</h3>
            <span class="text-[10px] font-bold text-gray-400 bg-brand-charcoal-light/20 px-2 py-0.5 rounded">
              Aksi komersial mendesak berdasarkan sisa hari event, nilai budget, dan resiko pembayaran
            </span>
          </div>

          <div v-if="followUpPriorities.length === 0" class="py-12 text-center text-xs text-gray-500 font-semibold">
            Tidak ada prioritas follow-up terdeteksi. Semua quotation dan penagihan terpantau aman.
          </div>

          <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div 
              v-for="(act, idx) in followUpPriorities" 
              :key="idx"
              class="p-4 rounded-2xl border flex flex-col justify-between gap-3 text-xs group"
              :class="getPrioClass(act.priority_level)"
            >
              <div>
                <div class="flex items-center justify-between border-b border-brand-charcoal-light/10 pb-2 mb-2 select-none">
                  <span class="font-bold font-mono tracking-wider">{{ act.project_code || 'UNCODED' }}</span>
                  <span class="px-2 py-0.5 rounded text-[8px] font-black uppercase" :class="getPrioBadgeClass(act.priority_level)">
                    {{ act.priority_level }}
                  </span>
                </div>
                <h4 class="font-bold text-white text-sm mb-1 leading-snug group-hover:text-brand-orange transition-colors">
                  {{ act.program_name }}
                </h4>
                <p class="text-gray-400 font-semibold text-[10px] mb-1">Klien: {{ act.customer_name }} • Budget: {{ formatCurrency(act.budget) }}</p>
                <p class="text-gray-300 font-semibold text-[11px] mb-2">{{ act.reason }}</p>
                
                <div class="bg-black/20 p-2.5 rounded-xl border border-white/5 space-y-1">
                  <p class="text-[9px] font-black text-brand-orange uppercase tracking-wider select-none">Rekomendasi Aksi:</p>
                  <p class="text-white font-bold leading-normal">{{ act.recommended_action }}</p>
                </div>
              </div>
              <div class="pt-2 flex justify-end">
                <router-link 
                  :to="'/projects/' + act.project_id"
                  class="px-3 py-1.5 rounded bg-white/10 hover:bg-white/20 text-white font-bold text-[10px] transition-all"
                >
                  Buka Proyek →
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- TAB 2: Owned Projects List -->
      <div v-show="activeTab === 'projects'" class="space-y-6">
        <div class="glass-panel p-5 border border-brand-charcoal-light/20 space-y-4">
          <h3 class="text-sm font-bold text-white uppercase tracking-wider">Daftar Proyek di Bawah PO</h3>
          <div class="overflow-x-auto">
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
            <div class="overflow-x-auto">
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
          </div>
        </div>

        <!-- Source Contribution Table -->
        <div class="glass-panel p-5 border border-brand-charcoal-light/20 space-y-4">
          <h3 class="text-sm font-bold text-white uppercase tracking-wider">Kontribusi Lead Source & Vendor Partner</h3>
          <div class="overflow-x-auto">
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
        </div>
      </div>

      <!-- TAB 4: Commercial Risks exceptions -->
      <div v-show="activeTab === 'risiko'" class="space-y-6">
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

        <!-- Invoice Sent Not Paid -->
        <div class="glass-panel p-5 border border-brand-charcoal-light/20 space-y-3">
          <div class="flex items-center justify-between border-b border-brand-charcoal-light/10 pb-2">
            <h4 class="text-xs font-black text-white uppercase tracking-wider flex items-center gap-2">
              <span class="w-2 h-2 rounded-full bg-indigo-500"></span>
              Invoice Sent (Menunggu Pelunasan Klien)
            </h4>
          </div>

          <div v-if="!commercialRisks.invoice_sent_not_paid || commercialRisks.invoice_sent_not_paid.length === 0" class="text-xs text-gray-500 py-3 font-semibold text-center select-none">
            Tidak ada invoice dalam masa tunggu pembayaran.
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
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

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
  follow_up_needed_count: 0
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

// Filters variables
const filterPo = ref('')
const filterPm = ref('')
const filterSourceType = ref('')
const filterCustomerCategory = ref('')
const filterQuotationStatus = ref('')
const filterProgramStatus = ref('')
const filterPaymentStatus = ref('')
const filterProjectStatus = ref('')
const filterDateFrom = ref('')
const filterDateTo = ref('')
const filterEventWindow = ref('all')
const filterIncludeClosed = ref(false)
const filterIncludeCanceled = ref(false)

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
      event_window: filterEventWindow.value,
      include_closed: filterIncludeClosed.value,
      include_canceled: filterIncludeCanceled.value
    }
    if (filterPo.value) params.po_id = filterPo.value
    if (filterPm.value) params.pm_id = filterPm.value
    if (filterSourceType.value) params.source_type = filterSourceType.value
    if (filterCustomerCategory.value) params.customer_category = filterCustomerCategory.value
    if (filterQuotationStatus.value) params.quotation_status = filterQuotationStatus.value
    if (filterProgramStatus.value) params.program_status = filterProgramStatus.value
    if (filterPaymentStatus.value) params.payment_status = filterPaymentStatus.value
    if (filterProjectStatus.value) params.project_status = filterProjectStatus.value
    if (filterDateFrom.value) params.date_from = filterDateFrom.value
    if (filterDateTo.value) params.date_to = filterDateTo.value

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

const resetFilters = () => {
  filterPo.value = ''
  filterPm.value = ''
  filterSourceType.value = ''
  filterCustomerCategory.value = ''
  filterQuotationStatus.value = ''
  filterProgramStatus.value = ''
  filterPaymentStatus.value = ''
  filterProjectStatus.value = ''
  filterDateFrom.value = ''
  filterDateTo.value = ''
  filterEventWindow.value = 'all'
  filterIncludeClosed.value = false
  filterIncludeCanceled.value = false
  fetchControlCenterData()
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

// Priority Action class helpers
const getPrioClass = (prio) => {
  if (prio === 'Critical') return 'bg-red-500/10 border-red-500/30 text-white shadow-lg shadow-red-500/5'
  if (prio === 'High') return 'bg-amber-500/10 border-amber-500/30 text-white'
  if (prio === 'Medium') return 'bg-brand-blue/10 border-brand-blue/30 text-white'
  return 'bg-brand-charcoal/40 border-brand-charcoal-light/20 text-gray-400'
}

const getPrioBadgeClass = (prio) => {
  if (prio === 'Critical') return 'bg-red-500 text-white'
  if (prio === 'High') return 'bg-amber-500 text-black'
  if (prio === 'Medium') return 'bg-brand-blue text-white'
  return 'bg-gray-600 text-white'
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
