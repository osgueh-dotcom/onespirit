<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 select-none">
      <div>
        <h2 class="text-xl font-bold text-white tracking-wide">PM Control Center</h2>
        <p class="text-xs text-gray-400 mt-1">
          Pusat kontrol operasional untuk membantu PM memantau event mendatang, readiness project, instrument overdue, dan prioritas tindakan.
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
        <span class="text-[10px] font-black uppercase tracking-wider text-gray-400">Filter Operasional</span>
        <button @click="resetFilters" class="text-[10px] font-bold text-brand-orange hover:underline">
          Reset Filter ✕
        </button>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4">
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

        <!-- Event Window -->
        <div>
          <label class="block text-[9px] font-extrabold uppercase tracking-widest text-gray-500 mb-1.5">Periode Event (Window)</label>
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

        <!-- Date Range -->
        <div class="md:col-span-2 grid grid-cols-2 gap-2">
          <div>
            <label class="block text-[9px] font-extrabold uppercase tracking-widest text-gray-500 mb-1.5">Dari Tanggal</label>
            <input 
              v-model="filterDateFrom" 
              type="date"
              @change="fetchControlCenterData"
              class="w-full px-3 py-2 rounded-lg bg-brand-charcoal-dark border border-brand-charcoal-light/45 hover:border-brand-orange/30 text-[11px] font-semibold text-gray-300 outline-none transition-all"
            />
          </div>
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

        <!-- Checkboxes Closed & Canceled -->
        <div class="flex items-center gap-4 pt-4">
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
      <span class="text-xs text-gray-400 font-semibold">Mengompilasi data PM Control Center...</span>
    </div>

    <!-- Main Content Grid -->
    <div v-else class="space-y-6">
      <!-- Operational KPI summary grid -->
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 select-none">
        <div class="glass-panel p-4 border border-brand-charcoal-light/25 bg-gradient-to-tr from-brand-charcoal-dark/30 to-brand-charcoal/20">
          <p class="text-[9px] font-extrabold uppercase tracking-widest text-gray-500 mb-1">Event Hari Ini</p>
          <div class="flex items-baseline gap-2">
            <span class="text-2xl font-black text-white">{{ summary.events_today }}</span>
            <span class="text-[10px] text-brand-orange font-bold">Event</span>
          </div>
        </div>
        
        <div class="glass-panel p-4 border border-brand-charcoal-light/25 bg-gradient-to-tr from-brand-charcoal-dark/30 to-brand-charcoal/20">
          <p class="text-[9px] font-extrabold uppercase tracking-widest text-gray-500 mb-1">Upcoming (7 Hari)</p>
          <div class="flex items-baseline gap-2">
            <span class="text-2xl font-black text-white">{{ summary.upcoming_events_7_days }}</span>
            <span class="text-[10px] text-indigo-400 font-bold">Event</span>
          </div>
        </div>

        <div class="glass-panel p-4 border border-brand-charcoal-light/25 bg-gradient-to-tr from-brand-charcoal-dark/30 to-brand-charcoal/20">
          <p class="text-[9px] font-extrabold uppercase tracking-widest text-gray-500 mb-1">Belum Siap (&lt;80%)</p>
          <div class="flex items-baseline gap-2">
            <span class="text-2xl font-black text-red-400">{{ summary.not_ready_projects }}</span>
            <span class="text-[10px] text-red-500 font-bold">Proyek</span>
          </div>
        </div>

        <div class="glass-panel p-4 border border-brand-charcoal-light/25 bg-gradient-to-tr from-brand-charcoal-dark/30 to-brand-charcoal/20">
          <p class="text-[9px] font-extrabold uppercase tracking-widest text-gray-500 mb-1">Instrumen Overdue</p>
          <div class="flex items-baseline gap-2">
            <span class="text-2xl font-black text-amber-500">{{ summary.overdue_instruments }}</span>
            <span class="text-[10px] text-amber-500 font-bold">Dokumen</span>
          </div>
        </div>

        <div class="glass-panel p-4 border border-brand-charcoal-light/25 bg-gradient-to-tr from-brand-charcoal-dark/30 to-brand-charcoal/20">
          <p class="text-[9px] font-extrabold uppercase tracking-widest text-gray-500 mb-1">Perlu Revisi</p>
          <div class="flex items-baseline gap-2">
            <span class="text-2xl font-black text-purple-400">{{ summary.need_revision_instruments }}</span>
            <span class="text-[10px] text-purple-400 font-bold">Revisi</span>
          </div>
        </div>

        <div class="glass-panel p-4 border border-brand-charcoal-light/25 bg-gradient-to-tr from-brand-charcoal-dark/30 to-brand-charcoal/20">
          <p class="text-[9px] font-extrabold uppercase tracking-widest text-gray-500 mb-1">Rata Kesiapan</p>
          <div class="flex items-baseline gap-2">
            <span class="text-2xl font-black text-brand-emerald">{{ Math.round(summary.average_readiness_score) }}%</span>
            <span class="text-[10px] text-brand-emerald font-bold">Skor</span>
          </div>
        </div>
      </div>

      <!-- Tab Buttons -->
      <div class="flex border-b border-brand-charcoal-light/25 select-none">
        <button 
          v-for="tab in tabs" 
          :key="tab.id"
          @click="activeTab = tab.id"
          class="px-5 py-3 text-xs font-bold tracking-wide transition-all border-b-2"
          :class="activeTab === tab.id ? 'border-brand-orange text-brand-orange bg-brand-orange/5' : 'border-transparent text-gray-400 hover:text-white'"
        >
          {{ tab.name }} ({{ tab.count }})
        </button>
      </div>

      <!-- TAB 1: Prioritas Tindakan -->
      <div v-show="activeTab === 'priority'" class="space-y-4">
        <div class="glass-panel p-5 border border-brand-charcoal-light/20 space-y-4">
          <div class="flex items-center justify-between">
            <h3 class="text-sm font-bold text-white uppercase tracking-wider">Priority Actions List</h3>
            <span class="text-[10px] font-bold text-gray-400 bg-brand-charcoal-light/20 px-2 py-0.5 rounded">
              Daftar aksi operasional yang diurutkan berdasarkan tingkat urgensi
            </span>
          </div>

          <div v-if="priorityActions.length === 0" class="py-12 text-center text-xs text-gray-500 font-semibold">
            Tidak ada tindakan prioritas terdeteksi. Semua proyek dalam kondisi aman.
          </div>

          <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div 
              v-for="(act, idx) in priorityActions" 
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
                  {{ act.title }}
                </h4>
                <p class="text-gray-300 font-semibold text-[11px] mb-2">{{ act.description }}</p>
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

      <!-- TAB 2: Upcoming & Not Ready Events -->
      <div v-show="activeTab === 'events'" class="space-y-6">
        <!-- Upcoming Events -->
        <div class="glass-panel p-5 border border-brand-charcoal-light/20 space-y-4">
          <h3 class="text-sm font-bold text-white uppercase tracking-wider">Jadwal Event Mendatang (14 Hari)</h3>
          <div class="overflow-x-auto">
            <table class="min-w-full text-left text-xs divide-y divide-brand-charcoal-light/10">
              <thead class="bg-brand-charcoal-dark/30 text-[9px] font-extrabold uppercase tracking-widest text-gray-500 select-none">
                <tr>
                  <th class="px-4 py-3">Tanggal Event</th>
                  <th class="px-4 py-3">Code</th>
                  <th class="px-4 py-3">Nama Program / Klien</th>
                  <th class="px-4 py-3 text-center">Urgency</th>
                  <th class="px-4 py-3 text-center">Readiness</th>
                  <th class="px-4 py-3 text-center">PM</th>
                  <th class="px-4 py-3">Aksi Terdekat</th>
                  <th class="px-4 py-3 text-right">Navigasi</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-brand-charcoal-light/5 font-medium">
                <tr v-if="upcomingEvents.length === 0">
                  <td colspan="8" class="px-4 py-8 text-center text-gray-500 font-semibold">
                    Tidak ada event mendatang untuk filter ini.
                  </td>
                </tr>
                <tr 
                  v-for="ev in upcomingEvents" 
                  :key="ev.project_id"
                  class="hover:bg-white/5 transition-colors"
                >
                  <td class="px-4 py-3 whitespace-nowrap text-white font-bold font-mono">
                    {{ formatDate(ev.event_date_start) }}
                    <span v-if="ev.event_date_end" class="text-[10px] text-gray-500 block">
                      s/d {{ formatDate(ev.event_date_end) }}
                    </span>
                  </td>
                  <td class="px-4 py-3 font-mono font-bold text-gray-400 select-all">{{ ev.project_code || '-' }}</td>
                  <td class="px-4 py-3">
                    <p class="text-white font-bold leading-tight">{{ ev.program_name }}</p>
                    <p class="text-[10px] text-gray-500 font-semibold">{{ ev.customer_name }}</p>
                  </td>
                  <td class="px-4 py-3 text-center whitespace-nowrap">
                    <span class="px-2 py-0.5 rounded text-[9px] font-black uppercase" :class="getDaysUrgencyClass(ev.days_until_event)">
                      {{ ev.days_until_event === 0 ? 'Hari Ini!' : `${ev.days_until_event} Hari` }}
                    </span>
                  </td>
                  <td class="px-4 py-3 text-center whitespace-nowrap">
                    <div class="flex flex-col items-center">
                      <span class="font-bold text-white">{{ Math.round(ev.readiness_score) }}% Ready</span>
                      <span class="text-[9px] text-gray-500">({{ Math.round(ev.instrument_completion_rate) }}% Inst)</span>
                    </div>
                  </td>
                  <td class="px-4 py-3 text-center whitespace-nowrap text-gray-400 font-semibold">{{ ev.pm_name }}</td>
                  <td class="px-4 py-3 text-gray-200 font-bold leading-relaxed">{{ ev.recommended_action }}</td>
                  <td class="px-4 py-3 text-right">
                    <router-link 
                      :to="'/projects/' + ev.project_id"
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

        <!-- Not Ready Projects -->
        <div class="glass-panel p-5 border border-brand-charcoal-light/20 space-y-4">
          <h3 class="text-sm font-bold text-white uppercase tracking-wider">Proyek Belum Siap (Readiness &lt; 80%)</h3>
          <div class="overflow-x-auto">
            <table class="min-w-full text-left text-xs divide-y divide-brand-charcoal-light/10">
              <thead class="bg-brand-charcoal-dark/30 text-[9px] font-extrabold uppercase tracking-widest text-gray-500 select-none">
                <tr>
                  <th class="px-4 py-3">Code</th>
                  <th class="px-4 py-3">Nama Program / Klien</th>
                  <th class="px-4 py-3">Jadwal Event</th>
                  <th class="px-4 py-3 text-center">Readiness</th>
                  <th class="px-4 py-3">Instrument Belum Done</th>
                  <th class="px-4 py-3 text-center">Assigned PM</th>
                  <th class="px-4 py-3">Aksi Pemulihan</th>
                  <th class="px-4 py-3 text-right">Navigasi</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-brand-charcoal-light/5 font-medium">
                <tr v-if="notReadyProjects.length === 0">
                  <td colspan="8" class="px-4 py-8 text-center text-gray-500 font-semibold">
                    Tidak ada project yang terdeteksi belum siap.
                  </td>
                </tr>
                <tr 
                  v-for="p in notReadyProjects" 
                  :key="p.project_id"
                  class="hover:bg-white/5 transition-colors"
                >
                  <td class="px-4 py-3 font-mono font-bold text-gray-400 select-all">{{ p.project_code || '-' }}</td>
                  <td class="px-4 py-3">
                    <p class="text-white font-bold leading-tight">{{ p.customer_name }}</p>
                  </td>
                  <td class="px-4 py-3 font-semibold text-gray-400 font-mono">{{ formatDate(p.event_date_start) }}</td>
                  <td class="px-4 py-3 text-center whitespace-nowrap font-bold text-red-400">
                    {{ Math.round(p.readiness_score) }}%
                  </td>
                  <td class="px-4 py-3 whitespace-nowrap">
                    <div class="flex gap-1">
                      <span 
                        v-for="item in p.missing_items" 
                        :key="item"
                        class="px-1.5 py-0.5 rounded text-[8px] font-black uppercase bg-red-500/10 text-red-400 border border-red-500/20"
                      >
                        {{ item }}
                      </span>
                    </div>
                  </td>
                  <td class="px-4 py-3 text-center text-gray-400 font-semibold">{{ p.pm_name }}</td>
                  <td class="px-4 py-3 text-gray-200 font-bold leading-relaxed">{{ p.recommended_action }}</td>
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

      <!-- TAB 3: Instrumen & Checklist Alerts -->
      <div v-show="activeTab === 'instruments'" class="space-y-6">
        <!-- Overdue Instruments -->
        <div class="glass-panel p-5 border border-brand-charcoal-light/20 space-y-4">
          <h3 class="text-sm font-bold text-white uppercase tracking-wider">Peringatan Jatuh Tempo Instrumen (Overdue)</h3>
          <div class="overflow-x-auto">
            <table class="min-w-full text-left text-xs divide-y divide-brand-charcoal-light/10">
              <thead class="bg-brand-charcoal-dark/30 text-[9px] font-extrabold uppercase tracking-widest text-gray-500 select-none">
                <tr>
                  <th class="px-4 py-3">Project Code</th>
                  <th class="px-4 py-3">Nama Klien</th>
                  <th class="px-4 py-3">Instrumen</th>
                  <th class="px-4 py-3">Jatuh Tempo</th>
                  <th class="px-4 py-3 text-center">Keterlambatan</th>
                  <th class="px-4 py-3 text-center">Status</th>
                  <th class="px-4 py-3 text-center">PM</th>
                  <th class="px-4 py-3">Rekomendasi Tindakan</th>
                  <th class="px-4 py-3 text-right">Navigasi</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-brand-charcoal-light/5 font-medium">
                <tr v-if="overdueInstruments.length === 0">
                  <td colspan="9" class="px-4 py-8 text-center text-gray-500 font-semibold">
                    Tidak ada instrumen overdue.
                  </td>
                </tr>
                <tr 
                  v-for="(inst, idx) in overdueInstruments" 
                  :key="idx"
                  class="hover:bg-white/5 transition-colors"
                >
                  <td class="px-4 py-3 font-mono font-bold text-gray-400 select-all">{{ inst.project_code || '-' }}</td>
                  <td class="px-4 py-3 text-white font-bold">{{ inst.customer_name }}</td>
                  <td class="px-4 py-3 font-bold text-brand-orange uppercase font-mono">{{ inst.instrument_label }}</td>
                  <td class="px-4 py-3 font-semibold text-gray-400 font-mono">{{ formatDate(inst.due_date) }}</td>
                  <td class="px-4 py-3 text-center text-red-400 font-bold whitespace-nowrap">
                    Lewat {{ inst.days_overdue }} Hari
                  </td>
                  <td class="px-4 py-3 text-center">
                    <span class="px-1.5 py-0.5 rounded text-[9px] font-black uppercase bg-amber-500/10 text-amber-400 border border-amber-500/20">
                      {{ inst.status }}
                    </span>
                  </td>
                  <td class="px-4 py-3 text-center text-gray-400 font-semibold">{{ inst.pm_name }}</td>
                  <td class="px-4 py-3 text-gray-200 font-bold leading-relaxed">{{ inst.recommended_action }}</td>
                  <td class="px-4 py-3 text-right">
                    <router-link 
                      :to="'/projects/' + inst.project_id"
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

        <!-- Need Revision Instruments -->
        <div class="glass-panel p-5 border border-brand-charcoal-light/20 space-y-4">
          <h3 class="text-sm font-bold text-white uppercase tracking-wider">Instrumen Membutuhkan Revisi (Need Revision)</h3>
          <div class="overflow-x-auto">
            <table class="min-w-full text-left text-xs divide-y divide-brand-charcoal-light/10">
              <thead class="bg-brand-charcoal-dark/30 text-[9px] font-extrabold uppercase tracking-widest text-gray-500 select-none">
                <tr>
                  <th class="px-4 py-3">Project Code</th>
                  <th class="px-4 py-3">Nama Klien</th>
                  <th class="px-4 py-3">Instrumen</th>
                  <th class="px-4 py-3">Catatan / Keterangan Revisi</th>
                  <th class="px-4 py-3 text-center">PM</th>
                  <th class="px-4 py-3">Rekomendasi Tindakan</th>
                  <th class="px-4 py-3 text-right">Navigasi</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-brand-charcoal-light/5 font-medium">
                <tr v-if="needRevisionInstruments.length === 0">
                  <td colspan="7" class="px-4 py-8 text-center text-gray-500 font-semibold">
                    Tidak ada instrumen yang perlu revisi.
                  </td>
                </tr>
                <tr 
                  v-for="(inst, idx) in needRevisionInstruments" 
                  :key="idx"
                  class="hover:bg-white/5 transition-colors"
                >
                  <td class="px-4 py-3 font-mono font-bold text-gray-400 select-all">{{ inst.project_code || '-' }}</td>
                  <td class="px-4 py-3 text-white font-bold">{{ inst.customer_name }}</td>
                  <td class="px-4 py-3 font-bold text-purple-400 uppercase font-mono">{{ inst.instrument_type }}</td>
                  <td class="px-4 py-3 text-gray-300 font-medium leading-relaxed">{{ inst.notes }}</td>
                  <td class="px-4 py-3 text-center text-gray-400 font-semibold whitespace-nowrap">{{ inst.pm_name }}</td>
                  <td class="px-4 py-3 text-gray-200 font-bold leading-relaxed">{{ inst.recommended_action }}</td>
                  <td class="px-4 py-3 text-right">
                    <router-link 
                      :to="'/projects/' + inst.project_id"
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

      <!-- TAB 4: Beban Kerja PM -->
      <div v-show="activeTab === 'pm_workload'" class="space-y-4">
        <div class="glass-panel p-5 border border-brand-charcoal-light/20 space-y-4">
          <h3 class="text-sm font-bold text-white uppercase tracking-wider">Beban Kerja Persiapan Event per PM</h3>
          <div class="overflow-x-auto">
            <table class="min-w-full text-left text-xs divide-y divide-brand-charcoal-light/10">
              <thead class="bg-brand-charcoal-dark/30 text-[9px] font-extrabold uppercase tracking-widest text-gray-500 select-none">
                <tr>
                  <th class="px-4 py-3">Nama Program Manager (PM)</th>
                  <th class="px-4 py-3 text-center">Total Proyek Dipimpin</th>
                  <th class="px-4 py-3 text-center">Event Mendatang (7 Hari)</th>
                  <th class="px-4 py-3 text-center">Proyek Belum Siap</th>
                  <th class="px-4 py-3 text-center">Instrumen Overdue</th>
                  <th class="px-4 py-3 text-center">Rata Kesiapan</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-brand-charcoal-light/5 font-medium">
                <tr v-if="pmWorkload.length === 0">
                  <td colspan="6" class="px-4 py-8 text-center text-gray-500 font-semibold">
                    Belum ada data beban kerja penugasan PM.
                  </td>
                </tr>
                <tr 
                  v-for="pm in pmWorkload" 
                  :key="pm.pm_id"
                  class="hover:bg-white/5 transition-colors"
                >
                  <td class="px-4 py-3">
                    <div class="flex items-center gap-2 select-none">
                      <div class="w-8 h-8 rounded-lg bg-brand-orange-soft/10 text-brand-orange font-bold flex items-center justify-center text-[10px]">
                        {{ pm.initial_code }}
                      </div>
                      <span class="text-white font-bold text-sm">{{ pm.pm_name }}</span>
                    </div>
                  </td>
                  <td class="px-4 py-3 text-center text-white font-extrabold text-sm">{{ pm.total_projects }}</td>
                  <td class="px-4 py-3 text-center text-indigo-400 font-bold">{{ pm.upcoming_events_7_days }}</td>
                  <td class="px-4 py-3 text-center text-red-400 font-bold">{{ pm.not_ready_projects }}</td>
                  <td class="px-4 py-3 text-center text-amber-500 font-bold">{{ pm.overdue_instruments }}</td>
                  <td class="px-4 py-3 text-center whitespace-nowrap">
                    <span class="px-2 py-0.5 rounded text-[10px] font-bold inline-block" :class="getReadinessScoreBadgeStyles(pm.average_readiness_score / 100)">
                      {{ Math.round(pm.average_readiness_score) }}% Ready
                    </span>
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
import { ref, onMounted } from 'vue'
import axios from 'axios'

