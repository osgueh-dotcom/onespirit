<template>
  <div class="space-y-6">
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Google Drive Reference Add Form -->
      <div v-if="auth.hasPermission('documents:write')" class="glass-panel p-5 space-y-4 h-fit">
        <h4 class="text-xs font-bold text-white uppercase tracking-wider">Link Operations Document</h4>
        <form @submit.prevent="handleSubmit" class="space-y-3 select-none">
          <div>
            <label class="block text-[10px] font-extrabold uppercase tracking-widest text-gray-400 mb-1">Document Title *</label>
            <input v-model="newDoc.title" type="text" placeholder="e.g. Approved Quotation PDF" required class="w-full px-3 py-2 rounded-lg bg-brand-charcoal-dark border border-brand-charcoal-light/40 text-xs text-white" />
          </div>
          <div>
            <label class="block text-[10px] font-extrabold uppercase tracking-widest text-gray-400 mb-1">Document Type *</label>
            <select v-model="newDoc.document_type" required class="w-full px-3 py-2 rounded-lg bg-brand-charcoal-dark border border-brand-charcoal-light/40 text-xs text-white">
              <option value="SIGNED_FILE">Signed File</option>
              <option value="PHOTO">Photo</option>
              <option value="VIDEO">Video</option>
              <option value="TEASER">Teaser</option>
              <option value="INSTAGRAM">Instagram</option>
              <option value="YOUTUBE">YouTube</option>
              <option value="OTHER">Other</option>
            </select>
          </div>
          <div>
            <label class="block text-[10px] font-extrabold uppercase tracking-widest text-gray-400 mb-1">Google Drive / Resource URL *</label>
            <input v-model="newDoc.file_path" type="url" placeholder="https://drive.google.com/..." required class="w-full px-3 py-2 rounded-lg bg-brand-charcoal-dark border border-brand-charcoal-light/40 text-xs text-white" />
          </div>
          <div>
            <label class="block text-[10px] font-extrabold uppercase tracking-widest text-gray-400 mb-1">Remarks</label>
            <textarea v-model="newDoc.notes" placeholder="Notes..." rows="2" class="w-full px-3 py-2 rounded-lg bg-brand-charcoal-dark border border-brand-charcoal-light/40 text-xs text-white"></textarea>
          </div>
          <button type="submit" class="w-full py-2 bg-brand-orange text-white rounded-lg font-bold text-xs hover:bg-brand-orange-dark transition-all">Link Document</button>
        </form>
      </div>

      <!-- Document lists -->
      <div class="glass-panel p-5 flex flex-col h-[400px]" :class="auth.hasPermission('documents:write') ? 'lg:col-span-2' : 'lg:col-span-3'">
        <h4 class="text-xs font-bold text-white uppercase tracking-wider mb-4 shrink-0">Archived Documents & Assets</h4>
        
        <div class="flex-1 overflow-y-auto space-y-3 pr-1">
          <div v-if="documents.length === 0" class="h-full flex items-center justify-center text-xs font-semibold text-gray-500 select-none">
            No linked documents or asset URLs recorded for this project.
          </div>
          
          <div 
            v-for="doc in documents" 
            :key="doc.id"
            class="p-4 bg-brand-charcoal border border-brand-charcoal-light/20 rounded-2xl flex items-center justify-between text-xs font-medium"
          >
            <div>
              <a :href="doc.url || doc.file_path" target="_blank" class="font-bold text-white hover:text-brand-orange transition-colors text-sm flex items-center gap-1.5 flex-wrap">
                {{ doc.title }}
                <span class="text-[9px] font-bold px-1.5 py-0.5 rounded bg-brand-orange/10 text-brand-orange border border-brand-orange/20">
                  {{ doc.document_type || 'OTHER' }}
                </span>
              </a>
              <p class="text-gray-400 mt-1 font-semibold">Uploaded by: {{ doc.uploaded_by?.full_name || 'System' }} | Date: {{ formatDateTime(doc.created_at) }}</p>
              <p v-if="doc.notes" class="text-gray-500 mt-1 text-[11px] font-medium leading-relaxed">{{ doc.notes }}</p>
            </div>
            <button 
              v-if="auth.hasPermission('documents:write')"
              @click="$emit('delete-doc', doc.id)"
              class="px-2 py-1 text-[10px] font-bold text-red-400 bg-red-500/10 rounded hover:bg-red-500/20 transition-all select-none"
            >
              Remove
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../store/auth'

const auth = useAuthStore()

defineProps({
  documents: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['save-doc', 'delete-doc'])

const newDoc = ref({
  title: '',
  file_path: '',
  file_type: 'link',
  storage_type: 'google_drive',
  notes: '',
  document_type: 'OTHER',
  url: ''
})

const handleSubmit = () => {
  newDoc.value.url = newDoc.value.file_path
  emit('save-doc', { ...newDoc.value })
  // Reset form
  newDoc.value = {
    title: '',
    file_path: '',
    file_type: 'link',
    storage_type: 'google_drive',
    notes: '',
    document_type: 'OTHER',
    url: ''
  }
}

const formatDateTime = (val) => {
  if (!val) return '-'
  return new Date(val).toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>
