<template>
  <div class="app-page">
    <AppPageHeader
      title="Projects"
      subtitle="Kelola pipeline project dari inquiry, CL, planning, execution, PNL, hingga final report."
    />

    <!-- Top actions toolbar -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 select-none">
      <div class="flex flex-col sm:flex-row sm:items-center gap-3">
        <span class="text-xs font-bold uppercase tracking-widest text-muted-theme">Tampilan Pipeline</span>
        <div class="flex rounded-xl p-0.5 bg-surface-theme border border-panel-theme">
          <button 
            @click="viewMode = 'board'" 
            class="px-4 py-2 rounded-lg text-xs font-bold transition-all"
            :class="viewMode === 'board' ? 'bg-brand-orange text-white' : 'text-muted-theme hover:text-main-theme'"
          >
            Kanban Board
          </button>
          <button 
            @click="viewMode = 'list'" 
            class="px-4 py-2 rounded-lg text-xs font-bold transition-all"
            :class="viewMode === 'list' ? 'bg-brand-orange text-white' : 'text-muted-theme hover:text-main-theme'"
          >
            All Projects List
          </button>
        </div>
      </div>

      <button 
        v-if="auth.hasPermission('projects:write')"
        @click="openAddModal"
        class="px-4 py-2.5 rounded-xl bg-gradient-to-r from-brand-orange to-brand-orange-light text-white font-bold text-xs shadow-lg hover:shadow-brand-orange/20 transition-all select-none"
      >
        + Add New Project
      </button>
    </div>

    <!-- Filters Toolbar -->
    <div class="glass-panel p-4 border border-brand-charcoal-light/30 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-3 select-none">
      <!-- Search Filter -->
      <div class="sm:col-span-2">
        <label class="app-label mb-1">Cari Project</label>
        <div class="relative">
          <input
            v-model="projectSearchQuery"
            type="search"
            placeholder="Cari project, klien, venue, PO, PM..."
            class="app-form-control-compact pr-8"
          />
          <button
            v-if="projectSearchQuery"
            type="button"
            @click="clearProjectSearch"
            class="absolute right-1.5 top-1/2 -translate-y-1/2 rounded-md px-1.5 py-0.5 text-[10px] font-black text-muted-theme transition-colors hover:bg-brand-orange/10 hover:text-brand-orange"
            title="Bersihkan pencarian"
          >
            x
          </button>
        </div>
      </div>

      <!-- PO Filter -->
      <div>
        <label class="app-label mb-1">Filter PO</label>
        <select 
          v-model="filterPo" 
          @change="fetchProjectsOnly"
          class="app-form-control-compact"
        >
          <option value="">Semua PO</option>
          <option v-for="u in users" :key="u.id" :value="u.id">{{ u.full_name }}</option>
        </select>
      </div>

      <!-- PM Filter -->
      <div>
        <label class="app-label mb-1">Filter PM</label>
        <select 
          v-model="filterPm" 
          @change="fetchProjectsOnly"
          class="app-form-control-compact"
        >
          <option value="">Semua PM</option>
          <option v-for="u in users" :key="u.id" :value="u.id">{{ u.full_name }}</option>
        </select>
      </div>

      <!-- Source Filter -->
      <div>
        <label class="app-label mb-1">Filter Source</label>
        <select 
          v-model="filterSource" 
          @change="fetchProjectsOnly"
          class="app-form-control-compact"
        >
          <option value="">Semua Sumber</option>
          <option v-for="s in eventSources" :key="s.id" :value="s.id">
            {{ s.vendor_name || 'Direct' }} {{ s.sales_name ? `(${s.sales_name})` : '' }}
          </option>
        </select>
      </div>

      <!-- Quotation Status Filter -->
      <div>
        <label class="app-label mb-1">Status Quote</label>
        <select 
          v-model="filterQuotationStatus" 
          @change="fetchProjectsOnly"
          class="app-form-control-compact"
        >
          <option value="">Semua</option>
          <option value="Draft">Draft</option>
          <option value="Sent">Dikirim (Sent)</option>
          <option value="Follow Up">Follow Up</option>
          <option value="Revision">Revisi (Revision)</option>
          <option value="Signed & Deal">Signed & Deal</option>
          <option value="Cancel">Batal (Cancel)</option>
        </select>
      </div>

      <!-- Program Status Filter -->
      <div>
        <label class="app-label mb-1">Status Prog</label>
        <select 
          v-model="filterProgramStatus" 
          @change="fetchProjectsOnly"
          class="app-form-control-compact"
        >
          <option value="">Semua</option>
          <option value="Inquiry">Inquiry</option>
          <option value="Confirmed">Terkonfirmasi (Confirmed)</option>
          <option value="Preparation">Persiapan (Preparation)</option>
          <option value="Ready">Siap (Ready)</option>
          <option value="Running">Berjalan (Running)</option>
          <option value="Completed">Selesai (Completed)</option>
          <option value="Reporting">Pelaporan (Reporting)</option>
          <option value="Closed">Ditutup (Closed)</option>
          <option value="Cancel">Batal (Cancel)</option>
        </select>
      </div>

      <!-- Payment Status Filter -->
      <div>
        <label class="app-label mb-1">Status Payment</label>
        <select 
          v-model="filterPaymentStatus" 
          @change="fetchProjectsOnly"
          class="app-form-control-compact"
        >
          <option value="">Semua</option>
          <option value="Not Invoiced">Belum Ditagih (Not Invoiced)</option>
          <option value="Invoice Sent">Tagihan Dikirim (Invoice Sent)</option>
          <option value="Partial Paid">Dibayar Sebagian (Partial Paid)</option>
          <option value="Paid">Lunas (Paid)</option>
          <option value="Outstanding">Outstanding (Belum Lunas)</option>
          <option value="Overdue">Jatuh Tempo (Overdue)</option>
        </select>
      </div>

      <!-- Project Status Filter -->
      <div>
        <label class="app-label mb-1">Status Project</label>
        <div class="flex gap-1.5 items-center">
          <select 
            v-model="filterProjectStatus" 
            @change="fetchProjectsOnly"
            class="app-form-control-compact flex-1"
          >
            <option value="">Semua</option>
            <option value="Open">Buka (Open)</option>
            <option value="Active">Aktif (Active)</option>
            <option value="Reporting">Laporan (Reporting)</option>
            <option value="Closed">Ditutup (Closed)</option>
            <option value="Canceled">Batal (Canceled)</option>
          </select>
          <button 
            @click="resetFilters" 
            class="p-1.5 rounded-lg border border-panel-theme bg-surface-theme text-muted-theme hover:text-brand-orange transition-all text-[11px]"
            title="Reset Filters"
          >
            ✕
          </button>
        </div>
      </div>
    </div>

    <!-- Loading matrix -->
    <AppLoadingState v-if="loading" message="Memuat daftar project..." />

    <!-- KANBAN BOARD VIEW -->
    <div v-else-if="filteredProjects.length === 0" class="glass-panel p-8 text-center text-sm app-empty-copy">
      {{ projectsEmptyMessage }}
    </div>

    <div v-else-if="viewMode === 'board'" class="flex gap-4 overflow-x-auto pb-4 h-[calc(100vh-250px)] min-w-full select-none items-start">
      <div 
        v-for="col in columns" 
        :key="col.status"
        class="w-80 shrink-0 bg-panel-theme border border-panel-theme rounded-2xl p-4 flex flex-col max-h-full"
      >
        <!-- Column Header -->
        <div class="flex items-center justify-between mb-4 border-b border-brand-charcoal-light/25 pb-3">
          <div class="flex items-center gap-2">
            <span class="h-2.5 w-2.5 rounded-full" :class="col.bullet"></span>
            <span class="font-extrabold text-xs text-main-theme uppercase tracking-wider">{{ col.name }}</span>
          </div>
          <span class="px-2 py-0.5 rounded bg-surface-theme border border-panel-theme text-[10px] font-bold text-muted-theme">
            {{ getProjectsByStatus(col.status).length }}
          </span>
        </div>

        <!-- Cards List -->
        <div class="flex-1 overflow-y-auto space-y-3.5 pr-1">
          <div 
            v-if="getProjectsByStatus(col.status).length === 0"
            class="py-8 text-center text-[10px] font-bold text-muted-theme border border-dashed border-panel-theme rounded-xl"
          >
            No projects in this stage
          </div>

          <div 
            v-for="proj in getProjectsByStatus(col.status)" 
            :key="proj.id"
            class="interactive-card p-4 space-y-3 select-none relative group text-xs"
          >
            <!-- Card Details -->
            <div>
              <div class="flex items-center justify-between mb-1">
                <span class="text-[9px] font-black text-muted-theme uppercase tracking-wider block">
                  {{ proj.project_code || 'No Code' }}
                </span>
                <span class="text-[9px] font-semibold text-muted-theme">
                  {{ formatDate(proj.event_date_start) }}
                </span>
              </div>
              <router-link :to="'/projects/' + proj.id" class="text-sm font-bold text-main-theme hover:text-brand-orange transition-colors block leading-tight mb-1">
                {{ proj.title }}
              </router-link>
              <!-- Quick Quality Indicators -->
              <div v-if="!proj.program_owner_id || !proj.program_manager_id || (proj.quotation_status === 'Cancel' && !proj.cancel_reason) || proj.payment_status === 'Overdue'" class="flex flex-wrap gap-1 items-center mb-2">
                <span v-if="!proj.program_owner_id" class="px-1.5 py-0.5 rounded text-[8px] font-black uppercase bg-red-500/10 text-red-400 border border-red-500/20">NO PO</span>
                <span v-if="!proj.program_manager_id" class="px-1.5 py-0.5 rounded text-[8px] font-black uppercase bg-yellow-500/10 text-yellow-400 border border-yellow-500/20">NO PM</span>
                <span v-if="proj.quotation_status === 'Cancel' && !proj.cancel_reason" class="px-1.5 py-0.5 rounded text-[8px] font-black uppercase bg-orange-500/10 text-orange-400 border border-orange-500/20">NO REASON</span>
                <span v-if="proj.payment_status === 'Overdue'" class="px-1.5 py-0.5 rounded text-[8px] font-black uppercase bg-purple-500/10 text-purple-400 border border-purple-500/20">OVERDUE</span>
              </div>
              <div class="space-y-0.5">
                <span class="text-[10px] font-extrabold text-soft-theme block truncate">
                  Client: {{ proj.customer?.company_name }}
                </span>
                <span v-if="proj.event_source" class="text-[9px] font-bold text-muted-theme block truncate">
                  Source: {{ proj.event_source.vendor_name || 'Partner' }} {{ proj.event_source.sales_name ? `(${proj.event_source.sales_name})` : '' }}
                </span>
              </div>
            </div>

            <!-- Program Manager & Owner -->
            <div class="grid grid-cols-2 gap-1.5 text-[9px] font-bold bg-surface-theme p-2 rounded-lg border border-panel-theme">
              <div>
                <p class="text-muted-theme">OWNER (PO)</p>
                <p class="text-main-theme truncate">{{ proj.program_owner?.full_name || '-' }}</p>
              </div>
              <div>
                <p class="text-muted-theme">MGR (PM)</p>
                <p class="text-main-theme truncate">{{ proj.program_manager?.full_name || '-' }}</p>
              </div>
            </div>

            <!-- Price & Status badges info -->
            <div class="flex items-center justify-between border-t border-brand-charcoal-light/10 pt-2.5">
              <span class="text-brand-emerald font-bold">{{ formatMoney(proj.budget) }}</span>
              <div class="flex gap-1.5">
                <span class="px-1.5 py-0.5 rounded text-[8px] font-black uppercase" :class="getQuotationStyles(proj.quotation_status)">
                  Q: {{ proj.quotation_status }}
                </span>
                <span class="px-1.5 py-0.5 rounded text-[8px] font-black uppercase" :class="getProjectStyles(proj.project_status)">
                  P: {{ proj.project_status }}
                </span>
              </div>
            </div>

            <!-- Quick workflow Shift Arrows -->
            <div class="flex items-center justify-between border-t border-brand-charcoal-light/10 pt-2 opacity-0 group-hover:opacity-100 transition-opacity">
              <button 
                v-if="auth.hasPermission('projects:write') && col.prev"
                @click="transitionStatus(proj, col.prev)"
              class="p-1 rounded bg-surface-theme border border-panel-theme hover:bg-brand-orange/10 text-muted-theme hover:text-brand-orange transition-all font-bold text-[10px]"
              >
                ← Shift Back
              </button>
              <div v-else></div>
              
              <button 
                v-if="auth.hasPermission('projects:write') && col.next"
                @click="transitionStatus(proj, col.next)"
              class="p-1 rounded bg-surface-theme border border-panel-theme hover:bg-brand-orange/10 text-muted-theme hover:text-brand-orange transition-all font-bold text-[10px]"
              >
                Advance →
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ALL PROJECTS LIST VIEW -->
    <div v-else class="space-y-4">
      <!-- Desktop/Tablet Table View (Hidden on mobile) -->
      <div class="hidden md:block glass-panel overflow-hidden border border-brand-charcoal-light/30">
        <div class="overflow-x-auto min-w-full">
          <table class="min-w-full text-left divide-y divide-brand-charcoal-light/20 text-xs">
            <thead class="app-table-header">
              <tr>
                <th class="px-6 py-4">Code</th>
                <th class="px-6 py-4">Project Title</th>
                <th class="px-6 py-4">Customer Account</th>
                <th class="px-6 py-4">Source / Sales</th>
                <th class="px-6 py-4">PO</th>
                <th class="px-6 py-4">PM</th>
                <th class="px-6 py-4">Event Date</th>
                <th class="px-6 py-4">Quote Status</th>
                <th class="px-6 py-4">Program Status</th>
                <th class="px-6 py-4">Payment Status</th>
                <th class="px-6 py-4">Project Status</th>
                <th class="px-6 py-4">Readiness</th>
                <th class="px-6 py-4">Budget</th>
                <th class="px-6 py-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-brand-charcoal-light/10 font-medium">
              <tr v-if="filteredProjects.length === 0">
                  <td colspan="14" class="px-6 py-12 text-center app-empty-copy">
                  {{ projectsEmptyMessage }}
                </td>
              </tr>
              <tr
                v-for="proj in filteredProjects"
                :key="proj.id"
                class="app-table-row"
              >
                <td class="px-6 py-4 app-table-cell-strong select-all font-mono">{{ proj.project_code || '-' }}</td>
                <td class="px-6 py-4">
                  <div class="flex items-center gap-2">
                    <router-link :to="'/projects/' + proj.id" class="app-table-cell-strong hover:text-brand-orange tracking-wide text-sm block">
                      {{ proj.title }}
                    </router-link>
                    <!-- Quality Warnings Indicators -->
                    <div class="flex gap-1 items-center select-none">
                      <!-- Missing PO -->
                      <span v-if="!proj.program_owner_id" class="h-2 w-2 rounded-full bg-red-500 shrink-0" title="Missing Program Owner (PO)"></span>
                      <!-- Missing PM -->
                      <span v-if="!proj.program_manager_id" class="h-2 w-2 rounded-full bg-yellow-500 shrink-0" title="Missing Program Manager (PM)"></span>
                      <!-- Cancel without reason -->
                      <span v-if="proj.quotation_status === 'Cancel' && !proj.cancel_reason" class="h-2 w-2 rounded-full bg-orange-500 shrink-0" title="Canceled without Reason"></span>
                      <!-- Overdue payment warning -->
                      <span v-if="proj.payment_status === 'Overdue' || (proj.project_status === 'Closed' && proj.payment_status !== 'Paid')" class="h-2 w-2 rounded-full bg-purple-500 shrink-0" title="Payment Overdue / Discrepancy"></span>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 app-table-cell-strong">{{ proj.customer?.company_name }}</td>
                <td class="px-6 py-4 app-table-cell">
                  <div v-if="proj.event_source" class="font-semibold">
                    <p>{{ proj.event_source.vendor_name || 'Partner' }}</p>
                    <p class="text-[10px] text-muted-theme font-medium">{{ proj.event_source.sales_name || 'No Sales' }}</p>
                  </div>
                  <span v-else class="text-muted-theme">-</span>
                </td>
                <td class="px-6 py-4 app-table-cell font-semibold whitespace-nowrap">{{ proj.program_owner?.full_name || '-' }}</td>
                <td class="px-6 py-4 app-table-cell font-semibold whitespace-nowrap">{{ proj.program_manager?.full_name || '-' }}</td>
                <td class="px-6 py-4 app-table-cell font-semibold whitespace-nowrap">
                  <div v-if="proj.event_date_start">
                    <p class="text-main-theme">{{ formatDate(proj.event_date_start) }}</p>
                    <p class="text-[10px] text-muted-theme">to {{ formatDate(proj.event_date_end) }}</p>
                  </div>
                  <span v-else-if="proj.start_date">
                    <p class="text-main-theme">{{ formatDate(proj.start_date) }}</p>
                    <p class="text-[10px] text-muted-theme">to {{ formatDate(proj.end_date) }}</p>
                  </span>
                  <span v-else class="text-muted-theme">-</span>
                </td>
                <td class="px-6 py-4 select-none">
                  <AppStatusBadge :status="proj.quotation_status" type="quotation" />
                </td>
                <td class="px-6 py-4 select-none">
                  <AppStatusBadge :status="proj.program_status || proj.status" type="project" />
                </td>
                <td class="px-6 py-4 select-none">
                  <AppStatusBadge :status="proj.payment_status" type="payment" />
                </td>
                <td class="px-6 py-4 select-none">
                  <AppStatusBadge :status="proj.project_status" type="project" />
                </td>
                <td class="px-6 py-4 select-none">
                  <div class="flex flex-col gap-1">
                    <span class="px-2 py-0.5 rounded text-[10px] font-bold text-center inline-block" :class="getReadinessScoreBadgeStyles(proj.project_readiness_score)">
                      {{ Math.round((proj.project_readiness_score || 0) * 100) }}% Ready
                    </span>
                    <span class="text-[9px] text-muted-theme font-semibold text-center block">
                      {{ Math.round((proj.instrument_completion_rate || 0) * 100) }}% Instruments
                    </span>
                  </div>
                </td>
                <td class="px-6 py-4 font-bold text-brand-emerald">{{ formatMoney(proj.budget) }}</td>
                <td class="px-6 py-4 text-right select-none space-x-2.5 whitespace-nowrap">
                  <router-link 
                    :to="'/projects/' + proj.id"
                    class="px-2.5 py-1 text-[10px] font-bold text-brand-orange bg-brand-orange/10 rounded hover:bg-brand-orange/20 transition-all inline-block"
                  >
                    {{ auth.hasPermission('projects:write') ? 'Manage' : 'View' }}
                  </router-link>
                  <button 
                    v-if="auth.hasPermission('projects:write')"
                    @click="archiveProject(proj.id)"
                    class="px-2.5 py-1 text-[10px] font-bold text-red-400 bg-red-500/10 rounded hover:bg-red-500/20 transition-all"
                  >
                    Archive
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Mobile List View (Hidden on desktop/tablet) -->
      <div class="block md:hidden space-y-4">
        <div v-if="filteredProjects.length === 0" class="glass-panel p-8 text-center app-empty-copy">
          {{ projectsEmptyMessage }}
        </div>
        <div
          v-for="proj in filteredProjects"
          :key="proj.id"
          class="glass-panel p-4 border border-panel-theme space-y-3"
        >
          <div class="flex items-center justify-between border-b border-brand-charcoal-light/10 pb-2">
            <span class="font-mono text-[10px] font-bold text-muted-theme">{{ proj.project_code || '-' }}</span>
            <div class="flex gap-1">
              <AppStatusBadge :status="proj.quotation_status" type="quotation" />
              <AppStatusBadge :status="proj.program_status || proj.status" type="project" />
            </div>
          </div>
          <div>
            <router-link :to="'/projects/' + proj.id" class="font-bold text-sm text-main-theme hover:text-brand-orange transition-colors">
              {{ proj.title }}
            </router-link>
            <p class="text-xs text-soft-theme mt-1 font-semibold">Client: {{ proj.customer?.company_name }}</p>
          </div>
          <div class="grid grid-cols-2 gap-2 bg-surface-theme p-2.5 rounded-xl text-[11px] border border-panel-theme">
            <div>
              <p class="text-muted-theme font-bold text-[9px] uppercase tracking-wider">Assigned PM</p>
              <p class="text-soft-theme font-semibold">{{ proj.program_manager?.full_name || '-' }}</p>
            </div>
            <div>
              <p class="text-muted-theme font-bold text-[9px] uppercase tracking-wider">Assigned PO</p>
              <p class="text-soft-theme font-semibold">{{ proj.program_owner?.full_name || '-' }}</p>
            </div>
            <div>
              <p class="text-muted-theme font-bold text-[9px] uppercase tracking-wider">Event Date</p>
              <p class="text-soft-theme font-semibold">{{ proj.event_date_start ? formatDate(proj.event_date_start) : '-' }}</p>
            </div>
            <div>
              <p class="text-muted-theme font-bold text-[9px] uppercase tracking-wider">Budget Allocation</p>
              <p class="text-brand-emerald font-bold">{{ formatMoney(proj.budget) }}</p>
            </div>
          </div>
          <div class="flex items-center justify-between pt-2">
            <div class="flex flex-col">
              <span class="text-xs font-bold text-main-theme">{{ Math.round((proj.project_readiness_score || 0) * 100) }}% Ready</span>
              <span class="text-[10px] text-muted-theme">{{ Math.round((proj.instrument_completion_rate || 0) * 100) }}% Instruments</span>
            </div>
            <div class="flex gap-2">
              <router-link 
                :to="'/projects/' + proj.id"
                class="px-3 py-1.5 text-xs font-bold text-brand-orange bg-brand-orange/10 rounded-xl hover:bg-brand-orange/20 transition-all"
              >
                {{ auth.hasPermission('projects:write') ? 'Manage' : 'View' }}
              </router-link>
              <button 
                v-if="auth.hasPermission('projects:write')"
                @click="archiveProject(proj.id)"
                class="px-3 py-1.5 text-xs font-bold text-red-400 bg-red-500/10 rounded-xl hover:bg-red-500/20 transition-all"
              >
                Archive
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Create Project Drawer / Modal -->
    <div v-if="showAddModal" class="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 select-none">
      <div class="bg-panel-theme border border-panel-theme rounded-3xl w-full max-w-2xl shadow-2xl p-6 relative overflow-y-auto max-h-[90vh]">
        <h3 class="text-base font-bold text-main-theme tracking-wide mb-5">Create Project Entry</h3>
        
        <form @submit.prevent="saveProject" class="space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- Title -->
            <div class="md:col-span-2">
              <label class="app-label mb-1.5">Project/Event Title *</label>
              <input 
                v-model="newProj.title"
                type="text" 
                required
                placeholder="e.g. Annual Outing & Team Building 2026"
                class="app-form-control text-xs"
              />
            </div>

            <!-- Project Code & Inquiry Date -->
            <div>
              <label class="app-label mb-1.5">Project Code</label>
              <input 
                v-model="newProj.project_code"
                type="text" 
                placeholder="e.g. OSA-2026-001"
                class="app-form-control text-xs"
              />
            </div>
            <div>
              <label class="app-label mb-1.5">Inquiry Date</label>
              <input 
                v-model="newProj.inquiry_date"
                type="date"
                class="app-form-control text-xs"
              />
            </div>

            <!-- Client & Event Source -->
            <div>
              <label class="app-label mb-1.5">Client Account</label>
              <select 
                v-model="newProj.customer_id"
                class="app-form-control text-xs"
              >
                <option value="">New client</option>
                <option v-for="c in customers" :key="c.id" :value="c.id">{{ c.company_name }}</option>
              </select>
            </div>
            <div>
              <label class="app-label mb-1.5">Event Source</label>
              <select 
                v-model="newProj.event_source_id"
                class="app-form-control text-xs"
              >
                <option :value="null">Direct / None</option>
                <option v-for="s in eventSources" :key="s.id" :value="s.id">
                  {{ s.vendor_name || 'Partner' }} {{ s.sales_name ? `(${s.sales_name})` : '' }}
                </option>
              </select>
            </div>
            <div>
              <label class="app-label mb-1.5">New Client Name <span v-if="!newProj.customer_id">*</span></label>
              <input
                v-model.trim="newProj.customer_name"
                type="text"
                :required="!newProj.customer_id"
                :disabled="Boolean(newProj.customer_id)"
                placeholder="e.g. PT Nusantara Event"
                class="app-form-control text-xs disabled:opacity-60"
              />
            </div>
            <div>
              <label class="app-label mb-1.5">New Client Category</label>
              <select
                v-model="newProj.customer_category"
                :disabled="Boolean(newProj.customer_id)"
                class="app-form-control text-xs disabled:opacity-60"
              >
                <option value="Prospect">Prospect</option>
                <option value="Corporate">Corporate</option>
                <option value="Agency">Agency</option>
                <option value="Partner">Partner</option>
                <option value="Individual">Individual</option>
              </select>
            </div>

            <!-- PO & PM -->
            <div>
              <label class="app-label mb-1.5">Program Owner (PO)</label>
              <select 
                v-model="newProj.program_owner_id"
                class="app-form-control text-xs"
              >
                <option :value="null">Unassigned</option>
                <option v-for="u in users" :key="u.id" :value="u.id">{{ u.full_name }}</option>
              </select>
            </div>
            <div>
              <label class="app-label mb-1.5">Program Manager (PM)</label>
              <select 
                v-model="newProj.program_manager_id"
                class="app-form-control text-xs"
              >
                <option :value="null">Unassigned</option>
                <option v-for="u in users" :key="u.id" :value="u.id">{{ u.full_name }}</option>
              </select>
            </div>

            <!-- Event Category & Program Type -->
            <div>
              <label class="app-label mb-1.5">Event Category</label>
              <input 
                v-model="newProj.event_category"
                type="text" 
                placeholder="e.g. Gathering, Outing, Training"
                class="app-form-control text-xs"
              />
            </div>
            <div>
              <label class="app-label mb-1.5">Program Type</label>
              <input 
                v-model="newProj.program_type"
                type="text" 
                placeholder="e.g. Team Building, Webinar"
                class="app-form-control text-xs"
              />
            </div>

            <!-- Program Name & Quantity -->
            <div>
              <label class="app-label mb-1.5">Program Name</label>
              <input 
                v-model="newProj.program_name"
                type="text" 
                placeholder="e.g. Spirit of Harmony"
                class="app-form-control text-xs"
              />
            </div>
            <div>
              <label class="app-label mb-1.5">Quantity / Pax</label>
              <input 
                v-model="newProj.quantity"
                type="number" 
                placeholder="e.g. 100"
                class="app-form-control text-xs"
              />
            </div>

            <!-- Venue & Duration -->
            <div>
              <label class="app-label mb-1.5">Event Venue</label>
              <input 
                v-model="newProj.venue"
                type="text" 
                placeholder="e.g. Dago Highlands Resort"
                class="app-form-control text-xs"
              />
            </div>
            <div>
              <label class="app-label mb-1.5">Duration</label>
              <input 
                v-model="newProj.duration"
                type="text" 
                placeholder="e.g. 3 Days 2 Nights"
                class="app-form-control text-xs"
              />
            </div>

            <!-- Start Date & End Date -->
            <div>
              <label class="app-label mb-1.5">Event Start Date</label>
              <input 
                v-model="newProj.event_date_start"
                type="date"
                class="app-form-control text-xs"
              />
            </div>
            <div>
              <label class="app-label mb-1.5">Event End Date</label>
              <input 
                v-model="newProj.event_date_end"
                type="date"
                class="app-form-control text-xs"
              />
            </div>

            <!-- Quotation Date & Quotation Number -->
            <div>
              <label class="app-label mb-1.5">Quotation Date</label>
              <input 
                v-model="newProj.quotation_date"
                type="date"
                class="app-form-control text-xs"
              />
            </div>
            <div>
              <label class="app-label mb-1.5">Quotation Number</label>
              <input 
                v-model="newProj.quotation_number"
                type="text" 
                placeholder="e.g. Q-2026-99"
                class="app-form-control text-xs"
              />
            </div>

            <!-- Quotation Status & Program Status -->
            <div>
              <label class="app-label mb-1.5">Quotation Status</label>
              <select 
                v-model="newProj.quotation_status"
                class="app-form-control text-xs"
              >
                <option value="Draft">Draft</option>
                <option value="Sent">Sent</option>
                <option value="Follow Up">Follow Up</option>
                <option value="Revision">Revision</option>
                <option value="Signed & Deal">Signed & Deal</option>
                <option value="Cancel">Cancel</option>
              </select>
            </div>
            <div>
              <label class="app-label mb-1.5">Program Status</label>
              <select 
                v-model="newProj.program_status"
                class="app-form-control text-xs"
              >
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

            <!-- Payment Status & Project Status -->
            <div>
              <label class="app-label mb-1.5">Payment Status</label>
              <select 
                v-model="newProj.payment_status"
                class="app-form-control text-xs"
              >
                <option value="Not Invoiced">Not Invoiced</option>
                <option value="Invoice Sent">Invoice Sent</option>
                <option value="Partial Paid">Partial Paid</option>
                <option value="Paid">Paid</option>
                <option value="Outstanding">Outstanding</option>
                <option value="Overdue">Overdue</option>
              </select>
            </div>
            <div>
              <label class="app-label mb-1.5">Project Status</label>
              <select 
                v-model="newProj.project_status"
                class="app-form-control text-xs"
              >
                <option value="Open">Open</option>
                <option value="Active">Active</option>
                <option value="Reporting">Reporting</option>
                <option value="Closed">Closed</option>
                <option value="Canceled">Canceled</option>
              </select>
            </div>

            <!-- Budget & Revenue -->
            <div>
              <label class="app-label mb-1.5">Budget Allocation (Rp)</label>
              <input 
                v-model="newProj.budget"
                type="number"
                step="0.01"
                placeholder="0.00"
                class="app-form-control text-xs"
              />
            </div>
            <div>
              <label class="app-label mb-1.5">Revenue Goal (Rp)</label>
              <input 
                v-model="newProj.revenue"
                type="number"
                step="0.01"
                placeholder="0.00"
                class="app-form-control text-xs"
              />
            </div>

            <!-- General Notes -->
            <div class="md:col-span-2">
              <label class="app-label mb-1.5">General Notes</label>
              <textarea 
                v-model="newProj.general_notes"
                placeholder="Enter general remarks..."
                rows="3"
                class="app-form-control text-xs"
              ></textarea>
            </div>
          </div>

          <div class="flex items-center justify-end gap-3 pt-3 select-none">
            <button 
              type="button"
              @click="showAddModal = false"
              class="px-4 py-2.5 rounded-xl border border-panel-theme text-xs font-bold text-muted-theme hover:text-main-theme hover:bg-surface-theme transition-all"
            >
              Cancel
            </button>
            <button 
              type="submit"
              class="px-5 py-2.5 rounded-xl bg-gradient-to-r from-brand-orange to-brand-orange-light text-white font-bold text-xs shadow-lg hover:shadow-brand-orange/20 transition-all"
            >
              Initialize Project
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import axios from 'axios'
import { useAuthStore } from '../store/auth'
import { useUiStore } from '../store/ui'
import AppPageHeader from '../components/ui/AppPageHeader.vue'
import AppStatusBadge from '../components/ui/AppStatusBadge.vue'
import AppLoadingState from '../components/ui/AppLoadingState.vue'

