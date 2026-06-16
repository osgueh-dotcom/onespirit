<template>
  <div class="app-page">
    <ProjectDetailHeader
      v-if="project"
      :project="project"
      :can-edit="auth.hasPermission('projects:write')"
      @transition="transitionStatus"
    />

    <!-- Loading Indicators -->
    <div v-if="loading" class="h-64 flex flex-col items-center justify-center gap-3">
      <svg class="animate-spin h-6 w-6 text-brand-orange" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
      <span class="text-xs text-muted-theme font-semibold">Memuat ledger operasional...</span>
    </div>

    <div v-else class="space-y-6">
      <ProjectValidationWarnings :warnings="validationWarnings" />

      <!-- Project Action Summary -->
      <div v-if="project" class="glass-panel p-5 border border-panel-theme bg-surface-theme select-none relative overflow-hidden">
        <!-- Accent line -->
        <div class="absolute left-0 top-0 bottom-0 w-1 bg-gradient-to-b from-brand-orange to-brand-orange-light"></div>
        
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-6 pl-2">
          <!-- Left side: Recommended action details -->
          <div class="flex-1 space-y-1.5">
            <p class="app-kicker">Recommended Next Action</p>
            <div class="flex items-center gap-2 flex-wrap">
              <span class="px-3 py-1 text-sm font-black rounded-xl border transition-all duration-300" :class="nextActionInfo.color">
                {{ nextActionInfo.text }}
              </span>
            </div>
            <p class="text-xs text-muted-theme font-medium leading-relaxed max-w-2xl">
              {{ nextActionInfo.description }}
            </p>
            <!-- CTA Action Links/Buttons -->
            <div v-if="nextActionInfo.ctas && nextActionInfo.ctas.length > 0" class="flex items-center gap-2 mt-3 flex-wrap">
              <button
                v-for="cta in nextActionInfo.ctas"
                :key="cta.label"
                @click="handleCtaClick(cta)"
                class="px-3 py-1.5 rounded-xl text-[11px] font-bold transition-all duration-200 border flex items-center gap-1.5 shadow-sm active:scale-95 cursor-pointer"
                :class="getCtaButtonClasses(nextActionInfo.tone)"
              >
                <span>{{ cta.label }}</span>
                <svg class="h-3 w-3 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </div>
          </div>

          <!-- Right side: Mini-grid of KPIs -->
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 shrink-0 min-w-0 md:min-w-[420px] lg:min-w-[480px]">
            <!-- Event Days Remaining -->
            <div class="app-subtle-panel p-3 text-center md:text-left">
              <p class="text-[9px] font-extrabold uppercase tracking-widest text-muted-theme">Days to Event</p>
              <p v-if="daysRemaining !== null" class="mt-1.5 text-base font-black tracking-tight" :class="daysRemaining < 0 ? 'text-red-400' : daysRemaining <= 7 ? 'text-brand-orange' : 'text-main-theme'">
                {{ daysRemaining }} <span class="text-xs font-semibold text-muted-theme">Days</span>
              </p>
              <p v-else class="mt-1.5 text-xs font-bold text-soft-theme italic">Not Scheduled</p>
            </div>

            <!-- Program Status -->
            <div class="app-subtle-panel p-3 text-center md:text-left">
              <p class="text-[9px] font-extrabold uppercase tracking-widest text-muted-theme">Program Status</p>
              <p class="mt-1.5 text-xs font-black text-main-theme truncate" :title="project.program_status">
                {{ project.program_status || 'Inquiry' }}
              </p>
            </div>

            <!-- Readiness Score -->
            <div class="app-subtle-panel p-3 text-center md:text-left">
              <p class="text-[9px] font-extrabold uppercase tracking-widest text-muted-theme">Readiness</p>
              <p class="mt-1.5 text-base font-black tracking-tight" :class="project.project_readiness_score >= 1.0 ? 'text-brand-emerald' : project.project_readiness_score >= 0.7 ? 'text-brand-blue' : 'text-brand-orange'">
                {{ (project.project_readiness_score !== null && !isNaN(project.project_readiness_score)) ? Math.round(project.project_readiness_score * 100) + '%' : '0%' }}
              </p>
            </div>

            <!-- Payment Status -->
            <div class="app-subtle-panel p-3 text-center md:text-left">
              <p class="text-[9px] font-extrabold uppercase tracking-widest text-muted-theme">Payment Status</p>
              <p class="mt-1.5 text-xs font-black truncate" :class="project.payment_status === 'Paid' ? 'text-brand-emerald' : project.payment_status === 'Partial Paid' ? 'text-brand-blue' : 'text-brand-orange'" :title="project.payment_status">
                {{ project.payment_status || 'Not Invoiced' }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Operational Dashboard Layout Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        <!-- Left Side: Event Details & Action ledger tabs -->
        <div class="lg:col-span-2 space-y-6">
          
          <!-- Parameters cards -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 select-none">
            <!-- Event parameters -->
            <div class="glass-panel p-5 space-y-3">
              <h4 class="text-xs font-bold text-main-theme uppercase tracking-wider border-b border-panel-theme pb-2">Event Parameters</h4>
              <div class="grid grid-cols-2 gap-3 text-xs">
                <div>
                  <p class="text-muted-theme font-semibold">Category</p>
                  <p class="text-main-theme font-bold mt-0.5">{{ project.event_category || '-' }}</p>
                </div>
                <div>
                  <p class="text-muted-theme font-semibold">Program Type</p>
                  <p class="text-main-theme font-bold mt-0.5">{{ project.program_type || '-' }}</p>
                </div>
                <div>
                  <p class="text-muted-theme font-semibold">Program Name</p>
                  <p class="text-main-theme font-bold mt-0.5">{{ project.program_name || '-' }}</p>
                </div>
                <div>
                  <p class="text-muted-theme font-semibold">Quantity (Pax)</p>
                  <p class="text-main-theme font-bold mt-0.5">{{ project.quantity || '-' }}</p>
                </div>
                <div>
                  <p class="text-muted-theme font-semibold">Venue</p>
                  <p class="text-main-theme font-bold mt-0.5">{{ project.venue || '-' }}</p>
                </div>
                <div>
                  <p class="text-muted-theme font-semibold">Duration</p>
                  <p class="text-main-theme font-bold mt-0.5">{{ project.duration || '-' }}</p>
                </div>
              </div>
            </div>

            <!-- Quotation Parameters -->
            <div class="glass-panel p-5 space-y-3">
              <h4 class="text-xs font-bold text-main-theme uppercase tracking-wider border-b border-panel-theme pb-2">Quotation & Financials</h4>
              <div class="grid grid-cols-2 gap-3 text-xs">
                <div>
                  <p class="text-muted-theme font-semibold">Quote Reference</p>
                  <p class="text-main-theme font-bold mt-0.5">{{ project.quotation_number || '-' }}</p>
                </div>
                <div>
                  <p class="text-muted-theme font-semibold">Quotation Date</p>
                  <p class="text-main-theme font-bold mt-0.5">{{ project.quotation_date || '-' }}</p>
                </div>
                <div>
                  <p class="text-muted-theme font-semibold">Inquiry Date</p>
                  <p class="text-main-theme font-bold mt-0.5">{{ project.inquiry_date || '-' }}</p>
                </div>
                <div>
                  <p class="text-muted-theme font-semibold">Allocated Revenue</p>
                  <p class="text-brand-emerald font-black mt-0.5">{{ formatMoney(project.revenue) }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Notes Card -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 select-none">
            <!-- General Notes & Cancel -->
            <div class="glass-panel p-5 space-y-3">
              <h4 class="text-xs font-bold text-main-theme uppercase tracking-wider border-b border-panel-theme pb-2">General & Cancel Notes</h4>
              <div class="text-xs space-y-3">
                <div v-if="project.cancel_reason">
                  <p class="text-red-400 font-bold">Cancellation Reason</p>
                  <p class="p-3 bg-red-500/10 border border-red-500/20 rounded-xl text-red-200 mt-1 font-semibold leading-relaxed">
                    {{ project.cancel_reason }}
                  </p>
                </div>
                <div>
                  <p class="text-muted-theme font-semibold">General Remarks</p>
                  <p class="text-soft-theme font-semibold mt-1 whitespace-pre-line leading-relaxed">
                    {{ project.general_notes || 'No general notes recorded.' }}
                  </p>
                </div>
              </div>
            </div>

            <!-- MOM Notes -->
            <div class="glass-panel p-5 space-y-3">
              <h4 class="text-xs font-bold text-main-theme uppercase tracking-wider border-b border-panel-theme pb-2">Minutes of Meeting (MOM)</h4>
              <div class="text-xs">
                <p class="text-soft-theme font-semibold whitespace-pre-line leading-relaxed">
                  {{ project.mom_notes || 'No meeting minutes logged yet.' }}
                </p>
              </div>
            </div>
          </div>

          <!-- Dynamic ledger action tabs -->
          <div class="space-y-6">
            <!-- Tabs Navigation -->
            <div id="tabs-navigation" class="flex border-b border-panel-theme pb-0.5 select-none gap-4 shrink-0 overflow-x-auto scroll-mt-24">
              <button 
                v-for="tab in tabs" 
                :key="tab.id"
                @click="activeTab = tab.id"
                class="pb-3 text-xs font-bold uppercase tracking-wider relative transition-colors whitespace-nowrap"
                :class="activeTab === tab.id ? 'text-brand-orange border-b-2 border-brand-orange' : 'text-muted-theme hover:text-main-theme'"
              >
                {{ tab.name }}
              </button>
            </div>

            <!-- TAB 1: EVENT TIMELINE (Rundowns) -->
            <div v-if="activeTab === 'schedules'" class="space-y-6">
              <div class="flex items-center justify-between gap-4 select-none">
                <h3 class="text-sm font-extrabold uppercase tracking-wider text-main-theme">Event Venues & Rundown Sheets</h3>
                <button 
                  v-if="auth.hasPermission('events:write')"
                  @click="showAddScheduleModal = true"
                  class="px-3.5 py-2 rounded-xl bg-brand-orange text-white font-bold text-xs shadow hover:bg-brand-orange-dark transition-all"
                >
                  + Link Venue Schedule
                </button>
              </div>

              <AppEmptyState
                v-if="schedules.length === 0"
                title="Belum Ada Data"
                message="Tidak ada rundown yang tercatat untuk project ini. Hubungkan jadwal venue untuk memulai."
              >
                <template #actions v-if="auth.hasPermission('events:write')">
                  <button 
                    @click="showAddScheduleModal = true"
                    class="px-4 py-2 bg-brand-orange text-white rounded-lg font-bold text-xs hover:bg-brand-orange-dark transition-all"
                  >
                    + Link Venue Schedule
                  </button>
                </template>
              </AppEmptyState>

              <!-- Venue Schedule Listing Grid -->
              <div v-else class="grid grid-cols-1 gap-6">
                <div 
                  v-for="sched in schedules" 
                  :key="sched.id"
                  class="glass-panel p-6 space-y-4"
                >
                  <!-- Schedule Header -->
                  <div class="flex items-center justify-between flex-wrap gap-4 border-b border-panel-theme pb-4 select-none">
                    <div class="space-y-1">
                      <div class="flex items-center gap-2 flex-wrap">
                        <h4 class="text-base font-extrabold text-main-theme tracking-wide">{{ sched.venue_name }}</h4>
                        
                        <!-- Status Badges -->
                        <span 
                          v-if="sched.rundown?.length > 0" 
                          class="px-2 py-0.5 rounded-full text-[9px] font-black uppercase tracking-wider bg-brand-emerald/15 text-brand-emerald border border-brand-emerald/20"
                        >
                          Siap
                        </span>
                        <span 
                          v-else 
                          class="px-2 py-0.5 rounded-full text-[9px] font-black uppercase tracking-wider bg-brand-orange/15 text-brand-orange border border-brand-orange/20"
                        >
                          Belum Lengkap
                        </span>
                        
                        <span 
                          v-if="isApproachingEvent(sched.start_time)" 
                          class="px-2 py-0.5 rounded-full text-[9px] font-black uppercase tracking-wider bg-amber-500/15 text-amber-500 border border-amber-500/25 animate-pulse"
                        >
                          Mendekati Event
                        </span>
                      </div>
                      <p class="text-xs text-muted-theme mt-1">
                        Location: <span class="text-soft-theme font-semibold">{{ sched.address || '-' }}</span>
                        <span v-if="sched.map_link">
                          | <a :href="sched.map_link" target="_blank" class="text-brand-blue hover:underline font-bold">Google Maps ↗</a>
                        </span>
                      </p>
                    </div>
                    <div class="text-right text-xs space-y-1.5">
                      <p class="font-bold text-soft-theme">Time: {{ formatDateTime(sched.start_time) }} to {{ formatDateTime(sched.end_time) }}</p>
                      <div class="flex items-center justify-end gap-1.5 mt-1">
                        <span class="text-[9px] text-muted-theme font-extrabold uppercase tracking-widest">PIC:</span>
                        <span class="px-2 py-0.5 rounded bg-brand-orange/15 text-brand-orange text-[10px] font-black border border-brand-orange/20">
                          {{ sched.pic?.full_name || 'Unassigned' }}
                        </span>
                      </div>
                    </div>
                  </div>

                  <!-- Rundown Table -->
                  <div>
                    <p class="text-[10px] font-extrabold uppercase tracking-widest text-brand-orange mb-3 select-none">Hour-by-Hour Rundown Timesheet</p>
                    <!-- Desktop Rundown Table -->
                    <div class="hidden md:block overflow-x-auto rounded-xl border border-panel-theme">
                      <table class="min-w-full text-left text-xs divide-y divide-panel-theme">
                        <thead class="app-table-header">
                          <tr>
                            <th class="px-4 py-3">Time</th>
                            <th class="px-4 py-3">Activity description</th>
                            <th class="px-4 py-3">PIC Assignment</th>
                            <th class="px-4 py-3">Special Instructions</th>
                          </tr>
                        </thead>
                        <tbody class="divide-y divide-panel-theme">
                          <tr v-if="sched.rundown?.length === 0">
                            <td colspan="4" class="px-4 py-8 text-center text-muted-theme font-semibold italic">Tidak ada rundown yang tercatat</td>
                          </tr>
                          <tr v-for="(item, idx) in sched.rundown" :key="idx" class="app-table-row">
                            <td class="px-4 py-3 font-bold text-brand-orange">{{ item.time }}</td>
                            <td class="px-4 py-3 text-main-theme font-bold">{{ item.activity }}</td>
                            <td class="px-4 py-3 text-soft-theme font-semibold">{{ item.pic }}</td>
                            <td class="px-4 py-3 text-muted-theme">{{ item.notes || '-' }}</td>
                          </tr>
                        </tbody>
                      </table>
                    </div>

                    <!-- Mobile Rundown Card List (Hidden on desktop/tablet) -->
                    <div class="block md:hidden space-y-3">
                      <div v-if="sched.rundown?.length === 0" class="p-8 text-center bg-surface-theme border border-dashed border-panel-theme rounded-2xl text-muted-theme font-semibold italic">
                        Tidak ada rundown yang tercatat
                      </div>
                      <div 
                        v-for="(item, idx) in sched.rundown" 
                        :key="idx"
                        class="bg-surface-theme border border-panel-theme p-3.5 rounded-xl space-y-2 text-xs"
                      >
                        <div class="flex items-center justify-between border-b border-panel-theme pb-1.5">
                          <span class="font-bold text-brand-orange font-mono">{{ item.time }}</span>
                          <span class="text-muted-theme font-bold">PIC: {{ item.pic }}</span>
                        </div>
                        <div>
                          <p class="font-bold text-main-theme leading-tight">{{ item.activity }}</p>
                          <p v-if="item.notes" class="text-xs text-muted-theme mt-1 font-medium"><span class="text-muted-theme font-bold">Notes:</span> {{ item.notes }}</p>
                        </div>
                      </div>
                    </div>

                    <!-- Quick Rundown Addition Form -->
                    <form 
                      v-if="auth.hasPermission('events:write')"
                      @submit.prevent="addRundownItem(sched)"
                      class="mt-4 grid grid-cols-1 sm:grid-cols-4 gap-3 bg-surface-theme p-3.5 rounded-xl border border-panel-theme"
                    >
                      <input v-model="newRundown.time" type="text" placeholder="e.g. 08:00" required class="w-full app-form-control-compact text-xs" />
                      <input v-model="newRundown.activity" type="text" placeholder="Activity" required class="w-full app-form-control-compact text-xs" />
                      <input v-model="newRundown.pic" type="text" placeholder="Assignee (PIC)" required class="w-full app-form-control-compact text-xs" />
                      <div class="flex gap-2">
                        <input v-model="newRundown.notes" type="text" placeholder="Notes/Remarks" class="flex-1 app-form-control-compact text-xs" />
                        <button type="submit" class="px-4 py-2 bg-brand-emerald text-white rounded-lg font-bold text-xs shrink-0 hover:bg-brand-emerald-dark transition-all">+</button>
                      </div>
                    </form>
                  </div>
                </div>
              </div>
            </div>

            <!-- TAB 2: TASKS CHECKLIST -->
            <div v-if="activeTab === 'tasks'" class="space-y-6">
              <div class="flex items-center justify-between gap-4 select-none">
                <h3 class="text-sm font-extrabold uppercase tracking-wider text-main-theme">Operations Task Checklist</h3>
                <button 
                  v-if="auth.hasPermission('tasks:write')"
                  @click="showAddTaskModal = true"
                  class="px-3.5 py-2 rounded-xl bg-brand-orange text-white font-bold text-xs shadow hover:bg-brand-orange-dark transition-all"
                >
                  + Create New Task
                </button>
              </div>

              <AppEmptyState
                v-if="tasks.length === 0"
                title="Belum Ada Data"
                message="Belum ada checklist operasi yang terdaftar."
              >
                <template #actions v-if="auth.hasPermission('tasks:write')">
                  <button 
                    @click="showAddTaskModal = true"
                    class="px-4 py-2 bg-brand-orange text-white rounded-lg font-bold text-xs hover:bg-brand-orange-dark transition-all"
                  >
                    + Create New Task
                  </button>
                </template>
              </AppEmptyState>

              <!-- Task Checklist Grid -->
              <div v-else class="space-y-3">
                <div 
                  v-for="task in tasks" 
                  :key="task.id"
                  class="p-4 bg-panel-theme border rounded-2xl flex items-center justify-between gap-4 flex-wrap transition-all duration-300"
                  :class="task.status === 'done' ? 'border-brand-emerald/20 opacity-70' : isTaskOverdue(task) ? 'border-red-500/35 bg-red-500/5' : 'border-panel-theme hover:border-brand-orange/30'"
                >
                  <div class="flex items-center gap-3.5 min-w-0 flex-1">
                    <!-- Quick check checkbox -->
                    <input 
                      v-if="auth.hasPermission('tasks:write')"
                      type="checkbox"
                      :checked="task.status === 'done'"
                      @change="toggleTaskDone(task)"
                      class="h-5 w-5 rounded-lg bg-surface-theme border-panel-theme checked:bg-brand-emerald focus:ring-0 text-brand-emerald shrink-0 cursor-pointer transition-all duration-200"
                    />
                    <div class="min-w-0">
                      <div class="flex items-center gap-2 flex-wrap">
                        <p class="font-extrabold text-sm tracking-wide text-main-theme" :class="{ 'line-through !text-muted-theme font-medium': task.status === 'done' }">
                          {{ task.title }}
                        </p>
                        
                        <!-- Status Badges -->
                        <span 
                          v-if="task.status === 'done'" 
                          class="px-2 py-0.5 rounded-full text-[9px] font-black uppercase tracking-wider bg-brand-emerald/15 text-brand-emerald border border-brand-emerald/20"
                        >
                          Siap
                        </span>
                        <span 
                          v-else-if="isTaskOverdue(task)" 
                          class="px-2 py-0.5 rounded-full text-[9px] font-black uppercase tracking-wider bg-red-500/15 text-red-400 border border-red-500/20 animate-pulse"
                        >
                          Perlu Dicek
                        </span>
                        <span 
                          v-else 
                          class="px-2 py-0.5 rounded-full text-[9px] font-black uppercase tracking-wider bg-brand-orange/15 text-brand-orange border border-brand-orange/20"
                        >
                          Belum Lengkap
                        </span>
                      </div>
                      <p class="text-xs text-muted-theme mt-1.5 font-semibold">
                        Due: <span :class="isTaskOverdue(task) ? 'text-red-400 font-extrabold' : 'text-soft-theme'">{{ formatDateTime(task.due_date) }}</span>
                        | PIC: <span class="text-soft-theme font-bold">{{ task.assigned_to?.full_name || 'Unassigned' }}</span>
                      </p>
                    </div>
                  </div>

                  <!-- Priority & Status badges -->
                  <div class="flex items-center gap-3.5 select-none shrink-0 font-sans">
                    <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider" :class="getPriorityStyles(task.priority)">
                      {{ task.priority }} Priority
                    </span>
                    <button 
                      v-if="auth.hasPermission('tasks:write')"
                      @click="deleteTask(task.id)"
                      class="text-red-400 hover:text-red-500 text-xs font-bold transition-colors select-none"
                    >
                      Delete
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- TAB 3: DOCUMENT ARCHIVES -->
            <div v-if="activeTab === 'documents'">
              <ProjectDocumentsPanel :documents="documents" @save-doc="saveDocLink" @delete-doc="deleteDoc" />
            </div>

            <!-- TAB 4: PROJECT INSTRUMENTS -->
            <div v-if="activeTab === 'instruments'">
              <ProjectInstrumentsPanel 
                :instruments="instruments" 
                @generate-defaults="generateDefaultInstruments"
                @create-instrument="createInstrument"
                @update-instrument="updateInstrument"
                @delete-instrument="deleteInstrument"
              />
            </div>

            <!-- TAB 5: STATUS TIMELINE -->
            <div v-if="activeTab === 'timeline'">
              <ProjectStatusTimeline :logs="logs" />
            </div>

            <!-- TAB 6: ACTIVITY LOG -->
            <div v-if="activeTab === 'activity'">
              <ProjectActivityLog :activity-logs="activityLogs" />
            </div>

          </div>

        </div>

        <!-- Right Side: Sidebar Cards for Customer, Assignments, Event Source, Financial Summary -->
        <div class="space-y-6">
          
          <!-- Assignments panel -->
          <div id="assignments-panel" class="glass-panel p-5 space-y-4 select-none transition-all duration-300 scroll-mt-24">
            <h4 class="text-xs font-bold text-main-theme uppercase tracking-wider border-b border-panel-theme pb-2">Operational Assignments</h4>
            <div class="space-y-3 text-xs">
              <div class="flex justify-between items-center bg-surface-theme p-2.5 rounded-xl border border-panel-theme">
                <div>
                  <p class="text-muted-theme font-bold uppercase tracking-widest text-[9px]">Program Owner (PO)</p>
                  <p class="text-main-theme font-extrabold mt-1 text-sm">{{ project.program_owner?.full_name || 'Unassigned' }}</p>
                </div>
                <span v-if="project.program_owner?.initial_code" class="px-2 py-1 bg-brand-orange/15 text-brand-orange text-xs font-black rounded border border-brand-orange/20">
                  {{ project.program_owner.initial_code }}
                </span>
              </div>
              <div class="flex justify-between items-center bg-surface-theme p-2.5 rounded-xl border border-panel-theme">
                <div>
                  <p class="text-muted-theme font-bold uppercase tracking-widest text-[9px]">Program Manager (PM)</p>
                  <p class="text-main-theme font-extrabold mt-1 text-sm">{{ project.program_manager?.full_name || 'Unassigned' }}</p>
                </div>
                <span v-if="project.program_manager?.initial_code" class="px-2 py-1 bg-brand-orange/15 text-brand-orange text-xs font-black rounded border border-brand-orange/20">
                  {{ project.program_manager.initial_code }}
                </span>
              </div>
            </div>
          </div>

          <!-- Project Readiness Scorecard (Sprint 7) -->
          <div v-if="project" id="readiness-panel" class="glass-panel p-5 space-y-4 select-none transition-all duration-300 scroll-mt-24">
            <h4 class="text-xs font-bold text-main-theme uppercase tracking-wider border-b border-panel-theme pb-2">Project Readiness Indicator</h4>
            <div class="space-y-3 text-xs">
              <div class="flex justify-between items-center bg-surface-theme p-2.5 rounded-xl border border-panel-theme">
                <div>
                  <p class="text-muted-theme font-bold uppercase tracking-widest text-[9px]">Readiness Score</p>
                  <p class="text-main-theme font-extrabold mt-1 text-sm">
                    {{ (project && project.project_readiness_score !== null && !isNaN(project.project_readiness_score)) ? Math.round(project.project_readiness_score * 100) + '%' : '0%' }}
                  </p>
                </div>
                <span class="px-2 py-1 text-xs font-black rounded border" :class="getReadinessScoreBadgeStyles(project.project_readiness_score)">
                  {{ getReadinessLabel(project.project_readiness_score) }}
                </span>
              </div>
              <div class="grid grid-cols-2 gap-2 text-xs pt-1">
                <div>
                  <p class="text-muted-theme font-bold text-[9px] uppercase tracking-widest">Completion Rate</p>
                  <p class="text-main-theme font-extrabold text-sm">{{ (project && project.instrument_completion_rate !== null && !isNaN(project.instrument_completion_rate)) ? Math.round(project.instrument_completion_rate * 100) + '%' : '0%' }}</p>
                </div>
                <div>
                  <p class="text-muted-theme font-bold text-[9px] uppercase tracking-widest">Done / Required</p>
                  <p class="text-brand-emerald font-black text-sm">{{ project.completed_required_instruments_count }} / {{ project.required_instruments_count }}</p>
                </div>
              </div>
              <div class="w-full bg-surface-theme border border-panel-theme h-2 rounded-full overflow-hidden mt-2">
                <div 
                  class="bg-brand-orange h-full rounded-full transition-all duration-500" 
                  :style="{ width: (project && project.project_readiness_score !== null && !isNaN(project.project_readiness_score)) ? Math.round(project.project_readiness_score * 100) + '%' : '0%' }"
                ></div>
              </div>
              <!-- Alerts inside readiness card -->
              <div class="grid grid-cols-2 gap-2 pt-1 border-t border-panel-theme mt-2 text-[10px]">
                <div class="flex items-center gap-1">
                  <span class="w-2 h-2 rounded-full" :class="project.overdue_instruments_count > 0 ? 'bg-red-400 animate-pulse' : 'bg-gray-600'"></span>
                  <span class="text-muted-theme font-medium">Overdue:</span>
                  <span class="font-extrabold" :class="project.overdue_instruments_count > 0 ? 'text-red-400' : 'text-soft-theme'">{{ project.overdue_instruments_count }}</span>
                </div>
                <div class="flex items-center gap-1">
                  <span class="w-2 h-2 rounded-full" :class="project.revision_required_count > 0 ? 'bg-rose-400 animate-pulse' : 'bg-gray-600'"></span>
                  <span class="text-muted-theme font-medium">Revision:</span>
                  <span class="font-extrabold" :class="project.revision_required_count > 0 ? 'text-rose-400' : 'text-soft-theme'">{{ project.revision_required_count }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Event Execution Control panel (Sprint 8) -->
          <ProjectExecutionControlPanel 
            v-if="project" 
            :project="project" 
            :warnings="validationWarnings"
          />

          <!-- Customer details -->
          <div class="glass-panel p-5 space-y-3 select-none">
            <h4 class="text-xs font-bold text-main-theme uppercase tracking-wider border-b border-panel-theme pb-2">Client Profile</h4>
            <div class="text-xs space-y-2">
              <p class="text-sm font-extrabold text-main-theme">{{ project.customer?.company_name }}</p>
              <p class="text-muted-theme font-semibold">Category: <span class="text-soft-theme">{{ project.customer?.category }}</span></p>
              <p class="text-muted-theme font-semibold">Mailing Address: <span class="text-soft-theme">{{ project.customer?.address || '-' }}</span></p>
            </div>
          </div>

          <!-- Event Source -->
          <div class="glass-panel p-5 space-y-3 select-none">
            <h4 class="text-xs font-bold text-main-theme uppercase tracking-wider border-b border-panel-theme pb-2">Event Source / Referral</h4>
            <div class="text-xs space-y-2">
              <div class="flex justify-between items-center">
                <p class="text-muted-theme font-semibold">Source Type</p>
                <span class="px-2 py-0.5 bg-brand-orange/10 text-brand-orange rounded font-bold uppercase text-[9px]">
                  {{ project.event_source?.source_type || 'Direct' }}
                </span>
              </div>
              <p class="text-muted-theme font-semibold">Partner/Vendor: <span class="text-soft-theme font-bold">{{ project.event_source?.vendor_name || '-' }}</span></p>
              <p class="text-muted-theme font-semibold">External Sales PIC: <span class="text-soft-theme font-bold">{{ project.event_source?.sales_name || '-' }}</span></p>
            </div>
          </div>

          <!-- Collections Progress Card -->
          <div id="collections-panel" class="glass-panel p-5 space-y-3 select-none transition-all duration-300 scroll-mt-24">
            <h4 class="text-xs font-bold text-main-theme uppercase tracking-wider border-b border-panel-theme pb-2">Collections Progress</h4>
            <div class="space-y-3 text-xs">
              <div class="flex justify-between items-center">
                <p class="text-muted-theme font-semibold">Billing Status</p>
                <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider" :class="getPaymentStatusStyles(project.payment_status)">
                  {{ project.payment_status }}
                </span>
              </div>
              <div class="grid grid-cols-2 gap-2 text-xs pt-1">
                <div>
                  <p class="text-muted-theme font-bold text-[9px] uppercase tracking-widest">Total Deal Value</p>
                  <p class="text-main-theme font-extrabold text-sm">{{ formatMoney(project.budget) }}</p>
                </div>
                <div>
                  <p class="text-muted-theme font-bold text-[9px] uppercase tracking-widest">Approved Collected</p>
                  <p class="text-brand-emerald font-black text-sm">{{ formatMoney(project.paid_amount) }}</p>
                </div>
              </div>
              <div class="w-full bg-surface-theme border border-panel-theme h-2 rounded-full overflow-hidden mt-2">
                <div 
                  class="bg-brand-emerald h-full rounded-full transition-all duration-500" 
                  :style="{ width: getPaymentPercent(project.budget, project.paid_amount) + '%' }"
                ></div>
              </div>
            </div>
          </div>

        </div>

      </div>

    </div>

    <!-- Link Venue Schedule Modal -->
    <div v-if="showAddScheduleModal" class="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 select-none">
      <div class="bg-panel-theme border border-panel-theme rounded-3xl w-full max-w-lg shadow-2xl p-6 relative">
        <h3 class="text-base font-bold text-main-theme tracking-wide mb-5">Link Venue Schedule</h3>
        <form @submit.prevent="saveSchedule" class="space-y-4">
          <div>
            <label class="app-label mb-2">Venue/Address Name</label>
            <input v-model="newSched.venue_name" type="text" required placeholder="e.g. Sentul Adventure Park Camp" class="app-form-control" />
          </div>
          <div>
            <label class="app-label mb-2">Full Mailing Address</label>
            <textarea v-model="newSched.address" rows="2" placeholder="Address..." class="app-form-control"></textarea>
          </div>
          <div>
            <label class="app-label mb-2">Google Maps Embed Link URL</label>
            <input v-model="newSched.map_link" type="url" placeholder="https://maps.google.com/..." class="app-form-control" />
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="app-label mb-2">Operational Start Time</label>
              <input v-model="newSched.start_time" type="datetime-local" required class="app-form-control text-xs" />
            </div>
            <div>
              <label class="app-label mb-2">Operational End Time</label>
              <input v-model="newSched.end_time" type="datetime-local" required class="app-form-control text-xs" />
            </div>
          </div>
          <div>
            <label class="app-label mb-2">Assign On-Site PIC Manager</label>
            <select v-model="newSched.pic_id" class="app-form-control text-xs">
              <option :value="null">Unassigned</option>
              <option v-for="u in users" :key="u.id" :value="u.id">{{ u.full_name }}</option>
            </select>
          </div>
          <div class="flex items-center justify-end gap-3 pt-3">
            <button type="button" @click="showAddScheduleModal = false" class="app-button-secondary">Cancel</button>
            <button type="submit" class="px-5 py-2.5 rounded-xl bg-gradient-to-r from-brand-orange to-brand-orange-light text-white font-bold text-xs shadow-lg">Save Schedule</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Create Task Modal -->
    <div v-if="showAddTaskModal" class="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 select-none">
      <div class="bg-panel-theme border border-panel-theme rounded-3xl w-full max-w-lg shadow-2xl p-6 relative">
        <h3 class="text-base font-bold text-main-theme tracking-wide mb-5">Create Operations Task</h3>
        <form @submit.prevent="saveTask" class="space-y-4">
          <div>
            <label class="app-label mb-2">Task Title</label>
            <input v-model="newTask.title" type="text" required placeholder="e.g. Procure sound equipment system" class="app-form-control" />
          </div>
          <div>
            <label class="app-label mb-2">Description / Instructions</label>
            <textarea v-model="newTask.description" rows="2" placeholder="Task requirements..." class="app-form-control"></textarea>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="app-label mb-2">Priority Level</label>
              <select v-model="newTask.priority" class="app-form-control text-xs">
                <option value="low">Low Priority</option>
                <option value="medium">Medium Priority</option>
                <option value="high">High Priority</option>
              </select>
            </div>
            <div>
              <label class="app-label mb-2">Due Date & Time</label>
              <input v-model="newTask.due_date" type="datetime-local" class="app-form-control text-xs" />
            </div>
          </div>
          <div>
            <label class="app-label mb-2">Assign On-Site PIC Manager</label>
            <select v-model="newTask.assigned_to_id" class="app-form-control text-xs">
              <option :value="null">Unassigned</option>
              <option v-for="u in users" :key="u.id" :value="u.id">{{ u.full_name }}</option>
            </select>
          </div>
          <div class="flex items-center justify-end gap-3 pt-3">
            <button type="button" @click="showAddTaskModal = false" class="app-button-secondary">Cancel</button>
            <button type="submit" class="px-5 py-2.5 rounded-xl bg-gradient-to-r from-brand-orange to-brand-orange-light text-white font-bold text-xs shadow-lg">Allocate Task</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Unified Readiness & Status Transition Modal (Sprint 8) -->
    <div v-if="showReadinessModal" class="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 select-none">
      <div class="bg-panel-theme border border-panel-theme rounded-3xl w-full max-w-xl shadow-2xl p-6 relative">
        <h3 class="text-base font-bold text-main-theme tracking-wide mb-2 flex items-center gap-2">
          <span>Ubah Status Project</span>
          <span v-if="pendingTransition.newStatus" class="px-2 py-0.5 text-[10px] bg-brand-orange/15 text-brand-orange border border-brand-orange/20 rounded font-black">
            {{ pendingTransition.newStatus }}
          </span>
        </h3>
        <p class="text-xs text-muted-theme font-semibold mb-5">
          Sistem sedang menganalisis tingkat kesiapan (readiness) operasional event Anda.
        </p>

        <!-- Loading state -->
        <div v-if="readinessCheckLoading" class="py-12 flex flex-col items-center justify-center gap-3">
          <svg class="animate-spin h-6 w-6 text-brand-orange" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span class="text-xs text-muted-theme font-semibold">Menganalisis checklist readiness...</span>
        </div>

        <!-- Loaded Check state -->
        <div v-else-if="readinessGateData" class="space-y-4">
          <!-- Readiness Scores -->
          <div class="grid grid-cols-2 gap-3 p-3 bg-surface-theme border border-panel-theme rounded-2xl text-xs select-none">
            <div>
              <p class="text-muted-theme font-bold text-[9px] uppercase tracking-widest">Readiness Score</p>
              <p class="text-main-theme font-extrabold text-sm mt-0.5">{{ Math.round(readinessGateData.readiness_score) }}%</p>
            </div>
            <div>
              <p class="text-muted-theme font-bold text-[9px] uppercase tracking-widest">Completion Rate</p>
              <p class="text-brand-emerald font-black text-sm mt-0.5">{{ Math.round(readinessGateData.instrument_completion_rate) }}%</p>
            </div>
          </div>

          <!-- Severity indicator callout -->
          <div v-if="readinessGateData.severity === 'critical'" class="p-3 bg-red-500/10 border border-red-500/20 text-red-200 rounded-xl text-[11px] font-semibold leading-relaxed flex items-start gap-2">
            <span>❌</span>
            <div>
              <p class="font-extrabold text-red-400 uppercase tracking-wider text-[9px]">Critical Blockers Detected</p>
              <p class="mt-0.5 text-red-300/90">Sistem mendeteksi blocker kritis yang berisiko merusak alur kerja. Silakan periksa rekomendasi di bawah.</p>
            </div>
          </div>
          <div v-else-if="readinessGateData.warnings.length > 0" class="p-3 bg-amber-500/10 border border-amber-500/20 text-amber-200 rounded-xl text-[11px] font-semibold leading-relaxed flex items-start gap-2">
            <span>⚠️</span>
            <div>
              <p class="font-extrabold text-amber-400 uppercase tracking-wider text-[9px]">Operational Warnings Detected</p>
              <p class="mt-0.5 text-amber-300/90">Sistem mendeteksi beberapa catatan kesiapan. Anda dapat mengabaikan ini namun pastikan untuk melengkapinya segera.</p>
            </div>
          </div>
          <div v-else class="p-3 bg-brand-emerald/10 border border-brand-emerald/20 text-brand-emerald rounded-xl text-[11px] font-semibold leading-relaxed flex items-start gap-2">
            <span>✅</span>
            <div>
              <p class="font-extrabold text-brand-emerald uppercase tracking-wider text-[9px]">Ready for Transition</p>
              <p class="mt-0.5">Project ini sepenuhnya siap untuk transisi status ini tanpa catatan apapun.</p>
            </div>
          </div>

          <!-- Blockers List -->
          <div v-if="readinessGateData.blockers.length > 0" class="space-y-1.5">
            <p class="text-[9px] font-extrabold uppercase tracking-widest text-red-400">Blocker Kritis (Blockers)</p>
            <div class="p-3 bg-red-950/20 border border-red-900/30 rounded-xl space-y-1 text-xs text-red-300 font-semibold leading-relaxed max-h-32 overflow-y-auto custom-scrollbar">
              <p v-for="(b, idx) in readinessGateData.blockers" :key="idx" class="flex gap-1.5 items-start">
                <span class="text-red-400 shrink-0">•</span>
                <span>{{ b }}</span>
              </p>
            </div>
          </div>

          <!-- Warnings List -->
          <div v-if="readinessGateData.warnings.length > 0" class="space-y-1.5">
            <p class="text-[9px] font-extrabold uppercase tracking-widest text-amber-400">Peringatan Operasional (Warnings)</p>
            <div class="p-3 bg-amber-950/10 border border-amber-900/20 rounded-xl space-y-1 text-xs text-amber-300 font-semibold leading-relaxed max-h-32 overflow-y-auto custom-scrollbar">
              <p v-for="(w, idx) in readinessGateData.warnings" :key="idx" class="flex gap-1.5 items-start">
                <span class="text-amber-400 shrink-0">•</span>
                <span>{{ w }}</span>
              </p>
            </div>
          </div>

          <!-- Recommendations -->
          <div v-if="readinessGateData.recommendations.length > 0" class="space-y-1.5">
            <p class="text-[9px] font-extrabold uppercase tracking-widest text-brand-blue">Rekomendasi Tindakan (Recommendations)</p>
            <div class="p-3 bg-blue-950/10 border border-blue-900/20 rounded-xl space-y-1 text-xs text-blue-200 font-semibold leading-relaxed max-h-32 overflow-y-auto custom-scrollbar">
              <p v-for="(r, idx) in readinessGateData.recommendations" :key="idx" class="flex gap-1.5 items-start">
                <span class="text-brand-blue shrink-0">•</span>
                <span>{{ r }}</span>
              </p>
            </div>
          </div>

          <!-- Notes textarea -->
          <div>
            <label class="app-label mb-2">Catatan Perubahan Status (Wajib)</label>
            <textarea v-model="transitionNotes" rows="2.5" placeholder="Masukkan alasan transisi atau tindakan mitigasi..." class="app-form-control"></textarea>
          </div>

          <!-- Override switch if critical blockers -->
          <div v-if="readinessGateData.severity === 'critical'" class="flex items-center gap-2 p-3 bg-red-950/10 border border-red-900/20 rounded-xl select-none">
            <input 
              id="force-override" 
              type="checkbox" 
              v-model="forceTransition"
              class="rounded border-red-900 bg-surface-theme text-red-500 focus:ring-red-500 h-4.5 w-4.5 cursor-pointer"
            />
            <label for="force-override" class="text-xs font-bold text-red-300 cursor-pointer select-none">
              Saya memahami risiko kritis di atas dan setuju untuk melakukan Force Update status.
            </label>
          </div>

          <!-- Action buttons -->
          <div class="flex items-center justify-end gap-3 pt-2">
            <button type="button" @click="showReadinessModal = false" class="app-button-secondary">Cancel</button>
            <button 
              type="button" 
              @click="confirmTransition"
              :disabled="readinessGateData.severity === 'critical' && !forceTransition"
              class="px-5 py-2.5 rounded-xl text-white font-bold text-xs shadow-lg transition-all"
              :class="(readinessGateData.severity === 'critical' && !forceTransition) ? 'bg-gray-700/50 text-gray-500 border border-gray-600/30 cursor-not-allowed' : 'bg-gradient-to-r from-brand-orange to-brand-orange-light hover:brightness-110'"
            >
              Ubah Status Project
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '../store/auth'
import { useUiStore } from '../store/ui'
import ProjectDetailHeader from '../components/ProjectDetailHeader.vue'
import ProjectValidationWarnings from '../components/ProjectValidationWarnings.vue'
import ProjectStatusTimeline from '../components/ProjectStatusTimeline.vue'
import ProjectActivityLog from '../components/ProjectActivityLog.vue'
import ProjectDocumentsPanel from '../components/ProjectDocumentsPanel.vue'
import ProjectInstrumentsPanel from '../components/ProjectInstrumentsPanel.vue'
import ProjectExecutionControlPanel from '../components/projects/ProjectExecutionControlPanel.vue'
import AppEmptyState from '../components/ui/AppEmptyState.vue'

const auth = useAuthStore()
const ui = useUiStore()
const route = useRoute()
const projectId = route.params.id

const getApiErrorMessage = (err, fallback) => {
  const detail = err.response?.data?.detail
  if (typeof detail === 'string') return detail
  if (detail?.message && typeof detail.message === 'string') return detail.message
  return fallback
}

const project = ref(null)
const schedules = ref([])
const tasks = ref([])
const documents = ref([])
const logs = ref([])
const activityLogs = ref([])
const validationWarnings = ref([])
const users = ref([])
const instruments = ref([])

const showReadinessModal = ref(false)
const readinessCheckLoading = ref(false)
const readinessGateData = ref(null)
const transitionNotes = ref('')
const forceTransition = ref(false)
const pendingTransition = ref({ statusType: '', newStatus: '' })

const loading = ref(true)
const activeTab = ref('schedules')

const showAddScheduleModal = ref(false)
const showAddTaskModal = ref(false)

const tabs = [
  { id: 'schedules', name: 'Event Timeline' },
  { id: 'tasks', name: 'Checklist Operations' },
  { id: 'instruments', name: 'Project Instruments' },
  { id: 'documents', name: 'Shared Documents' },
  { id: 'timeline', name: 'Status Timeline' },
  { id: 'activity', name: 'Activity Log' }
]

const daysRemaining = computed(() => {
  if (!project.value?.event_date_start) return null
  const start = new Date(project.value.event_date_start)
  if (isNaN(start.getTime())) return null
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  start.setHours(0, 0, 0, 0)
  const diff = start.getTime() - today.getTime()
  return Math.ceil(diff / (1000 * 60 * 60 * 24))
})

const nextActionInfo = computed(() => {
  if (!project.value) return { text: 'Loading...', color: 'text-muted-theme', tone: 'neutral', ctas: [] }

  // 1. Check PO/PM assignment
  if (!project.value.program_manager?.id || !project.value.program_owner?.id) {
    return {
      text: 'Lengkapi PO/PM assignment',
      description: 'Program Owner (PO) dan Program Manager (PM) harus ditunjuk untuk memimpin koordinasi operasional.',
      color: 'text-brand-orange border-brand-orange/25 bg-brand-orange/5',
      tone: 'warning',
      ctas: [
        { label: 'Lengkapi Assignment', actionType: 'scroll', target: 'assignments-panel' }
      ]
    }
  }

  // 2. Check document/instrument completion
  const completionRate = project.value.instrument_completion_rate || 0
  const reqCount = project.value.required_instruments_count || 0
  const compCount = project.value.completed_required_instruments_count || 0
  if (compCount < reqCount || completionRate < 1) {
    return {
      text: 'Lengkapi dokumen/instrument project',
      description: 'Masih ada instrumen project atau dokumen operasional yang wajib dilengkapi.',
      color: 'text-brand-orange border-brand-orange/25 bg-brand-orange/5',
      tone: 'warning',
      ctas: [
        { label: 'Cek Instrument', actionType: 'tab', target: 'instruments' },
        { label: 'Cek Dokumen', actionType: 'tab', target: 'documents' }
      ]
    }
  }

  // 3. Check outstanding payments
  const payStatus = project.value.payment_status
  if (payStatus === 'Outstanding' || payStatus === 'Overdue' || payStatus === 'Not Invoiced') {
    return {
      text: 'Follow-up outstanding payment',
      description: 'Periksa tagihan invoice outstanding atau status overdue untuk menjaga kelancaran cashflow proyek.',
      color: 'text-red-400 border-red-500/25 bg-red-500/5',
      tone: 'danger',
      ctas: [
        { label: 'Cek Pembayaran', actionType: 'scroll', target: 'collections-panel' }
      ]
    }
  }

  // 4. Check readiness before event
  const readiness = project.value.project_readiness_score || 0
  if (readiness < 1) {
    return {
      text: 'Review readiness sebelum event',
      description: 'Lakukan review checklist operasional dan pastikan semua warning diselesaikan sebelum hari pelaksanaan.',
      color: 'text-brand-blue border-brand-blue/25 bg-brand-blue/5',
      tone: 'info',
      ctas: [
        { label: 'Review Readiness', actionType: 'scroll', target: 'readiness-panel' }
      ]
    }
  }

  // 5. Check running or completed program status
  const progStatus = project.value.program_status
  if (progStatus === 'Confirmed' || progStatus === 'Preparation' || progStatus === 'Ready') {
    return {
      text: 'Project siap dieksekusi',
      description: 'Seluruh gate operasional, penunjukan PIC, dan checklist kesiapan telah lengkap. Project siap dijalankan.',
      color: 'text-brand-emerald border-brand-emerald/25 bg-brand-emerald/5',
      tone: 'success',
      ctas: [
        { label: 'Buka Rundown', actionType: 'tab', target: 'schedules' }
      ]
    }
  }

  if (progStatus === 'Running' || progStatus === 'Completed') {
    return {
      text: 'Review execution dan lengkapi rundown',
      description: 'Event sedang berlangsung atau telah selesai dilaksanakan. Selesaikan laporan penutupan.',
      color: 'text-brand-emerald border-brand-emerald/25 bg-brand-emerald/5',
      tone: 'success',
      ctas: [
        { label: 'Buka Rundown', actionType: 'tab', target: 'schedules' }
      ]
    }
  }

  if (progStatus === 'Reporting' || progStatus === 'Closed') {
    return {
      text: 'Project sudah reporting/closing',
      description: 'Proyek ini berada dalam tahap pelaporan akhir atau telah diarsipkan secara formal.',
      color: 'text-muted-theme border-panel-theme bg-surface-theme',
      tone: 'neutral',
      ctas: [
        { label: 'Buka Rundown', actionType: 'tab', target: 'schedules' }
      ]
    }
  }

  return {
    text: 'Review status operasional',
    description: 'Silakan periksa detail timeline dan instrumen project untuk langkah kerja selanjutnya.',
    color: 'text-muted-theme border-panel-theme bg-surface-theme',
    tone: 'neutral',
    ctas: [
      { label: 'Buka Rundown', actionType: 'tab', target: 'schedules' }
    ]
  }
})

const getCtaButtonClasses = (tone) => {
  if (tone === 'warning') return 'bg-brand-orange/10 hover:bg-brand-orange/20 text-brand-orange border-brand-orange/30'
  if (tone === 'danger') return 'bg-red-500/10 hover:bg-red-500/20 text-red-400 border-red-500/30'
  if (tone === 'info') return 'bg-brand-blue/10 hover:bg-brand-blue/20 text-brand-blue border-brand-blue/30 font-semibold'
  if (tone === 'success') return 'bg-brand-emerald/10 hover:bg-brand-emerald/20 text-brand-emerald border-brand-emerald/30'
  return 'bg-surface-theme hover:bg-panel-theme text-soft-theme border-panel-theme'
}

const handleCtaClick = (cta) => {
  if (cta.actionType === 'tab') {
    activeTab.value = cta.target
    const tabEl = document.getElementById('tabs-navigation')
    if (tabEl) {
      tabEl.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }
  } else if (cta.actionType === 'scroll') {
    const el = document.getElementById(cta.target)
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'center' })
      el.classList.add('ring-2', 'ring-brand-orange', 'ring-offset-2', 'ring-offset-background')
      setTimeout(() => {
        el.classList.remove('ring-2', 'ring-brand-orange', 'ring-offset-2', 'ring-offset-background')
      }, 2000)
    }
  }
}

