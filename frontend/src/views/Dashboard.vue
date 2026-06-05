<template>
  <div class="space-y-6 pb-12 print:bg-white print:text-charcoal-900 print:p-0">
    
    <!-- A. Dashboard Header -->
    <DashboardHeader :filters="analyticsFilters" @print="triggerPrint" />
    
    <!-- B. Dashboard Filters -->
    <DashboardFilters 
      :filters="analyticsFilters" 
      :usersList="usersList" 
      @change="onFiltersChanged" 
      @reset="onFiltersReset" 
    />
    
    <!-- Loading Indicators -->
    <div v-if="analyticsLoading" class="h-96 flex flex-col items-center justify-center gap-3 print:hidden">
      <svg class="animate-spin h-10 w-10 text-brand-orange" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
      <span class="text-xs font-bold text-charcoal-400 tracking-wider">Compiling executive analytics...</span>
    </div>
    
    <div v-else-if="analyticsData" class="space-y-6">
      
      <!-- D. Executive Summary Narrative -->
      <ExecutiveSummaryNarrative 
        :executive="analyticsData.executive" 
        :target="analyticsData.target" 
      />
      
      <!-- C. Executive KPI Cards -->
      <ExecutiveKpiCards 
        :executive="analyticsData.executive" 
        :target="analyticsData.target" 
      />
      
      <!-- E. Revenue & Target Section -->
      <RevenueSummary 
        :executive="analyticsData.executive" 
        :target="analyticsData.target" 
      />
      
      <!-- F. Funnel / Status Summary -->
      <StatusSummary 
        :quotation="analyticsData.quotation" 
        :program="analyticsData.program" 
        :payment="analyticsData.payment" 
        :project="analyticsData.project" 
      />
      
      <!-- G & H. PO & PM tables -->
      <div class="grid grid-cols-1 xl:grid-cols-2 gap-6 print:grid-cols-1">
        <PoPerformanceTable :data="analyticsData.po_performance" />
        <PmWorkloadTable :data="analyticsData.pm_workload" />
      </div>
      
      <!-- I. Source & Market Analytics -->
      <SourceAnalytics 
        :sources="analyticsData.source_analytics" 
        :customers="analyticsData.customer_analytics" 
        :eventCategories="analyticsData.event_category_analytics" 
        :programTypes="analyticsData.program_type_analytics" 
      />
      
      <!-- J & K & L. Finance, Data Quality & Management Notes -->
      <div class="grid grid-cols-1 xl:grid-cols-2 gap-6 print:grid-cols-1">
        <DataQualityPanel :quality="analyticsData.data_quality" />
        <ManagementEvaluationNotes 
          :executive="analyticsData.executive" 
          :target="analyticsData.target" 
        />
      </div>
      
      <!-- Collapsible Legacy BI section -->
      <div class="glass-panel p-5 bg-charcoal-800 border border-charcoal-700 rounded-3xl space-y-4 print:hidden">
        <div class="flex items-center justify-between cursor-pointer select-none" @click="showLegacyBI = !showLegacyBI">
          <h3 class="text-xs font-bold text-white tracking-widest uppercase flex items-center gap-2">
            <svg class="w-4.5 h-4.5 text-charcoal-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 6a7.5 7.5 0 107.5 7.5h-7.5V6z" />
              <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 10.5H21A7.5 7.5 0 0013.5 3v7.5z" />
            </svg>
            Legacy Operational BI Streams (Tabs view)
          </h3>
          <span class="text-xs text-charcoal-400 font-bold hover:underline">
            {{ showLegacyBI ? 'Collapse Section' : 'Expand Section' }}
          </span>
        </div>
        
        <div v-show="showLegacyBI" class="pt-4 border-t border-charcoal-700 space-y-6">
          <div v-if="legacyLoading" class="py-12 flex flex-col items-center justify-center gap-3">
            <svg class="animate-spin h-8 w-8 text-brand-orange" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span class="text-xs font-bold text-charcoal-400 tracking-wider">Syncing operational data stream...</span>
          </div>
          <DashboardLegacy v-else :stats="stats" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'

