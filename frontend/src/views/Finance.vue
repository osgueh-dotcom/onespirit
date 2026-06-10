<template>
  <div class="space-y-6">
    <!-- Header -->
    <AppPageHeader 
      title="Finance Tracking" 
      subtitle="Kelola penagihan invoice klien, pencatatan receipt pembayaran, dan status outstanding keuangan proyek."
    />

    <!-- Top toolbar filter and actions -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 select-none">
      <div class="flex items-center gap-3">
        <span class="text-xs font-bold uppercase tracking-widest text-gray-400">View</span>
        <div class="flex rounded-xl p-0.5 bg-brand-charcoal border border-brand-charcoal-light/35">
          <button 
            @click="activeSubTab = 'invoices'" 
            class="px-4 py-2 rounded-lg text-xs font-bold transition-all"
            :class="activeSubTab === 'invoices' ? 'bg-brand-orange text-white' : 'text-gray-400 hover:text-white'"
          >
            Billing Invoices
          </button>
          <button 
            @click="activeSubTab = 'payments'" 
            class="px-4 py-2 rounded-lg text-xs font-bold transition-all"
            :class="activeSubTab === 'payments' ? 'bg-brand-orange text-white' : 'text-gray-400 hover:text-white'"
          >
            Payment Collection Receipts
          </button>
        </div>
      </div>

      <button 
        v-if="auth.hasPermission('finance:write') && activeSubTab === 'invoices'"
        @click="showAddInvoiceModal = true"
        class="px-4 py-2.5 rounded-xl bg-gradient-to-r from-brand-orange to-brand-orange-light text-white font-bold text-xs shadow-lg hover:shadow-brand-orange/20 transition-all select-none w-full sm:w-auto"
      >
        + Generate New Invoice
      </button>

      <button 
        v-if="auth.hasPermission('finance:write') && activeSubTab === 'payments'"
        @click="showAddPaymentModal = true"
        class="px-4 py-2.5 rounded-xl bg-gradient-to-r from-brand-orange to-brand-orange-light text-white font-bold text-xs shadow-lg hover:shadow-brand-orange/20 transition-all select-none w-full sm:w-auto"
      >
        + Record Payment Receipt
      </button>
    </div>

    <!-- Data loading indicator -->
    <AppLoadingState v-if="loading" message="Loading ledger catalog..." />

    <div v-else class="space-y-6 animate-fade-in">
      <!-- INVOICES SUB-TAB -->
      <div v-if="activeSubTab === 'invoices'">
        <!-- Desktop Table View -->
        <div class="hidden md:block glass-panel overflow-hidden border border-brand-charcoal-light/30">
          <div class="overflow-x-auto min-w-full">
            <table class="min-w-full text-left divide-y divide-brand-charcoal-light/20 text-xs">
              <thead class="bg-brand-charcoal/50 text-[10px] font-extrabold uppercase tracking-widest text-gray-400 select-none">
                <tr>
                  <th class="px-6 py-4">Invoice Number</th>
                  <th class="px-6 py-4">Project Name</th>
                  <th class="px-6 py-4">Issue Date</th>
                  <th class="px-6 py-4">Due Date</th>
                  <th class="px-6 py-4">Amount</th>
                  <th class="px-6 py-4">Billing Status</th>
                  <th class="px-6 py-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-brand-charcoal-light/10 font-medium">
                <tr v-if="invoices.length === 0">
                  <td colspan="7" class="px-6 py-12 text-center text-gray-500 font-semibold select-none">
                    No invoices generated in current ledger.
                  </td>
                </tr>
                <tr 
                  v-for="inv in invoices" 
                  :key="inv.id"
                  class="hover:bg-brand-charcoal-light/10 transition-colors"
                >
                  <td class="px-6 py-4 font-bold text-white tracking-wide text-sm">{{ inv.invoice_number }}</td>
                  <td class="px-6 py-4 text-white font-semibold">
                    {{ getProjectTitle(inv.project_id) }}
                  </td>
                  <td class="px-6 py-4 text-gray-400">{{ inv.issue_date }}</td>
                  <td class="px-6 py-4 text-gray-400">{{ inv.due_date }}</td>
                  <td class="px-6 py-4 font-bold text-brand-emerald">{{ formatMoney(inv.amount) }}</td>
                  <td class="px-6 py-4 select-none">
                    <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider" :class="getInvoiceStatusStyles(inv.status)">
                      {{ inv.status }}
                    </span>
                  </td>
                  <td class="px-6 py-4 text-right select-none space-x-2.5">
                    <button 
                      v-if="auth.hasPermission('finance:write')"
                      @click="archiveInvoice(inv.id)"
                      class="px-2.5 py-1 text-[10px] font-bold text-red-400 bg-red-500/10 rounded hover:bg-red-500/20 transition-all"
                    >
                      Void Invoice
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Mobile Card List View -->
        <div class="block md:hidden space-y-4">
          <div v-if="invoices.length === 0" class="py-12 text-center text-gray-500 font-semibold select-none">
            No invoices generated in current ledger.
          </div>
          <div 
            v-for="inv in invoices" 
            :key="inv.id"
            class="glass-panel p-4 border border-brand-charcoal-light/30 space-y-3 bg-brand-charcoal/40"
          >
            <div class="flex items-center justify-between border-b border-brand-charcoal-light/10 pb-2">
              <span class="font-bold text-white tracking-wide text-xs select-all">{{ inv.invoice_number }}</span>
              <span class="px-2 py-0.5 rounded text-[9px] font-bold uppercase tracking-wider" :class="getInvoiceStatusStyles(inv.status)">
                {{ inv.status }}
              </span>
            </div>
            <div>
              <h4 class="text-white font-bold text-sm">{{ getProjectTitle(inv.project_id) }}</h4>
              <p class="text-brand-emerald font-bold font-mono mt-1">{{ formatMoney(inv.amount) }}</p>
            </div>
            <div class="grid grid-cols-2 gap-2 bg-black/20 p-2 rounded-xl text-[10px] text-gray-400 font-semibold">
              <div>
                <p class="text-gray-500 text-[8px] uppercase tracking-wider">Issue Date</p>
                <p class="text-white">{{ inv.issue_date }}</p>
              </div>
              <div>
                <p class="text-gray-500 text-[8px] uppercase tracking-wider">Due Date</p>
                <p class="text-white">{{ inv.due_date }}</p>
              </div>
            </div>
            <div class="flex justify-end pt-1" v-if="auth.hasPermission('finance:write')">
              <button 
                @click="archiveInvoice(inv.id)"
                class="px-3 py-1.5 text-[10px] font-bold text-red-400 bg-red-500/10 rounded-xl hover:bg-red-500/20 transition-all"
              >
                Void Invoice
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- PAYMENT COLLECTIONS SUB-TAB -->
      <div v-else>
        <!-- Desktop Table View -->
        <div class="hidden md:block glass-panel overflow-hidden border border-brand-charcoal-light/30">
          <div class="overflow-x-auto min-w-full">
            <table class="min-w-full text-left divide-y divide-brand-charcoal-light/20 text-xs">
              <thead class="bg-brand-charcoal/50 text-[10px] font-extrabold uppercase tracking-widest text-gray-400 select-none">
                <tr>
                  <th class="px-6 py-4">Receipt ID</th>
                  <th class="px-6 py-4">Linked Invoice</th>
                  <th class="px-6 py-4">Collection Date</th>
                  <th class="px-6 py-4">Reference / Receipt Number</th>
                  <th class="px-6 py-4">Paid Amount</th>
                  <th class="px-6 py-4">Status</th>
                  <th class="px-6 py-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-brand-charcoal-light/10 font-medium">
                <tr v-if="payments.length === 0">
                  <td colspan="7" class="px-6 py-12 text-center text-gray-500 font-semibold select-none">
                    No payment collections logged.
                  </td>
                </tr>
                <tr 
                  v-for="pay in payments" 
                  :key="pay.id"
                  class="hover:bg-brand-charcoal-light/10 transition-colors"
                >
                  <td class="px-6 py-4 font-bold text-white tracking-wide text-xs truncate max-w-[80px]">{{ pay.id }}</td>
                  <td class="px-6 py-4 font-bold text-brand-orange">
                    {{ getInvoiceNumber(pay.invoice_id) }}
                  </td>
                  <td class="px-6 py-4 text-gray-400">{{ pay.payment_date }}</td>
                  <td class="px-6 py-4 text-gray-400 font-bold">{{ pay.reference_number || '-' }}</td>
                  <td class="px-6 py-4 font-bold text-brand-emerald">{{ formatMoney(pay.amount) }}</td>
                  <td class="px-6 py-4 select-none">
                    <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider" :class="getPaymentStatusStyles(pay.status)">
                      {{ pay.status }}
                    </span>
                  </td>
                  <td class="px-6 py-4 text-right select-none space-x-2.5">
                    <button 
                      v-if="auth.hasPermission('finance:write')"
                      @click="archivePayment(pay)"
                      class="px-2.5 py-1 text-[10px] font-bold text-red-400 bg-red-500/10 rounded hover:bg-red-500/20 transition-all"
                    >
                      Delete Receipt
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Mobile Card List View -->
        <div class="block md:hidden space-y-4">
          <div v-if="payments.length === 0" class="py-12 text-center text-gray-500 font-semibold select-none">
            No payment collections logged.
          </div>
          <div 
            v-for="pay in payments" 
            :key="pay.id"
            class="glass-panel p-4 border border-brand-charcoal-light/30 space-y-3 bg-brand-charcoal/40"
          >
            <div class="flex items-center justify-between border-b border-brand-charcoal-light/10 pb-2">
              <span class="font-mono text-[9px] text-gray-400">ID: {{ pay.id.slice(0, 8) }}...</span>
              <span class="px-2 py-0.5 rounded text-[9px] font-bold uppercase tracking-wider" :class="getPaymentStatusStyles(pay.status)">
                {{ pay.status }}
              </span>
            </div>
            <div>
              <p class="text-[9px] text-gray-500 uppercase font-black">Linked Invoice</p>
              <p class="text-brand-orange font-bold text-sm select-all">{{ getInvoiceNumber(pay.invoice_id) }}</p>
              <p class="text-brand-emerald font-bold font-mono text-sm mt-1">{{ formatMoney(pay.amount) }}</p>
            </div>
            <div class="grid grid-cols-2 gap-2 bg-black/20 p-2 rounded-xl text-[10px] text-gray-400 font-semibold">
              <div>
                <p class="text-gray-500 text-[8px] uppercase tracking-wider">Collection Date</p>
                <p class="text-white">{{ pay.payment_date }}</p>
              </div>
              <div>
                <p class="text-gray-500 text-[8px] uppercase tracking-wider">Ref Number</p>
                <p class="text-white">{{ pay.reference_number || '-' }}</p>
              </div>
            </div>
            <div class="flex justify-end pt-1" v-if="auth.hasPermission('finance:write')">
              <button 
                @click="archivePayment(pay)"
                class="px-3 py-1.5 text-[10px] font-bold text-red-400 bg-red-500/10 rounded-xl hover:bg-red-500/20 transition-all"
              >
                Delete Receipt
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Generate Invoice Modal -->
    <div v-if="showAddInvoiceModal" class="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 select-none">
      <div class="bg-brand-charcoal border border-brand-charcoal-light/35 rounded-3xl w-full max-w-lg shadow-2xl p-6 relative overflow-y-auto max-h-[90vh]">
        <h3 class="text-base font-bold text-white tracking-wide mb-5">Generate Billing Invoice</h3>
        <form @submit.prevent="saveInvoice" class="space-y-4">
          <div>
            <label class="block text-[10px] font-extrabold uppercase tracking-widest text-gray-400 mb-2">Project Association *</label>
            <select 
              v-model="newInvoice.project_id"
              required
              class="w-full px-4 py-2.5 rounded-xl bg-brand-charcoal-dark border border-brand-charcoal-light/45 hover:border-brand-orange/30 focus:border-brand-orange text-xs font-semibold outline-none transition-all text-gray-300"
            >
              <option value="" disabled>Select Project</option>
              <option v-for="p in projects" :key="p.id" :value="p.id">{{ p.title }} (Client: {{ p.customer?.company_name }})</option>
            </select>
          </div>

          <div>
            <label class="block text-[10px] font-extrabold uppercase tracking-widest text-gray-400 mb-2">Invoice Number Reference</label>
            <input v-model="newInvoice.invoice_number" type="text" required placeholder="e.g. OSA-2026-0001" class="w-full px-4 py-2.5 rounded-xl bg-brand-charcoal-dark border border-brand-charcoal-light/45 text-sm font-semibold outline-none text-white focus:border-brand-orange" />
          </div>

          <div>
            <label class="block text-[10px] font-extrabold uppercase tracking-widest text-gray-400 mb-2">Billing Amount (Rp)</label>
            <input v-model="newInvoice.amount" type="number" step="0.01" required placeholder="0.00" class="w-full px-4 py-2.5 rounded-xl bg-brand-charcoal-dark border border-brand-charcoal-light/45 text-sm font-semibold outline-none text-white focus:border-brand-orange" />
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-[10px] font-extrabold uppercase tracking-widest text-gray-400 mb-2">Billing Date</label>
              <input v-model="newInvoice.issue_date" type="date" required class="w-full px-4 py-2.5 rounded-xl bg-brand-charcoal-dark border border-brand-charcoal-light/45 text-xs font-semibold text-gray-300 outline-none focus:border-brand-orange" />
            </div>
            <div>
              <label class="block text-[10px] font-extrabold uppercase tracking-widest text-gray-400 mb-2">Due Date</label>
              <input v-model="newInvoice.due_date" type="date" required class="w-full px-4 py-2.5 rounded-xl bg-brand-charcoal-dark border border-brand-charcoal-light/45 text-xs font-semibold text-gray-300 outline-none focus:border-brand-orange" />
            </div>
          </div>

          <div class="flex items-center justify-end gap-3 pt-3">
            <button type="button" @click="showAddInvoiceModal = false" class="px-4 py-2.5 rounded-xl border border-brand-charcoal-light/40 text-xs font-bold text-gray-400 hover:text-white transition-all">Cancel</button>
            <button type="submit" class="px-5 py-2.5 rounded-xl bg-gradient-to-r from-brand-orange to-brand-orange-light text-white font-bold text-xs shadow-lg">Issue Invoice</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Record Payment Modal -->
    <div v-if="showAddPaymentModal" class="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 select-none">
      <div class="bg-brand-charcoal border border-brand-charcoal-light/35 rounded-3xl w-full max-w-lg shadow-2xl p-6 relative overflow-y-auto max-h-[90vh]">
        <h3 class="text-base font-bold text-white tracking-wide mb-5">Record Payment Receipt</h3>
        <form @submit.prevent="savePayment" class="space-y-4">
          <div>
            <label class="block text-[10px] font-extrabold uppercase tracking-widest text-gray-400 mb-2">Billing Invoice Reference *</label>
            <select 
              v-model="newPayment.invoice_id"
              required
              class="w-full px-4 py-2.5 rounded-xl bg-brand-charcoal-dark border border-brand-charcoal-light/45 hover:border-brand-orange/30 focus:border-brand-orange text-xs font-semibold outline-none transition-all text-gray-300"
            >
              <option value="" disabled>Select Invoice</option>
              <option v-for="i in invoices" :key="i.id" :value="i.id">{{ i.invoice_number }} (Amt: {{ formatMoney(i.amount) }} - Status: {{ i.status }})</option>
            </select>
          </div>

          <div>
            <label class="block text-[10px] font-extrabold uppercase tracking-widest text-gray-400 mb-2">Paid Amount Collection (Rp)</label>
            <input v-model="newPayment.amount" type="number" step="0.01" required placeholder="0.00" class="w-full px-4 py-2.5 rounded-xl bg-brand-charcoal-dark border border-brand-charcoal-light/45 text-sm font-semibold outline-none text-white focus:border-brand-orange" />
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-[10px] font-extrabold uppercase tracking-widest text-gray-400 mb-2">Collection Date</label>
              <input v-model="newPayment.payment_date" type="date" required class="w-full px-4 py-2.5 rounded-xl bg-brand-charcoal-dark border border-brand-charcoal-light/45 text-xs font-semibold text-gray-300 outline-none focus:border-brand-orange" />
            </div>
            <div>
              <label class="block text-[10px] font-extrabold uppercase tracking-widest text-gray-400 mb-2">Bank Reference Number</label>
              <input v-model="newPayment.reference_number" type="text" placeholder="e.g. TRF-12345" class="w-full px-4 py-2.5 rounded-xl bg-brand-charcoal-dark border border-brand-charcoal-light/45 text-sm font-semibold outline-none text-white focus:border-brand-orange" />
            </div>
          </div>

          <div class="flex items-center justify-end gap-3 pt-3">
            <button type="button" @click="showAddPaymentModal = false" class="px-4 py-2.5 rounded-xl border border-brand-charcoal-light/40 text-xs font-bold text-gray-400 hover:text-white transition-all">Cancel</button>
            <button type="submit" class="px-5 py-2.5 rounded-xl bg-gradient-to-r from-brand-orange to-brand-orange-light text-white font-bold text-xs shadow-lg">Link Receipt</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useAuthStore } from '../store/auth'