const newRundown = ref({ time: '', activity: '', pic: '', notes: '' })

const newSched = ref({
  venue_name: '',
  address: '',
  map_link: '',
  start_time: '',
  end_time: '',
  pic_id: null,
  rundown: []
})

const newTask = ref({
  title: '',
  description: '',
  priority: 'medium',
  due_date: '',
  assigned_to_id: null,
  status: 'todo'
})

const getPaymentPercent = (budget, paid) => {
  const b = parseFloat(budget) || 0
  const p = parseFloat(paid) || 0
  if (b <= 0) return 0
  return Math.min(100, Math.round((p / b) * 100))
}

const fetchProjectDetail = async () => {
  try {
    const res = await axios.get(`/api/v1/projects/${projectId}`)
    project.value = res.data
    validationWarnings.value = res.data.validation_warnings || []
    activityLogs.value = res.data.activity_logs || []
  } catch (err) {
    console.error('Failed to refresh project details', err)
  }
}

const fetchInstruments = async () => {
  try {
    const res = await axios.get(`/api/v1/projects/${projectId}/instruments`)
    instruments.value = res.data
  } catch (err) {
    console.error('Failed to load project instruments', err)
  }
}

const fetchData = async () => {
  try {
    const [projRes, schedsRes, tasksRes, docsRes, logsRes, usersRes, instsRes] = await Promise.all([
      axios.get(`/api/v1/projects/${projectId}`),
      axios.get(`/api/v1/projects/${projectId}/events`),
      axios.get(`/api/v1/projects/${projectId}/tasks`),
      axios.get(`/api/v1/projects/${projectId}/documents`),
      axios.get(`/api/v1/projects/${projectId}/logs`),
      axios.get('/api/v1/auth/users/options'),
      axios.get(`/api/v1/projects/${projectId}/instruments`)
    ])
    
    project.value = projRes.data
    schedules.value = schedsRes.data
    tasks.value = tasksRes.data
    documents.value = docsRes.data
    logs.value = logsRes.data
    users.value = usersRes.data
    instruments.value = instsRes.data
    
    validationWarnings.value = projRes.data.validation_warnings || []
    activityLogs.value = projRes.data.activity_logs || []
  } catch (err) {
    console.error('Failed to load project detailed context', err)
  } finally {
    loading.value = false
  }
}

