<template>
  <div class="space-y-6">
    <!-- PNL Access Sensitivity Warning Alert -->
    <div class="glass-panel p-4 border-l-4 border-amber-500 bg-amber-500/5 text-amber-200 text-xs font-semibold leading-relaxed flex items-start gap-3">
      <svg class="w-5 h-5 text-amber-500 shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
      </svg>
      <div>
        <span class="font-extrabold uppercase text-amber-400 block mb-0.5">Catatan Akses PNL (Profit &amp; Loss)</span>
        PNL berisi informasi profit/loss dan direkomendasikan untuk dibatasi pada Management/Finance/Admin pada fase permission refinement.
      </div>
    </div>

    <!-- Top Summary Progress Cards Grid (Sprint 7) -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 select-none">
      <div class="glass-panel p-4 rounded-2xl border border-brand-charcoal-light/10 text-center">
        <p class="text-[10px] font-extrabold uppercase tracking-widest text-gray-400">Instrument Completion</p>
        <p class="text-2xl font-black text-white mt-1">{{ completionPercentage }}%</p>
        <div class="w-full bg-brand-charcoal-dark border border-brand-charcoal-light/20 h-1.5 rounded-full overflow-hidden mt-2">
          <div class="bg-brand-orange h-full rounded-full transition-all duration-500" :style="{ width: completionPercentage + '%' }"></div>
        </div>
      </div>
      
      <div class="glass-panel p-4 rounded-2xl border border-brand-charcoal-light/10 text-center">
        <p class="text-[10px] font-extrabold uppercase tracking-widest text-gray-400">Done / Required</p>
        <p class="text-2xl font-black text-brand-emerald mt-1">{{ doneCount }} <span class="text-xs text-gray-500 font-normal">/ {{ totalRequired }}</span></p>
        <p class="text-[9px] text-gray-500 mt-2">Required instruments completed</p>
      </div>

      <div class="glass-panel p-4 rounded-2xl border border-brand-charcoal-light/10 text-center">
        <p class="text-[10px] font-extrabold uppercase tracking-widest text-gray-400">Need Revision</p>
        <p class="text-2xl font-black mt-1" :class="needRevisionCount > 0 ? 'text-rose-400' : 'text-gray-400'">{{ needRevisionCount }}</p>
        <p class="text-[9px] text-gray-500 mt-2">Instruments needing attention</p>
      </div>

      <div class="glass-panel p-4 rounded-2xl border border-brand-charcoal-light/10 text-center">
        <p class="text-[10px] font-extrabold uppercase tracking-widest text-gray-400">Overdue</p>
        <p class="text-2xl font-black mt-1" :class="overdueCount > 0 ? 'text-red-400 animate-pulse' : 'text-gray-400'">{{ overdueCount }}</p>
        <p class="text-[9px] text-gray-500 mt-2">Due date passed and incomplete</p>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
      <!-- Left side: Add custom instrument form (only if has permission) -->
      <div v-if="auth.hasPermission('projects:write')" class="glass-panel p-5 space-y-4 h-fit lg:col-span-1 select-none">
        <h4 class="text-xs font-bold text-white uppercase tracking-wider">Add Custom Instrument</h4>
        <form @submit.prevent="handleAddInstrument" class="space-y-3">
          <div>
            <label class="block text-[10px] font-extrabold uppercase tracking-widest text-gray-400 mb-1">Instrument Type *</label>
            <select v-model="newInstrument.instrument_type" required class="w-full px-3 py-2 rounded-lg bg-brand-charcoal-dark border border-brand-charcoal-light/40 text-xs text-white">
              <option value="CL">CL - Contract/Confirmation Letter</option>
              <option value="ROS">ROS - Rundown of Show</option>
              <option value="CK">CK - Check List</option>
              <option value="PNL">PNL - Profit and Loss</option>
              <option value="PF">PF</option>
              <option value="MATRIX">MATRIX</option>
              <option value="OTHER">OTHER</option>
            </select>
          </div>
          <div v-if="newInstrument.instrument_type === 'OTHER'">
            <label class="block text-[10px] font-extrabold uppercase tracking-widest text-gray-400 mb-1">Custom Title *</label>
            <input v-model="newInstrument.title" type="text" placeholder="e.g. Vendor Agreement" required class="w-full px-3 py-2 rounded-lg bg-brand-charcoal-dark border border-brand-charcoal-light/40 text-xs text-white" />
          </div>
          <div>
            <label class="block text-[10px] font-extrabold uppercase tracking-widest text-gray-400 mb-1">Status</label>
            <select v-model="newInstrument.status" required class="w-full px-3 py-2 rounded-lg bg-brand-charcoal-dark border border-brand-charcoal-light/40 text-xs text-white">
              <option value="Not Started">Not Started</option>
              <option value="In Progress">In Progress</option>
              <option value="Done">Done</option>
              <option value="Need Revision">Need Revision</option>
              <option value="Not Required">Not Required</option>
            </select>
          </div>
          <div>
            <label class="block text-[10px] font-extrabold uppercase tracking-widest text-gray-400 mb-1">Document URL</label>
            <input v-model="newInstrument.document_url" type="url" placeholder="https://drive.google.com/..." class="w-full px-3 py-2 rounded-lg bg-brand-charcoal-dark border border-brand-charcoal-light/40 text-xs text-white" />
          </div>
          <div>
            <label class="block text-[10px] font-extrabold uppercase tracking-widest text-gray-400 mb-1">Due Date</label>
            <input v-model="newInstrument.due_date" type="date" class="w-full px-3 py-2 rounded-lg bg-brand-charcoal-dark border border-brand-charcoal-light/40 text-xs text-white" />
          </div>
          <div>
            <label class="block text-[10px] font-extrabold uppercase tracking-widest text-gray-400 mb-1">Notes</label>
            <textarea v-model="newInstrument.notes" placeholder="Remarks..." rows="2" class="w-full px-3 py-2 rounded-lg bg-brand-charcoal-dark border border-brand-charcoal-light/40 text-xs text-white"></textarea>
          </div>
          <button type="submit" class="w-full py-2 bg-brand-orange text-white rounded-lg font-bold text-xs hover:bg-brand-orange-dark transition-all">Add Instrument</button>
        </form>
      </div>

      <!-- Right side: Instruments Table / List -->
      <div class="glass-panel p-5 flex flex-col min-h-[400px]" :class="auth.hasPermission('projects:write') ? 'lg:col-span-3' : 'lg:col-span-4'">
        <div class="flex items-center justify-between gap-4 mb-4 select-none shrink-0">
          <h4 class="text-xs font-bold text-white uppercase tracking-wider">Project Instruments / Checklist</h4>
          <button 
            v-if="auth.hasPermission('projects:write')"
            @click="$emit('generate-defaults')"
            class="px-3 py-1.5 bg-brand-orange/15 hover:bg-brand-orange/30 text-brand-orange border border-brand-orange/20 rounded-lg font-bold text-xs transition-all"
          >
            Generate Default Instruments
          </button>
        </div>

        <div class="flex-1 overflow-x-auto custom-scrollbar">
          <div v-if="!instruments || instruments.length === 0" class="h-full flex flex-col items-center justify-center text-center p-8 select-none">
            <p class="text-xs font-semibold text-gray-500 mb-4">Belum ada instrument untuk project ini.</p>
            <button 
              v-if="auth.hasPermission('projects:write')"
              @click="$emit('generate-defaults')"
              class="px-4 py-2 bg-brand-orange text-white rounded-lg font-bold text-xs hover:bg-brand-orange-dark transition-all"
            >
              Generate Default Instruments
            </button>
          </div>

          <table v-else class="w-full text-left text-xs font-semibold border-collapse">
            <thead>
              <tr class="border-b border-brand-charcoal-light/20 text-gray-400 uppercase tracking-widest text-[9px] select-none">
                <th class="pb-3 pl-2">Instrument</th>
                <th class="pb-3">Label / Meaning</th>
                <th class="pb-3 text-center">Status</th>
                <th class="pb-3 text-center">Due Date</th>
                <th class="pb-3 text-center">Completed</th>
                <th class="pb-3 pr-2 text-right">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr 
                v-for="inst in instruments" 
                :key="inst.id"
                class="border-b border-brand-charcoal-light/10 hover:bg-brand-charcoal-light/5 transition-all"
              >
                <!-- Instrument Type & Title -->
                <td class="py-3.5 pl-2 font-bold text-white flex items-center gap-2">
                  <span class="px-1.5 py-0.5 rounded bg-brand-charcoal-dark border border-brand-charcoal-light/30 text-brand-orange text-[10px] font-black">
                    {{ inst.instrument_type }}
                  </span>
                  <span v-if="inst.title" class="text-gray-300 font-semibold text-[11px] max-w-[120px] truncate" :title="inst.title">
                    {{ inst.title }}
                  </span>
                </td>

                <!-- Label / Meaning & Doc URL -->
                <td class="py-3.5">
                  <div class="flex flex-col">
                    <span class="text-white">{{ getInstrumentLabel(inst.instrument_type) }}</span>
                    
                    <!-- PNL sensitive visibility masking (Sprint 7) -->
                    <template v-if="inst.instrument_type === 'PNL' && !isAuthorizedForPnl">
                      <span class="text-amber-500/80 text-[10px] italic font-bold mt-1 flex items-center gap-1 select-none">
                        <svg class="w-3.5 h-3.5 text-amber-500 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                        </svg>
                        Restricted (Admin/Finance/Mgmt Only)
                      </span>
                    </template>
                    <template v-else>
                      <a 
                        v-if="inst.document_url" 
                        :href="inst.document_url" 
                        target="_blank" 
                        class="text-brand-orange hover:underline text-[10px] font-bold mt-0.5 flex items-center gap-1"
                      >
                        <svg class="w-3 h-3 inline" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                        </svg>
                        Open Document
                      </a>
                      <span v-else class="text-gray-500 text-[10px] italic">No document linked</span>
                    </template>
                    
                    <p v-if="inst.notes" class="text-gray-400 text-[10px] font-normal leading-relaxed mt-1 whitespace-pre-line max-w-[200px] break-words">
                      {{ inst.notes }}
                    </p>
                  </div>
                </td>

                <!-- Status Badge (with Quick Action Dropdown for Write Users in Sprint 7) -->
                <td class="py-3.5 text-center select-none">
                  <div class="flex flex-col items-center gap-1.5">
                    <select 
                      v-if="auth.hasPermission('projects:write')"
                      :value="inst.status"
                      @change="handleQuickStatusChange(inst, $event.target.value)"
                      class="px-2 py-1 bg-brand-charcoal-dark border border-brand-charcoal-light/30 rounded text-[10px] font-bold uppercase tracking-wider outline-none cursor-pointer focus:border-brand-orange"
                      :class="getStatusBadgeStyles(inst.status)"
                    >
                      <option value="Not Started" class="bg-brand-charcoal text-white">Not Started</option>
                      <option value="In Progress" class="bg-brand-charcoal text-white">In Progress</option>
                      <option value="Done" class="bg-brand-charcoal text-white">Done</option>
                      <option value="Need Revision" class="bg-brand-charcoal text-white">Need Revision</option>
                      <option value="Not Required" class="bg-brand-charcoal text-white">Not Required</option>
                    </select>
                    <span v-else class="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider inline-block" :class="getStatusBadgeStyles(inst.status)">
                      {{ inst.status }}
                    </span>
                    <div v-if="inst.updated_by_user" class="text-[9px] text-gray-500" :title="`Updated at ${formatDateTime(inst.updated_at)}`">
                      by {{ inst.updated_by_user.full_name }}
                    </div>
                  </div>
                </td>

                <!-- Due Date (with Overdue Indicator in Sprint 7) -->
                <td class="py-3.5 text-center font-semibold">
                  <div class="flex flex-col items-center gap-0.5">
                    <span :class="isOverdue(inst) ? 'text-rose-400 font-extrabold' : 'text-gray-300'">
                      {{ formatDate(inst.due_date) }}
                    </span>
                    <span v-if="isOverdue(inst)" class="px-1.5 py-0.2 rounded bg-rose-500/20 text-rose-400 text-[8px] font-bold uppercase tracking-wider animate-pulse">
                      Overdue
                    </span>
                  </div>
                </td>

                <!-- Completed Date -->
                <td class="py-3.5 text-center text-gray-300 font-semibold">
                  {{ formatDate(inst.completed_date) }}
                </td>

                <!-- Actions -->
                <td class="py-3.5 pr-2 text-right select-none">
                  <div class="flex items-center justify-end gap-2">
                    <button 
                      v-if="auth.hasPermission('projects:write')"
                      @click="openEditModal(inst)"
                      class="px-2 py-1 text-[10px] font-bold text-brand-orange bg-brand-orange/10 rounded hover:bg-brand-orange/20 transition-all"
                    >
                      Edit
                    </button>
                    <button 
                      v-if="auth.hasPermission('projects:write')"
                      @click="handleDelete(inst)"
                      class="px-2 py-1 text-[10px] font-bold text-red-400 bg-red-500/10 rounded hover:bg-red-500/20 transition-all"
                    >
                      Delete
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Edit Instrument Modal -->
    <div v-if="showEditModal" class="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 select-none">
      <div class="bg-brand-charcoal border border-brand-charcoal-light/35 rounded-3xl w-full max-w-lg shadow-2xl p-6 relative">
        <h3 class="text-base font-bold text-white tracking-wide mb-5">
          Edit Operational Instrument: 
          <span class="text-brand-orange font-black">{{ editingInstrument.instrument_type }}</span>
        </h3>
        <form @submit.prevent="handleUpdateInstrument" class="space-y-4">
          <div>
            <label class="block text-[10px] font-extrabold uppercase tracking-widest text-gray-400 mb-2">Instrument Name / Details</label>
            <div class="text-sm font-semibold text-white bg-brand-charcoal-dark px-4 py-2.5 rounded-xl border border-brand-charcoal-light/30">
              {{ getInstrumentLabel(editingInstrument.instrument_type) }} 
              <span v-if="editingInstrument.title">({{ editingInstrument.title }})</span>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-[10px] font-extrabold uppercase tracking-widest text-gray-400 mb-2">Status</label>
              <select v-model="editingInstrument.status" required class="w-full px-4 py-2.5 rounded-xl bg-brand-charcoal-dark border border-brand-charcoal-light/45 text-xs font-semibold text-gray-300 outline-none focus:border-brand-orange">
                <option value="Not Started">Not Started</option>
                <option value="In Progress">In Progress</option>
                <option value="Done">Done</option>
                <option value="Need Revision">Need Revision</option>
                <option value="Not Required">Not Required</option>
              </select>
            </div>
            <div>
              <label class="block text-[10px] font-extrabold uppercase tracking-widest text-gray-400 mb-2">Due Date</label>
              <input v-model="editingInstrument.due_date" type="date" class="w-full px-4 py-2.5 rounded-xl bg-brand-charcoal-dark border border-brand-charcoal-light/45 text-xs font-semibold text-gray-300 outline-none focus:border-brand-orange" />
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-[10px] font-extrabold uppercase tracking-widest text-gray-400 mb-2">Completed Date</label>
              <input v-model="editingInstrument.completed_date" type="date" class="w-full px-4 py-2.5 rounded-xl bg-brand-charcoal-dark border border-brand-charcoal-light/45 text-xs font-semibold text-gray-300 outline-none focus:border-brand-orange" />
            </div>
            <div>
              <label class="block text-[10px] font-extrabold uppercase tracking-widest text-gray-400 mb-2">Document URL Reference</label>
              <!-- PNL sensitive URL masking in edit modal (Sprint 7) -->
              <template v-if="editingInstrument.instrument_type === 'PNL' && !isAuthorizedForPnl">
                <input type="text" disabled placeholder="[RESTRICTED]" class="w-full px-4 py-2.5 rounded-xl bg-brand-charcoal-dark border border-brand-charcoal-light/35 text-xs font-semibold text-gray-500 outline-none" />
              </template>
              <template v-else>
                <input v-model="editingInstrument.document_url" type="url" placeholder="https://drive.google.com/..." class="w-full px-4 py-2.5 rounded-xl bg-brand-charcoal-dark border border-brand-charcoal-light/45 text-xs font-semibold text-white outline-none focus:border-brand-orange" />
              </template>
            </div>
          </div>

          <div v-if="editingInstrument.instrument_type === 'OTHER'">
            <label class="block text-[10px] font-extrabold uppercase tracking-widest text-gray-400 mb-2">Custom Title</label>
            <input v-model="editingInstrument.title" type="text" placeholder="Title..." class="w-full px-4 py-2.5 rounded-xl bg-brand-charcoal-dark border border-brand-charcoal-light/45 text-sm font-semibold outline-none text-white focus:border-brand-orange" />
          </div>

          <div>
            <label class="block text-[10px] font-extrabold uppercase tracking-widest text-gray-400 mb-2">Notes / Internal Remarks</label>
            <textarea v-model="editingInstrument.notes" rows="3" placeholder="Notes..." class="w-full px-4 py-2.5 rounded-xl bg-brand-charcoal-dark border border-brand-charcoal-light/45 text-sm font-semibold outline-none text-white focus:border-brand-orange"></textarea>
          </div>

          <div class="flex items-center justify-end gap-3 pt-3">
            <button type="button" @click="showEditModal = false" class="px-4 py-2.5 rounded-xl border border-brand-charcoal-light/40 text-xs font-bold text-gray-400 hover:text-white transition-all">Cancel</button>
            <button type="submit" class="px-5 py-2.5 rounded-xl bg-gradient-to-r from-brand-orange to-brand-orange-light text-white font-bold text-xs shadow-lg">Save Changes</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '../store/auth'