const users = ref([])
const summary = ref({
  total_active_projects: 0,
  events_today: 0,
  upcoming_events_7_days: 0,
  overdue_events: 0,
  not_ready_projects: 0,
  overdue_instruments: 0,
  need_revision_instruments: 0,
  average_readiness_score: 0
})

const upcomingEvents = ref([])
const notReadyProjects = ref([])
const overdueInstruments = ref([])
const needRevisionInstruments = ref([])
const pmWorkload = ref([])
const priorityActions = ref([])

const loading = ref(true)
const error = ref(null)
const activeTab = ref('priority')

// Filters variables
const filterPm = ref('')
const filterPo = ref('')
const filterEventWindow = ref('all')
const filterDateFrom = ref('')
const filterDateTo = ref('')
const filterIncludeClosed = ref(false)
const filterIncludeCanceled = ref(false)

const tabs = computed(() => [
  { id: 'priority', name: 'Prioritas Tindakan', count: priorityActions.value.length },
  { id: 'events', name: 'Jadwal Event & Kesiapan', count: upcomingEvents.value.length + notReadyProjects.value.length },
  { id: 'instruments', name: 'Checklist & Revisi', count: overdueInstruments.value.length + needRevisionInstruments.value.length },
  { id: 'pm_workload', name: 'Beban Kerja PM', count: pmWorkload.value.length }
])

