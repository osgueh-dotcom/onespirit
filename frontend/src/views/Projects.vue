<template>
  <div class="space-y-6">
    <!-- Top actions toolbar -->
    <div class="flex items-center justify-between gap-4 select-none">
      <div class="flex items-center gap-3">
        <span class="text-xs font-bold uppercase tracking-widest text-gray-400">View Pipeline</span>
        <div class="flex rounded-xl p-0.5 bg-brand-charcoal border border-brand-charcoal-light/35">
          <button 
            @click="viewMode = 'board'" 
            class="px-4 py-2 rounded-lg text-xs font-bold transition-all"
            :class="viewMode === 'board' ? 'bg-brand-orange text-white' : 'text-gray-400 hover:text-white'"
          >
            Kanban Board
          </button>
          <button 
            @click="viewMode = 'list'" 
            class="px-4 py-2 rounded-lg text-xs font-bold transition-all"
            :class="viewMode === 'list' ? 'bg-brand-orange text-white' : 'text-gray-400 hover:text-white'"
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

    <!-- Loading matrix -->
    <div v-if="loading" class="h-64 flex flex-col items-center justify-center gap-3">
      <svg class="animate-spin h-6 w-6 text-brand-orange" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
      <span class="text-xs text-gray-400 font-semibold">Loading project matrix pipeline...</span>
    </div>

    <!-- KANBAN BOARD VIEW -->
    <div v-else-if="viewMode === 'board'" class="flex gap-4 overflow-x-auto pb-4 h-[calc(100vh-210px)] min-w-full select-none items-start">
      <div 
        v-for="col in columns" 
        :key="col.status"
        class="w-80 shrink-0 bg-brand-charcoal/50 border border-brand-charcoal-light/20 rounded-2xl p-4 flex flex-col max-h-full"
      >
        <!-- Column Header -->
        <div class="flex items-center justify-between mb-4 border-b border-brand-charcoal-light/25 pb-3">
          <div class="flex items-center gap-2">
            <span class="h-2.5 w-2.5 rounded-full" :class="col.bullet"></span>
            <span class="font-extrabold text-xs text-white uppercase tracking-wider">{{ col.name }}</span>
          </div>
          <span class="px-2 py-0.5 rounded bg-brand-charcoal-light/30 text-[10px] font-bold text-gray-400">
            {{ getProjectsByStatus(col.status).length }}
          </span>
        </div>

        <!-- Cards List -->
        <div class="flex-1 overflow-y-auto space-y-3.5 pr-1">
          <div 
            v-if="getProjectsByStatus(col.status).length === 0"
            class="py-8 text-center text-[10px] font-bold text-gray-600 border border-dashed border-brand-charcoal-light/20 rounded-xl"
          >
            No projects in this stage
          </div>

          <div 
            v-for="proj in getProjectsByStatus(col.status)" 
            :key="proj.id"
            class="interactive-card p-4 space-y-3 select-none relative group"
          >
            <!-- Card Details -->
            <div>
              <router-link :to="'/projects/' + proj.id" class="text-sm font-bold text-white hover:text-brand-orange transition-colors block leading-tight mb-1">
                {{ proj.title }}
              </router-link>
              <span class="text-[10px] font-bold text-gray-400 block truncate">{{ proj.customer?.company_name }}</span>
            </div>

            <!-- Price & Owner info -->
            <div class="flex items-center justify-between text-[11px] font-bold border-t border-brand-charcoal-light/10 pt-2.5">
              <span class="text-brand-emerald">{{ formatMoney(proj.budget) }}</span>
              <span class="text-gray-400 bg-brand-charcoal-light/35 px-1.5 py-0.5 rounded truncate max-w-[100px]">
                {{ proj.assigned_to?.full_name || 'Unassigned' }}
              </span>
            </div>

            <!-- Quick workflow Shift Arrows -->
            <div class="flex items-center justify-between border-t border-brand-charcoal-light/10 pt-2 opacity-0 group-hover:opacity-100 transition-opacity">
              <button 
                v-if="col.prev"
                @click="transitionStatus(proj, col.prev)"
                class="p-1 rounded bg-brand-charcoal-light/30 hover:bg-brand-orange/20 text-gray-400 hover:text-brand-orange transition-all"
              >
                ← Shift Back
              </button>
              <div v-else></div>
              
              <button 
                v-if="col.next"
                @click="transitionStatus(proj, col.next)"
                class="p-1 rounded bg-brand-charcoal-light/30 hover:bg-brand-orange/20 text-gray-400 hover:text-brand-orange transition-all"
              >
                Advance →
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ALL PROJECTS LIST VIEW -->
    <div v-else class="glass-panel overflow-hidden border border-brand-charcoal-light/30">
      <div class="overflow-x-auto min-w-full">
        <table class="min-w-full text-left divide-y divide-brand-charcoal-light/20 text-xs">
          <thead class="bg-brand-charcoal/50 text-[10px] font-extrabold uppercase tracking-widest text-gray-400 select-none">
            <tr>
              <th class="px-6 py-4">Project Title</th>
              <th class="px-6 py-4">Customer Account</th>
              <th class="px-6 py-4">Pipeline Status</th>
              <th class="px-6 py-4">Quotation</th>
              <th class="px-6 py-4">Budget</th>
              <th class="px-6 py-4">Assigned PM</th>
              <th class="px-6 py-4 text-right">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-brand-charcoal-light/10 font-medium">
            <tr v-if="projects.length === 0">
              <td colspan="7" class="px-6 py-12 text-center text-gray-500 font-semibold">
                No active event projects cataloged.
              </td>
            </tr>
            <tr 
              v-for="proj in projects" 
              :key="proj.id"
              class="hover:bg-brand-charcoal-light/10 transition-colors"
            >
              <td class="px-6 py-4">
                <router-link :to="'/projects/' + proj.id" class="font-bold text-white hover:text-brand-orange tracking-wide text-sm block">
                  {{ proj.title }}
                </router-link>
                <span class="text-[10px] text-gray-400">Duration: {{ proj.start_date || '-' }} to {{ proj.end_date || '-' }}</span>
              </td>
              <td class="px-6 py-4 font-bold text-white">{{ proj.customer?.company_name }}</td>
              <td class="px-6 py-4 select-none">
                <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider" :class="getStatusStyles(proj.status)">
                  {{ proj.status }}
                </span>
              </td>
              <td class="px-6 py-4 select-none">
                <span class="px-2 py-0.5 rounded text-[10px] font-bold" :class="getQuotationStyles(proj.quotation_status)">
                  {{ proj.quotation_status }}
                </span>
              </td>
              <td class="px-6 py-4 font-bold text-brand-emerald">{{ formatMoney(proj.budget) }}</td>
              <td class="px-6 py-4 text-gray-400 font-semibold">{{ proj.assigned_to?.full_name || 'Unassigned' }}</td>
              <td class="px-6 py-4 text-right select-none space-x-2.5">
                <router-link 
                  :to="'/projects/' + proj.id"
                  class="px-2.5 py-1 text-[10px] font-bold text-brand-orange bg-brand-orange/10 rounded hover:bg-brand-orange/20 transition-all inline-block"
                >
                  Manage Workflow
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

    <!-- Create Project Drawer / Modal -->
    <div v-if="showAddModal" class="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 select-none">
      <div class="bg-brand-charcoal border border-brand-charcoal-light/35 rounded-3xl w-full max-w-lg shadow-2xl p-6 relative">
        <h3 class="text-base font-bold text-white tracking-wide mb-5">Create Project Entry</h3>
        
        <form @submit.prevent="saveProject" class="space-y-4">
          <div>
            <label class="block text-[10px] font-extrabold uppercase tracking-widest text-gray-400 mb-2">Project/Event Title</label>
            <input 
              v-model="newProj.title"
              type="text" 
              required
              placeholder="e.g. Annual Outing & Team Building 2026"
              class="w-full px-4 py-2.5 rounded-xl bg-brand-charcoal-dark border border-brand-charcoal-light/45 hover:border-brand-orange/30 focus:border-brand-orange text-sm font-semibold outline-none transition-all text-white"
            />
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-[10px] font-extrabold uppercase tracking-widest text-gray-400 mb-2">Client Account *</label>
              <select 
                v-model="newProj.customer_id"
                required
                class="w-full px-4 py-2.5 rounded-xl bg-brand-charcoal-dark border border-brand-charcoal-light/45 hover:border-brand-orange/30 focus:border-brand-orange text-xs font-semibold outline-none transition-all text-gray-300"
              >
                <option value="" disabled>Select Client</option>
                <option v-for="c in customers" :key="c.id" :value="c.id">{{ c.company_name }}</option>
              </select>
            </div>

            <div>
              <label class="block text-[10px] font-extrabold uppercase tracking-widest text-gray-400 mb-2">Assign Project Manager</label>
              <select 
                v-model="newProj.assigned_to_id"
                class="w-full px-4 py-2.5 rounded-xl bg-brand-charcoal-dark border border-brand-charcoal-light/45 hover:border-brand-orange/30 focus:border-brand-orange text-xs font-semibold outline-none transition-all text-gray-300"
              >
                <option :value="null">Unassigned</option>
                <option v-for="u in users" :key="u.id" :value="u.id">{{ u.full_name }} ({{ u.role?.name }})</option>
              </select>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-[10px] font-extrabold uppercase tracking-widest text-gray-400 mb-2">Proposed Start Date</label>
              <input 
                v-model="newProj.start_date"
                type="date"
                class="w-full px-4 py-2.5 rounded-xl bg-brand-charcoal-dark border border-brand-charcoal-light/45 hover:border-brand-orange/30 focus:border-brand-orange text-xs font-semibold outline-none transition-all text-gray-300"
              />
            </div>
            <div>
              <label class="block text-[10px] font-extrabold uppercase tracking-widest text-gray-400 mb-2">Proposed End Date</label>
              <input 
                v-model="newProj.end_date"
                type="date"
                class="w-full px-4 py-2.5 rounded-xl bg-brand-charcoal-dark border border-brand-charcoal-light/45 hover:border-brand-orange/30 focus:border-brand-orange text-xs font-semibold outline-none transition-all text-gray-300"
              />
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-[10px] font-extrabold uppercase tracking-widest text-gray-400 mb-2">Budget Allocation (Rp)</label>
              <input 
                v-model="newProj.budget"
                type="number"
                step="0.01"
                placeholder="0.00"
                class="w-full px-4 py-2.5 rounded-xl bg-brand-charcoal-dark border border-brand-charcoal-light/45 hover:border-brand-orange/30 focus:border-brand-orange text-sm font-semibold outline-none transition-all text-white"
              />
            </div>
            <div>
              <label class="block text-[10px] font-extrabold uppercase tracking-widest text-gray-400 mb-2">Revenue Goal (Rp)</label>
              <input 
                v-model="newProj.revenue"
                type="number"
                step="0.01"
                placeholder="0.00"
                class="w-full px-4 py-2.5 rounded-xl bg-brand-charcoal-dark border border-brand-charcoal-light/45 hover:border-brand-orange/30 focus:border-brand-orange text-sm font-semibold outline-none transition-all text-white"
              />
            </div>
          </div>

          <div class="flex items-center justify-end gap-3 pt-3">
            <button 
              type="button"
              @click="showAddModal = false"
              class="px-4 py-2.5 rounded-xl border border-brand-charcoal-light/40 text-xs font-bold text-gray-400 hover:text-white hover:bg-brand-charcoal-light/10 transition-all"
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
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useAuthStore } from '../store/auth'

