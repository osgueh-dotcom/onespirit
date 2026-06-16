<template>
  <div class="app-page">
    <!-- Header -->
    <AppPageHeader 
      title="PM Control Center" 
      subtitle="Pusat kontrol operasional untuk membantu PM memantau event mendatang, readiness project, instrument overdue, dan prioritas tindakan."
    >
      <template #actions>
        <button 
          @click="fetchControlCenterData"
          class="app-button-secondary"
        >
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
          </svg>
          Refresh Data
        </button>
      </template>
    </AppPageHeader>

    <!-- Filters Bar -->
    <div class="glass-panel p-5 border border-brand-charcoal-light/30 space-y-4 select-none">
      <div class="flex items-center justify-between border-b border-brand-charcoal-light/15 pb-2">
        <span class="text-[10px] font-black uppercase tracking-wider text-muted-theme">Filter Operasional</span>
        <button @click="resetFilters" class="text-[10px] font-bold text-brand-orange hover:underline">
          Reset Filter ✕
        </button>
      </div>
      
      <div class="flex flex-wrap gap-2">
        <button
          v-for="filter in pmQuickFilters"
          :key="filter.key"
          type="button"
          @click="applyPmQuickFilter(filter.key)"
          class="app-quick-chip"
          :class="activePmQuickFilter === filter.key ? 'app-quick-chip-active' : ''"
        >
          {{ filter.label }}
        </button>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4">
        <!-- Filter PM -->
        <div>
          <label class="app-label mb-1.5">Program Manager (PM)</label>
          <select 
            v-model="filterPm" 
            @change="handleManualFilterChange"
            class="app-form-control-compact"
          >
            <option value="">Semua PM</option>
            <option v-for="u in users" :key="u.id" :value="u.id">{{ u.full_name }}</option>
          </select>
        </div>

        <!-- Filter PO -->
        <div>
          <label class="app-label mb-1.5">Program Owner (PO)</label>
          <select 
            v-model="filterPo" 
            @change="handleManualFilterChange"
            class="app-form-control-compact"
          >
            <option value="">Semua PO</option>
            <option v-for="u in users" :key="u.id" :value="u.id">{{ u.full_name }}</option>
          </select>
        </div>

        <!-- Event Window -->
        <div>
          <label class="app-label mb-1.5">Periode Event (Window)</label>
          <select 
            v-model="filterEventWindow" 
            @change="handleManualFilterChange"
            class="app-form-control-compact"
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
            <label class="app-label mb-1.5">Dari Tanggal</label>
            <input 
              v-model="filterDateFrom" 
              type="date"
              @change="handleManualFilterChange"
              class="app-form-control-compact"
            />
          </div>
          <div>
            <label class="app-label mb-1.5">Sampai Tanggal</label>
            <input 
              v-model="filterDateTo" 
              type="date"
              @change="handleManualFilterChange"
              class="app-form-control-compact"
            />
          </div>
        </div>

        <!-- Checkboxes Closed & Canceled -->
        <div class="flex items-center gap-4 pt-4">
          <label class="flex items-center gap-2 text-[10px] font-bold text-muted-theme hover:text-main-theme cursor-pointer transition-colors">
            <input 
              v-model="filterIncludeClosed" 
              type="checkbox" 
              @change="handleManualFilterChange"
              class="rounded border-panel-theme bg-surface-theme text-brand-orange focus:ring-0"
            />
            Closed Project
          </label>
          <label class="flex items-center gap-2 text-[10px] font-bold text-muted-theme hover:text-main-theme cursor-pointer transition-colors">
            <input 
              v-model="filterIncludeCanceled" 
              type="checkbox" 
              @change="handleManualFilterChange"
              class="rounded border-panel-theme bg-surface-theme text-brand-orange focus:ring-0"
            />
            Batal (Canceled)
          </label>
        </div>
      </div>

      <!-- Advanced Filters Row -->
      <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4 border-t border-brand-charcoal-light/10 pt-4">
        <!-- Filter Readiness Min -->
        <div>
          <label class="app-label mb-1.5">Readiness Min (%)</label>
          <input 
            v-model.number="filterReadinessMin" 
            type="number"
            min="0"
            max="100"
            placeholder="0"
            @change="handleManualFilterChange"
            class="app-form-control-compact"
          />
        </div>

        <!-- Filter Readiness Max -->
        <div>
          <label class="app-label mb-1.5">Readiness Max (%)</label>
          <input 
            v-model.number="filterReadinessMax" 
            type="number"
            min="0"
            max="100"
            placeholder="100"
            @change="handleManualFilterChange"
            class="app-form-control-compact"
          />
        </div>

        <!-- Filter Instrument Status -->
        <div>
          <label class="app-label mb-1.5">Status Instrumen</label>
          <select 
            v-model="filterInstrumentStatus" 
            @change="handleManualFilterChange"
            class="app-form-control-compact"
          >
            <option value="">Semua Status</option>
            <option value="Not Started">Not Started</option>
            <option value="In Progress">In Progress</option>
            <option value="Need Revision">Need Revision</option>
            <option value="Done">Done</option>
            <option value="Not Required">Not Required</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Error State -->
    <AppErrorState 
      v-if="error" 
      title="Gagal Memuat PM Control Center" 
      :message="error" 
      @retry="fetchControlCenterData" 
    />

    <!-- Loading State -->
    <AppLoadingState v-else-if="loading" message="Mengompilasi data PM Control Center..." />

    <!-- Main Content Grid -->
    <div v-else class="space-y-6">
      <!-- Operational KPI summary grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-4 select-none">
        <AppStatCard 
          title="Event Hari Ini" 
          :value="summary.events_today" 
          subtitle="Event Hari Ini" 
          theme="orange" 
        />
        <AppStatCard 
          title="Upcoming (7 Hari)" 
          :value="summary.upcoming_events_7_days" 
          subtitle="Event Mendatang" 
          theme="blue" 
        />
        <AppStatCard 
          title="Belum Siap (<80%)" 
          :value="summary.not_ready_projects" 
          subtitle="Proyek Belum Siap" 
          theme="red" 
        />
        <AppStatCard 
          title="Instrumen Overdue" 
          :value="summary.overdue_instruments" 
          subtitle="Dokumen Terlambat" 
          theme="amber" 
        />
        <AppStatCard 
          title="Perlu Revisi" 
          :value="summary.need_revision_instruments" 
          subtitle="Revisi Diperlukan" 
          theme="purple" 
        />
        <AppStatCard 
          title="Rata Kesiapan" 
          :value="`${Math.round(summary.average_readiness_score || 0)}%`" 
          subtitle="Skor Kesiapan Rata-rata" 
          theme="emerald" 
        />
      </div>

      <!-- Tab Buttons -->
      <div class="flex border-b border-brand-charcoal-light/25 select-none overflow-x-auto">
        <button 
          v-for="tab in tabs" 
          :key="tab.id"
          @click="activeTab = tab.id"
          class="px-5 py-3 text-xs font-bold tracking-wide transition-all border-b-2 whitespace-nowrap"
          :class="activeTab === tab.id ? 'border-brand-orange text-brand-orange bg-brand-orange/5' : 'border-transparent text-muted-theme hover:text-main-theme'"
        >
          {{ tab.name }} ({{ tab.count }})
        </button>
      </div>

      <!-- TAB 1: Prioritas Tindakan -->
      <div v-show="activeTab === 'priority'" class="space-y-4">
        <div class="glass-panel p-5 border border-brand-charcoal-light/20 space-y-4">
          <div class="flex items-center justify-between">
            <h3 class="text-sm font-bold text-main-theme uppercase tracking-wider">Daftar Prioritas Tindakan (Priority Actions)</h3>
            <span class="hidden md:inline text-[10px] font-bold text-muted-theme bg-surface-theme border border-panel-theme px-2 py-0.5 rounded">
              Daftar aksi operasional yang diurutkan berdasarkan tingkat urgensi
            </span>
          </div>

          <AppEmptyState 
            v-if="priorityActions.length === 0"
            title="Tidak Ada Tindakan Prioritas"
            message="Semua proyek dalam kondisi aman dan siap dijalankan."
          />

          <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div 
              v-for="(act, idx) in priorityActions" 
              :key="idx"
              class="p-4 rounded-2xl border flex flex-col justify-between gap-3 text-xs group animate-fade-in"
              :class="getPrioClass(act.priority_level)"
            >
              <div>
                <div class="flex items-center justify-between border-b border-brand-charcoal-light/10 pb-2 mb-2 select-none">
                  <span class="font-bold font-mono tracking-wider">{{ act.project_code || 'UNCODED' }}</span>
                  <span class="px-2 py-0.5 rounded text-[8px] font-black uppercase" :class="getPrioBadgeClass(act.priority_level)">
                    {{ act.priority_level }}
                  </span>
                </div>
                <h4 class="font-bold text-main-theme text-sm mb-1 leading-snug group-hover:text-brand-orange transition-colors">
                  {{ act.title }}
                </h4>
                <p class="text-soft-theme font-semibold text-[11px] mb-2">{{ act.description }}</p>
                <div class="bg-surface-theme p-2.5 rounded-xl border border-panel-theme space-y-1">
                  <p class="text-[9px] font-black text-brand-orange uppercase tracking-wider select-none">Rekomendasi Aksi:</p>
                  <p class="text-main-theme font-bold leading-normal">{{ act.recommended_action }}</p>
                </div>
              </div>
              <div class="pt-2 flex justify-end">
                <router-link 
                  :to="'/projects/' + act.project_id"
                  class="px-3 py-1.5 rounded bg-brand-orange/10 hover:bg-brand-orange/20 text-brand-orange font-bold text-[10px] transition-all"
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
          <h3 class="text-sm font-bold text-main-theme uppercase tracking-wider">Event yang Perlu Disiapkan (Upcoming 14 Hari)</h3>
          
          <!-- Desktop Table View -->
          <div class="hidden md:block overflow-x-auto">
            <table class="min-w-full text-left text-xs divide-y divide-brand-charcoal-light/10">
              <thead class="app-table-header">
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
                  <td colspan="8" class="px-4 py-8 text-center app-empty-copy">
                    Tidak ada event mendatang untuk filter ini.
                  </td>
                </tr>
                <tr 
                  v-for="ev in upcomingEvents" 
                  :key="ev.project_id"
                  class="app-table-row"
                >
                  <td class="px-4 py-3 whitespace-nowrap app-table-cell-strong font-mono">
                    {{ formatDate(ev.event_date_start) }}
                    <span v-if="ev.event_date_end" class="text-[10px] text-muted-theme block">
                      s/d {{ formatDate(ev.event_date_end) }}
                    </span>
                  </td>
                  <td class="px-4 py-3 font-mono font-bold app-table-cell-muted select-all">{{ ev.project_code || '-' }}</td>
                  <td class="px-4 py-3">
                    <p class="app-table-cell-strong leading-tight">{{ ev.program_name }}</p>
                    <p class="text-[10px] text-muted-theme font-semibold">{{ ev.customer_name }}</p>
                  </td>
                  <td class="px-4 py-3 text-center whitespace-nowrap">
                    <span class="px-2 py-0.5 rounded text-[9px] font-black uppercase" :class="getDaysUrgencyClass(ev.days_until_event)">
                      {{ ev.days_until_event === 0 ? 'Hari Ini!' : `${ev.days_until_event} Hari` }}
                    </span>
                  </td>
                  <td class="px-4 py-3 text-center whitespace-nowrap">
                    <div class="flex flex-col items-center">
                      <span class="font-bold text-main-theme">{{ Math.round(ev.readiness_score || 0) }}% Ready</span>
                      <span class="text-[9px] text-muted-theme">({{ Math.round(ev.instrument_completion_rate || 0) }}% Inst)</span>
                    </div>
                  </td>
                  <td class="px-4 py-3 text-center whitespace-nowrap app-table-cell-muted font-semibold">{{ ev.pm_name }}</td>
                  <td class="px-4 py-3 app-table-cell-strong leading-relaxed">{{ ev.recommended_action }}</td>
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

          <!-- Mobile Card View -->
          <div class="block md:hidden space-y-4">
            <div v-if="upcomingEvents.length === 0" class="py-6 text-center app-empty-copy">
              Tidak ada event mendatang untuk filter ini.
            </div>
            <div 
              v-for="ev in upcomingEvents" 
              :key="ev.project_id"
              class="bg-surface-theme border border-panel-theme p-4 rounded-2xl space-y-3"
            >
              <div class="flex items-center justify-between border-b border-brand-charcoal-light/10 pb-2">
                <span class="font-mono text-[10px] font-bold text-muted-theme">{{ ev.project_code || 'OSA-EVENT' }}</span>
                <span class="px-2 py-0.5 rounded text-[8px] font-black uppercase" :class="getDaysUrgencyClass(ev.days_until_event)">
                  {{ ev.days_until_event === 0 ? 'Hari Ini!' : `${ev.days_until_event} Hari` }}
                </span>
              </div>
              <div>
                <h4 class="font-bold text-main-theme text-sm">{{ ev.program_name }}</h4>
                <p class="text-xs text-muted-theme mt-0.5 font-semibold">{{ ev.customer_name }}</p>
              </div>
              <div class="grid grid-cols-2 gap-2 bg-surface-theme p-2.5 rounded-xl border border-panel-theme text-[11px] font-semibold">
                <div>
                  <p class="text-muted-theme text-[9px] uppercase tracking-wider">Tanggal Event</p>
                  <p class="text-main-theme">{{ formatDate(ev.event_date_start) }}</p>
                </div>
                <div>
                  <p class="text-muted-theme text-[9px] uppercase tracking-wider">PM In Charge</p>
                  <p class="text-main-theme">{{ ev.pm_name }}</p>
                </div>
                <div>
                  <p class="text-muted-theme text-[9px] uppercase tracking-wider">Kesiapan (Readiness)</p>
                  <p class="text-brand-orange font-bold">{{ Math.round(ev.readiness_score || 0) }}% Ready</p>
                </div>
                <div>
                  <p class="text-muted-theme text-[9px] uppercase tracking-wider">Instrumen Done</p>
                  <p class="text-soft-theme">{{ Math.round(ev.instrument_completion_rate || 0) }}% Done</p>
                </div>
              </div>
              <div class="bg-brand-orange/5 border border-brand-orange/10 p-2.5 rounded-xl text-[11px] text-main-theme">
                <p class="text-[8px] font-black text-brand-orange uppercase tracking-wider mb-1 select-none">Rekomendasi Tindakan:</p>
                <p class="font-bold leading-normal">{{ ev.recommended_action }}</p>
              </div>
              <div class="flex justify-end pt-1">
                <router-link 
                  :to="'/projects/' + ev.project_id"
                  class="px-3 py-1.5 rounded bg-brand-orange/10 hover:bg-brand-orange/20 text-brand-orange font-bold text-[10px] transition-all"
                >
                  Buka Proyek →
                </router-link>
              </div>
            </div>
          </div>
        </div>

        <!-- Not Ready Projects -->
        <div class="glass-panel p-5 border border-brand-charcoal-light/20 space-y-4">
          <h3 class="text-sm font-bold text-main-theme uppercase tracking-wider">Penghambat Kesiapan (Readiness &lt; 80%)</h3>
          
          <!-- Desktop Table View -->
          <div class="hidden md:block overflow-x-auto">
            <table class="min-w-full text-left text-xs divide-y divide-brand-charcoal-light/10">
              <thead class="app-table-header">
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
                  <td colspan="8" class="px-4 py-8 text-center app-empty-copy">
                    Tidak ada project yang terdeteksi belum siap.
                  </td>
                </tr>
                <tr 
                  v-for="p in notReadyProjects" 
                  :key="p.project_id"
                  class="app-table-row"
                >
                  <td class="px-4 py-3 font-mono font-bold app-table-cell-muted select-all">{{ p.project_code || '-' }}</td>
                  <td class="px-4 py-3">
                    <p class="app-table-cell-strong leading-tight">{{ p.customer_name }}</p>
                  </td>
                  <td class="px-4 py-3 font-semibold app-table-cell-muted font-mono">{{ formatDate(p.event_date_start) }}</td>
                  <td class="px-4 py-3 text-center whitespace-nowrap font-bold text-red-400">
                    {{ Math.round(p.readiness_score || 0) }}%
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
                  <td class="px-4 py-3 text-center app-table-cell-muted font-semibold">{{ p.pm_name }}</td>
                  <td class="px-4 py-3 app-table-cell-strong leading-relaxed">{{ p.recommended_action }}</td>
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

          <!-- Mobile Card View -->
          <div class="block md:hidden space-y-4">
            <div v-if="notReadyProjects.length === 0" class="py-6 text-center app-empty-copy">
              Tidak ada project yang terdeteksi belum siap.
            </div>
            <div 
              v-for="p in notReadyProjects" 
              :key="p.project_id"
              class="bg-surface-theme border border-panel-theme p-4 rounded-2xl space-y-3"
            >
              <div class="flex items-center justify-between border-b border-brand-charcoal-light/10 pb-2">
                <span class="font-mono text-[10px] font-bold text-muted-theme">{{ p.project_code || 'OSA-EVENT' }}</span>
                <span class="px-2 py-0.5 rounded text-[10px] font-black uppercase bg-red-500/10 text-red-400 border border-red-500/20">
                  {{ Math.round(p.readiness_score || 0) }}% Ready
                </span>
              </div>
              <div>
                <h4 class="font-bold text-main-theme text-sm">{{ p.customer_name }}</h4>
                <p class="text-xs text-muted-theme mt-0.5">Event: {{ formatDate(p.event_date_start) }}</p>
              </div>
              <div class="space-y-1.5 bg-surface-theme p-2.5 rounded-xl border border-panel-theme text-[11px]">
                <div>
                  <p class="text-muted-theme text-[9px] uppercase tracking-wider font-bold">PM In Charge</p>
                  <p class="text-main-theme font-semibold">{{ p.pm_name }}</p>
                </div>
                <div>
                  <p class="text-muted-theme text-[9px] uppercase tracking-wider font-bold mb-1">Instrumen Belum Siap</p>
                  <div class="flex flex-wrap gap-1">
                    <span 
                      v-for="item in p.missing_items" 
                      :key="item"
                      class="px-1.5 py-0.5 rounded text-[8px] font-black uppercase bg-red-500/10 text-red-400 border border-red-500/20"
                    >
                      {{ item }}
                    </span>
                  </div>
                </div>
              </div>
              <div class="bg-red-500/5 border border-red-500/10 p-2.5 rounded-xl text-[11px] text-main-theme">
                <p class="text-[8px] font-black text-red-400 uppercase tracking-wider mb-1 select-none">Aksi Pemulihan:</p>
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

      <!-- TAB 3: Instrumen & Checklist Alerts -->
      <div v-show="activeTab === 'instruments'" class="space-y-6">
        <!-- Overdue Instruments -->
        <div class="glass-panel p-5 border border-brand-charcoal-light/20 space-y-4">
          <h3 class="text-sm font-bold text-main-theme uppercase tracking-wider">Dokumen Terlambat (Overdue Instruments)</h3>
          
          <!-- Desktop Table View -->
          <div class="hidden md:block overflow-x-auto">
            <table class="min-w-full text-left text-xs divide-y divide-brand-charcoal-light/10">
              <thead class="app-table-header">
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
                  <td colspan="9" class="px-4 py-8 text-center app-empty-copy">
                    Tidak ada instrumen overdue.
                  </td>
                </tr>
                <tr 
                  v-for="(inst, idx) in overdueInstruments" 
                  :key="idx"
                  class="app-table-row"
                >
                  <td class="px-4 py-3 font-mono font-bold app-table-cell-muted select-all">{{ inst.project_code || '-' }}</td>
                  <td class="px-4 py-3 app-table-cell-strong">{{ inst.customer_name }}</td>
                  <td class="px-4 py-3 font-bold text-brand-orange uppercase font-mono">{{ inst.instrument_label }}</td>
                  <td class="px-4 py-3 font-semibold app-table-cell-muted font-mono">{{ formatDate(inst.due_date) }}</td>
                  <td class="px-4 py-3 text-center text-red-400 font-bold whitespace-nowrap">
                    Lewat {{ inst.days_overdue }} Hari
                  </td>
                  <td class="px-4 py-3 text-center">
                    <span class="px-1.5 py-0.5 rounded text-[9px] font-black uppercase bg-amber-500/10 text-amber-400 border border-amber-500/20">
                      {{ inst.status }}
                    </span>
                  </td>
                  <td class="px-4 py-3 text-center app-table-cell-muted font-semibold">{{ inst.pm_name }}</td>
                  <td class="px-4 py-3 app-table-cell-strong leading-relaxed">{{ inst.recommended_action }}</td>
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

          <!-- Mobile Card View -->
          <div class="block md:hidden space-y-4">
            <div v-if="overdueInstruments.length === 0" class="py-6 text-center app-empty-copy">
              Tidak ada instrumen overdue.
            </div>
            <div 
              v-for="(inst, idx) in overdueInstruments" 
              :key="idx"
              class="bg-surface-theme border border-panel-theme p-4 rounded-2xl space-y-3"
            >
              <div class="flex items-center justify-between border-b border-brand-charcoal-light/10 pb-2">
                <span class="font-mono text-[10px] font-bold text-muted-theme">{{ inst.project_code || 'OSA-EVENT' }}</span>
                <span class="px-2 py-0.5 rounded text-[8px] font-black uppercase bg-red-500/10 text-red-400 border border-red-500/20 font-bold">
                  Lewat {{ inst.days_overdue }} Hari
                </span>
              </div>
              <div>
                <h4 class="font-bold text-brand-orange uppercase text-sm font-mono">{{ inst.instrument_label }}</h4>
                <p class="text-xs text-soft-theme font-semibold mt-1">Klien: {{ inst.customer_name }}</p>
              </div>
              <div class="grid grid-cols-2 gap-2 bg-surface-theme p-2.5 rounded-xl border border-panel-theme text-[11px] font-semibold">
                <div>
                  <p class="text-muted-theme text-[9px] uppercase tracking-wider">Jatuh Tempo</p>
                  <p class="text-main-theme">{{ formatDate(inst.due_date) }}</p>
                </div>
                <div>
                  <p class="text-muted-theme text-[9px] uppercase tracking-wider">PM In Charge</p>
                  <p class="text-main-theme">{{ inst.pm_name }}</p>
                </div>
                <div class="col-span-2">
                  <p class="text-muted-theme text-[9px] uppercase tracking-wider">Status Dokumen</p>
                  <span class="px-1.5 py-0.5 rounded text-[9px] font-black uppercase bg-amber-500/10 text-amber-400 border border-amber-500/20">
                    {{ inst.status }}
                  </span>
                </div>
              </div>
              <div class="bg-amber-500/5 border border-amber-500/10 p-2.5 rounded-xl text-[11px] text-main-theme">
                <p class="text-[8px] font-black text-amber-400 uppercase tracking-wider mb-1 select-none">Rekomendasi Tindakan:</p>
                <p class="font-bold leading-normal">{{ inst.recommended_action }}</p>
              </div>
              <div class="flex justify-end pt-1">
                <router-link 
                  :to="'/projects/' + inst.project_id"
                  class="px-3 py-1.5 rounded bg-brand-orange/10 hover:bg-brand-orange/20 text-brand-orange font-bold text-[10px] transition-all"
                >
                  Buka Proyek →
                </router-link>
              </div>
            </div>
          </div>
        </div>

        <!-- Need Revision Instruments -->
        <div class="glass-panel p-5 border border-brand-charcoal-light/20 space-y-4">
          <h3 class="text-sm font-bold text-main-theme uppercase tracking-wider">Instrumen Perlu Tindakan (Need Revision)</h3>
          
          <!-- Desktop Table View -->
          <div class="hidden md:block overflow-x-auto">
            <table class="min-w-full text-left text-xs divide-y divide-brand-charcoal-light/10">
              <thead class="app-table-header">
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
                  <td colspan="7" class="px-4 py-8 text-center app-empty-copy">
                    Tidak ada instrumen yang perlu revisi.
                  </td>
                </tr>
                <tr 
                  v-for="(inst, idx) in needRevisionInstruments" 
                  :key="idx"
                  class="app-table-row"
                >
                  <td class="px-4 py-3 font-mono font-bold app-table-cell-muted select-all">{{ inst.project_code || '-' }}</td>
                  <td class="px-4 py-3 app-table-cell-strong">{{ inst.customer_name }}</td>
                  <td class="px-4 py-3 font-bold text-purple-400 uppercase font-mono">{{ inst.instrument_type }}</td>
                  <td class="px-4 py-3 text-soft-theme font-medium leading-relaxed">{{ inst.notes }}</td>
                  <td class="px-4 py-3 text-center app-table-cell-muted font-semibold whitespace-nowrap">{{ inst.pm_name }}</td>
                  <td class="px-4 py-3 app-table-cell-strong leading-relaxed">{{ inst.recommended_action }}</td>
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

          <!-- Mobile Card View -->
          <div class="block md:hidden space-y-4">
            <div v-if="needRevisionInstruments.length === 0" class="py-6 text-center app-empty-copy">
              Tidak ada instrumen yang perlu revisi.
            </div>
            <div 
              v-for="(inst, idx) in needRevisionInstruments" 
              :key="idx"
              class="bg-surface-theme border border-panel-theme p-4 rounded-2xl space-y-3"
            >
              <div class="flex items-center justify-between border-b border-brand-charcoal-light/10 pb-2">
                <span class="font-mono text-[10px] font-bold text-muted-theme">{{ inst.project_code || 'OSA-EVENT' }}</span>
                <span class="px-2 py-0.5 rounded text-[8px] font-black uppercase bg-purple-500/10 text-purple-400 border border-purple-500/20 font-bold">
                  Need Revision
                </span>
              </div>
              <div>
                <h4 class="font-bold text-purple-400 uppercase text-sm font-mono">{{ inst.instrument_type }}</h4>
                <p class="text-xs text-soft-theme font-semibold mt-1">Klien: {{ inst.customer_name }}</p>
                <p class="text-[11px] text-muted-theme bg-surface-theme p-2.5 rounded-xl border border-panel-theme mt-2 leading-relaxed">
                  <span class="text-[9px] font-bold text-purple-400 uppercase block mb-1">Catatan Revisi:</span>
                  {{ inst.notes }}
                </p>
              </div>
              <div class="grid grid-cols-2 gap-2 bg-surface-theme p-2.5 rounded-xl border border-panel-theme text-[11px] font-semibold">
                <div>
                  <p class="text-muted-theme text-[9px] uppercase tracking-wider font-bold">PM In Charge</p>
                  <p class="text-main-theme">{{ inst.pm_name }}</p>
                </div>
              </div>
              <div class="bg-brand-orange/5 border border-brand-orange/10 p-2.5 rounded-xl text-[11px] text-main-theme">
                <p class="text-[8px] font-black text-brand-orange uppercase tracking-wider mb-1 select-none">Rekomendasi Tindakan:</p>
                <p class="font-bold leading-normal">{{ inst.recommended_action }}</p>
              </div>
              <div class="flex justify-end pt-1">
                <router-link 
                  :to="'/projects/' + inst.project_id"
                  class="px-3 py-1.5 rounded bg-brand-orange/10 hover:bg-brand-orange/20 text-brand-orange font-bold text-[10px] transition-all"
                >
                  Buka Proyek →
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- TAB 4: Beban Kerja PM -->
      <div v-show="activeTab === 'pm_workload'" class="space-y-4">
        <div class="glass-panel p-5 border border-brand-charcoal-light/20 space-y-4">
          <h3 class="text-sm font-bold text-main-theme uppercase tracking-wider">Beban Kerja PM (PM Workload)</h3>
          
          <!-- Desktop Table View -->
          <div class="hidden md:block overflow-x-auto">
            <table class="min-w-full text-left text-xs divide-y divide-brand-charcoal-light/10">
              <thead class="app-table-header">
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
                  <td colspan="6" class="px-4 py-8 text-center app-empty-copy">
                    Belum ada data beban kerja penugasan PM.
                  </td>
                </tr>
                <tr 
                  v-for="pm in pmWorkload" 
                  :key="pm.pm_id"
                  class="app-table-row"
                >
                  <td class="px-4 py-3">
                    <div class="flex items-center gap-2 select-none">
                      <div class="w-8 h-8 rounded-lg bg-brand-orange-soft/10 text-brand-orange font-bold flex items-center justify-center text-[10px]">
                        {{ pm.initial_code }}
                      </div>
                      <span class="text-main-theme font-bold text-sm">{{ pm.pm_name }}</span>
                    </div>
                  </td>
                  <td class="px-4 py-3 text-center text-main-theme font-extrabold text-sm">{{ pm.total_projects }}</td>
                  <td class="px-4 py-3 text-center text-indigo-400 font-bold">{{ pm.upcoming_events_7_days }}</td>
                  <td class="px-4 py-3 text-center text-red-400 font-bold">{{ pm.not_ready_projects }}</td>
                  <td class="px-4 py-3 text-center text-amber-500 font-bold">{{ pm.overdue_instruments }}</td>
                  <td class="px-4 py-3 text-center whitespace-nowrap">
                    <span class="px-2 py-0.5 rounded text-[10px] font-bold inline-block" :class="getReadinessScoreBadgeStyles(pm.average_readiness_score)">
                      {{ Math.round(pm.average_readiness_score || 0) }}% Ready
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Mobile Card View -->
          <div class="block md:hidden space-y-4">
            <div v-if="pmWorkload.length === 0" class="py-6 text-center app-empty-copy">
              Belum ada data beban kerja penugasan PM.
            </div>
            <div 
              v-for="pm in pmWorkload" 
              :key="pm.pm_id"
              class="bg-surface-theme border border-panel-theme p-4 rounded-2xl space-y-3 animate-fade-in"
            >
              <div class="flex items-center justify-between border-b border-brand-charcoal-light/10 pb-2">
                <div class="flex items-center gap-2">
                  <div class="w-7 h-7 rounded-lg bg-brand-orange-soft/10 text-brand-orange font-bold flex items-center justify-center text-[10px]">
                    {{ pm.initial_code }}
                  </div>
                  <span class="text-main-theme font-bold text-sm">{{ pm.pm_name }}</span>
                </div>
                <span class="px-2 py-0.5 rounded text-[10px] font-bold" :class="getReadinessScoreBadgeStyles(pm.average_readiness_score)">
                  {{ Math.round(pm.average_readiness_score || 0) }}% Ready
                </span>
              </div>
              <div class="grid grid-cols-2 gap-2 bg-surface-theme p-2.5 rounded-xl border border-panel-theme text-[11px] font-semibold">
                <div>
                  <p class="text-muted-theme text-[9px] uppercase tracking-wider">Total Proyek</p>
                  <p class="text-main-theme text-sm font-extrabold">{{ pm.total_projects }} Proyek</p>
                </div>
                <div>
                  <p class="text-indigo-400 text-[9px] uppercase tracking-wider">Upcoming (7 Hari)</p>
                  <p class="text-main-theme text-sm font-extrabold">{{ pm.upcoming_events_7_days }} Event</p>
                </div>
                <div>
                  <p class="text-red-400 text-[9px] uppercase tracking-wider">Belum Siap</p>
                  <p class="text-main-theme text-sm font-extrabold">{{ pm.not_ready_projects }} Proyek</p>
                </div>
                <div>
                  <p class="text-amber-500 text-[9px] uppercase tracking-wider">Instrumen Overdue</p>
                  <p class="text-main-theme text-sm font-extrabold">{{ pm.overdue_instruments }} Dokumen</p>
                </div>
              </div>
            </div>
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
import AppEmptyState from '../components/ui/AppEmptyState.vue'
import AppLoadingState from '../components/ui/AppLoadingState.vue'
import AppErrorState from '../components/ui/AppErrorState.vue'

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
const activePmQuickFilter = ref('all')