import { useUiStore } from '../store/ui'

const auth = useAuthStore()
const ui = useUiStore()

const props = defineProps({
  instruments: {
    type: Array,
    required: true,
    default: () => []
  }
})

const emit = defineEmits(['generate-defaults', 'create-instrument', 'update-instrument', 'delete-instrument'])

// Add Form State
const newInstrument = ref({
  instrument_type: 'CL',
  title: '',
  status: 'Not Started',
  document_url: '',
  due_date: '',
  notes: ''
})

// Edit Modal State
const showEditModal = ref(false)
const editingInstrument = ref({
  id: '',
  instrument_type: '',
  title: '',
  status: '',
  document_url: '',
  due_date: '',
  completed_date: '',
  notes: ''
})

const instrumentLabels = {
  CL: 'Contract Letter / Confirmation Letter',
  ROS: 'Rundown of Show',
  CK: 'Check List',
  PNL: 'Profit and Loss',
  PF: 'PF',
  MATRIX: 'Matrix',
  OTHER: 'Other'
}

const getInstrumentLabel = (type) => {
  return instrumentLabels[type] || type
}

const getStatusBadgeStyles = (status) => {
  if (status === 'Done') return 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
  if (status === 'In Progress') return 'bg-blue-500/10 text-blue-400 border border-blue-500/20'
  if (status === 'Need Revision') return 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
  if (status === 'Not Required') return 'bg-gray-500/10 text-gray-400 border border-gray-500/20'
  return 'bg-amber-500/10 text-amber-400 border border-amber-500/20' // Not Started
}