const fetchUsers = async () => {
  try {
    const res = await axios.get('/api/v1/auth/users')
    users.value = res.data
  } catch (err) {
    console.error('Failed to load users for filter dropdowns', err)
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
    if (filterPm.value) params.pm_id = filterPm.value
    if (filterPo.value) params.po_id = filterPo.value
    if (filterDateFrom.value) params.date_from = filterDateFrom.value
    if (filterDateTo.value) params.date_to = filterDateTo.value

    const res = await axios.get('/api/v1/dashboard/pm-control-center', { params })
    
    summary.value = res.data.summary
    upcomingEvents.value = res.data.upcoming_events
    notReadyProjects.value = res.data.not_ready_projects
    overdueInstruments.value = res.data.overdue_instruments
    needRevisionInstruments.value = res.data.need_revision_instruments
    pmWorkload.value = res.data.pm_workload
    priorityActions.value = res.data.priority_actions
  } catch (err) {
    console.error('Failed to load operational dashboard data', err)
    error.value = err.response?.data?.detail?.message || err.response?.data?.detail || 'Gagal memuat data PM Control Center.'
  } finally {
    loading.value = false
  }
}

const resetFilters = () => {
  filterPm.value = ''
  filterPo.value = ''
  filterEventWindow.value = 'all'
  filterDateFrom.value = ''
  filterDateTo.value = ''
  filterIncludeClosed.value = false
  filterIncludeCanceled.value = false
  fetchControlCenterData()
}

