<template>
  <div class="app-page">
    <!-- Header -->
    <AppPageHeader 
      title="CRM Client Directory" 
      subtitle="Kelola data akun klien corporate, klasifikasi partner, dan point of contact (POC) operasional event."
    />

    <!-- Top toolbar actions -->
    <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4 select-none">
      <div class="flex flex-col sm:flex-row sm:items-center gap-3 flex-1">
        <div class="relative w-full sm:max-w-md">
          <input
            v-model="crmSearchQuery"
            type="search"
            placeholder="Cari perusahaan, PIC, email, atau nomor telepon..."
            class="app-form-control pr-9 text-xs"
          />
          <button
            v-if="crmSearchQuery"
            type="button"
            @click="clearCrmSearch"
            class="absolute right-2 top-1/2 -translate-y-1/2 rounded-lg px-1.5 py-0.5 text-[10px] font-black text-muted-theme transition-colors hover:bg-brand-orange/10 hover:text-brand-orange"
            title="Bersihkan pencarian"
          >
            x
          </button>
        </div>
        <select 
          v-model="filterCategory"
          class="app-form-control w-full sm:w-auto text-xs"
        >
          <option value="">All Client Categories</option>
          <option value="Corporate">Corporate Accounts</option>
          <option value="Agency">Creative Agencies</option>
          <option value="Partner">Logistic Partners</option>
          <option value="Government">Government</option>
          <option value="School">Educational Institutes</option>
        </select>
      </div>

      <button 
        v-if="auth.hasPermission('crm:write')"
        @click="showAddModal = true"
        class="px-4 py-2.5 rounded-xl bg-gradient-to-r from-brand-orange to-brand-orange-light text-white font-bold text-xs shadow-lg hover:shadow-brand-orange/20 transition-all select-none w-full sm:w-auto text-center"
      >
        + Tambah Akun Klien Baru
      </button>
    </div>

    <!-- Accounts Grid -->
    <AppLoadingState v-if="loading" message="Memuat data CRM..." />

    <div v-else class="space-y-6 animate-fade-in">
      <!-- Desktop Table View -->
      <div class="hidden md:block glass-panel overflow-hidden border border-brand-charcoal-light/30">
        <div class="overflow-x-auto min-w-full">
          <table class="min-w-full text-left divide-y divide-brand-charcoal-light/20 text-xs">
            <thead class="app-table-header">
              <tr>
                <th class="px-6 py-4">Nama Perusahaan</th>
                <th class="px-6 py-4">Kategori</th>
                <th class="px-6 py-4">Alamat</th>
                <th class="px-6 py-4">Narahubung (POC)</th>
                <th class="px-6 py-4 text-right">Aksi</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-brand-charcoal-light/10">
              <tr v-if="filteredCustomers.length === 0">
                <td colspan="5" class="px-6 py-12 text-center app-empty-copy">
                  {{ crmEmptyMessage }}
                </td>
              </tr>
              <tr 
                v-for="cust in filteredCustomers" 
                :key="cust.id"
                class="app-table-row"
              >
                <td class="px-6 py-4 app-table-cell-strong tracking-wide text-sm">{{ cust.company_name }}</td>
                <td class="px-6 py-4 select-none">
                  <span class="px-2 py-0.5 rounded text-[10px] font-bold" :class="getCategoryStyles(cust.category)">
                    {{ cust.category }}
                  </span>
                </td>
                <td class="px-6 py-4 app-table-cell truncate max-w-xs font-medium">{{ cust.address || '-' }}</td>
                <td class="px-6 py-4">
                  <div v-if="cust.contacts?.length > 0" class="space-y-1">
                    <div v-for="c in cust.contacts.slice(0, 1)" :key="c.id" class="font-semibold text-main-theme">
                      {{ c.name }} <span class="text-[10px] text-brand-orange font-semibold">({{ c.position || 'POC' }})</span>
                    </div>
                    <span v-if="cust.contacts.length > 1" class="text-[10px] text-gray-500 font-bold block">
                      + {{ cust.contacts.length - 1 }} narahubung lainnya
                    </span>
                  </div>
                  <span v-else class="text-muted-theme font-bold italic">Belum ada kontak</span>
                </td>
                <td class="px-6 py-4 text-right select-none space-x-2.5">
                  <button 
                    @click="openContactDetails(cust)"
                    class="px-2.5 py-1 text-[10px] font-bold text-brand-blue bg-brand-blue/10 rounded hover:bg-brand-blue/20 transition-all"
                  >
                    Kelola Kontak
                  </button>
                  <button 
                    v-if="auth.hasPermission('crm:write')"
                    @click="deleteCustomer(cust.id)"
                    class="px-2.5 py-1 text-[10px] font-bold text-red-400 bg-red-500/10 rounded hover:bg-red-500/20 transition-all"
                  >
                    Deaktivasi
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Mobile Card List View -->
      <div class="block md:hidden space-y-4">
        <div v-if="filteredCustomers.length === 0" class="py-12 text-center app-empty-copy">
          {{ crmEmptyMessage }}
        </div>
        <div 
          v-for="cust in filteredCustomers" 
          :key="cust.id"
          class="glass-panel p-4 border border-panel-theme space-y-3 bg-surface-theme"
        >
          <div class="flex items-center justify-between border-b border-brand-charcoal-light/10 pb-2">
            <span class="font-bold text-main-theme tracking-wide text-sm">{{ cust.company_name }}</span>
            <span class="px-2 py-0.5 rounded text-[10px] font-bold" :class="getCategoryStyles(cust.category)">
              {{ cust.category }}
            </span>
          </div>
          <div>
            <p class="text-xs text-soft-theme font-medium">Alamat: {{ cust.address || '-' }}</p>
          </div>
          <div class="bg-surface-theme p-2.5 rounded-xl border border-panel-theme text-[11px] font-semibold space-y-1">
            <p class="text-muted-theme text-[8px] uppercase tracking-wider font-bold">Point of Contact</p>
            <div v-if="cust.contacts?.length > 0" class="space-y-1">
              <div v-for="c in cust.contacts" :key="c.id" class="text-main-theme">
                • {{ c.name }} <span class="text-[10px] text-brand-orange font-semibold">({{ c.position || 'POC' }})</span>
                <span class="text-[10px] text-muted-theme block pl-2" v-if="c.email || c.phone">{{ c.email || '-' }} | {{ c.phone || '-' }}</span>
              </div>
            </div>
            <span v-else class="text-muted-theme font-bold italic block">No contacts added</span>
          </div>
          <div class="flex justify-end gap-2 pt-1">
            <button 
              @click="openContactDetails(cust)"
              class="px-3 py-1.5 text-xs font-bold text-brand-blue bg-brand-blue/10 rounded-xl hover:bg-brand-blue/20 transition-all"
            >
              Manage Contacts
            </button>
            <button 
              v-if="auth.hasPermission('crm:write')"
              @click="deleteCustomer(cust.id)"
              class="px-3 py-1.5 text-xs font-bold text-red-400 bg-red-500/10 rounded-xl hover:bg-red-500/20 transition-all"
            >
              Deactivate
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Client Account Creation Modal -->
    <div v-if="showAddModal" class="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 select-none">
      <div class="bg-brand-charcoal border border-brand-charcoal-light/35 rounded-3xl w-full max-w-lg shadow-2xl p-6 relative overflow-y-auto max-h-[90vh]">
        <h3 class="text-base font-bold text-white tracking-wide mb-5">Register Client Profile</h3>
        
        <form @submit.prevent="saveCustomer" class="space-y-4">
          <div>
            <label class="block text-[10px] font-extrabold uppercase tracking-widest text-gray-400 mb-2">Company Name</label>
            <input 
              v-model="newCust.company_name"
              type="text" 
              required
              placeholder="e.g. Google Indonesia"
              class="w-full px-4 py-2.5 rounded-xl bg-brand-charcoal-dark border border-brand-charcoal-light/45 hover:border-brand-orange/30 focus:border-brand-orange text-sm font-semibold outline-none transition-all text-white"
            />
          </div>

          <div>
            <label class="block text-[10px] font-extrabold uppercase tracking-widest text-gray-400 mb-2">Account Classification</label>
            <select 
              v-model="newCust.category"
              required
              class="w-full px-4 py-2.5 rounded-xl bg-brand-charcoal-dark border border-brand-charcoal-light/45 hover:border-brand-orange/30 focus:border-brand-orange text-sm font-semibold outline-none transition-all text-gray-300"
            >
              <option value="Corporate">Corporate Account</option>
              <option value="Agency">Creative Agency</option>
              <option value="Partner">Logistic Partner</option>
              <option value="Government">Government / BUMN</option>
              <option value="School">Educational Institute</option>
            </select>
          </div>

          <div>
            <label class="block text-[10px] font-extrabold uppercase tracking-widest text-gray-400 mb-2">Headquarters Address</label>
            <textarea 
              v-model="newCust.address"
              rows="3"
              placeholder="Full mailing address details..."
              class="w-full px-4 py-2.5 rounded-xl bg-brand-charcoal-dark border border-brand-charcoal-light/45 hover:border-brand-orange/30 focus:border-brand-orange text-sm font-semibold outline-none transition-all text-white"
            ></textarea>
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
              Save Account
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Point of Contact Modal -->
    <div v-if="showContactModal" class="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 select-none">
      <div class="bg-brand-charcoal border border-brand-charcoal-light/35 rounded-3xl w-full max-w-2xl shadow-2xl p-6 relative overflow-y-auto max-h-[90vh]">
        <h3 class="text-base font-bold text-white tracking-wide mb-4">
          Point of Contacts: <span class="text-brand-orange">{{ activeCust?.company_name }}</span>
        </h3>

        <!-- Contact List -->
        <div class="max-h-60 overflow-y-auto space-y-2 mb-6">
          <div v-if="activeCust?.contacts?.length === 0" class="p-4 bg-brand-charcoal-light/10 rounded-2xl text-center text-xs font-semibold text-gray-500">
            No contacts recorded for this client.
          </div>
          <div 
            v-for="c in activeCust?.contacts" 
            :key="c.id"
            class="p-4 bg-brand-charcoal-light/20 border border-brand-charcoal-light/10 rounded-2xl flex items-center justify-between text-xs font-medium"
          >
            <div>
              <p class="font-bold text-white">{{ c.name }} <span class="text-[10px] text-brand-orange font-semibold">({{ c.position || 'POC' }})</span></p>
              <p class="text-gray-400 mt-1">Email: {{ c.email || '-' }} | Phone: {{ c.phone || '-' }}</p>
            </div>
            <button 
              v-if="auth.hasPermission('crm:write')"
              @click="deleteContact(c.id)"
              class="px-2 py-1 text-[10px] font-bold text-red-400 bg-red-500/10 rounded hover:bg-red-500/20 transition-all"
            >
              Delete
            </button>
          </div>
        </div>

        <!-- Add Contact Form -->
        <div v-if="auth.hasPermission('crm:write')" class="border-t border-brand-charcoal-light/30 pt-4">
          <h4 class="text-xs font-bold text-white uppercase tracking-wider mb-3">Add New Point of Contact</h4>
          <form @submit.prevent="saveContact" class="grid grid-cols-2 gap-3">
            <div class="col-span-2">
              <input 
                v-model="newContact.name" 
                type="text" 
                required
                placeholder="POC Name *"
                class="w-full px-4 py-2.5 rounded-xl bg-brand-charcoal-dark border border-brand-charcoal-light/45 text-xs font-semibold outline-none text-white placeholder-gray-500"
              />
            </div>
            <div>
              <input 
                v-model="newContact.email" 
                type="email" 
                placeholder="Email Address"
                class="w-full px-4 py-2.5 rounded-xl bg-brand-charcoal-dark border border-brand-charcoal-light/45 text-xs font-semibold outline-none text-white placeholder-gray-500"
              />
            </div>
            <div>
              <input 
                v-model="newContact.phone" 
                type="text" 
                placeholder="Phone Number"
                class="w-full px-4 py-2.5 rounded-xl bg-brand-charcoal-dark border border-brand-charcoal-light/45 text-xs font-semibold outline-none text-white placeholder-gray-500"
              />
            </div>
            <div class="col-span-2">
              <input 
                v-model="newContact.position" 
                type="text" 
                placeholder="Position / Title (e.g. Marketing Lead)"
                class="w-full px-4 py-2.5 rounded-xl bg-brand-charcoal-dark border border-brand-charcoal-light/45 text-xs font-semibold outline-none text-white placeholder-gray-500"
              />
            </div>
            <div class="col-span-2 flex items-center justify-end gap-3 mt-2">
              <button 
                type="button"
                @click="showContactModal = false"
                class="px-4 py-2 rounded-xl border border-brand-charcoal-light/40 text-xs font-bold text-gray-400 hover:text-white transition-all"
              >
                Close
              </button>
              <button 
                type="submit"
                class="px-4 py-2 rounded-xl bg-brand-orange text-white font-bold text-xs transition-all"
              >
                + Link Contact
              </button>
            </div>
          </form>
        </div>
        <div v-else class="flex justify-end pt-2">
          <button 
            @click="showContactModal = false"
            class="px-4 py-2 rounded-xl bg-brand-charcoal-light text-white font-bold text-xs"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useAuthStore } from '../store/auth'