const auth = useAuthStore()
const projects = ref([])
const customers = ref([])
const users = ref([])

const loading = ref(true)
const viewMode = ref('board')
const showAddModal = ref(false)

const newProj = ref({
  title: '',
  customer_id: '',
  assigned_to_id: null,
  start_date: '',
  end_date: '',
  budget: 0,
  revenue: 0,
  status: 'inquiry',
  quotation_status: 'draft'
})

const columns = [
  { status: 'inquiry', name: 'Inquiry', bullet: 'bg-brand-orange', next: 'quotation' },
  { status: 'quotation', name: 'Quotation Out', bullet: 'bg-yellow-500', prev: 'inquiry', next: 'negotiation' },
  { status: 'negotiation', name: 'Negotiation', bullet: 'bg-brand-blue', prev: 'quotation', next: 'confirmed' },
  { status: 'confirmed', name: 'Confirmed', bullet: 'bg-purple-500', prev: 'negotiation', next: 'ongoing' },
  { status: 'ongoing', name: 'Ongoing Ops', bullet: 'bg-orange-500', prev: 'confirmed', next: 'completed' },
  { status: 'completed', name: 'Completed', bullet: 'bg-brand-emerald', prev: 'ongoing' },
  { status: 'canceled', name: 'Canceled', bullet: 'bg-red-500' }
]