// Shared UI Components
import AppPageHeader from '../components/ui/AppPageHeader.vue'
import AppLoadingState from '../components/ui/AppLoadingState.vue'

const auth = useAuthStore()

const invoices = ref([])
const payments = ref([])
const projects = ref([])

const loading = ref(true)
const activeSubTab = ref('invoices')

const showAddInvoiceModal = ref(false)
const showAddPaymentModal = ref(false)

const newInvoice = ref({
  project_id: '',
  invoice_number: '',
  amount: 0,
  issue_date: '',
  due_date: '',
  status: 'unpaid',
  notes: ''
})

const newPayment = ref({
  invoice_id: '',
  amount: 0,
  payment_date: '',
  reference_number: '',
  proof_url: '',
  status: 'approved'
})

const fetchData = async () => {
  try {
    const [invRes, custPayRes, projRes] = await Promise.all([
      axios.get('/api/v1/invoices'),
      axios.get('/api/v1/invoices'), // Need payment details. In FastAPI, Payment is separate, let's load all approved payments or invoices which aggregates payments
      axios.get('/api/v1/projects')
    ])
    invoices.value = invRes.data
    projects.value = projRes.data
    
    // Flat map payments from invoices for collection list
    const mappedPayments = []
    invRes.data.forEach(inv => {
      inv.payments.forEach(p => {
        mappedPayments.push({
          ...p,
          invoice_number: inv.invoice_number
        })
      })
    })
    payments.value = mappedPayments
  } catch (err) {
    console.error('Failed to load financial records', err)
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

const getProjectTitle = (id) => {
  const p = projects.value.find(proj => proj.id === id)
  return p ? p.title : 'OSA Project'
}

const getInvoiceNumber = (id) => {
  const inv = invoices.value.find(i => i.id === id)
  return inv ? inv.invoice_number : 'OSA-INV'
}

const getInvoiceStatusStyles = (status) => {
  if (status === 'paid') return 'bg-brand-emerald/15 text-brand-emerald border border-brand-emerald/20'
  if (status === 'overdue') return 'bg-red-500/15 text-red-400 border border-red-500/20'
  if (status === 'partial') return 'bg-brand-blue/15 text-brand-blue border border-brand-blue/20'
  return 'bg-brand-orange/15 text-brand-orange border border-brand-orange/20'
}

const getPaymentStatusStyles = (status) => {
  if (status === 'approved') return 'bg-brand-emerald/10 text-brand-emerald'
  if (status === 'rejected') return 'bg-red-500/10 text-red-400'
  return 'bg-brand-orange/10 text-brand-orange'
}

const saveInvoice = async () => {
  try {
    const response = await axios.post('/api/v1/invoices', newInvoice.value)
    invoices.value.push(response.data)
    showAddInvoiceModal.value = false
    newInvoice.value = { project_id: '', invoice_number: '', amount: 0, issue_date: '', due_date: '', status: 'unpaid', notes: '' }
  } catch (err) {
    alert(err.response?.data?.detail || 'Failed to issue invoice')
  }
}

const savePayment = async () => {
  try {
    const response = await axios.post('/api/v1/payments', newPayment.value)
    
    // Add relation metadata
    const matchedInvoice = invoices.value.find(i => i.id === response.data.invoice_id)
    response.data.invoice_number = matchedInvoice ? matchedInvoice.invoice_number : 'OSA-INV'
    payments.value.push(response.data)
    
    // Recalculate invoice status locally
    if (matchedInvoice) {
      // Refresh database records in the backend
      const refreshRes = await axios.get('/api/v1/invoices')
      invoices.value = refreshRes.data
    }
    
    showAddPaymentModal.value = false
    newPayment.value = { invoice_id: '', amount: 0, payment_date: '', reference_number: '', proof_url: '', status: 'approved' }
  } catch (err) {
    alert(err.response?.data?.detail || 'Failed to save payment collection')
  }
}

const archiveInvoice = async (id) => {
  if (!confirm('Are you sure you want to void this invoice? This action soft deletes payments associated.')) return
  try {
    await axios.delete(`/api/v1/invoices/${id}`)
    invoices.value = invoices.value.filter(i => i.id !== id)
    payments.value = payments.value.filter(p => p.invoice_id !== id)
  } catch (err) {
    alert('Failed to void invoice')
  }
}

const archivePayment = async (pay) => {
  if (!confirm('Are you sure you want to delete this payment collection receipt?')) return
  try {
    await axios.delete(`/api/v1/payments/${pay.id}`)
    payments.value = payments.value.filter(p => p.id !== pay.id)
    // Refresh local invoices status from server
    const refreshRes = await axios.get('/api/v1/invoices')
    invoices.value = refreshRes.data
  } catch (err) {
    alert('Failed to delete payment receipt')
  }
}
</script>

<style scoped>
.glass-panel {
  background: rgba(26, 32, 44, 0.75);
  backdrop-filter: blur(12px);
  border-radius: 1.25rem;
}
</style>
