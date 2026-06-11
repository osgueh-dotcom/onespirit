<template>
  <div v-if="project" class="space-y-4">
    <section class="app-section-card relative overflow-hidden">
      <div class="absolute inset-x-0 top-0 h-1 bg-gradient-to-r from-brand-orange via-brand-amber to-brand-yellow"></div>
      <div class="relative flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
        <div class="min-w-0">
          <div class="flex flex-wrap items-center gap-2">
            <AppStatusBadge :status="project.project_status" />
            <span v-if="project.project_code" class="text-xs font-extrabold font-mono text-brand-orange">
              {{ project.project_code }}
            </span>
          </div>
          <p class="mt-4 text-xs font-bold uppercase tracking-wider text-muted-theme">
            {{ project.customer?.company_name || 'Client belum ditentukan' }}
          </p>
          <h2 class="mt-1 text-2xl md:text-3xl font-black tracking-tight text-main-theme">{{ project.title }}</h2>
          <p class="mt-2 text-sm font-medium text-muted-theme">
            {{ project.event_date_start || '-' }} sampai {{ project.event_date_end || '-' }}
          </p>
        </div>

        <div class="grid grid-cols-2 gap-3 sm:min-w-[360px]">
          <div class="app-subtle-panel p-4">
            <p class="text-[10px] font-extrabold uppercase tracking-wider text-muted-theme">Budget Allocated</p>
            <p class="mt-1 text-lg font-black text-brand-emerald">{{ formatMoney(project.budget) }}</p>
          </div>
          <div class="app-subtle-panel p-4">
            <p class="text-[10px] font-extrabold uppercase tracking-wider text-muted-theme">Lead PM</p>
            <p class="mt-1 text-sm font-black text-main-theme">{{ project.program_manager?.full_name || 'Unassigned' }}</p>
          </div>
        </div>
      </div>
    </section>

    <section class="app-section-card">
      <div class="mb-4">
        <p class="app-kicker">Workflow Gates</p>
        <h3 class="mt-1 text-base font-black tracking-tight text-main-theme">Status project dan tindakan berikutnya</h3>
      </div>

      <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <label v-for="gate in gates" :key="gate.field" class="block">
          <span class="mb-1.5 block text-[10px] font-extrabold uppercase tracking-wider text-muted-theme">{{ gate.label }}</span>
          <select
            :value="project[gate.field]"
            :disabled="!canEdit"
            class="app-form-control text-xs font-bold"
            :class="{ 'cursor-not-allowed opacity-70': !canEdit }"
            @change="$emit('transition', gate.field, $event.target.value)"
          >
            <option v-for="status in gate.options" :key="status" :value="status">{{ status }}</option>
          </select>
        </label>
      </div>
    </section>
  </div>
</template>

<script setup>
import AppStatusBadge from './ui/AppStatusBadge.vue'

defineProps({
  project: {
    type: Object,
    required: true
  },
  canEdit: {
    type: Boolean,
    default: false
  }
})

defineEmits(['transition'])

const gates = [
  {
    field: 'quotation_status',
    label: 'Quotation Status',
    options: ['Draft', 'Sent', 'Follow Up', 'Revision', 'Signed & Deal', 'Cancel']
  },
  {
    field: 'program_status',
    label: 'Program Status',
    options: ['Inquiry', 'Confirmed', 'Preparation', 'Ready', 'Running', 'Completed', 'Reporting', 'Closed', 'Cancel']
  },
  {
    field: 'payment_status',
    label: 'Payment Status',
    options: ['Not Invoiced', 'Invoice Sent', 'Partial Paid', 'Paid', 'Outstanding', 'Overdue']
  },
  {
    field: 'project_status',
    label: 'Project Status',
    options: ['Open', 'Active', 'Reporting', 'Closed', 'Canceled']
  }
]

const formatMoney = (value) => `Rp ${Number(value || 0).toLocaleString('id-ID', {
  minimumFractionDigits: 0,
  maximumFractionDigits: 0
})}`
</script>