const auth = useAuthStore()
const ui = useUiStore()

const getApiErrorMessage = (err, fallback) => {
  const detail = err.response?.data?.detail
  if (typeof detail === 'string') return detail
  if (detail?.message && typeof detail.message === 'string') return detail.message
  return fallback
}
const projects = ref([])
const customers = ref([])
const users = ref([])
const eventSources = ref([])

const loading = ref(true)
const viewMode = ref('board')
const showAddModal = ref(false)

// Filter variables
const filterPo = ref('')
const filterPm = ref('')
const filterSource = ref('')
const filterQuotationStatus = ref('')
const filterProgramStatus = ref('')
const filterPaymentStatus = ref('')
const filterProjectStatus = ref('')
const projectSearchQuery = ref('')

const newProj = ref({
  title: '',
  project_code: '',
  inquiry_date: '',
  customer_id: '',
  customer_name: '',
  customer_category: 'Prospect',
  event_source_id: null,
  program_owner_id: null,
  program_manager_id: null,
  event_category: '',
  program_type: '',
  program_name: '',
  quantity: null,
  venue: '',
  duration: '',
  event_date_start: '',
  event_date_end: '',
  quotation_date: '',
  quotation_number: '',
  quotation_status: 'Draft',
  program_status: 'Inquiry',
  payment_status: 'Not Invoiced',
  project_status: 'Open',
  budget: 0,
  revenue: 0,
  general_notes: ''
})

