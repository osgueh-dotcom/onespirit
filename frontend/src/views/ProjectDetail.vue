<template>
  <div class="space-y-6">
    <ProjectDetailHeader v-if="project" :project="project" @transition="transitionStatus" />

    <!-- Loading Indicators -->
    <div v-if="loading" class="h-64 flex flex-col items-center justify-center gap-3">
      <svg class="animate-spin h-6 w-6 text-brand-orange" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
      <span class="text-xs text-gray-400 font-semibold">Loading operational ledger...</span>
    </div>

    <div v-else class="space-y-6">
      <ProjectValidationWarnings :warnings="validationWarnings" />

      <!-- Main Operational Dashboard Layout Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        <!-- Left Side: Event Details & Action ledger tabs -->
        <div class="lg:col-span-2 space-y-6">
          
          <!-- Parameters cards -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 select-none">
            <!-- Event parameters -->
            <div class="glass-panel p-5 space-y-3">
              <h4 class="text-xs font-bold text-white uppercase tracking-wider border-b border-brand-charcoal-light/20 pb-2">Event Parameters</h4>
              <div class="grid grid-cols-2 gap-3 text-xs">
                <div>
                  <p class="text-gray-400 font-semibold">Category</p>
                  <p class="text-white font-bold mt-0.5">{{ project.event_category || '-' }}</p>
                </div>
                <div>
                  <p class="text-gray-400 font-semibold">Program Type</p>
                  <p class="text-white font-bold mt-0.5">{{ project.program_type || '-' }}</p>
                </div>
                <div>
                  <p class="text-gray-400 font-semibold">Program Name</p>
                  <p class="text-white font-bold mt-0.5">{{ project.program_name || '-' }}</p>
                </div>
                <div>
                  <p class="text-gray-400 font-semibold">Quantity (Pax)</p>
                  <p class="text-white font-bold mt-0.5">{{ project.quantity || '-' }}</p>
                </div>
                <div>
                  <p class="text-gray-400 font-semibold">Venue</p>
                  <p class="text-white font-bold mt-0.5">{{ project.venue || '-' }}</p>
                </div>
                <div>
                  <p class="text-gray-400 font-semibold">Duration</p>
                  <p class="text-white font-bold mt-0.5">{{ project.duration || '-' }}</p>
                </div>
              </div>
            </div>

            <!-- Quotation Parameters -->
            <div class="glass-panel p-5 space-y-3">
              <h4 class="text-xs font-bold text-white uppercase tracking-wider border-b border-brand-charcoal-light/20 pb-2">Quotation & Financials</h4>
              <div class="grid grid-cols-2 gap-3 text-xs">
                <div>
                  <p class="text-gray-400 font-semibold">Quote Reference</p>
                  <p class="text-white font-bold mt-0.5">{{ project.quotation_number || '-' }}</p>
                </div>
                <div>
                  <p class="text-gray-400 font-semibold">Quotation Date</p>
                  <p class="text-white font-bold mt-0.5">{{ project.quotation_date || '-' }}</p>
                </div>
                <div>
                  <p class="text-gray-400 font-semibold">Inquiry Date</p>
                  <p class="text-white font-bold mt-0.5">{{ project.inquiry_date || '-' }}</p>
                </div>
                <div>
                  <p class="text-gray-400 font-semibold">Allocated Revenue</p>
                  <p class="text-brand-emerald font-black mt-0.5">{{ formatMoney(project.revenue) }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Notes Card -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 select-none">
            <!-- General Notes & Cancel -->
            <div class="glass-panel p-5 space-y-3">
              <h4 class="text-xs font-bold text-white uppercase tracking-wider border-b border-brand-charcoal-light/20 pb-2">General & Cancel Notes</h4>
              <div class="text-xs space-y-3">
                <div v-if="project.cancel_reason">
                  <p class="text-red-400 font-bold">Cancellation Reason</p>
                  <p class="p-3 bg-red-500/10 border border-red-500/20 rounded-xl text-red-200 mt-1 font-semibold leading-relaxed">
                    {{ project.cancel_reason }}
                  </p>
                </div>
                <div>
                  <p class="text-gray-400 font-semibold">General Remarks</p>
                  <p class="text-gray-200 font-semibold mt-1 whitespace-pre-line leading-relaxed">
                    {{ project.general_notes || 'No general notes recorded.' }}
                  </p>
                </div>
              </div>
            </div>

            <!-- MOM Notes -->
            <div class="glass-panel p-5 space-y-3">
              <h4 class="text-xs font-bold text-white uppercase tracking-wider border-b border-brand-charcoal-light/20 pb-2">Minutes of Meeting (MOM)</h4>
              <div class="text-xs">
                <p class="text-gray-200 font-semibold whitespace-pre-line leading-relaxed">
                  {{ project.mom_notes || 'No meeting minutes logged yet.' }}
                </p>
              </div>
            </div>
          </div>

          <!-- Dynamic ledger action tabs -->
          <div class="space-y-6">
            <!-- Tabs Navigation -->
            <div class="flex border-b border-brand-charcoal-light/20 pb-0.5 select-none gap-4 shrink-0 overflow-x-auto">
              <button 
                v-for="tab in tabs" 
                :key="tab.id"
                @click="activeTab = tab.id"
                class="pb-3 text-xs font-bold uppercase tracking-wider relative transition-colors whitespace-nowrap"
                :class="activeTab === tab.id ? 'text-brand-orange border-b-2 border-brand-orange' : 'text-gray-400 hover:text-white'"
              >
                {{ tab.name }}
              </button>
            </div>

            <!-- TAB 1: EVENT TIMELINE (Rundowns) -->
            <div v-if="activeTab === 'schedules'" class="space-y-6">
              <div class="flex items-center justify-between gap-4 select-none">
                <h3 class="text-sm font-extrabold uppercase tracking-wider text-white">Event Venues & Rundown Sheets</h3>
                <button 
                  v-if="auth.hasPermission('events:write')"
                  @click="showAddScheduleModal = true"
                  class="px-3.5 py-2 rounded-xl bg-brand-orange text-white font-bold text-xs shadow hover:bg-brand-orange-dark transition-all"
                >
                  + Link Venue Schedule
                </button>
              </div>

              <div v-if="schedules.length === 0" class="p-12 text-center border border-dashed border-brand-charcoal-light/25 rounded-3xl text-xs font-semibold text-gray-500 select-none">
                No event schedule venues created. Click Link Venue Schedule to initialize rundowns.
              </div>

              <!-- Venue Schedule Listing Grid -->
              <div v-else class="grid grid-cols-1 gap-6">
                <div 
                  v-for="sched in schedules" 
                  :key="sched.id"
                  class="glass-panel p-6 space-y-4"
                >
                  <!-- Schedule Header -->
                  <div class="flex items-center justify-between flex-wrap gap-3 border-b border-brand-charcoal-light/20 pb-4 select-none">
                    <div>
                      <h4 class="text-base font-extrabold text-white tracking-wide">{{ sched.venue_name }}</h4>
                      <p class="text-xs text-gray-400 mt-1">Location: {{ sched.address || '-' }} | <a :href="sched.map_link" target="_blank" class="text-brand-blue hover:underline">Google Maps</a></p>
                    </div>
                    <div class="text-right text-xs">
                      <p class="font-bold text-gray-300">Time: {{ formatDateTime(sched.start_time) }} to {{ formatDateTime(sched.end_time) }}</p>
                      <p class="text-[10px] text-brand-orange font-bold uppercase mt-1">PIC: {{ sched.pic?.full_name || 'Unassigned' }}</p>
                    </div>
                  </div>

                  <!-- Rundown Table -->
                  <div>
                    <p class="text-[10px] font-extrabold uppercase tracking-widest text-brand-orange mb-3 select-none">Hour-by-Hour Rundown Timesheet</p>
                    <div class="overflow-x-auto rounded-xl border border-brand-charcoal-light/20">
                      <table class="min-w-full text-left text-xs divide-y divide-brand-charcoal-light/10">
                        <thead class="bg-brand-charcoal/50 text-[10px] font-extrabold uppercase tracking-widest text-gray-400 select-none">
                          <tr>
                            <th class="px-4 py-3">Time</th>
                            <th class="px-4 py-3">Activity description</th>
                            <th class="px-4 py-3">PIC Assignment</th>
                            <th class="px-4 py-3">Special Instructions</th>
                          </tr>
                        </thead>
                        <tbody class="divide-y divide-brand-charcoal-light/5">
                          <tr v-if="sched.rundown?.length === 0">
                            <td colspan="4" class="px-4 py-6 text-center text-gray-500 font-semibold italic">No rundown items added.</td>
                          </tr>
                          <tr v-for="(item, idx) in sched.rundown" :key="idx" class="hover:bg-brand-charcoal-light/5">
                            <td class="px-4 py-3 font-bold text-brand-orange">{{ item.time }}</td>
                            <td class="px-4 py-3 text-white font-bold">{{ item.activity }}</td>
                            <td class="px-4 py-3 text-gray-300 font-semibold">{{ item.pic }}</td>
                            <td class="px-4 py-3 text-gray-400">{{ item.notes || '-' }}</td>
                          </tr>
                        </tbody>
                      </table>
                    </div>

                    <!-- Quick Rundown Addition Form -->
                    <form 
                      v-if="auth.hasPermission('events:write')"
                      @submit.prevent="addRundownItem(sched)"
                      class="mt-4 grid grid-cols-4 gap-3 bg-brand-charcoal-light/10 p-3.5 rounded-xl border border-brand-charcoal-light/10"
                    >
                      <input v-model="newRundown.time" type="text" placeholder="e.g. 08:00" required class="px-3 py-2 rounded-lg bg-brand-charcoal-dark border border-brand-charcoal-light/40 text-xs text-white" />
                      <input v-model="newRundown.activity" type="text" placeholder="Activity" required class="px-3 py-2 rounded-lg bg-brand-charcoal-dark border border-brand-charcoal-light/40 text-xs text-white" />
                      <input v-model="newRundown.pic" type="text" placeholder="Assignee (PIC)" required class="px-3 py-2 rounded-lg bg-brand-charcoal-dark border border-brand-charcoal-light/40 text-xs text-white" />
                      <div class="flex gap-2">
                        <input v-model="newRundown.notes" type="text" placeholder="Notes/Remarks" class="flex-1 px-3 py-2 rounded-lg bg-brand-charcoal-dark border border-brand-charcoal-light/40 text-xs text-white" />
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
                <h3 class="text-sm font-extrabold uppercase tracking-wider text-white">Operations Task Checklist</h3>
                <button 
                  v-if="auth.hasPermission('tasks:write')"
                  @click="showAddTaskModal = true"
                  class="px-3.5 py-2 rounded-xl bg-brand-orange text-white font-bold text-xs shadow hover:bg-brand-orange-dark transition-all"
                >
                  + Create New Task
                </button>
              </div>

              <div v-if="tasks.length === 0" class="p-12 text-center border border-dashed border-brand-charcoal-light/25 rounded-3xl text-xs font-semibold text-gray-500 select-none">
                No operations tasks registered. Click Create New Task to add checklists.
              </div>

              <!-- Task Checklist Grid -->
              <div v-else class="space-y-3">
                <div 
                  v-for="task in tasks" 
                  :key="task.id"
                  class="p-4 bg-brand-charcoal border rounded-2xl flex items-center justify-between gap-4 flex-wrap"
                  :class="task.status === 'done' ? 'border-brand-emerald/20 opacity-70' : 'border-brand-charcoal-light/40 hover:border-brand-orange/30 transition-all'"
                >
                  <div class="flex items-center gap-3 min-w-0 flex-1">
                    <!-- Quick check checkbox -->
                    <input 
                      v-if="auth.hasPermission('tasks:write')"
                      type="checkbox"
                      :checked="task.status === 'done'"
                      @change="toggleTaskDone(task)"
                      class="h-4.5 w-4.5 rounded-lg bg-brand-charcoal-dark border-brand-charcoal-light/45 checked:bg-brand-emerald focus:ring-0 text-brand-emerald shrink-0 cursor-pointer"
                    />
                    <div class="min-w-0">
                      <p class="font-bold text-sm tracking-wide text-white" :class="{ 'line-through !text-gray-500': task.status === 'done' }">
                        {{ task.title }}
                      </p>
                      <p class="text-xs text-gray-400 mt-1 font-semibold">
                        Due: {{ formatDateTime(task.due_date) }} | PIC: {{ task.assigned_to?.full_name || 'Unassigned' }}
                      </p>
                    </div>
                  </div>

                  <!-- Priority & Status badges -->
                  <div class="flex items-center gap-3.5 select-none shrink-0 font-sans">
                    <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider" :class="getPriorityStyles(task.priority)">
                      {{ task.priority }} Priority
                    </span>
                    <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider" :class="getTaskStatusStyles(task.status)">
                      {{ task.status }}
                    </span>
                    <button 
                      v-if="auth.hasPermission('tasks:write')"
                      @click="deleteTask(task.id)"
                      class="text-red-400 hover:text-red-500 text-xs font-bold transition-colors"
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

            <!-- TAB 4: STATUS TIMELINE -->
            <div v-if="activeTab === 'timeline'">
              <ProjectStatusTimeline :logs="logs" />
            </div>

            <!-- TAB 5: ACTIVITY LOG -->
            <div v-if="activeTab === 'activity'">
              <ProjectActivityLog :activity-logs="activityLogs" />
            </div>

          </div>

        </div>

        <!-- Right Side: Sidebar Cards for Customer, Assignments, Event Source, Financial Summary -->
        <div class="space-y-6">
          
          <!-- Assignments panel -->
          <div class="glass-panel p-5 space-y-4 select-none">
            <h4 class="text-xs font-bold text-white uppercase tracking-wider border-b border-brand-charcoal-light/20 pb-2">Operational Assignments</h4>
            <div class="space-y-3 text-xs">
              <div class="flex justify-between items-center bg-brand-charcoal-light/10 p-2.5 rounded-xl border border-brand-charcoal-light/15">
                <div>
                  <p class="text-gray-400 font-bold uppercase tracking-widest text-[9px]">Program Owner (PO)</p>
                  <p class="text-white font-extrabold mt-1 text-sm">{{ project.program_owner?.full_name || 'Unassigned' }}</p>
                </div>
                <span v-if="project.program_owner?.initial_code" class="px-2 py-1 bg-brand-orange/15 text-brand-orange text-xs font-black rounded border border-brand-orange/20">
                  {{ project.program_owner.initial_code }}
                </span>
              </div>
              <div class="flex justify-between items-center bg-brand-charcoal-light/10 p-2.5 rounded-xl border border-brand-charcoal-light/15">
                <div>
                  <p class="text-gray-400 font-bold uppercase tracking-widest text-[9px]">Program Manager (PM)</p>
                  <p class="text-white font-extrabold mt-1 text-sm">{{ project.program_manager?.full_name || 'Unassigned' }}</p>
                </div>
                <span v-if="project.program_manager?.initial_code" class="px-2 py-1 bg-brand-orange/15 text-brand-orange text-xs font-black rounded border border-brand-orange/20">
                  {{ project.program_manager.initial_code }}
                </span>
              </div>
            </div>
          </div>

          <!-- Customer details -->
          <div class="glass-panel p-5 space-y-3 select-none">
            <h4 class="text-xs font-bold text-white uppercase tracking-wider border-b border-brand-charcoal-light/20 pb-2">Client Profile</h4>
            <div class="text-xs space-y-2">
              <p class="text-sm font-extrabold text-white">{{ project.customer?.company_name }}</p>
              <p class="text-gray-400 font-semibold">Category: <span class="text-gray-200">{{ project.customer?.category }}</span></p>
              <p class="text-gray-400 font-semibold">Mailing Address: <span class="text-gray-300">{{ project.customer?.address || '-' }}</span></p>
            </div>
          </div>

          <!-- Event Source -->
          <div class="glass-panel p-5 space-y-3 select-none">
            <h4 class="text-xs font-bold text-white uppercase tracking-wider border-b border-brand-charcoal-light/20 pb-2">Event Source / Referral</h4>
            <div class="text-xs space-y-2">
              <div class="flex justify-between items-center">
                <p class="text-gray-400 font-semibold">Source Type</p>
                <span class="px-2 py-0.5 bg-brand-orange/10 text-brand-orange rounded font-bold uppercase text-[9px]">
                  {{ project.event_source?.source_type || 'Direct' }}
                </span>
              </div>
              <p class="text-gray-400 font-semibold">Partner/Vendor: <span class="text-gray-200 font-bold">{{ project.event_source?.vendor_name || '-' }}</span></p>
              <p class="text-gray-400 font-semibold">External Sales PIC: <span class="text-gray-200 font-bold">{{ project.event_source?.sales_name || '-' }}</span></p>
            </div>
          </div>

          <!-- Collections Progress Card -->
          <div class="glass-panel p-5 space-y-3 select-none">
            <h4 class="text-xs font-bold text-white uppercase tracking-wider border-b border-brand-charcoal-light/20 pb-2">Collections Progress</h4>
            <div class="space-y-3 text-xs">
              <div class="flex justify-between items-center">
                <p class="text-gray-400 font-semibold">Billing Status</p>
                <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider" :class="getPaymentStatusStyles(project.payment_status)">
                  {{ project.payment_status }}
                </span>
              </div>
              <div class="grid grid-cols-2 gap-2 text-xs pt-1">
                <div>
                  <p class="text-gray-500 font-bold text-[9px] uppercase tracking-widest">Total Deal Value</p>
                  <p class="text-white font-extrabold text-sm">{{ formatMoney(project.budget) }}</p>
                </div>
                <div>
                  <p class="text-gray-500 font-bold text-[9px] uppercase tracking-widest">Approved Collected</p>
                  <p class="text-brand-emerald font-black text-sm">{{ formatMoney(project.paid_amount) }}</p>
                </div>
              </div>
              <div class="w-full bg-brand-charcoal-dark border border-brand-charcoal-light/20 h-2 rounded-full overflow-hidden mt-2">
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
      <div class="bg-brand-charcoal border border-brand-charcoal-light/35 rounded-3xl w-full max-w-lg shadow-2xl p-6 relative">
        <h3 class="text-base font-bold text-white tracking-wide mb-5">Link Venue Schedule</h3>
        <form @submit.prevent="saveSchedule" class="space-y-4">
          <div>
            <label class="block text-[10px] font-extrabold uppercase tracking-widest text-gray-400 mb-2">Venue/Address Name</label>
            <input v-model="newSched.venue_name" type="text" required placeholder="e.g. Sentul Adventure Park Camp" class="w-full px-4 py-2.5 rounded-xl bg-brand-charcoal-dark border border-brand-charcoal-light/45 text-sm font-semibold outline-none text-white focus:border-brand-orange" />
          </div>
          <div>
            <label class="block text-[10px] font-extrabold uppercase tracking-widest text-gray-400 mb-2">Full Mailing Address</label>
            <textarea v-model="newSched.address" rows="2" placeholder="Address..." class="w-full px-4 py-2.5 rounded-xl bg-brand-charcoal-dark border border-brand-charcoal-light/45 text-sm font-semibold outline-none text-white focus:border-brand-orange"></textarea>
          </div>
          <div>
            <label class="block text-[10px] font-extrabold uppercase tracking-widest text-gray-400 mb-2">Google Maps Embed Link URL</label>
            <input v-model="newSched.map_link" type="url" placeholder="https://maps.google.com/..." class="w-full px-4 py-2.5 rounded-xl bg-brand-charcoal-dark border border-brand-charcoal-light/45 text-sm font-semibold outline-none text-white focus:border-brand-orange" />
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-[10px] font-extrabold uppercase tracking-widest text-gray-400 mb-2">Operational Start Time</label>
              <input v-model="newSched.start_time" type="datetime-local" required class="w-full px-4 py-2.5 rounded-xl bg-brand-charcoal-dark border border-brand-charcoal-light/45 text-xs font-semibold text-gray-300 outline-none focus:border-brand-orange" />
            </div>
            <div>
              <label class="block text-[10px] font-extrabold uppercase tracking-widest text-gray-400 mb-2">Operational End Time</label>
              <input v-model="newSched.end_time" type="datetime-local" required class="w-full px-4 py-2.5 rounded-xl bg-brand-charcoal-dark border border-brand-charcoal-light/45 text-xs font-semibold text-gray-300 outline-none focus:border-brand-orange" />
            </div>
          </div>
          <div>
            <label class="block text-[10px] font-extrabold uppercase tracking-widest text-gray-400 mb-2">Assign On-Site PIC Manager</label>
            <select v-model="newSched.pic_id" class="w-full px-4 py-2.5 rounded-xl bg-brand-charcoal-dark border border-brand-charcoal-light/45 text-xs font-semibold text-gray-300 outline-none focus:border-brand-orange">
              <option :value="null">Unassigned</option>
              <option v-for="u in users" :key="u.id" :value="u.id">{{ u.full_name }}</option>
            </select>
          </div>
          <div class="flex items-center justify-end gap-3 pt-3">
            <button type="button" @click="showAddScheduleModal = false" class="px-4 py-2.5 rounded-xl border border-brand-charcoal-light/40 text-xs font-bold text-gray-400 hover:text-white transition-all">Cancel</button>
            <button type="submit" class="px-5 py-2.5 rounded-xl bg-gradient-to-r from-brand-orange to-brand-orange-light text-white font-bold text-xs shadow-lg">Save Schedule</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Create Task Modal -->
    <div v-if="showAddTaskModal" class="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 select-none">
      <div class="bg-brand-charcoal border border-brand-charcoal-light/35 rounded-3xl w-full max-w-lg shadow-2xl p-6 relative">
        <h3 class="text-base font-bold text-white tracking-wide mb-5">Create Operations Task</h3>
        <form @submit.prevent="saveTask" class="space-y-4">
          <div>
            <label class="block text-[10px] font-extrabold uppercase tracking-widest text-gray-400 mb-2">Task Title</label>
            <input v-model="newTask.title" type="text" required placeholder="e.g. Procure sound equipment system" class="w-full px-4 py-2.5 rounded-xl bg-brand-charcoal-dark border border-brand-charcoal-light/45 text-sm font-semibold outline-none text-white focus:border-brand-orange" />
          </div>
          <div>
            <label class="block text-[10px] font-extrabold uppercase tracking-widest text-gray-400 mb-2">Description / Instructions</label>
            <textarea v-model="newTask.description" rows="2" placeholder="Task requirements..." class="w-full px-4 py-2.5 rounded-xl bg-brand-charcoal-dark border border-brand-charcoal-light/45 text-sm font-semibold outline-none text-white focus:border-brand-orange"></textarea>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-[10px] font-extrabold uppercase tracking-widest text-gray-400 mb-2">Priority Level</label>
              <select v-model="newTask.priority" class="w-full px-4 py-2.5 rounded-xl bg-brand-charcoal-dark border border-brand-charcoal-light/45 text-xs font-semibold text-gray-300 outline-none focus:border-brand-orange">
                <option value="low">Low Priority</option>
                <option value="medium">Medium Priority</option>
                <option value="high">High Priority</option>
              </select>
            </div>
            <div>
              <label class="block text-[10px] font-extrabold uppercase tracking-widest text-gray-400 mb-2">Due Date & Time</label>
              <input v-model="newTask.due_date" type="datetime-local" class="w-full px-4 py-2.5 rounded-xl bg-brand-charcoal-dark border border-brand-charcoal-light/45 text-xs font-semibold text-gray-300 outline-none focus:border-brand-orange" />
            </div>
          </div>
          <div>
            <label class="block text-[10px] font-extrabold uppercase tracking-widest text-gray-400 mb-2">Assign On-Site PIC Manager</label>
            <select v-model="newTask.assigned_to_id" class="w-full px-4 py-2.5 rounded-xl bg-brand-charcoal-dark border border-brand-charcoal-light/45 text-xs font-semibold text-gray-300 outline-none focus:border-brand-orange">
              <option :value="null">Unassigned</option>
              <option v-for="u in users" :key="u.id" :value="u.id">{{ u.full_name }}</option>
            </select>
          </div>
          <div class="flex items-center justify-end gap-3 pt-3">
            <button type="button" @click="showAddTaskModal = false" class="px-4 py-2.5 rounded-xl border border-brand-charcoal-light/40 text-xs font-bold text-gray-400 hover:text-white transition-all">Cancel</button>
            <button type="submit" class="px-5 py-2.5 rounded-xl bg-gradient-to-r from-brand-orange to-brand-orange-light text-white font-bold text-xs shadow-lg">Allocate Task</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '../store/auth'
import ProjectDetailHeader from '../components/ProjectDetailHeader.vue'
import ProjectValidationWarnings from '../components/ProjectValidationWarnings.vue'
import ProjectStatusTimeline from '../components/ProjectStatusTimeline.vue'
import ProjectActivityLog from '../components/ProjectActivityLog.vue'
import ProjectDocumentsPanel from '../components/ProjectDocumentsPanel.vue'

const auth = useAuthStore()
const route = useRoute()
const projectId = route.params.id

const project = ref(null)
const schedules = ref([])
const tasks = ref([])
const documents = ref([])
const logs = ref([])
const activityLogs = ref([])
const validationWarnings = ref([])
const users = ref([])

const loading = ref(true)
const activeTab = ref('schedules')

const showAddScheduleModal = ref(false)
const showAddTaskModal = ref(false)

const tabs = [
  { id: 'schedules', name: 'Event Timeline' },
  { id: 'tasks', name: 'Checklist Operations' },
  { id: 'documents', name: 'Shared Documents' },
  { id: 'timeline', name: 'Status Timeline' },
  { id: 'activity', name: 'Activity Log' }
]

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

const fetchData = async () => {
  try {
    const [projRes, schedsRes, tasksRes, docsRes, logsRes, usersRes] = await Promise.all([
      axios.get(`/api/v1/projects/${projectId}`),
      axios.get(`/api/v1/projects/${projectId}/events`),
      axios.get(`/api/v1/projects/${projectId}/tasks`),
      axios.get(`/api/v1/projects/${projectId}/documents`),
      axios.get(`/api/v1/projects/${projectId}/logs`),
      axios.get('/api/v1/auth/users')
    ])
    
    project.value = projRes.data
    schedules.value = schedsRes.data
    tasks.value = tasksRes.data
    documents.value = docsRes.data
    logs.value = logsRes.data
    users.value = usersRes.data
    
    validationWarnings.value = projRes.data.validation_warnings || []
    activityLogs.value = projRes.data.activity_logs || []
  } catch (err) {
    console.error('Failed to load project detailed context', err)
  } finally {
    loading.value = false
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
  return 'bg-brand-charcoal-light text-gray-300'
}

const getTaskStatusStyles = (status) => {
  if (status === 'done') return 'bg-brand-emerald/10 text-brand-emerald'
  if (status === 'review') return 'bg-purple-500/10 text-purple-500'
  if (status === 'in_progress') return 'bg-brand-blue/10 text-brand-blue'
  return 'bg-brand-charcoal-light text-gray-300'
}

const getPaymentStatusStyles = (status) => {
  if (status === 'Paid') return 'bg-brand-emerald/10 text-brand-emerald border border-brand-emerald/20'
  if (status === 'Partial Paid') return 'bg-brand-blue/10 text-brand-blue border border-brand-blue/20'
  if (status === 'Outstanding' || status === 'Overdue') return 'bg-red-500/10 text-red-400 border border-red-500/20'
  return 'bg-brand-charcoal-light text-gray-300 border border-brand-charcoal-light/30'
}

// Transition Status Action
const transitionStatus = async (statusType, newStatus) => {
  const notes = prompt(`Please enter transition notes for shifting ${statusType.replace('_', ' ')} to "${newStatus}":`, "")
  if (notes === null) return // cancelled
  try {
    await axios.patch(`/api/v1/projects/${projectId}/status`, {
      status_type: statusType,
      new_status: newStatus,
      notes: notes
    })
    await fetchProjectDetail()
    // Fetch logs again
    const logsRes = await axios.get(`/api/v1/projects/${projectId}/logs`)
    logs.value = logsRes.data
    alert('Workflow status transitioned successfully')
  } catch (err) {
    alert(err.response?.data?.detail || 'Failed to transition workflow status')
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
  } catch (err) {
    alert('Failed to save venue schedule')
  }
}

const addRundownItem = async (sched) => {
  try {
    const updatedRundown = [...sched.rundown, { ...newRundown.value }]
    const response = await axios.put(`/api/v1/events/${sched.id}`, { rundown: updatedRundown })
    sched.rundown = response.data.rundown
    newRundown.value = { time: '', activity: '', pic: '', notes: '' }
    await fetchProjectDetail()
  } catch (err) {
    alert('Failed to save rundown timesheet item')
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
  } catch (err) {
    alert('Failed to allocate task')
  }
}

const toggleTaskDone = async (task) => {
  try {
    const newStatus = task.status === 'done' ? 'todo' : 'done'
    const response = await axios.put(`/api/v1/tasks/${task.id}`, { status: newStatus })
    task.status = response.data.status
    await fetchProjectDetail()
  } catch (err) {
    alert('Failed to update task status')
  }
}

const deleteTask = async (id) => {
  if (!confirm('Are you sure you want to delete this task?')) return
  try {
    await axios.delete(`/api/v1/tasks/${id}`)
    tasks.value = tasks.value.filter(t => t.id !== id)
    await fetchProjectDetail()
  } catch (err) {
    alert('Failed to delete task')
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
  } catch (err) {
    alert('Failed to link cloud document reference')
  }
}

const deleteDoc = async (id) => {
  if (!confirm('Are you sure you want to delete this linked asset reference?')) return
  try {
    await axios.delete(`/api/v1/documents/${id}`)
    documents.value = documents.value.filter(d => d.id !== id)
    await fetchProjectDetail()
  } catch (err) {
    alert('Failed to delete document reference')
  }
}
</script>
