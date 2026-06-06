<template>
  <div class="glass-panel p-5 space-y-4 border border-brand-charcoal-light/20 select-none">
    <div class="flex items-center justify-between border-b border-brand-charcoal-light/20 pb-2">
      <h4 class="text-xs font-bold text-white uppercase tracking-wider">Event Execution Control</h4>
      <span class="w-2.5 h-2.5 rounded-full" :class="statusColor"></span>
    </div>

    <!-- Active Status Grid -->
    <div class="grid grid-cols-2 gap-3 text-xs bg-brand-charcoal-dark/25 p-3 rounded-2xl border border-brand-charcoal-light/10">
      <div>
        <p class="text-gray-400 font-semibold mb-0.5">Program Status</p>
        <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-brand-orange/10 text-brand-orange">
          {{ project.program_status || 'Inquiry' }}
        </span>
      </div>
      <div>
        <p class="text-gray-400 font-semibold mb-0.5">Project Status</p>
        <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-sky-500/10 text-sky-400">
          {{ project.project_status || 'Open' }}
        </span>
      </div>
    </div>

    <!-- Event Date Countdown -->
    <div class="text-xs space-y-1 bg-brand-charcoal-dark/25 p-3 rounded-2xl border border-brand-charcoal-light/10">
      <p class="text-gray-400 font-semibold">Event Dates</p>
      <div class="flex justify-between items-center mt-1">
        <p class="text-white font-bold">{{ project.event_date_start || '-' }} to {{ project.event_date_end || '-' }}</p>
        <span class="px-2 py-0.5 rounded text-[10px] font-extrabold" :class="dateBadgeClass">
          {{ eventDateLabel }}
        </span>
      </div>
    </div>

    <!-- PM & PO Assignments -->
    <div class="text-xs space-y-2 bg-brand-charcoal-dark/25 p-3 rounded-2xl border border-brand-charcoal-light/10">
      <div class="flex justify-between items-center">
        <span class="text-gray-400 font-semibold">Program Manager</span>
        <span class="text-white font-bold">{{ project.program_manager?.full_name || 'Not Assigned' }}</span>
      </div>
      <div class="flex justify-between items-center">
        <span class="text-gray-400 font-semibold">Program Owner</span>
        <span class="text-white font-bold">{{ project.program_owner?.full_name || 'Not Assigned' }}</span>
      </div>
    </div>

    <!-- Next Action Guidance -->
    <div class="text-xs space-y-2 p-3.5 bg-brand-orange/5 border border-brand-orange/15 rounded-2xl">
      <p class="text-brand-orange font-bold text-[10px] uppercase tracking-widest">Recommended Next Action</p>
      <p class="text-gray-200 font-medium leading-relaxed mt-1">
        {{ nextActionGuidance }}
      </p>
    </div>

    <!-- Readiness Warnings (Collapsible) -->
    <div v-if="validationWarnings.length > 0" class="text-xs space-y-2">
      <div 
        @click="showWarnings = !showWarnings" 
        class="flex items-center justify-between cursor-pointer border-t border-brand-charcoal-light/10 pt-3 text-[10px] uppercase tracking-wider font-extrabold text-gray-400 hover:text-white"
      >
        <span>Readiness Warnings ({{ validationWarnings.length }})</span>
        <svg 
          class="w-4 h-4 transition-transform duration-200" 
          :class="showWarnings ? 'rotate-180' : ''"
          fill="none" 
          stroke="currentColor" 
          stroke-width="2" 
          viewBox="0 0 24 24"
        >
          <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" />
        </svg>
      </div>

      <div v-show="showWarnings" class="space-y-1.5 pt-1 max-h-48 overflow-y-auto custom-scrollbar">
        <div 
          v-for="(w, idx) in validationWarnings" 
          :key="idx"
          class="p-2.5 rounded-xl border flex items-start gap-2 text-[11px] font-semibold leading-relaxed"
          :class="getWarningClass(w)"
        >
          <span class="mt-0.5 shrink-0">⚠️</span>
          <span>{{ w }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  project: {
    type: Object,
    required: true
  },
  warnings: {
    type: Array,
    required: false,
    default: () => []
  }
})

const showWarnings = ref(true)

const validationWarnings = computed(() => {
  // Exclude PNL security warnings to keep the panel focused on operational blockers
  return (props.warnings || []).filter(w => !w.includes('PNL access warning'))
})

const daysUntilEvent = computed(() => {
  if (!props.project.event_date_start) return null
  const eventDate = new Date(props.project.event_date_start)
  const today = new Date()
  today.setHours(0,0,0,0)
  eventDate.setHours(0,0,0,0)
  const diffTime = eventDate - today
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  return diffDays
})

