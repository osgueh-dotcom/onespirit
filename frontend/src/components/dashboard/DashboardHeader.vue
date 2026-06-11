<template>
  <section class="app-section-card relative overflow-hidden print:bg-white print:border-none print:p-0 print:shadow-none">
    <div class="absolute inset-x-0 top-0 h-1 bg-gradient-to-r from-brand-orange via-brand-amber to-brand-yellow print:hidden"></div>
    <div class="absolute -right-16 -top-20 h-48 w-48 rounded-full bg-brand-orange/5 print:hidden"></div>

    <div class="relative flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
      <div>
        <p class="app-kicker">Executive Overview</p>
        <h2 class="mt-2 text-3xl font-black tracking-tight text-main-theme print:text-charcoal-900">
          Executive Dashboard
        </h2>
        <p class="mt-2 max-w-2xl text-sm font-medium leading-relaxed text-muted-theme print:text-charcoal-600">
          Ringkasan operasional dan komersial One Spirit, dari inquiry hingga revenue dan readiness project.
        </p>
        <p class="mt-2 hidden text-[10px] font-semibold text-charcoal-500 print:block">
          Filter: {{ getFilterSummary() }} | Diunduh: {{ lastSync || timestamp }}
        </p>
      </div>

      <div class="flex flex-col gap-3 sm:flex-row sm:items-center print:hidden">
        <div class="app-subtle-panel flex items-center gap-3 px-4 py-2.5">
          <span class="h-2 w-2 rounded-full bg-brand-emerald"></span>
          <div>
            <p class="text-[9px] font-extrabold uppercase tracking-wider text-muted-theme">Sinkronisasi terakhir</p>
            <p class="mt-0.5 text-xs font-extrabold text-main-theme">{{ lastSync || timestamp }}</p>
          </div>
        </div>

        <button type="button" @click="$emit('refresh')" :disabled="loading" class="app-button-secondary">
          <svg :class="['h-4 w-4 text-brand-orange', loading ? 'animate-spin' : '']" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992M2.985 19.644v-4.992m0 0h4.992m-4.993 0 3.181 3.183a8.25 8.25 0 0 0 13.803-3.7M4.031 9.865a8.25 8.25 0 0 1 13.803-3.7l3.181 3.182m0-4.991v4.99" />
          </svg>
          Refresh
        </button>

        <button type="button" @click="$emit('print')" class="app-button-primary">
          <svg class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6.72 13.829a42.415 42.415 0 0 1 10.56 0L17.66 18l.229 2.523a1.125 1.125 0 0 1-1.12 1.227H7.231a1.125 1.125 0 0 1-1.12-1.227L6.34 18l.38-4.171Zm10.938-5.657.012-2.342a2.25 2.25 0 0 0-1.979-1.956 41.302 41.302 0 0 0-7.382 0A2.25 2.25 0 0 0 6.33 5.83l.001 2.342a3 3 0 0 0 0 5.658m11.327-5.658a3 3 0 0 1 0 5.658" />
          </svg>
          Print / Save Report
        </button>
      </div>
    </div>
  </section>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue'

const props = defineProps({
  filters: {
    type: Object,
    required: true,
    default: () => ({})
  },
  loading: {
    type: Boolean,
    default: false
  },
  lastSync: {
    type: String,
    default: ''
  }
})

defineEmits(['print', 'refresh'])

const timestamp = ref('')
let timerId = null

const updateTimestamp = () => {
  const now = new Date()
  timestamp.value = `${now.toLocaleTimeString('id-ID', {
    hour: '2-digit',
    minute: '2-digit'
  })} (${now.toLocaleDateString('id-ID', {
    day: 'numeric',
    month: 'short',
    year: 'numeric'
  })})`
}

const getFilterSummary = () => {
  const parts = []
  if (props.filters.year) parts.push(`Tahun ${props.filters.year}`)
  if (props.filters.month) {
    parts.push(new Date(2000, props.filters.month - 1).toLocaleString('id-ID', { month: 'long' }))
  }
  if (props.filters.date_from) parts.push(`Mulai ${props.filters.date_from}`)
  if (props.filters.date_to) parts.push(`Hingga ${props.filters.date_to}`)
  if (props.filters.po_id) parts.push('PO terpilih')
  if (props.filters.pm_id) parts.push('PM terpilih')
  if (props.filters.source_type) parts.push(`Source ${props.filters.source_type}`)
  return parts.length > 0 ? parts.join(', ') : 'Semua periode'
}

onMounted(() => {
  updateTimestamp()
  timerId = window.setInterval(updateTimestamp, 60000)
})

onUnmounted(() => {
  if (timerId) window.clearInterval(timerId)
})
</script>