const columns = [
  { status: 'Inquiry', name: 'Inquiry', bullet: 'bg-brand-orange', next: 'Confirmed' },
  { status: 'Confirmed', name: 'Confirmed', bullet: 'bg-purple-500', prev: 'Inquiry', next: 'Preparation' },
  { status: 'Preparation', name: 'Preparation', bullet: 'bg-yellow-500', prev: 'Confirmed', next: 'Ready' },
  { status: 'Ready', name: 'Ready', bullet: 'bg-indigo-500', prev: 'Preparation', next: 'Running' },
  { status: 'Running', name: 'Running', bullet: 'bg-orange-500', prev: 'Ready', next: 'Completed' },
  { status: 'Completed', name: 'Completed', bullet: 'bg-brand-emerald', prev: 'Running', next: 'Reporting' },
  { status: 'Reporting', name: 'Reporting', bullet: 'bg-teal-500', prev: 'Completed', next: 'Closed' },
  { status: 'Closed', name: 'Closed', bullet: 'bg-gray-500', prev: 'Reporting' },
  { status: 'Cancel', name: 'Cancel', bullet: 'bg-red-500' }
]

const fetchData = async () => {
  try {
    const canLoadCrmReferenceData = auth.hasPermission('crm:read')
    const [projRes, sourceRes, custRes, usersRes] = await Promise.all([
      axios.get('/api/v1/projects'),
      axios.get('/api/v1/event-sources'),
      canLoadCrmReferenceData ? axios.get('/api/v1/customers') : Promise.resolve({ data: [] }),
      canLoadCrmReferenceData ? axios.get('/api/v1/auth/users/options') : Promise.resolve({ data: [] })
    ])
    projects.value = projRes.data
    customers.value = custRes.data
    users.value = usersRes.data
    eventSources.value = sourceRes.data
  } catch (err) {
    console.error('Failed to load project database', err)
  } finally {
    loading.value = false
  }
}