const formatDate = (val) => {
  if (!val) return '-'
  return new Date(val).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
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

// Sprint 7: Computed Summary indicators
const isAuthorizedForPnl = computed(() => {
  return auth.canViewPnl()
})

const totalRequired = computed(() => {
  const list = props.instruments || []
  return list.filter(i => i && i.status !== 'Not Required').length
})

const doneCount = computed(() => {
  const list = props.instruments || []
  return list.filter(i => i && i.status === 'Done').length
})

const completionPercentage = computed(() => {
  if (totalRequired.value === 0) return 0
  return Math.round((doneCount.value / totalRequired.value) * 100)
})

const needRevisionCount = computed(() => {
  const list = props.instruments || []
  return list.filter(i => i && i.status === 'Need Revision').length
})

const overdueCount = computed(() => {
  const todayStr = new Date().toISOString().split('T')[0]
  const list = props.instruments || []
  return list.filter(i => {
    return i && i.due_date && i.due_date < todayStr && i.status !== 'Done' && i.status !== 'Not Required'
  }).length
})

const isOverdue = (inst) => {
  if (!inst.due_date || inst.status === 'Done' || inst.status === 'Not Required') return false
  const todayStr = new Date().toISOString().split('T')[0]
  return inst.due_date < todayStr
}

// Handlers
const handleAddInstrument = () => {
  const payload = { ...newInstrument.value }
  if (payload.instrument_type !== 'OTHER') {
    payload.title = ''
  }
  if (!payload.due_date) delete payload.due_date
  
  emit('create-instrument', payload)
  
  // Reset Form
  newInstrument.value = {
    instrument_type: 'CL',
    title: '',
    status: 'Not Started',
    document_url: '',
    due_date: '',
    notes: ''
  }
}

const openEditModal = (inst) => {
  editingInstrument.value = {
    id: inst.id,
    instrument_type: inst.instrument_type,
    title: inst.title || '',
    status: inst.status,
    document_url: inst.document_url || '',
    due_date: inst.due_date || '',
    completed_date: inst.completed_date || '',
    notes: inst.notes || ''
  }
  showEditModal.value = true
}

const handleUpdateInstrument = () => {
  const payload = { ...editingInstrument.value }
  if (!payload.due_date) payload.due_date = null
  if (!payload.completed_date) payload.completed_date = null
  
  emit('update-instrument', {
    id: payload.id,
    data: {
      status: payload.status,
      title: payload.title || null,
      document_url: payload.document_url || null,
      due_date: payload.due_date,
      completed_date: payload.completed_date,
      notes: payload.notes || null
    }
  })
  showEditModal.value = false
}

// Quick status select toggle (Sprint 7)
const handleQuickStatusChange = (inst, newStatus) => {
  emit('update-instrument', {
    id: inst.id,
    data: {
      status: newStatus,
      title: inst.title || null,
      document_url: inst.document_url || null,
      due_date: inst.due_date || null,
      completed_date: inst.completed_date || null,
      notes: inst.notes || null
    }
  })
}

const handleDelete = async (inst) => {
  const confirmed = await ui.confirm ({
    title: `Hapus Instrumen ${inst.instrument_type}?`,
    message: `Instrumen ${inst.instrument_type} akan dihapus dari ledger project.`,
    confirmText: 'Hapus',
    cancelText: 'Batal',
    tone: 'danger'
  })
  if (!confirmed) return

  emit('delete-instrument', inst.id)
}
</script>

<style scoped>
.glass-panel {
  background: rgba(26, 32, 44, 0.7);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
  height: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.15);
  border-radius: 2px;
}
</style>