const eventDateLabel = computed(() => {
  if (daysUntilEvent.value === null) return 'No Date Set'
  if (daysUntilEvent.value > 0) {
    return `${daysUntilEvent.value} Hari Lagi`
  } else if (daysUntilEvent.value === 0) {
    return 'Hari Ini!'
  } else {
    return `Lewat ${Math.abs(daysUntilEvent.value)} Hari`
  }
})

const dateBadgeClass = computed(() => {
  if (daysUntilEvent.value === null) return 'bg-gray-600/10 text-gray-400 border border-gray-600/20'
  if (daysUntilEvent.value > 7) {
    return 'bg-brand-blue/10 text-brand-blue border border-brand-blue/20'
  } else if (daysUntilEvent.value >= 0) {
    return 'bg-brand-orange/10 text-brand-orange border border-brand-orange/20 animate-pulse'
  } else {
    return 'bg-gray-700/20 text-gray-400 border border-gray-700/35'
  }
})

const statusColor = computed(() => {
  const score = props.project.project_readiness_score || 0
  if (score >= 0.8) return 'bg-brand-emerald'
  if (score >= 0.5) return 'bg-amber-400'
  return 'bg-red-500'
})

const nextActionGuidance = computed(() => {
  const pStatus = props.project.program_status || 'Inquiry'
  const pProjStatus = props.project.project_status || 'Open'
  
  if (pProjStatus === 'Canceled') {
    return 'Project sudah dibatalkan. Aktifkan kembali (Open/Active) jika ingin menjalankan ulang.'
  }
  if (pProjStatus === 'Closed' || pStatus === 'Closed') {
    return 'Project sudah selesai dan ditutup secara administratif.'
  }

  // Instrument lookup helper
  const instruments = props.project.instruments || []
  const checkStatus = (type) => {
    const inst = instruments.find(i => i.instrument_type === type)
    return inst ? inst.status : null
  }
  
  const clStatus = checkStatus('CL')
  const rosStatus = checkStatus('ROS')
  const ckStatus = checkStatus('CK')
  const pnlStatus = checkStatus('PNL')
  const hasDocuments = props.project.documents && props.project.documents.length > 0

  if (pStatus === 'Inquiry' || pStatus === 'Confirmed') {
    if (clStatus !== 'Done' || rosStatus !== 'Done' || ckStatus !== 'Done') {
      return 'Lengkapi CL, Rundown (ROS), dan checklist kesiapan (CK) sebelum event masuk status Ready.'
    }
    return 'Seluruh instrumen utama lengkap. Project siap diubah statusnya ke Ready.'
  }
  
  if (pStatus === 'Preparation' || pStatus === 'Ready') {
    if (rosStatus !== 'Done' || ckStatus !== 'Done') {
      return 'Pastikan Rundown of Show (ROS) & Check List (CK) bertanda Done sebelum menjalankan event.'
    }
    return 'Event siap dijalankan. Ubah status ke Running ketika acara dimulai.'
  }
  
  if (pStatus === 'Running') {
    return 'Event sedang berjalan. PM agar memonitor checklist lapangan secara real-time.'
  }
  
  if (pStatus === 'Completed' || pStatus === 'Reporting') {
    if (!hasDocuments) {
      return 'Dokumentasi/LPJ belum diunggah. Unggah laporan pertanggungjawaban sebelum Closing.'
    }
    if (pnlStatus !== 'Done') {
      return 'Profit & Loss (PNL) sheet belum selesai. Selesaikan PNL sebelum menutup project.'
    }
    return 'Seluruh dokumen pertanggungjawaban lengkap. Project siap untuk ditutup (Closed).'
  }
  
  return 'Periksa daftar checklist instrumen dan tanggapi peringatan yang menyala.'
})

const getWarningClass = (warn) => {
  const w = warn.toLowerCase()
  if (w.includes('pnl access') || w.includes('sensitive')) {
    return 'bg-blue-500/5 border-blue-500/15 text-blue-300'
  }
  if (w.includes('overdue') || w.includes('exceeds') || w.includes('block') || w.includes('cannot')) {
    return 'bg-red-500/5 border-red-500/15 text-red-300'
  }
  if (w.includes('revision') || w.includes('missing') || w.includes('not marked')) {
    return 'bg-amber-500/5 border-amber-500/15 text-amber-300'
  }
  return 'bg-brand-charcoal-light/10 border-brand-charcoal-light/15 text-gray-300'
}
</script>

<style scoped>
.glass-panel {
  background: rgba(26, 32, 44, 0.7);
  backdrop-filter: blur(12px);
}
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 99px;
}
</style>
