<template>
  <div class="space-y-6">
    <!-- Project Header Panel -->
    <div v-if="project" class="p-6 bg-gradient-to-r from-brand-charcoal to-brand-charcoal-light/45 border border-brand-charcoal-light/35 rounded-3xl relative overflow-hidden select-none flex items-center justify-between flex-wrap gap-4">
      <div class="absolute top-0 right-0 -mt-8 -mr-8 w-48 h-48 bg-brand-orange/5 rounded-full blur-3xl pointer-events-none"></div>
      
      <div>
        <div class="flex items-center flex-wrap gap-2">
          <span class="px-2 py-0.5 text-[9px] uppercase font-bold tracking-wider rounded bg-brand-orange/15 text-brand-orange border border-brand-orange/20">
            {{ project.project_status }}
          </span>
          <span v-if="project.project_code" class="text-xs text-brand-orange font-bold font-mono">
            {{ project.project_code }}
          </span>
        </div>
        <span class="text-xs text-gray-400 font-bold mt-1.5 block">Client: {{ project.customer?.company_name }}</span>
        <h2 class="text-2xl font-black text-white mt-1 tracking-wide">{{ project.title }}</h2>
        <p class="text-xs text-gray-500 font-bold mt-1">Duration: {{ project.event_date_start || '-' }} to {{ project.event_date_end || '-' }}</p>
      </div>

      <div class="flex items-center gap-5 text-right font-sans">
        <div>
          <p class="text-[10px] uppercase font-bold tracking-widest text-gray-500 mb-0.5">Budget Allocated</p>
          <p class="text-lg font-black text-brand-emerald">{{ formatMoney(project.budget) }}</p>
        </div>
        <div>
          <p class="text-[10px] uppercase font-bold tracking-widest text-gray-500 mb-0.5">Lead PM</p>
          <p class="text-sm font-extrabold text-white">{{ project.program_manager?.full_name || 'Unassigned' }}</p>
        </div>
      </div>
    </div>

    <!-- Quick Workflow Status Gates -->
    <div v-if="project" class="grid grid-cols-2 sm:grid-cols-4 gap-4 bg-brand-charcoal-light/10 p-4 rounded-3xl border border-brand-charcoal-light/15">
      <div>
        <label class="block text-[9px] font-extrabold uppercase tracking-widest text-gray-400 mb-1">Quotation Status</label>
        <select 
          :value="project.quotation_status" 
          @change="$emit('transition', 'quotation_status', $event.target.value)"
          class="w-full bg-brand-charcoal-dark border border-brand-charcoal-light/45 rounded-xl px-3 py-2 text-xs font-bold text-white outline-none focus:border-brand-orange"
        >
          <option v-for="st in ['Draft', 'Sent', 'Follow Up', 'Revision', 'Signed & Deal', 'Cancel']" :key="st" :value="st">{{ st }}</option>
        </select>
      </div>
      <div>
        <label class="block text-[9px] font-extrabold uppercase tracking-widest text-gray-400 mb-1">Program Status</label>
        <select 
          :value="project.program_status" 
          @change="$emit('transition', 'program_status', $event.target.value)"
          class="w-full bg-brand-charcoal-dark border border-brand-charcoal-light/45 rounded-xl px-3 py-2 text-xs font-bold text-white outline-none focus:border-brand-orange"
        >
          <option v-for="st in ['Inquiry', 'Confirmed', 'Preparation', 'Ready', 'Running', 'Completed', 'Reporting', 'Closed', 'Cancel']" :key="st" :value="st">{{ st }}</option>
        </select>
      </div>
      <div>
        <label class="block text-[9px] font-extrabold uppercase tracking-widest text-gray-400 mb-1">Payment Status</label>
        <select 
          :value="project.payment_status" 
          @change="$emit('transition', 'payment_status', $event.target.value)"
          class="w-full bg-brand-charcoal-dark border border-brand-charcoal-light/45 rounded-xl px-3 py-2 text-xs font-bold text-white outline-none focus:border-brand-orange"
        >
          <option v-for="st in ['Not Invoiced', 'Invoice Sent', 'Partial Paid', 'Paid', 'Outstanding', 'Overdue']" :key="st" :value="st">{{ st }}</option>
        </select>
      </div>
      <div>
        <label class="block text-[9px] font-extrabold uppercase tracking-widest text-gray-400 mb-1">Project Status</label>
        <select 
          :value="project.project_status" 
          @change="$emit('transition', 'project_status', $event.target.value)"
          class="w-full bg-brand-charcoal-dark border border-brand-charcoal-light/45 rounded-xl px-3 py-2 text-xs font-bold text-white outline-none focus:border-brand-orange"
        >
          <option v-for="st in ['Open', 'Active', 'Reporting', 'Closed', 'Canceled']" :key="st" :value="st">{{ st }}</option>
        </select>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  project: {
    type: Object,
    required: true
  }
})

defineEmits(['transition'])

const formatMoney = (val) => {
  return 'Rp ' + Number(val || 0).toLocaleString('id-ID', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  })
}
</script>