const fetchData = async () => {
  try {
    const [projRes, custRes, usersRes] = await Promise.all([
      axios.get('/api/v1/projects'),
      axios.get('/api/v1/customers'),
      axios.get('/api/v1/auth/users')
    ])
    projects.value = projRes.data
    customers.value = custRes.data
    users.value = usersRes.data
  } catch (err) {
    console.error('Failed to load project database', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchData()
})

const getProjectsByStatus = (status) => {
  return projects.value.filter(p => p.status === status)
}

const formatMoney = (val) => {
  return 'Rp ' + Number(val || 0).toLocaleString('id-ID', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  })
}

const getStatusStyles = (status) => {
  if (status === 'inquiry') return 'bg-brand-orange/15 text-brand-orange border border-brand-orange/20'
  if (status === 'quotation') return 'bg-yellow-500/10 text-yellow-500'
  if (status === 'negotiation') return 'bg-brand-blue/10 text-brand-blue'
  if (status === 'confirmed') return 'bg-purple-500/10 text-purple-500'
  if (status === 'ongoing') return 'bg-orange-500/10 text-orange-400'
  if (status === 'completed') return 'bg-brand-emerald/15 text-brand-emerald border border-brand-emerald/20'
  return 'bg-red-500/10 text-red-400'
}

const getQuotationStyles = (status) => {
  if (status === 'approved') return 'bg-brand-emerald/10 text-brand-emerald'
  if (status === 'rejected') return 'bg-red-500/10 text-red-400'
  if (status === 'sent') return 'bg-brand-blue/10 text-brand-blue'
  return 'bg-brand-charcoal-light text-gray-300'
}

