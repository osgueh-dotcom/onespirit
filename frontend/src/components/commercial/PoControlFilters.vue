<template>
  <div class="glass-panel p-5 border border-brand-charcoal-light/30 space-y-4 select-none">
    <div class="flex items-center justify-between border-b border-brand-charcoal-light/15 pb-2">
      <span class="text-[10px] font-black uppercase tracking-wider text-gray-400">Filter Komersial</span>
      <button @click="resetFilters" class="text-[10px] font-bold text-brand-orange hover:underline">
        Reset Filter ✕
      </button>
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4">
      <!-- Filter PO -->
      <div>
        <label class="block text-[9px] font-extrabold uppercase tracking-widest text-gray-500 mb-1.5">Program Owner (PO)</label>
        <select 
          v-model="filters.po_id" 
          @change="emitChange"
          class="w-full px-3 py-2 rounded-lg bg-brand-charcoal-dark border border-brand-charcoal-light/45 hover:border-brand-orange/30 text-[11px] font-semibold text-gray-300 outline-none transition-all"
        >
          <option value="">Semua PO</option>
          <option v-for="u in users" :key="u.id" :value="u.id">{{ u.full_name }}</option>
        </select>
      </div>

      <!-- Filter PM -->
      <div>
        <label class="block text-[9px] font-extrabold uppercase tracking-widest text-gray-500 mb-1.5">Program Manager (PM)</label>
        <select 
          v-model="filters.pm_id" 
          @change="emitChange"
          class="w-full px-3 py-2 rounded-lg bg-brand-charcoal-dark border border-brand-charcoal-light/45 hover:border-brand-orange/30 text-[11px] font-semibold text-gray-300 outline-none transition-all"
        >
          <option value="">Semua PM</option>
          <option v-for="u in users" :key="u.id" :value="u.id">{{ u.full_name }}</option>
        </select>
      </div>

      <!-- Source Type -->
      <div>
        <label class="block text-[9px] font-extrabold uppercase tracking-widest text-gray-500 mb-1.5">Source Type</label>
        <select 
          v-model="filters.source_type" 
          @change="emitChange"
          class="w-full px-3 py-2 rounded-lg bg-brand-charcoal-dark border border-brand-charcoal-light/45 hover:border-brand-orange/30 text-[11px] font-semibold text-gray-300 outline-none transition-all"
        >
          <option value="">Semua Source</option>
          <option value="Hotel">Hotel</option>
          <option value="Direct">Direct</option>
          <option value="Repeater">Repeater</option>
          <option value="Partner">Partner</option>
          <option value="Instagram">Instagram</option>
          <option value="Web">Web</option>
          <option value="Other">Other</option>
        </select>
      </div>

      <!-- Customer Category -->
      <div>
        <label class="block text-[9px] font-extrabold uppercase tracking-widest text-gray-500 mb-1.5">Kategori Klien</label>
        <select 
          v-model="filters.customer_category" 
          @change="emitChange"
          class="w-full px-3 py-2 rounded-lg bg-brand-charcoal-dark border border-brand-charcoal-light/45 hover:border-brand-orange/30 text-[11px] font-semibold text-gray-300 outline-none transition-all"
        >
          <option value="">Semua Kategori</option>
          <option value="Corporate">Corporate</option>
          <option value="Agency">Agency</option>
          <option value="Partner">Partner</option>
          <option value="Government">Government</option>
          <option value="Other">Other</option>
        </select>
      </div>

      <!-- Date Range From -->
      <div>
        <label class="block text-[9px] font-extrabold uppercase tracking-widest text-gray-500 mb-1.5">Dari Tanggal</label>
        <input 
          v-model="filters.date_from" 
          type="date"
          @change="emitChange"
          class="w-full px-3 py-2 rounded-lg bg-brand-charcoal-dark border border-brand-charcoal-light/45 hover:border-brand-orange/30 text-[11px] font-semibold text-gray-300 outline-none transition-all"
        />
      </div>

      <!-- Date Range To -->
      <div>
        <label class="block text-[9px] font-extrabold uppercase tracking-widest text-gray-500 mb-1.5">Sampai Tanggal</label>
        <input 
          v-model="filters.date_to" 
          type="date"
          @change="emitChange"
          class="w-full px-3 py-2 rounded-lg bg-brand-charcoal-dark border border-brand-charcoal-light/45 hover:border-brand-orange/30 text-[11px] font-semibold text-gray-300 outline-none transition-all"
        />
      </div>
    </div>

    <!-- Second Row of Filters -->
    <div class="grid grid-cols-1 md:grid-cols-4 lg:grid-cols-6 gap-4 border-t border-brand-charcoal-light/10 pt-4">
      <!-- Quotation Status -->
      <div>
        <label class="block text-[9px] font-extrabold uppercase tracking-widest text-gray-500 mb-1.5">Status Quotation</label>
        <select 
          v-model="filters.quotation_status" 
          @change="emitChange"
          class="w-full px-3 py-2 rounded-lg bg-brand-charcoal-dark border border-brand-charcoal-light/45 hover:border-brand-orange/30 text-[11px] font-semibold text-gray-300 outline-none transition-all"
        >
          <option value="">Semua Quotation</option>
          <option value="Draft">Draft</option>
          <option value="Sent">Sent</option>
          <option value="Follow Up">Follow Up</option>
          <option value="Revision">Revision</option>
          <option value="Signed & Deal">Signed & Deal</option>
          <option value="Cancel">Cancel</option>
        </select>
      </div>

      <!-- Program Status -->
      <div>
        <label class="block text-[9px] font-extrabold uppercase tracking-widest text-gray-500 mb-1.5">Status Program</label>
        <select 
          v-model="filters.program_status" 
          @change="emitChange"
          class="w-full px-3 py-2 rounded-lg bg-brand-charcoal-dark border border-brand-charcoal-light/45 hover:border-brand-orange/30 text-[11px] font-semibold text-gray-300 outline-none transition-all"
        >
          <option value="">Semua Program</option>
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
      <div>
        <label class="block text-[9px] font-extrabold uppercase tracking-widest text-gray-500 mb-1.5">Status Pembayaran</label>
        <select 
          v-model="filters.payment_status" 
          @change="emitChange"
          class="w-full px-3 py-2 rounded-lg bg-brand-charcoal-dark border border-brand-charcoal-light/45 hover:border-brand-orange/30 text-[11px] font-semibold text-gray-300 outline-none transition-all"
        >
          <option value="">Semua Pembayaran</option>
          <option value="Not Invoiced">Not Invoiced</option>
          <option value="Invoice Sent">Invoice Sent</option>
          <option value="Partial Paid">Partial Paid</option>
          <option value="Paid">Paid</option>
          <option value="Outstanding">Outstanding</option>
          <option value="Overdue">Overdue</option>
        </select>
      </div>

      <!-- Event Window -->
      <div>
        <label class="block text-[9px] font-extrabold uppercase tracking-widest text-gray-500 mb-1.5">Event Window</label>
        <select 
          v-model="filters.event_window" 
          @change="emitChange"
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

      <!-- Checkboxes -->
      <div class="md:col-span-2 flex items-center gap-4 pt-4 select-none">
        <label class="flex items-center gap-2 text-[10px] font-bold text-gray-400 hover:text-white cursor-pointer transition-colors">
          <input 
            v-model="filters.include_closed" 
            type="checkbox" 
            @change="emitChange"
            class="rounded bg-brand-charcoal border-brand-charcoal-light/40 text-brand-orange focus:ring-0"
          />
          Closed Project
        </label>
        <label class="flex items-center gap-2 text-[10px] font-bold text-gray-400 hover:text-white cursor-pointer transition-colors">
          <input 
            v-model="filters.include_canceled" 
            type="checkbox" 
            @change="emitChange"
            class="rounded bg-brand-charcoal border-brand-charcoal-light/40 text-brand-orange focus:ring-0"
          />
          Batal (Canceled)
        </label>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  users: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['change'])

const filters = ref({
  po_id: '',
  pm_id: '',
  source_type: '',
  customer_category: '',
  quotation_status: '',
  program_status: '',
  payment_status: '',
  project_status: '',
  date_from: '',
  date_to: '',
  event_window: 'all',
  include_closed: false,
  include_canceled: false
})

const emitChange = () => {
  emit('change', { ...filters.value })
}

const resetFilters = () => {
  filters.value = {
    po_id: '',
    pm_id: '',
    source_type: '',
    customer_category: '',
    quotation_status: '',
    program_status: '',
    payment_status: '',
    project_status: '',
    date_from: '',
    date_to: '',
    event_window: 'all',
    include_closed: false,
    include_canceled: false
  }
  emitChange()
}
</script>

<style scoped>
.glass-panel {
  background: rgba(26, 32, 44, 0.75);
  backdrop-filter: blur(12px);
  border-radius: 1.25rem;
}
</style>
