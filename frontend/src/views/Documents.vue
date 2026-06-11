<template>
  <div class="app-page">
    <!-- Top toolbar selection -->
    <div class="flex items-center justify-between gap-4 select-none">
      <div class="flex items-center gap-3">
        <select 
          v-model="selectedProjectId"
          @change="fetchDocuments"
          class="px-4 py-2.5 rounded-xl bg-brand-charcoal border border-brand-charcoal-light/35 hover:border-brand-orange/35 focus:border-brand-orange text-xs font-semibold text-gray-300 outline-none transition-all"
        >
          <option value="">Pilih Arsip Proyek</option>
          <option v-for="p in projects" :key="p.id" :value="p.id">{{ p.title }} (Client: {{ p.customer?.company_name }})</option>
        </select>
      </div>
    </div>

    <!-- Loading Indicators -->
    <div v-if="loadingProjects" class="h-64 flex flex-col items-center justify-center gap-3">
      <svg class="animate-spin h-6 w-6 text-brand-orange" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
      <span class="text-xs text-gray-400 font-semibold">Membuka pusat dokumen...</span>
    </div>

    <div v-else class="space-y-6">
      <div v-if="!selectedProjectId" class="p-12 text-center border border-dashed border-brand-charcoal-light/25 rounded-3xl text-xs font-semibold text-gray-500 select-none">
        Silakan pilih arsip proyek dari pilihan di atas untuk melihat dokumen.
      </div>

      <div v-else-if="loadingDocs" class="h-48 flex flex-col items-center justify-center gap-2">
        <svg class="animate-spin h-5 w-5 text-brand-orange" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <span class="text-xs text-gray-400">Memuat arsip...</span>
      </div>

      <!-- Archive folder grid -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <!-- Folders/Files -->
        <div v-if="docs.length === 0" class="col-span-full p-12 text-center border border-dashed border-brand-charcoal-light/25 rounded-3xl text-xs font-semibold text-gray-500 select-none">
          Tidak ada file, lembar presentasi, atau template Google Drive yang diunggah untuk proyek ini.
        </div>

        <div 
          v-for="d in docs" 
          :key="d.id"
          class="interactive-card p-5 space-y-4 relative flex flex-col justify-between"
        >
          <div>
            <div class="flex items-center justify-between gap-2 border-b border-brand-charcoal-light/10 pb-3 mb-3">
              <span class="px-2 py-0.5 rounded text-[9px] font-bold uppercase tracking-wider" :class="d.storage_type === 'google_drive' ? 'bg-brand-orange/15 text-brand-orange' : 'bg-brand-blue/15 text-brand-blue'">
                {{ d.storage_type }}
              </span>
              <span class="text-[10px] text-gray-500 font-extrabold uppercase">{{ d.file_type }}</span>
            </div>
            
            <a :href="d.file_path" target="_blank" class="font-extrabold text-white text-sm hover:text-brand-orange transition-colors line-clamp-2 leading-snug">
              {{ d.title }}
            </a>
            <p v-if="d.notes" class="text-xs text-gray-400 mt-2 line-clamp-3 leading-relaxed font-medium">{{ d.notes }}</p>
          </div>

          <div class="pt-3 border-t border-brand-charcoal-light/10 text-[10px] font-bold text-gray-500 flex items-center justify-between">
            <span>Oleh: {{ d.uploaded_by?.full_name || 'System' }}</span>
            <a :href="d.file_path" target="_blank" class="text-brand-orange hover:underline font-extrabold">Buka File →</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useAuthStore } from '../store/auth'

const auth = useAuthStore()

const projects = ref([])
const docs = ref([])

const selectedProjectId = ref('')
const loadingProjects = ref(true)
const loadingDocs = ref(false)

const fetchProjects = async () => {
  try {
    const response = await axios.get('/api/v1/projects')
    projects.value = response.data
  } catch (err) {
    console.error('Failed to load projects list', err)
  } finally {
    loadingProjects.value = false
  }
}

const fetchDocuments = async () => {
  if (!selectedProjectId.value) {
    docs.value = []
    return
  }
  loadingDocs.value = true
  try {
    const response = await axios.get(`/api/v1/projects/${selectedProjectId.value}/documents`)
    docs.value = response.data
  } catch (err) {
    console.error('Failed to load documents list', err)
  } finally {
    loadingDocs.value = false
  }
}

onMounted(() => {
  fetchProjects()
})
</script>