// Import Refactored Subcomponents
import DashboardHeader from '../components/dashboard/DashboardHeader.vue'
import DashboardFilters from '../components/dashboard/DashboardFilters.vue'
import ExecutiveKpiCards from '../components/dashboard/ExecutiveKpiCards.vue'
import ExecutiveSummaryNarrative from '../components/dashboard/ExecutiveSummaryNarrative.vue'
import RevenueSummary from '../components/dashboard/RevenueSummary.vue'
import StatusSummary from '../components/dashboard/StatusSummary.vue'
import PoPerformanceTable from '../components/dashboard/PoPerformanceTable.vue'
import PmWorkloadTable from '../components/dashboard/PmWorkloadTable.vue'
import SourceAnalytics from '../components/dashboard/SourceAnalytics.vue'
import DataQualityPanel from '../components/dashboard/DataQualityPanel.vue'
import ManagementEvaluationNotes from '../components/dashboard/ManagementEvaluationNotes.vue'
import DashboardLegacy from '../components/dashboard/DashboardLegacy.vue'

const stats = ref({})
const legacyLoading = ref(false)
const showLegacyBI = ref(false)

const analyticsData = ref(null)
const analyticsLoading = ref(true)

const analyticsFilters = ref({
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
})

const usersList = ref([])

// Load users list for filters
const loadUsers = async () => {
  try {
    const response = await axios.get('/api/v1/auth/users')
    usersList.value = response.data
  } catch (err) {
    console.error('Failed to load user credentials list', err)
  }
}

// Fetch master analytics response
const fetchAnalytics = async () => {
  analyticsLoading.value = true
  try {
    const params = {}
    for (const key in analyticsFilters.value) {
      if (analyticsFilters.value[key]) {
        params[key] = analyticsFilters.value[key]
      }
    }
    const response = await axios.get('/api/v1/dashboard/analytics', { params })
    analyticsData.value = response.data
  } catch (err) {
    console.error('Failed to load dashboard analytics metrics', err)
  } finally {
    analyticsLoading.value = false
  }
}

// Fetch legacy aggregates when legacy tab is expanded
const fetchDashboard = async () => {
  legacyLoading.value = true
  try {
    const params = {}
    for (const key in analyticsFilters.value) {
      if (analyticsFilters.value[key]) {
        params[key] = analyticsFilters.value[key]
      }
    }
    const response = await axios.get('/api/v1/dashboard', { params })
    stats.value = response.data
  } catch (err) {
    console.error('Failed to load legacy dashboard statistics', err)
  } finally {
    legacyLoading.value = false
  }
}

// Watch legacy BI expanded status
watch(showLegacyBI, (val) => {
  if (val && Object.keys(stats.value).length === 0) {
    fetchDashboard()
  }
})

// Listen to filter updates
const onFiltersChanged = (newFilters) => {
  analyticsFilters.value = newFilters
  fetchAnalytics()
  if (showLegacyBI.value) {
    fetchDashboard()
  }
}

const onFiltersReset = () => {
  analyticsFilters.value = {
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
  fetchAnalytics()
  if (showLegacyBI.value) {
    fetchDashboard()
  }
}

const triggerPrint = () => {
  window.print()
}

onMounted(() => {
  loadUsers()
  fetchAnalytics()
})
</script>

<style scoped>
.glass-panel {
  background: rgba(26, 32, 44, 0.7);
  backdrop-filter: blur(12px);
}
</style>

<!-- Global print style definitions -->
<style>
@media print {
  body {
    background: #ffffff !important;
    background-color: #ffffff !important;
    color: #1a202c !important;
  }
  
  /* Hide navigation panels, app sidebar, reset buttons and BI tabs */
  header, nav, aside, .sidebar, .navbar, .no-print, button, .print\:hidden {
    display: none !important;
  }

  /* Make main layout full width */
  main, .content, .container, .space-y-6 {
    width: 100% !important;
    max-width: 100% !important;
    padding: 0 !important;
    margin: 0 !important;
    background: transparent !important;
    border: none !important;
  }

  /* Force page breaks on specific tables/grids if too long */
  .grid {
    page-break-inside: avoid;
  }
}
</style>