// Filters variables
const filterPm = ref('')
const filterPo = ref('')
const filterEventWindow = ref('all')
const filterDateFrom = ref('')
const filterDateTo = ref('')
const filterIncludeClosed = ref(false)
const filterIncludeCanceled = ref(false)
const filterReadinessMin = ref('')
const filterReadinessMax = ref('')
const filterInstrumentStatus = ref('')

const pmQuickFilters = [
  { key: 'all', label: 'Semua' },
  { key: 'today', label: 'Hari Ini' },
  { key: 'next_7_days', label: '7 Hari' },
  { key: 'next_14_days', label: '14 Hari' },
  { key: 'not_ready', label: 'Belum Siap' },
  { key: 'overdue', label: 'Overdue' }
]

const tabs = computed(() => [
  { id: 'priority', name: 'Prioritas Tindakan', count: priorityActions.value.length },
  { id: 'events', name: 'Jadwal Event & Kesiapan', count: upcomingEvents.value.length + notReadyProjects.value.length },
  { id: 'instruments', name: 'Checklist & Revisi', count: overdueInstruments.value.length + needRevisionInstruments.value.length },
  { id: 'pm_workload', name: 'Beban Kerja PM', count: pmWorkload.value.length }
])

const fetchUsers = async () => {
  try {
    const res = await axios.get('/api/v1/auth/users/options')
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
    if (filterReadinessMin.value !== '' && filterReadinessMin.value !== null) params.readiness_min = filterReadinessMin.value
    if (filterReadinessMax.value !== '' && filterReadinessMax.value !== null) params.readiness_max = filterReadinessMax.value
    if (filterInstrumentStatus.value) params.instrument_status = filterInstrumentStatus.value

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

const handleManualFilterChange = () => {
  activePmQuickFilter.value = 'custom'
  fetchControlCenterData()
}

const clearPmQuickFilterFields = () => {
  filterDateFrom.value = ''
  filterDateTo.value = ''
  filterReadinessMin.value = ''
  filterReadinessMax.value = ''
  filterInstrumentStatus.value = ''
}

const applyPmQuickFilter = (key) => {
  activePmQuickFilter.value = key

  if (key === 'all') {
    resetFilters()
    return
  }

  clearPmQuickFilterFields()
  filterEventWindow.value = 'all'

  if (key === 'today' || key === 'next_7_days' || key === 'next_14_days' || key === 'overdue') {
    filterEventWindow.value = key
  }

  if (key === 'not_ready') {
    filterReadinessMax.value = 79
  }

  fetchControlCenterData()
}

const resetFilters = () => {
  activePmQuickFilter.value = 'all'
  filterPm.value = ''
  filterPo.value = ''
  filterEventWindow.value = 'all'
  filterDateFrom.value = ''
  filterDateTo.value = ''
  filterIncludeClosed.value = false
  filterIncludeCanceled.value = false
  filterReadinessMin.value = ''
  filterReadinessMax.value = ''
  filterInstrumentStatus.value = ''
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
  if (s >= 80) return 'bg-brand-emerald/15 text-brand-emerald border border-brand-emerald/20'
  if (s >= 50) return 'bg-yellow-500/10 text-yellow-500 border border-yellow-500/20'
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
