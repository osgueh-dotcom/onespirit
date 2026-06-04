<template>
  <div class="space-y-6 pb-12">
    <!-- Top Header Banner -->
    <div class="p-6 bg-gradient-to-r from-brand-charcoal to-brand-charcoal-light/45 border border-brand-charcoal-light/35 rounded-3xl relative overflow-hidden select-none">
      <div class="absolute top-0 right-0 -mt-8 -mr-8 w-48 h-48 bg-brand-orange/5 rounded-full blur-3xl pointer-events-none"></div>
      <h2 class="text-2xl font-black text-white tracking-wide">Excel Migration & Sync Hub</h2>
      <p class="text-xs text-brand-orange font-bold mt-1 flex items-center gap-1.5">
        <span class="h-1.5 w-1.5 rounded-full bg-brand-emerald animate-ping"></span>
        Synchronize Flat Spreadsheet Databases into Normalized Ledgers
      </p>
    </div>

    <!-- Drag & Drop Uploader Console -->
    <div 
      v-if="!previewData && !importReport"
      class="border-2 border-dashed border-charcoal-600 hover:border-brand-orange/50 bg-charcoal-800/40 p-12 rounded-3xl text-center select-none cursor-pointer transition-all duration-300 flex flex-col items-center justify-center gap-4"
      :class="dragOver ? 'border-brand-orange bg-brand-orange/5' : ''"
      @dragover.prevent="dragOver = true"
      @dragleave="dragOver = false"
      @drop.prevent="handleFileDrop"
      @click="triggerFileInput"
    >
      <input 
        ref="fileInput"
        type="file" 
        class="hidden" 
        accept=".xlsx, .xls"
        @change="handleFileSelect"
      />
      <!-- Icon -->
      <div class="w-16 h-16 bg-brand-orange/10 rounded-2xl flex items-center justify-center text-brand-orange border border-brand-orange/20 shadow-xl">
        <svg class="w-8 h-8" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 16.5V9.75m0 0l3 3m-3-3l-3 3M6.75 19.5h10.5a2.25 2.25 0 002.25-2.25V6.75a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v10.5a2.25 2.25 0 002.25 2.25z" />
        </svg>
      </div>

      <div class="space-y-1.5">
        <p class="text-sm font-bold text-white">Drag & drop your Excel sheet here, or <span class="text-brand-orange underline">browse files</span></p>
        <p class="text-[10px] font-bold text-charcoal-400 uppercase tracking-widest">Supports .xlsx spreadsheets containing "Workflow" sheet</p>
      </div>

      <div v-if="parsing" class="flex items-center gap-2 mt-4 text-xs font-bold text-brand-orange">
        <svg class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <span>Validating spreadsheet matrix structure...</span>
      </div>
    </div>

    <!-- PREVIEW AREA PANEL -->
    <div v-if="previewData && !importReport" class="space-y-6">
      <!-- Preview Statistics Cards -->
      <div class="grid grid-cols-2 md:grid-cols-5 gap-4 select-none">
        <div class="p-4 bg-charcoal-800 border border-charcoal-700 rounded-2xl">
          <p class="text-[9px] uppercase tracking-wider text-charcoal-400 font-bold">Total Rows</p>
          <h4 class="text-2xl font-black text-white mt-1">{{ previewData.total_rows }}</h4>
        </div>
        <div class="p-4 bg-charcoal-800 border border-charcoal-700 rounded-2xl">
          <p class="text-[9px] uppercase tracking-wider text-charcoal-400 font-bold">Valid Runs</p>
          <h4 class="text-2xl font-black text-emerald-400 mt-1">{{ previewData.valid_rows_count }}</h4>
        </div>
        <div class="p-4 bg-charcoal-800 border border-charcoal-700 rounded-2xl">
          <p class="text-[9px] uppercase tracking-wider text-charcoal-400 font-bold">New Clients</p>
          <h4 class="text-2xl font-black text-brand-orange mt-1">{{ previewData.new_customers_count }}</h4>
        </div>
        <div class="p-4 bg-charcoal-800 border border-charcoal-700 rounded-2xl">
          <p class="text-[9px] uppercase tracking-wider text-charcoal-400 font-bold">New Projects</p>
          <h4 class="text-2xl font-black text-sky-400 mt-1">{{ previewData.new_projects_count }}</h4>
        </div>
        <div class="p-4 bg-charcoal-800 border border-charcoal-700 rounded-2xl">
          <p class="text-[9px] uppercase tracking-wider text-charcoal-400 font-bold">Conflicts/Skips</p>
          <h4 class="text-2xl font-black text-rose-400 mt-1">{{ previewData.invalid_rows_count }}</h4>
        </div>
      </div>

      <!-- Action Panel bar -->
      <div class="flex items-center justify-between p-4 bg-charcoal-800/80 border border-charcoal-700 rounded-2xl select-none">
        <span class="text-xs text-charcoal-300 font-semibold">Review warnings and matched entries below before committing updates.</span>
        <div class="flex gap-3">
          <button 
            @click="cancelImport"
            class="px-4 py-2 border border-charcoal-600 rounded-xl text-xs font-bold text-charcoal-300 hover:text-white transition-colors"
          >
            Cancel Sync
          </button>
          <button 
            @click="commitImport"
            :disabled="committing"
            class="px-5 py-2 bg-gradient-to-r from-brand-orange to-brand-orange-light text-white font-bold text-xs rounded-xl shadow-lg hover:scale-102 transition-transform flex items-center gap-2"
          >
            <svg v-if="committing" class="animate-spin h-3.5 w-3.5 text-white" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span>Confirm & Execute Sync</span>
          </button>
        </div>
      </div>

      <!-- Validation Warnings Console -->
      <div v-if="previewData.warnings?.length > 0" class="glass-panel p-5 bg-charcoal-800 border border-charcoal-700 rounded-2xl space-y-3">
        <h4 class="text-xs font-bold uppercase tracking-wider text-rose-400 flex items-center gap-2 select-none">
          <span class="w-1.5 h-1.5 rounded-full bg-rose-500 animate-pulse"></span>
          Data Validation Warnings ({{ previewData.warnings.length }})
        </h4>
        <div class="max-h-36 overflow-y-auto space-y-2 pr-1 custom-scrollbar">
          <div 
            v-for="(warn, idx) in previewData.warnings" 
            :key="idx"
            class="p-2.5 bg-rose-500/5 border border-rose-500/15 rounded-xl text-[11px] text-rose-300 font-semibold"
          >
            Row {{ warn.row }}: {{ warn.message }}
          </div>
        </div>
      </div>

      <!-- Preview Data Sheet Table -->
      <div class="glass-panel p-6 bg-charcoal-800 border border-charcoal-700 rounded-2xl flex flex-col">
        <h4 class="text-xs font-bold text-white uppercase tracking-widest mb-4 shrink-0 select-none">Excel Row Preview</h4>
        
        <div class="overflow-x-auto rounded-xl border border-charcoal-700">
          <table class="min-w-full text-left text-xs divide-y divide-charcoal-700 font-medium">
            <thead class="bg-charcoal-900 text-[9px] font-black uppercase tracking-widest text-charcoal-400 select-none">
              <tr>
                <th class="px-4 py-3">Row</th>
                <th class="px-4 py-3">Company Name</th>
                <th class="px-4 py-3">Client Category</th>
                <th class="px-4 py-3">Program Title</th>
                <th class="px-4 py-3">Estimated Budget</th>
                <th class="px-4 py-3">Proposed Dates</th>
                <th class="px-4 py-3">Quote #</th>
                <th class="px-4 py-3">Project Status</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-charcoal-800">
              <tr 
                v-for="row in previewData.preview_rows" 
                :key="row.row_index"
                class="hover:bg-charcoal-700/20 text-charcoal-200"
              >
                <td class="px-4 py-3 font-bold text-brand-orange">{{ row.row_index }}</td>
                <td class="px-4 py-3 font-bold text-white">{{ row.company_name }}</td>
                <td class="px-4 py-3 text-xs capitalize">{{ row.customer_category }}</td>
                <td class="px-4 py-3 font-bold text-white max-w-xs truncate">{{ row.project_title }}</td>
                <td class="px-4 py-3 font-bold text-emerald-400">{{ formatMoney(row.budget) }}</td>
                <td class="px-4 py-3 text-[10px] text-charcoal-400 font-bold">
                  {{ row.start_date || '-' }} to {{ row.end_date || '-' }}
                </td>
                <td class="px-4 py-3 font-bold text-sky-400">{{ row.quotation_number || '-' }}</td>
                <td class="px-4 py-3">
                  <span class="px-2 py-0.5 rounded-[5px] text-[9px] uppercase font-black" :class="getStatusStyles(row.project_status)">
                    {{ row.project_status }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- EXECUTION REPORT BOARD -->
    <div v-if="importReport" class="space-y-6">
      <div 
        class="p-6 border rounded-3xl flex items-start gap-4"
        :class="importReport.success ? 'bg-emerald-500/5 border-emerald-500/15' : 'bg-red-500/5 border-red-500/15'"
      >
        <div 
          class="w-10 h-10 rounded-2xl flex items-center justify-center text-white flex-shrink-0"
          :class="importReport.success ? 'bg-emerald-500' : 'bg-red-500'"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
            <path v-if="importReport.success" stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            <path v-else stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
          </svg>
        </div>

        <div class="space-y-1">
          <h3 class="text-base font-extrabold text-white">
            {{ importReport.success ? 'Migration Commit Completed' : 'Commit Encountered Issues' }}
          </h3>
          <p class="text-xs text-charcoal-300 font-medium">
            Workflow synchronization completed. System has transactionalized ledger records and updated audit activity timelines.
          </p>
        </div>
      </div>

      <div class="grid grid-cols-2 gap-6 select-none max-w-md">
        <div class="p-5 bg-charcoal-800 border border-charcoal-700 rounded-3xl text-center">
          <p class="text-[10px] uppercase font-bold tracking-widest text-charcoal-400">Created Records</p>
          <h4 class="text-4xl font-black text-emerald-400 mt-1.5">{{ importReport.created_count }}</h4>
        </div>
        <div class="p-5 bg-charcoal-800 border border-charcoal-700 rounded-3xl text-center">
          <p class="text-[10px] uppercase font-bold tracking-widest text-charcoal-400">Updated/Merged Records</p>
          <h4 class="text-4xl font-black text-sky-400 mt-1.5">{{ importReport.updated_count }}</h4>
        </div>
      </div>

      <!-- Import Errors Console -->
      <div v-if="importReport.errors?.length > 0" class="glass-panel p-6 bg-charcoal-800 border border-charcoal-700 rounded-2xl space-y-4">
        <h4 class="text-xs font-bold uppercase tracking-wider text-red-400 flex items-center gap-2 select-none">
          <span class="w-1.5 h-1.5 rounded-full bg-red-500 animate-pulse"></span>
          Execution Errors ({{ importReport.errors.length }})
        </h4>
        <div class="space-y-2 max-h-48 overflow-y-auto custom-scrollbar pr-1">
          <div 
            v-for="(err, idx) in importReport.errors" 
            :key="idx"
            class="p-3 bg-red-500/5 border border-red-500/15 rounded-xl text-xs text-red-300 font-semibold"
          >
            {{ err }}
          </div>
        </div>
      </div>

      <div class="flex gap-4 select-none">
        <button 
          @click="resetHub"
          class="px-5 py-2.5 bg-charcoal-800 hover:bg-charcoal-700 text-white font-bold text-xs rounded-xl border border-charcoal-700 transition-colors"
        >
          Return to Hub
        </button>
        <router-link 
          to="/projects"
          class="px-5 py-2.5 bg-gradient-to-r from-brand-orange to-brand-orange-light text-white font-bold text-xs rounded-xl shadow-lg inline-block"
        >
          Manage Projects Kanban
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const dragOver = ref(false)
const parsing = ref(false)
const committing = ref(false)

const fileInput = ref(null)
const selectedFile = ref(null)
const previewData = ref(null)
const importReport = ref(null)

const triggerFileInput = () => {
  fileInput.value.click()
}

const handleFileSelect = (event) => {
  const files = event.target.files
  if (files.length > 0) {
    processFile(files[0])
  }
}

const handleFileDrop = (event) => {
  dragOver.value = false
  const files = event.dataTransfer.files
  if (files.length > 0) {
    processFile(files[0])
  }
}

const processFile = async (file) => {
  if (!file.name.endswith('.xlsx') && !file.name.endswith('.xls')) {
    alert('Please upload a valid Excel spreadsheet (.xlsx, .xls)')
    return
  }
  selectedFile.value = file
  parsing.value = true
  
  try {
    const formData = new FormData()
    formData.append('file', file)
    
    const response = await axios.post('/api/v1/imports/validate', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    previewData.value = response.data
  } catch (err) {
    alert(err.response?.data?.detail || 'Failed to parse spreadsheet workflow')
    selectedFile.value = null
  } finally {
    parsing.value = false
  }
}

const commitImport = async () => {
  if (!selectedFile.value) return
  committing.value = true
  
  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value)
    
    const response = await axios.post('/api/v1/imports/commit', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    importReport.value = response.data
  } catch (err) {
    alert(err.response?.data?.detail || 'Import transaction commit failed')
  } finally {
    committing.value = false
  }
}

const cancelImport = () => {
  selectedFile.value = null
  previewData.value = null
}

const resetHub = () => {
  selectedFile.value = null
  previewData.value = null
  importReport.value = null
}

const formatMoney = (val) => {
  return 'Rp ' + Number(val || 0).toLocaleString('id-ID', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  })
}

const getStatusStyles = (status) => {
  if (status === 'inquiry') return 'bg-orange-500/10 text-orange-500 border border-orange-500/20'
  if (status === 'quotation') return 'bg-yellow-500/10 text-yellow-500'
  if (status === 'negotiation') return 'bg-brand-blue/10 text-brand-blue'
  if (status === 'confirmed') return 'bg-purple-500/10 text-purple-500'
  if (status === 'ongoing') return 'bg-orange-500/10 text-orange-400'
  if (status === 'completed') return 'bg-brand-emerald/10 text-brand-emerald border border-brand-emerald/20'
  return 'bg-red-500/10 text-red-400'
}

// Add simple helper for custom endswith check in template strings
String.prototype.endswith = function(suffix) {
    return this.indexOf(suffix, this.length - suffix.length) !== -1;
};
</script>

<style scoped>
.glass-panel {
  background: rgba(26, 32, 44, 0.7);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 2px;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.15);
  border-radius: 2px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.35);
}
</style>