const generateDefaultInstruments = async () => {
  try {
    await axios.post(`/api/v1/projects/${projectId}/instruments/defaults`)
    await Promise.all([
      fetchInstruments(),
      fetchProjectDetail()
    ])
  } catch (err) {
    ui.error(getApiErrorMessage(err, 'Gagal membuat default instrumen operasional.'))
  }
}

const createInstrument = async (payload) => {
  try {
    await axios.post(`/api/v1/projects/${projectId}/instruments`, payload)
    await Promise.all([
      fetchInstruments(),
      fetchProjectDetail()
    ])
  } catch (err) {
    ui.error(getApiErrorMessage(err, 'Gagal membuat instrumen operasional.'))
  }
}

const updateInstrument = async ({ id, data }) => {
  try {
    await axios.patch(`/api/v1/projects/${projectId}/instruments/${id}`, data)
    await Promise.all([
      fetchInstruments(),
      fetchProjectDetail()
    ])
  } catch (err) {
    ui.error(getApiErrorMessage(err, 'Gagal memperbarui instrumen operasional.'))
  }
}

const deleteInstrument = async (id) => {
  try {
    await axios.delete(`/api/v1/projects/${projectId}/instruments/${id}`)
    await Promise.all([
      fetchInstruments(),
      fetchProjectDetail()
    ])
  } catch (err) {
    ui.error(getApiErrorMessage(err, 'Gagal menghapus instrumen operasional.'))
  }
}