const openAddModal = () => {
  if (customers.value.length === 0) {
    alert('Please register at least one client account in CRM before starting a project!')
    return
  }
  showAddModal.value = true
}

const saveProject = async () => {
  try {
    const payload = { ...newProj.value }
    if (!payload.start_date) delete payload.start_date
    if (!payload.end_date) delete payload.end_date

    const response = await axios.post('/api/v1/projects', payload)
    
    // Add relation metadata manually to prevent reload
    const client = customers.value.find(c => c.id === response.data.customer_id)
    const pm = users.value.find(u => u.id === response.data.assigned_to_id)
    response.data.customer = client
    response.data.assigned_to = pm
    
    projects.value.push(response.data)
    showAddModal.value = false
    newProj.value = {
      title: '',
      customer_id: '',
      assigned_to_id: null,
      start_date: '',
      end_date: '',
      budget: 0,
      revenue: 0,
      status: 'inquiry',
      quotation_status: 'draft'
    }
  } catch (err) {
    alert(err.response?.data?.detail || 'Failed to create project')
  }
}

const transitionStatus = async (proj, newStatus) => {
  try {
    const response = await axios.post(`/api/v1/projects/${proj.id}/transition?new_status=${newStatus}`)
    proj.status = response.data.status
  } catch (err) {
    alert('Failed to transition status')
  }
}

const archiveProject = async (id) => {
  if (!confirm('Are you sure you want to archive this project?')) return
  try {
    await axios.delete(`/api/v1/projects/${id}`)
    projects.value = projects.value.filter(p => p.id !== id)
  } catch (err) {
    alert('Failed to archive project')
  }
}
</script>