const fetchProjectsOnly = async () => {
  try {
    const params = {}
    if (filterPo.value) params.po_id = filterPo.value
    if (filterPm.value) params.pm_id = filterPm.value
    if (filterSource.value) params.source_id = filterSource.value
    if (filterQuotationStatus.value) params.quotation_status = filterQuotationStatus.value
    if (filterProgramStatus.value) params.program_status = filterProgramStatus.value
    if (filterPaymentStatus.value) params.payment_status = filterPaymentStatus.value
    if (filterProjectStatus.value) params.project_status = filterProjectStatus.value

    const res = await axios.get('/api/v1/projects', { params })
    projects.value = res.data
  } catch (err) {
    console.error('Failed to filter project lists', err)
  }
}

const resetFilters = () => {
  filterPo.value = ''
  filterPm.value = ''
  filterSource.value = ''
  filterQuotationStatus.value = ''
  filterProgramStatus.value = ''
  filterPaymentStatus.value = ''
  filterProjectStatus.value = ''
  projectSearchQuery.value = ''
  fetchProjectsOnly()
}

onMounted(() => {
  fetchData()
})

const normalizedProjectSearchQuery = computed(() => projectSearchQuery.value.trim().toLowerCase())

const getProjectSearchText = (project) => {
  const customer = project.customer?.company_name || customers.value.find(c => c.id === project.customer_id)?.company_name || ''
  const programOwner = project.program_owner?.full_name || users.value.find(u => u.id === project.program_owner_id)?.full_name || ''
  const programManager = project.program_manager?.full_name || users.value.find(u => u.id === project.program_manager_id)?.full_name || ''
  return [
    project.title,
    project.project_code,
    customer,
    project.venue,
    programOwner,
    programManager,
    project.program_type,
    project.event_category,
    project.program_name
  ].filter(Boolean).join(' ').toLowerCase()
}