onMounted(() => {
  fetchUsers()
  fetchControlCenterData()
})

// Formatting functions
const formatDate = (val) => {
  if (!val) return '-'
  return new Date(val).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

// Visual color rules helpers
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

const getDaysUrgencyClass = (days) => {
  if (days === null || days === undefined) return 'bg-gray-600/10 text-gray-400 border border-gray-600/20'
  if (days === 0) return 'bg-red-500/20 text-red-400 border border-red-500/30 animate-pulse font-black'
  if (days <= 3) return 'bg-amber-500/10 text-amber-400 border border-amber-500/20 font-bold'
  if (days <= 7) return 'bg-brand-orange/15 text-brand-orange border border-brand-orange/20'
  return 'bg-brand-blue/10 text-brand-blue border border-brand-blue/20'
}

const getReadinessScoreBadgeStyles = (score) => {
  const s = score || 0
  if (s >= 0.8) return 'bg-brand-emerald/15 text-brand-emerald border border-brand-emerald/20'
  if (s >= 0.5) return 'bg-yellow-500/10 text-yellow-500 border border-yellow-500/20'
  return 'bg-red-500/10 text-red-400 border border-red-500/20'
}
</script>

<style scoped>
.glass-panel {
  background: rgba(26, 32, 44, 0.75);
  backdrop-filter: blur(12px);
  border-radius: 1.25rem;
}
</style>