onMounted(() => {
  fetchData()
})

const formatMoney = (val) => {
  return 'Rp ' + Number(val || 0).toLocaleString('id-ID', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  })
}

const formatDateTime = (val) => {
  if (!val) return '-'
  return new Date(val).toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getPriorityStyles = (priority) => {
  if (priority === 'high') return 'bg-red-500/10 text-red-400'
  if (priority === 'medium') return 'bg-brand-orange/10 text-brand-orange'
  return 'bg-surface-theme text-muted-theme'
}



const getPaymentStatusStyles = (status) => {
  if (status === 'Paid') return 'bg-brand-emerald/10 text-brand-emerald border border-brand-emerald/20'
  if (status === 'Partial Paid') return 'bg-brand-blue/10 text-brand-blue border border-brand-blue/20'
  if (status === 'Outstanding' || status === 'Overdue') return 'bg-red-500/10 text-red-400 border border-red-500/20'
  return 'bg-surface-theme text-muted-theme border border-panel-theme'
}

// Transition Status Action
const transitionStatus = async (statusType, newStatus) => {
  if (!auth.hasPermission('projects:write')) return

  pendingTransition.value = { statusType, newStatus }
  transitionNotes.value = ''
  forceTransition.value = false
  readinessGateData.value = null
  showReadinessModal.value = true
  readinessCheckLoading.value = true
  
  try {
    const res = await axios.post(`/api/v1/projects/${projectId}/readiness/check`, {
      status_type: statusType,
      target_status: newStatus
    })
    readinessGateData.value = res.data
  } catch (err) {
    console.error('Failed to run readiness gate check', err)
    ui.error(getApiErrorMessage(err, 'Gagal menjalankan analisis readiness check.'))
    showReadinessModal.value = false
  } finally {
    readinessCheckLoading.value = false
  }
}

const confirmTransition = async () => {
  const { statusType, newStatus } = pendingTransition.value
  
  if (!transitionNotes.value.trim()) {
    ui.warning('Catatan perubahan status wajib diisi.')
    return
  }
  
  try {
    await axios.patch(`/api/v1/projects/${projectId}/status`, {
      status_type: statusType,
      new_status: newStatus,
      notes: transitionNotes.value,
      force: forceTransition.value
    })
    
    showReadinessModal.value = false
    await fetchProjectDetail()
    
    // Refresh logs
    const logsRes = await axios.get(`/api/v1/projects/${projectId}/logs`)
    logs.value = logsRes.data
    ui.success('Status workflow project berhasil diubah.')
  } catch (err) {
    ui.error(getApiErrorMessage(err, 'Gagal mengubah status project.'))
  }
}

// Actions
const saveSchedule = async () => {
  try {
    const payload = {
      ...newSched.value,
      project_id: projectId
    }
    const response = await axios.post('/api/v1/events', payload)
    
    // Add rel attributes
    const pm = users.value.find(u => u.id === response.data.pic_id)
    response.data.pic = pm
    
    schedules.value.push(response.data)
    showAddScheduleModal.value = false
    newSched.value = { venue_name: '', address: '', map_link: '', start_time: '', end_time: '', pic_id: null, rundown: [] }
    await fetchProjectDetail()
  } catch {
    ui.error('Gagal menyimpan jadwal venue.')
  }
}

const addRundownItem = async (sched) => {
  try {
    const updatedRundown = [...sched.rundown, { ...newRundown.value }]
    const response = await axios.put(`/api/v1/events/${sched.id}`, { rundown: updatedRundown })
    sched.rundown = response.data.rundown
    newRundown.value = { time: '', activity: '', pic: '', notes: '' }
    await fetchProjectDetail()
  } catch {
    ui.error('Gagal menyimpan item ROS.')
  }
}

const saveTask = async () => {
  try {
    const payload = {
      ...newTask.value,
      project_id: projectId
    }
    if (!payload.due_date) delete payload.due_date
    
    const response = await axios.post('/api/v1/tasks', payload)
    
    const pm = users.value.find(u => u.id === response.data.assigned_to_id)
    response.data.assigned_to = pm
    response.data.created_by = auth.user
    
    tasks.value.push(response.data)
    showAddTaskModal.value = false
    newTask.value = { title: '', description: '', priority: 'medium', due_date: '', assigned_to_id: null, status: 'todo' }
    await fetchProjectDetail()
  } catch {
    ui.error('Gagal menyimpan CK operasional.')
  }
}

const toggleTaskDone = async (task) => {
  try {
    const newStatus = task.status === 'done' ? 'todo' : 'done'
    const response = await axios.put(`/api/v1/tasks/${task.id}`, { status: newStatus })
    task.status = response.data.status
    await fetchProjectDetail()
  } catch {
    ui.error('Gagal memperbarui status CK.')
  }
}

const deleteTask = async (id) => {
  const confirmed = await ui.confirm ({
    title: 'Hapus CK Ini?',
    message: 'Item CK operasional akan dihapus dari project.',
    confirmText: 'Hapus',
    cancelText: 'Batal',
    tone: 'danger'
  })
  if (!confirmed) return
  try {
    await axios.delete(`/api/v1/tasks/${id}`)
    tasks.value = tasks.value.filter(t => t.id !== id)
    await fetchProjectDetail()
  } catch {
    ui.error('Gagal menghapus CK.')
  }
}

const saveDocLink = async (docData) => {
  try {
    const payload = {
      ...docData,
      project_id: projectId
    }
    const response = await axios.post('/api/v1/documents', payload)
    response.data.uploaded_by = auth.user
    
    documents.value.push(response.data)
    await fetchProjectDetail()
  } catch {
    ui.error('Gagal menautkan referensi dokumen cloud.')
  }
}

const deleteDoc = async (id) => {
  const confirmed = await ui.confirm ({
    title: 'Hapus Referensi Dokumen Ini?',
    message: 'Link dokumen cloud akan dihapus dari ledger project.',
    confirmText: 'Hapus',
    cancelText: 'Batal',
    tone: 'danger'
  })
  if (!confirmed) return
  try {
    await axios.delete(`/api/v1/documents/${id}`)
    documents.value = documents.value.filter(d => d.id !== id)
    await fetchProjectDetail()
  } catch {
    ui.error('Gagal menghapus referensi dokumen.')
  }
}

const getReadinessScoreBadgeStyles = (score) => {
  if (score === null || score === undefined) return 'bg-gray-500/10 text-gray-400 border-gray-500/20'
  if (score >= 0.8) return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
  if (score >= 0.5) return 'bg-amber-500/10 text-amber-400 border-amber-500/20'
  return 'bg-rose-500/10 text-rose-400 border-rose-500/20'
}

const getReadinessLabel = (score) => {
  if (score === null || score === undefined) return 'UNKNOWN'
  if (score >= 0.8) return 'READY'
  if (score >= 0.5) return 'PREPARING'
  return 'NOT READY'
}

const isApproachingEvent = (startTime) => {
  if (!startTime) return false
  const start = new Date(startTime)
  if (isNaN(start.getTime())) return false
  const today = new Date()
  const diffTime = start.getTime() - today.getTime()
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  return diffDays >= 0 && diffDays <= 7
}

const isTaskOverdue = (task) => {
  if (!task.due_date || task.status === 'done') return false
  const today = new Date()
  const due = new Date(task.due_date)
  return due < today
}
</script>