import { useUiStore } from '../store/ui'

// Shared UI Components
import AppPageHeader from '../components/ui/AppPageHeader.vue'
import AppLoadingState from '../components/ui/AppLoadingState.vue'

const auth = useAuthStore()
const ui = useUiStore()

const getApiErrorMessage = (err, fallback) => {
  const detail = err.response?.data?.detail
  if (typeof detail === 'string') return detail
  if (detail?.message && typeof detail.message === 'string') return detail.message
  return fallback
}

const customers = ref([])
const loading = ref(true)

const filterCategory = ref('')
const crmSearchQuery = ref('')
const showAddModal = ref(false)
const showContactModal = ref(false)

const activeCust = ref(null)

const newCust = ref({
  company_name: '',
  category: 'Corporate',
  address: '',
  notes: ''
})

const newContact = ref({
  name: '',
  email: '',
  phone: '',
  position: ''
})

const fetchCustomers = async () => {
  try {
    const response = await axios.get('/api/v1/customers')
    customers.value = response.data
  } catch (err) {
    console.error('Failed to load customers', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchCustomers()
})

const filteredCustomers = computed(() => {
  const query = crmSearchQuery.value.trim().toLowerCase()
  return customers.value.filter(customer => {
    if (filterCategory.value && customer.category !== filterCategory.value) return false
    if (!query) return true

    const contactsText = (customer.contacts || []).map(contact => [
      contact.name,
      contact.email,
      contact.phone,
      contact.whatsapp,
      contact.position
    ].filter(Boolean).join(' ')).join(' ')

    return [
      customer.company_name,
      customer.category,
      customer.status,
      customer.address,
      contactsText
    ].filter(Boolean).join(' ').toLowerCase().includes(query)
  })
})

const crmEmptyMessage = computed(() => {
  return crmSearchQuery.value.trim()
    ? 'Tidak ada data klien/kontak yang cocok.'
    : 'Tidak ada akun klien yang cocok dengan kriteria filter.'
})

const clearCrmSearch = () => {
  crmSearchQuery.value = ''
}

const getCategoryStyles = (cat) => {
  if (cat === 'Corporate') return 'bg-brand-orange/10 text-brand-orange'
  if (cat === 'Agency') return 'bg-brand-blue/10 text-brand-blue'
  if (cat === 'Partner') return 'bg-brand-emerald/10 text-brand-emerald'
  return 'bg-brand-charcoal-light text-gray-300'
}

const saveCustomer = async () => {
  try {
    const response = await axios.post('/api/v1/customers', newCust.value)
    customers.value.push(response.data)
    showAddModal.value = false
    newCust.value = { company_name: '', category: 'Corporate', address: '', notes: '' }
  } catch (err) {
    ui.error(getApiErrorMessage(err, 'Gagal mendaftarkan akun klien.'))
  }
}

const deleteCustomer = async (id) => {
  const confirmed = await ui.confirm ({
    title: 'Nonaktifkan Akun Klien?',
    message: 'Akun klien dan seluruh narahubung terkait akan dinonaktifkan dari CRM operasional.',
    confirmText: 'Nonaktifkan',
    cancelText: 'Batal',
    tone: 'danger'
  })
  if (!confirmed) return
  try {
    await axios.delete(`/api/v1/customers/${id}`)
    customers.value = customers.value.filter(c => c.id !== id)
  } catch {
    ui.error('Gagal menghapus akun klien.')
  }
}

const openContactDetails = (cust) => {
  activeCust.value = cust
  showContactModal.value = true
}

const saveContact = async () => {
  try {
    const payload = {
      ...newContact.value,
      customer_id: activeCust.value.id
    }
    // Clean empty optional fields to prevent validation issues
    if (!payload.email) delete payload.email
    if (!payload.phone) delete payload.phone
    if (!payload.position) delete payload.position

    const response = await axios.post('/api/v1/contacts', payload)
    
    // Push newly created contact
    activeCust.value.contacts.push(response.data)
    newContact.value = { name: '', email: '', phone: '', position: '' }
  } catch (err) {
    ui.error(getApiErrorMessage(err, 'Gagal menautkan narahubung klien.'))
  }
}

const deleteContact = async (id) => {
  const confirmed = await ui.confirm ({
    title: 'Hapus Kontak Ini?',
    message: 'Narahubung akan dihapus dari akun klien dan tidak tampil lagi di CRM.',
    confirmText: 'Hapus',
    cancelText: 'Batal',
    tone: 'danger'
  })
  if (!confirmed) return
  try {
    await axios.delete(`/api/v1/contacts/${id}`)
    activeCust.value.contacts = activeCust.value.contacts.filter(c => c.id !== id)
  } catch {
    ui.error('Gagal menghapus kontak.')
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
