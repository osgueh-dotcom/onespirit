<template>
  <div class="glass-panel p-5 bg-charcoal-800 border border-charcoal-700 rounded-3xl space-y-4 print:hidden select-none">
    <div class="flex items-center justify-between cursor-pointer select-none" @click="showFilters = !showFilters">
      <h3 class="text-xs font-bold text-white tracking-widest uppercase flex items-center gap-2">
        <svg class="w-4 h-4 text-brand-orange" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 3c2.755 0 5.455.232 8.083.678.533.09 1.917.746 1.917 2.322v1.844c0 .536-.213 1.05-.592 1.43l-4.708 4.708c-.38.38-.592.895-.592 1.43v5.275c0 .324-.162.627-.433.808l-2.625 1.75c-.563.375-1.313-.028-1.313-.708v-7.125c0-.536-.213-1.05-.592-1.43L4.592 9.274C4.213 8.895 4 8.38 4 7.844V5c0-1.576 1.384-2.233 1.917-2.322C8.545 3.232 11.245 3 12 3z" />
        </svg>
        Advanced BI Query Filters
      </h3>
      <span class="text-xs text-brand-orange font-bold hover:underline">
        {{ showFilters ? 'Hide Panel' : 'Show Panel' }}
      </span>
    </div>

    <!-- Active filters grid -->
    <div v-show="showFilters" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4 transition-all duration-300">
      <!-- Date Start -->
      <div class="flex flex-col gap-1.5">
        <label class="text-[9px] uppercase tracking-wider text-charcoal-400 font-black">Date Range Start</label>
        <input 
          type="date" 
          v-model="localFilters.date_from" 
          @change="emitFilters"
          class="bg-charcoal-900 border border-charcoal-700 text-xs text-white p-2.5 rounded-xl outline-none focus:border-brand-orange"
        />
      </div>

      <!-- Date End -->
      <div class="flex flex-col gap-1.5">
        <label class="text-[9px] uppercase tracking-wider text-charcoal-400 font-black">Date Range End</label>
        <input 
          type="date" 
          v-model="localFilters.date_to" 
          @change="emitFilters"
          class="bg-charcoal-900 border border-charcoal-700 text-xs text-white p-2.5 rounded-xl outline-none focus:border-brand-orange"
        />
      </div>

      <!-- Year Select -->
      <div class="flex flex-col gap-1.5">
        <label class="text-[9px] uppercase tracking-wider text-charcoal-400 font-black">Year</label>
        <select 
          v-model="localFilters.year" 
          @change="emitFilters"
          class="bg-charcoal-900 border border-charcoal-700 text-xs text-white p-2.5 rounded-xl outline-none focus:border-brand-orange"
        >
          <option value="">All Years</option>
          <option :value="2025">2025</option>
          <option :value="2026">2026</option>
          <option :value="2027">2027</option>
        </select>
      </div>

      <!-- Month Select -->
      <div class="flex flex-col gap-1.5">
        <label class="text-[9px] uppercase tracking-wider text-charcoal-400 font-black">Month</label>
        <select 
          v-model="localFilters.month" 
          @change="emitFilters"
          class="bg-charcoal-900 border border-charcoal-700 text-xs text-white p-2.5 rounded-xl outline-none focus:border-brand-orange"
        >
          <option value="">All Months</option>
          <option v-for="m in 12" :key="m" :value="m">{{ new Date(2000, m - 1).toLocaleString('default', { month: 'long' }) }}</option>
        </select>
      </div>

      <!-- PO Selector -->
      <div class="flex flex-col gap-1.5">
        <label class="text-[9px] uppercase tracking-wider text-charcoal-400 font-black">Program Owner (PO)</label>
        <select 
          v-model="localFilters.po_id" 
          @change="emitFilters"
          class="bg-charcoal-900 border border-charcoal-700 text-xs text-white p-2.5 rounded-xl outline-none focus:border-brand-orange"
        >
          <option value="">All POs</option>
          <option v-for="user in usersList" :key="user.id" :value="user.id">
            {{ user.full_name }}
          </option>
        </select>
      </div>

      <!-- PM Selector -->
      <div class="flex flex-col gap-1.5">
        <label class="text-[9px] uppercase tracking-wider text-charcoal-400 font-black">Program Manager (PM)</label>
        <select 
          v-model="localFilters.pm_id" 
          @change="emitFilters"
          class="bg-charcoal-900 border border-charcoal-700 text-xs text-white p-2.5 rounded-xl outline-none focus:border-brand-orange"
        >
          <option value="">All PMs</option>
          <option v-for="user in usersList" :key="user.id" :value="user.id">
            {{ user.full_name }}
          </option>
        </select>
      </div>

      <!-- Quotation Status -->
      <div class="flex flex-col gap-1.5">
        <label class="text-[9px] uppercase tracking-wider text-charcoal-400 font-black">Quotation Status</label>
        <select 
          v-model="localFilters.quotation_status" 
          @change="emitFilters"
          class="bg-charcoal-900 border border-charcoal-700 text-xs text-white p-2.5 rounded-xl outline-none focus:border-brand-orange"
        >
          <option value="">All Quotation Statuses</option>
          <option value="Draft">Draft</option>
          <option value="Sent">Sent</option>
          <option value="Follow Up">Follow Up</option>
          <option value="Revision">Revision</option>
          <option value="Signed & Deal">Signed & Deal</option>
          <option value="Cancel">Cancel</option>
        </select>
      </div>

      <!-- Program Status -->
      <div class="flex flex-col gap-1.5">
        <label class="text-[9px] uppercase tracking-wider text-charcoal-400 font-black">Program Status</label>
        <select 
          v-model="localFilters.program_status" 
          @change="emitFilters"
          class="bg-charcoal-900 border border-charcoal-700 text-xs text-white p-2.5 rounded-xl outline-none focus:border-brand-orange"
        >
          <option value="">All Program Statuses</option>
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
      <div class="flex flex-col gap-1.5">
        <label class="text-[9px] uppercase tracking-wider text-charcoal-400 font-black">Payment Status</label>
        <select 
          v-model="localFilters.payment_status" 
          @change="emitFilters"
          class="bg-charcoal-900 border border-charcoal-700 text-xs text-white p-2.5 rounded-xl outline-none focus:border-brand-orange"
        >
          <option value="">All Payment Statuses</option>
          <option value="Not Invoiced">Not Invoiced</option>
          <option value="Invoice Sent">Invoice Sent</option>
          <option value="Partial Paid">Partial Paid</option>
          <option value="Paid">Paid</option>
          <option value="Outstanding">Outstanding</option>
          <option value="Overdue">Overdue</option>
        </select>
      </div>

      <!-- Project Status -->
      <div class="flex flex-col gap-1.5">
        <label class="text-[9px] uppercase tracking-wider text-charcoal-400 font-black">Project Status</label>
        <select 
          v-model="localFilters.project_status" 
          @change="emitFilters"
          class="bg-charcoal-900 border border-charcoal-700 text-xs text-white p-2.5 rounded-xl outline-none focus:border-brand-orange"
        >
          <option value="">All Project Statuses</option>
          <option value="Open">Open</option>
          <option value="Active">Active</option>
          <option value="Reporting">Reporting</option>
          <option value="Closed">Closed</option>
          <option value="Canceled">Canceled</option>
        </select>
      </div>

      <!-- Customer Category -->
      <div class="flex flex-col gap-1.5">
        <label class="text-[9px] uppercase tracking-wider text-charcoal-400 font-black">Customer Category</label>
        <select 
          v-model="localFilters.customer_category" 
          @change="emitFilters"
          class="bg-charcoal-900 border border-charcoal-700 text-xs text-white p-2.5 rounded-xl outline-none focus:border-brand-orange"
        >
          <option value="">All Customer Categories</option>
          <option value="Corporate">Corporate</option>
          <option value="Goverment">Government</option>
          <option value="Agency">Agency</option>
          <option value="Other">Other</option>
        </select>
      </div>

      <!-- Event Source Type -->
      <div class="flex flex-col gap-1.5">
        <label class="text-[9px] uppercase tracking-wider text-charcoal-400 font-black">Event Source Type</label>
        <select 
          v-model="localFilters.source_type" 
          @change="emitFilters"
          class="bg-charcoal-900 border border-charcoal-700 text-xs text-white p-2.5 rounded-xl outline-none focus:border-brand-orange"
        >
          <option value="">All Source Types</option>
          <option value="Hotel">Hotel</option>
          <option value="Direct">Direct</option>
          <option value="Repeater">Repeater</option>
          <option value="Partner">Partner</option>
          <option value="Instagram">Instagram</option>
          <option value="Web">Web</option>
          <option value="Other">Other</option>
        </select>
      </div>

      <!-- Event Category (text search) -->
      <div class="flex flex-col gap-1.5">
        <label class="text-[9px] uppercase tracking-wider text-charcoal-400 font-black">Event Category Tag</label>
        <input 
          type="text" 
          placeholder="e.g. Gathering, Outbound" 
          v-model="localFilters.event_category" 
          @input="debounceEmit"
          class="bg-charcoal-900 border border-charcoal-700 text-xs text-white p-2.5 rounded-xl outline-none focus:border-brand-orange"
        />
      </div>

      <!-- Program Type (text search) -->
      <div class="flex flex-col gap-1.5">
        <label class="text-[9px] uppercase tracking-wider text-charcoal-400 font-black">Program Type Tag</label>
        <input 
          type="text" 
          placeholder="e.g. Entertainment" 
          v-model="localFilters.program_type" 
          @input="debounceEmit"
          class="bg-charcoal-900 border border-charcoal-700 text-xs text-white p-2.5 rounded-xl outline-none focus:border-brand-orange"
        />
      </div>

      <!-- Reset Filters button -->
      <div class="flex items-end sm:col-span-2 gap-3">
        <button 
          @click="resetFilters"
          class="w-full py-2.5 border border-charcoal-600 hover:border-brand-orange text-xs text-charcoal-300 hover:text-white rounded-xl transition-all duration-200"
        >
          Reset All Query Filters
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  filters: {
    type: Object,
    required: true
  },
  usersList: {
    type: Array,
    required: true,
    default: () => []
  }
})

const emit = defineEmits(['change', 'reset'])

const showFilters = ref(false)
const localFilters = ref({ ...props.filters })

// Sync local state if parent changes it (like clear/reset)
watch(() => props.filters, (newVal) => {
  localFilters.value = { ...newVal }
}, { deep: true })

const emitFilters = () => {
  emit('change', localFilters.value)
}

let debounceTimeout = null
const debounceEmit = () => {
  if (debounceTimeout) clearTimeout(debounceTimeout)
  debounceTimeout = setTimeout(() => {
    emitFilters()
  }, 400)
}

const resetFilters = () => {
  localFilters.value = {
    year: '',
    month: '',
    date_from: '',
    date_to: '',
    po_id: '',
    pm_id: '',
    source_type: '',
    quotation_status: '',
    program_status: '',
    payment_status: '',
    project_status: '',
    customer_category: '',
    event_category: '',
    program_type: ''
  }
  emit('reset')
}
</script>

<style scoped>
.glass-panel {
  background: rgba(26, 32, 44, 0.7);
  backdrop-filter: blur(12px);
}
</style>