const filteredProjects = computed(() => {
  if (!normalizedProjectSearchQuery.value) return projects.value
  return projects.value.filter(project => getProjectSearchText(project).includes(normalizedProjectSearchQuery.value))
})

const projectsEmptyMessage = computed(() => {
  return normalizedProjectSearchQuery.value
    ? 'Tidak ada project yang cocok dengan pencarian.'
    : 'Belum ada project aktif dalam katalog.'
})

const clearProjectSearch = () => {
  projectSearchQuery.value = ''
}

const getProjectsByStatus = (status) => {
  return filteredProjects.value.filter(p => {
    const progStatus = p.program_status || p.status || ''
    return progStatus.toLowerCase() === status.toLowerCase()
  })
}

const formatMoney = (val) => {
  return 'Rp ' + Number(val || 0).toLocaleString('id-ID', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  })
}

const formatDate = (val) => {
  if (!val) return '-'
  return new Date(val).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

const getQuotationStyles = (status) => {
  const cleaned = (status || '').toLowerCase()
  if (cleaned === 'signed & deal' || cleaned === 'signed' || cleaned === 'deal' || cleaned === 'approved') {
    return 'bg-brand-emerald/15 text-brand-emerald border border-brand-emerald/20'
  }
  if (cleaned === 'sent') return 'bg-brand-blue/10 text-brand-blue border border-brand-blue/20'
  if (cleaned === 'follow up' || cleaned === 'followup') return 'bg-orange-500/10 text-orange-400 border border-orange-500/20'
  if (cleaned === 'revision') return 'bg-yellow-500/10 text-yellow-500 border border-yellow-500/20'
  if (cleaned === 'cancel' || cleaned === 'canceled' || cleaned === 'rejected') return 'bg-red-500/10 text-red-400 border border-red-500/20'
  return 'bg-brand-charcoal-light/35 text-gray-300'
}

const getProjectStyles = (status) => {
  const cleaned = (status || '').toLowerCase()
  if (cleaned === 'open') return 'bg-brand-blue/10 text-brand-blue border border-brand-blue/20'
  if (cleaned === 'active') return 'bg-brand-orange/15 text-brand-orange border border-brand-orange/20'
  if (cleaned === 'reporting') return 'bg-purple-500/10 text-purple-500 border border-purple-500/20'
  if (cleaned === 'closed') return 'bg-gray-500/10 text-gray-400 border border-gray-500/20'
  if (cleaned === 'canceled') return 'bg-red-500/10 text-red-400 border border-red-500/20'
  return 'bg-brand-charcoal-light/35 text-gray-400'
}

const getReadinessScoreBadgeStyles = (score) => {
  const s = score || 0
  if (s >= 0.8) return 'bg-brand-emerald/15 text-brand-emerald border border-brand-emerald/20'
  if (s >= 0.5) return 'bg-yellow-500/10 text-yellow-500 border border-yellow-500/20'
  return 'bg-red-500/10 text-red-400 border border-red-500/20'
}

const openAddModal = () => {
  showAddModal.value = true
}

const saveProject = async () => {
  try {
    const payload = { ...newProj.value }
    if (payload.customer_id) {
      delete payload.customer_name
      delete payload.customer_category
    } else {
      delete payload.customer_id
      payload.customer_name = (payload.customer_name || '').trim()
      if (!payload.customer_name) {
        ui.error('Pilih Client Account atau isi nama klien baru.')
        return
      }
      payload.customer_category = payload.customer_category || 'Prospect'
    }

    // Clean up empty optional date fields so backend does not fail validation
    if (!payload.inquiry_date) delete payload.inquiry_date
    if (!payload.event_date_start) delete payload.event_date_start
    if (!payload.event_date_end) delete payload.event_date_end
    if (!payload.quotation_date) delete payload.quotation_date

    // Set legacy fields for backward compatibility
    payload.start_date = payload.event_date_start || null
    payload.end_date = payload.event_date_end || null
    payload.status = (payload.program_status || 'Inquiry').toLowerCase()
    payload.assigned_to_id = payload.program_manager_id || null

    const response = await axios.post('/api/v1/projects', payload)
    
    // Fetch and append relation metadata manually to prevent reload
    const client = response.data.customer || customers.value.find(c => c.id === response.data.customer_id)
    const source = eventSources.value.find(s => s.id === response.data.event_source_id)
    const po = users.value.find(u => u.id === response.data.program_owner_id)
    const pm = users.value.find(u => u.id === response.data.program_manager_id)
    
    if (client && !customers.value.some(c => c.id === client.id)) {
      customers.value.push(client)
    }

    response.data.customer = client
    response.data.event_source = source
    response.data.program_owner = po
    response.data.program_manager = pm
    response.data.assigned_to = pm
    
    projects.value.push(response.data)
    showAddModal.value = false
    
    // Reset form
    newProj.value = {
      title: '',
      project_code: '',
      inquiry_date: '',
      customer_id: '',
      customer_name: '',
      customer_category: 'Prospect',
      event_source_id: null,
      program_owner_id: null,
      program_manager_id: null,
      event_category: '',
      program_type: '',
      program_name: '',
      quantity: null,
      venue: '',
      duration: '',
      event_date_start: '',
      event_date_end: '',
      quotation_date: '',
      quotation_number: '',
      quotation_status: 'Draft',
      program_status: 'Inquiry',
      payment_status: 'Not Invoiced',
      project_status: 'Open',
      budget: 0,
      revenue: 0,
      general_notes: ''
    }
  } catch (err) {
    ui.error(getApiErrorMessage(err, 'Gagal membuat project.'))
  }
}

const transitionStatus = async (proj, newStatus) => {
  try {
    const response = await axios.post(`/api/v1/projects/${proj.id}/transition?new_status=${newStatus}`)
    proj.status = response.data.status
    proj.program_status = response.data.program_status
  } catch (err) {
    ui.error(getApiErrorMessage(err, 'Gagal mengubah status project.'))
  }
}

const archiveProject = async (id) => {
  const confirmed = await ui.confirm ({
    title: 'Arsipkan Project?',
    message: 'Project akan diarsipkan dari workflow aktif dan dipindahkan ke proses arsip.',
    confirmText: 'Arsipkan',
    cancelText: 'Batal',
    tone: 'warning'
  })
  if (!confirmed) return
  try {
    await axios.delete(`/api/v1/projects/${id}`)
    projects.value = projects.value.filter(p => p.id !== id)
  } catch {
    ui.error('Gagal mengarsipkan project.')
  }
}
</script>
