<template>
  <div class="space-y-6">
    <!-- Tab Selection -->
    <div class="flex border-b border-panel-theme overflow-x-auto select-none custom-scrollbar pb-1">
      <button 
        v-for="tab in legacyTabs" 
        :key="tab.id"
        @click="activeLegacyTab = tab.id"
        class="px-5 py-3 text-xs font-black uppercase tracking-wider border-b-2 transition-all duration-300 whitespace-nowrap"
        :class="activeLegacyTab === tab.id ? 'border-brand-orange text-brand-orange' : 'border-transparent text-muted-theme hover:text-main-theme'"
      >
        {{ tab.label }}
      </button>
    </div>

    <!-- 1. OVERVIEW VIEW PANEL -->
    <div v-if="activeLegacyTab === 'overview'" class="space-y-6">
      <!-- 4 KPI Cards -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <!-- Active Projects Card -->
        <div class="interactive-card p-5 relative overflow-hidden select-none">
          <div class="absolute -top-10 -right-10 w-24 h-24 bg-brand-orange/5 rounded-full blur-3xl"></div>
          <p class="text-[10px] font-extrabold uppercase tracking-widest text-muted-theme mb-1">Active Projects</p>
          <h3 class="text-3xl font-black text-main-theme font-sans">
            {{ stats.ongoing_projects || 0 }} 
            <span class="text-xs text-muted-theme font-semibold">/ {{ stats.total_projects || 0 }} total</span>
          </h3>
          <span class="inline-flex mt-3 text-[10px] font-bold text-brand-orange px-2.5 py-1 bg-brand-orange/10 rounded-lg">
            In Prep / Run State
          </span>
        </div>

        <!-- Upcoming Events Card -->
        <div class="interactive-card p-5 relative overflow-hidden select-none">
          <div class="absolute -top-10 -right-10 w-24 h-24 bg-brand-blue/5 rounded-full blur-2xl"></div>
          <p class="text-[10px] font-extrabold uppercase tracking-widest text-muted-theme mb-1">Upcoming Runs</p>
          <h3 class="text-3xl font-black text-main-theme font-sans">{{ stats.upcoming_events || 0 }}</h3>
          <span class="inline-flex mt-3 text-[10px] font-bold text-brand-blue px-2.5 py-1 bg-brand-blue/10 rounded-lg">
            Next 7 Days
          </span>
        </div>

        <!-- Revenue Collected Card -->
        <div class="interactive-card p-5 relative overflow-hidden select-none">
          <div class="absolute -top-10 -right-10 w-24 h-24 bg-brand-emerald/5 rounded-full blur-2xl"></div>
          <p class="text-[10px] font-extrabold uppercase tracking-widest text-muted-theme mb-1">Cash Received</p>
          <h3 class="text-2xl font-black text-brand-emerald font-sans">{{ formatMoney(stats.revenue_received) }}</h3>
          <span class="inline-flex mt-3.5 text-[10px] font-bold text-muted-theme">
            Projected Pipeline: {{ formatMoney(stats.revenue_projected) }}
          </span>
        </div>

        <!-- Pending Invoices Card -->
        <div class="interactive-card p-5 relative overflow-hidden select-none">
          <div class="absolute -top-10 -right-10 w-24 h-24 bg-rose-500/5 rounded-full blur-2xl"></div>
          <p class="text-[10px] font-extrabold uppercase tracking-widest text-muted-theme mb-1">Outstanding Balances</p>
          <h3 class="text-2xl font-black text-rose-400 font-sans">{{ formatMoney(stats.pending_invoices_amount) }}</h3>
          <span class="inline-flex mt-3.5 text-[10px] font-bold text-rose-400 px-2.5 py-1 bg-rose-500/10 rounded-lg">
            {{ stats.pending_invoices_count || 0 }} Pending Invoices
          </span>
        </div>
      </div>

      <!-- Upper Layout Grid: Area Chart & Alerts -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="lg:col-span-2 flex flex-col">
          <AreaChart :data="stats.monthly_trends || []" />
        </div>

        <!-- Alerts Board -->
        <div class="glass-panel p-6 flex flex-col h-[288px]">
          <h3 class="text-xs font-bold text-main-theme tracking-widest uppercase mb-4 shrink-0 flex items-center gap-2">
            <span class="h-2 w-2 rounded-full bg-brand-orange animate-pulse"></span>
            Critical Safety Alerts
          </h3>
          
          <div class="flex-1 overflow-y-auto space-y-3 pr-1 custom-scrollbar">
            <div v-if="!stats.alerts || stats.alerts.length === 0" class="h-full flex items-center justify-center text-xs font-semibold text-muted-theme text-center">
              All systems nominal.<br>No active bottlenecks.
            </div>
            <div 
              v-for="alert in stats.alerts" 
              :key="alert.message"
              class="p-3 rounded-xl flex items-start gap-2 border text-[11px] font-medium leading-relaxed bg-surface-theme transition-all hover:scale-[1.01]"
              :class="getAlertStyles(alert.type)"
            >
              <span class="h-2 w-2 rounded-full mt-1 shrink-0" :class="getAlertBulletColor(alert.type)"></span>
              <div>
                <span class="text-[9px] uppercase font-black tracking-widest block mb-0.5" :class="getAlertTextColor(alert.type)">
                  {{ alert.module }}
                </span>
                <p class="text-soft-theme font-semibold leading-normal">{{ alert.message }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Target Banner -->
      <div class="glass-panel p-6 rounded-3xl flex flex-col sm:flex-row items-center justify-between gap-6">
        <div class="space-y-1.5 text-center sm:text-left">
          <h4 class="text-xs font-bold uppercase tracking-widest text-brand-orange">Annual Confirmed collections vs Target 2025</h4>
          <p class="text-sm text-main-theme font-black">
            Target goal of <span class="text-emerald-400">Rp 9,200,000,000</span> set by One Spirit Asia executives.
          </p>
          <p class="text-xs text-muted-theme font-semibold">
            Currently achieved: {{ formatMoney(stats.revenue_received) }} Confirmed Revenue.
          </p>
        </div>
        
        <div class="flex flex-col items-center gap-1 shrink-0 select-none">
          <div class="relative w-20 h-20 flex items-center justify-center">
            <svg class="w-full h-full transform -rotate-90">
              <circle cx="40" cy="40" r="34" stroke="rgba(255,255,255,0.05)" stroke-width="6" fill="transparent" />
              <circle 
                cx="40" 
                cy="40" 
                r="34" 
                stroke="#FF6B00" 
                stroke-width="6" 
                fill="transparent" 
                :stroke-dasharray="213.6"
                :stroke-dashoffset="calculateDashoffset(stats.revenue_received, 9200000000)"
              />
            </svg>
            <span class="absolute text-xs font-black text-main-theme">
              {{ calculatePercentage(stats.revenue_received, 9200000000) }}%
            </span>
          </div>
          <span class="text-[9px] uppercase font-black text-muted-theme mt-1">Operational Progress</span>
        </div>
      </div>
    </div>

    <!-- 2. REVENUE ANALYSIS TAB -->
    <div v-if="activeLegacyTab === 'revenue'" class="space-y-6">
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-5 select-none">
        <div class="interactive-card p-5">
          <p class="text-[9px] font-black uppercase tracking-widest text-muted-theme">Total Projected Revenue</p>
          <h4 class="text-2xl font-black text-main-theme mt-1">{{ formatMoney(stats.revenue_projected) }}</h4>
        </div>
        <div class="interactive-card p-5">
          <p class="text-[9px] font-black uppercase tracking-widest text-muted-theme">Confirmed Received Cash</p>
          <h4 class="text-2xl font-black text-emerald-400 mt-1">{{ formatMoney(stats.revenue_received) }}</h4>
        </div>
        <div class="interactive-card p-5">
          <p class="text-[9px] font-black uppercase tracking-widest text-muted-theme">Pending Pipeline Balance</p>
          <h4 class="text-2xl font-black text-brand-orange mt-1">{{ formatMoney((stats.revenue_projected || 0) - (stats.revenue_received || 0)) }}</h4>
        </div>
        <div class="interactive-card p-5">
          <p class="text-[9px] font-black uppercase tracking-widest text-muted-theme">Excel Conversion Rate</p>
          <h4 class="text-2xl font-black text-sky-400 mt-1">46.2%</h4>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="lg:col-span-2">
          <AreaChart :data="stats.monthly_trends || []" />
        </div>

        <div class="glass-panel p-6 flex flex-col h-[400px]">
          <h3 class="text-xs font-bold text-main-theme tracking-widest uppercase mb-4">Revenue share by Event Category</h3>
          <div class="flex-1 overflow-y-auto space-y-4 custom-scrollbar pr-1">
            <div 
              v-for="cat in stats.revenue_by_category || mockRevenueCategory" 
              :key="cat.category"
              class="space-y-1.5"
            >
              <div class="flex justify-between text-xs font-bold select-none">
                <span class="text-soft-theme">{{ cat.category }}</span>
                <span class="text-main-theme">{{ formatMoney(cat.amount) }}</span>
              </div>
              <div class="h-2 w-full bg-surface-theme rounded-full overflow-hidden">
                <div 
                  class="h-full bg-brand-orange transition-all duration-300"
                  :style="`width: ${calculatePercentage(cat.amount, stats.revenue_projected)}%`"
                ></div>
              </div>
            </div>
          </div>
        </div>

        <div class="glass-panel p-6 flex flex-col h-[400px]">
          <h3 class="text-xs font-bold text-main-theme tracking-widest uppercase mb-4">Revenue shares by Sales PM</h3>
          <div class="flex-1 overflow-y-auto space-y-4 custom-scrollbar pr-1">
            <div 
              v-for="pm_rev in stats.revenue_by_sales || mockRevenuePM" 
              :key="pm_rev.sales"
              class="space-y-1.5"
            >
              <div class="flex justify-between text-xs font-bold select-none">
                <span class="text-soft-theme">{{ pm_rev.sales }}</span>
                <span class="text-main-theme">{{ formatMoney(pm_rev.amount) }}</span>
              </div>
              <div class="h-2 w-full bg-surface-theme rounded-full overflow-hidden">
                <div 
                  class="h-full bg-sky-400 transition-all duration-300"
                  :style="`width: ${calculatePercentage(pm_rev.amount, stats.revenue_projected)}%`"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 3. WORKFLOW PIPELINE TAB -->
    <div v-if="activeLegacyTab === 'workflow'" class="space-y-6">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="glass-panel p-6 flex flex-col h-[400px]">
          <h3 class="text-xs font-bold text-main-theme tracking-widest uppercase mb-3 shrink-0">Pipeline Conversion Funnel</h3>
          <div class="flex-1 flex items-center justify-center overflow-hidden">
            <FunnelChart :data="stats.pipeline_funnel || []" />
          </div>
        </div>

        <div class="glass-panel p-6 flex flex-col h-[400px]">
          <h3 class="text-xs font-bold text-main-theme tracking-widest uppercase mb-3 shrink-0">Projects Status Shares</h3>
          <div class="flex-1 flex items-center justify-center overflow-hidden">
            <DonutChart :data="stats.project_status_counts || {}" />
          </div>
        </div>

        <div class="glass-panel p-6 flex flex-col h-[400px]">
          <h3 class="text-xs font-bold text-main-theme tracking-widest uppercase mb-4">Workflow Conversion Insights</h3>
          <div class="space-y-5 flex-1 overflow-y-auto pr-1 custom-scrollbar select-none text-xs leading-relaxed font-semibold">
            <div class="p-4 bg-surface-theme border border-panel-theme rounded-xl space-y-1">
              <span class="text-[9px] uppercase tracking-wider text-brand-orange block">Inquiry to Quote</span>
              <span class="text-xl font-black text-main-theme">53.7% Rate</span>
              <p class="text-muted-theme mt-1">Excellent initial engagement. The sales PIC team is highly responsive to incoming corporate hotel briefs.</p>
            </div>
            <div class="p-4 bg-surface-theme border border-panel-theme rounded-xl space-y-1">
              <span class="text-[9px] uppercase tracking-wider text-sky-400 block">Quote to Deal conversion</span>
              <span class="text-xl font-black text-main-theme">46.2% Deal Rate</span>
              <p class="text-muted-theme mt-1">Almost half of all generated proposals convert successfully into actual cash budget operations.</p>
            </div>
            <div class="p-4 bg-surface-theme border border-panel-theme rounded-xl space-y-1">
              <span class="text-[9px] uppercase tracking-wider text-emerald-400 block">Run Phase completed</span>
              <span class="text-xl font-black text-main-theme">96.8% Success Rate</span>
              <p class="text-muted-theme mt-1">Event schedules are completed flawlessly by Dago Highlands operations with negligible cancel rates.</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 4. TEAM WORKLOADS TAB -->
    <div v-if="activeLegacyTab === 'workloads'" class="space-y-6">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="lg:col-span-2 glass-panel p-6 flex flex-col h-[450px]">
          <h3 class="text-xs font-bold text-main-theme tracking-widest uppercase mb-3 shrink-0">PM Allocation Workloads</h3>
          <div class="flex-1 flex items-center justify-center overflow-hidden">
            <WorkbarChart :data="stats.team_workload || []" />
          </div>
        </div>

        <div class="glass-panel p-6 flex flex-col h-[450px]">
          <h3 class="text-xs font-bold text-main-theme tracking-widest uppercase mb-4">Operations Task Balance</h3>
          <div class="flex-1 overflow-y-auto space-y-4 custom-scrollbar pr-1 select-none text-xs">
            <div v-if="!stats.team_workload || stats.team_workload.length === 0" class="h-full flex items-center justify-center text-muted-theme text-center font-bold">
              No tasks currently assigned to PM staff.
            </div>
            <div 
              v-for="pm_work in stats.team_workload" 
              :key="pm_work.name"
              class="p-3.5 bg-surface-theme border border-panel-theme rounded-xl flex items-center justify-between gap-4 font-bold"
            >
              <div class="space-y-1">
                <span class="text-xs font-bold text-main-theme block">{{ pm_work.name }}</span>
                <span class="text-[9px] uppercase font-black text-muted-theme bg-panel-theme py-0.5 px-1.5 rounded">
                  PIC PM
                </span>
              </div>
              <div class="text-right space-y-1">
                <span class="text-xs font-black text-brand-orange block">{{ pm_work.total }} Active Tasks</span>
                <span class="text-[10px] text-emerald-400 font-bold">
                  {{ calculatePercentage(pm_work.done, pm_work.total) }}% Done
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 5. CENTRAL TIMELINE TAB -->
    <div v-if="activeLegacyTab === 'timeline'" class="space-y-6">
      <div class="glass-panel p-6 flex flex-col max-h-[700px]">
        <div class="flex items-center justify-between border-b border-panel-theme pb-4 mb-4">
          <div class="flex flex-col">
            <h3 class="text-xs font-bold text-main-theme tracking-widest uppercase flex items-center gap-2">
              <span class="w-2 h-2 rounded-full bg-brand-emerald animate-pulse"></span>
              Centralized Operational Timeline
            </h3>
            <span class="text-[10px] text-muted-theme font-semibold">Real-time status, payments, and checklists ledger</span>
          </div>
        </div>

        <div class="overflow-y-auto space-y-3.5 pr-2 max-h-[580px] custom-scrollbar">
          <div v-if="!stats.recent_activities || stats.recent_activities.length === 0" class="py-12 flex flex-col items-center justify-center text-xs font-semibold text-muted-theme text-center gap-2">
            <span>No operational activities logged in the matrix.</span>
          </div>
          
          <div 
            v-for="log in stats.recent_activities" 
            :key="log.id"
            class="flex items-start gap-4 p-3.5 bg-surface-theme border border-panel-theme hover:border-brand-orange/30 rounded-xl transition-all duration-200"
          >
            <div 
              class="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 text-white font-bold"
              :class="getActionStyles(log.action).bg"
            >
              <svg class="w-4.5 h-4.5" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" :d="getActionStyles(log.action).icon" />
              </svg>
            </div>

            <div class="flex-1 min-w-0">
              <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-1">
                <span class="text-xs font-black text-main-theme capitalize leading-none">
                  {{ getActionStyles(log.action).label }}
                </span>
                <span class="text-[9px] font-bold text-muted-theme uppercase tracking-widest sm:text-right">
                  {{ formatTimeAgo(log.created_at) }}
                </span>
              </div>

              <p class="text-xs text-soft-theme mt-1 font-semibold leading-relaxed">
                {{ formatLogDetails(log) }}
              </p>

              <div class="flex items-center gap-2.5 mt-2 text-[10px] font-bold text-muted-theme">
                <span class="flex items-center gap-1">
                  <svg class="w-3.5 h-3.5 text-muted-theme" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
                  </svg>
                  {{ log.user_name }}
                </span>
                <span>•</span>
                <span class="uppercase text-[9px] tracking-wider bg-panel-theme py-0.5 px-1.5 rounded border border-panel-theme">
                  {{ log.entity_type }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import AreaChart from '../charts/AreaChart.vue'
import FunnelChart from '../charts/FunnelChart.vue'
import DonutChart from '../charts/DonutChart.vue'
import WorkbarChart from '../charts/WorkbarChart.vue'

defineProps({
  stats: {
    type: Object,
    required: true,
    default: () => ({})
  }
})

const activeLegacyTab = ref('overview')

const legacyTabs = [
  { id: 'overview', label: 'Overview Metrics' },
  { id: 'revenue', label: 'Revenue Shares' },
  { id: 'workflow', label: 'Workflow Funnel' },
  { id: 'workloads', label: 'PM Task Load' },
  { id: 'timeline', label: 'Live activity Stream' }
]

const formatMoney = (val) => {
  if (val >= 1e9) {
    return 'Rp ' + (val / 1e9).toFixed(2) + ' B'
  }
  if (val >= 1e6) {
    return 'Rp ' + (val / 1e6).toFixed(1) + ' M'
  }
  return 'Rp ' + Number(val || 0).toLocaleString('id-ID')
}

const calculatePercentage = (part, total) => {
  if (!total || total <= 0) return 0
  return Math.round((part / total) * 100)
}

const calculateDashoffset = (received, target) => {
  if (!target || target <= 0) return 213.6
  const percentage = received / target
  const dasharray = 213.6
  if (percentage >= 1) return 0
  return dasharray - (percentage * dasharray)
}

const getAlertStyles = (type) => {
  if (type === 'danger') return 'bg-red-500/5 border-red-500/15'
  if (type === 'warning') return 'bg-brand-orange/5 border-brand-orange/15'
  return 'bg-brand-blue/5 border-brand-blue/15'
}

const getAlertBulletColor = (type) => {
  if (type === 'danger') return 'bg-red-500'
  if (type === 'warning') return 'bg-brand-orange'
  return 'bg-brand-blue'
}

const getAlertTextColor = (type) => {
  if (type === 'danger') return 'text-red-400'
  if (type === 'warning') return 'text-brand-orange'
  return 'text-brand-blue'
}

const getActionStyles = (action) => {
  const configs = {
    project_created: {
      bg: 'bg-orange-500',
      label: 'New Project Registered',
      icon: 'M12 9v6m3-3H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z'
    },
    status_transitioned: {
      bg: 'bg-indigo-500',
      label: 'Project Status Shifted',
      icon: 'M19.5 12c0-1.232-.046-2.453-.138-3.662a4.006 4.006 0 00-3.7-3.7 48.656 48.656 0 00-7.324 0 4.006 4.006 0 00-3.7 3.7c-.017.22-.032.441-.046.662M19.5 12l3-3m-3 3l-3-3m-12 3c0 1.232.046 2.453.138 3.662a4.006 4.006 0 003.7 3.7 48.656 48.656 0 007.324 0 4.006 4.006 0 003.7-3.7c.017-.22.032-.441.046-.662M4.5 12l3 3m-3-3l-3 3'
    },
    project_archived: {
      bg: 'bg-gray-600',
      label: 'Project Archived',
      icon: 'M20.25 7.5l-.625 10.632a2.25 2.25 0 01-2.247 2.118H6.622a2.25 2.25 0 01-2.247-2.118L3.75 7.5m8.25 3v6.75m0 0l-3-3m3 3l3-3M3.375 7.5h17.25c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125z'
    },
    task_allocated: {
      bg: 'bg-sky-500',
      label: 'Task Checklist Assigned',
      icon: 'M18 18.72a9.094 9.094 0 003.741-.479 3 3 0 00-4.682-2.72m.94 3.198l.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0112 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 016 18.719m12 0a5.971 5.971 0 00-.941-3.197m0 0A5.995 5.995 0 0012 12.75a5.995 5.995 0 00-5.058 2.772m0 0a3 3 0 00-4.681 2.72 8.986 8.986 0 003.74.477m.94-3.197a5.971 5.971 0 00-.94 3.197M15 6.75a3 3 0 11-6 0 3 3 0 016 0zm6 3a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0zm-13.5 0a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0z'
    },
    task_completed: {
      bg: 'bg-emerald-500',
      label: 'Task Checklist Completed',
      icon: 'M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z'
    },
    task_status_changed: {
      bg: 'bg-amber-500',
      label: 'Task Status Updated',
      icon: 'M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0115.75 21H5.25A2.25 2.25 0 013 18.75V8.25A2.25 2.25 0 015.25 6H10'
    },
    invoice_issued: {
      bg: 'bg-yellow-500',
      label: 'Invoice Issued',
      icon: 'M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z'
    },
    payment_receipt_posted: {
      bg: 'bg-emerald-600',
      label: 'Payment Posted',
      icon: 'M2.25 18.75a60.07 60.07 0 0115.797 2.101c.727.198 1.453-.342 1.453-1.096V18.75M3.75 4.5h16.5c.621 0 1.125.504 1.125 1.125v12.75c0 .621-.504 1.125-1.125 1.125H3.75c-.621 0-1.125-.504-1.125-1.125V5.625c0-.621.504-1.125 1.125-1.125zM12 9v4.5m0 0l-1.5-1.5m1.5 1.5l1.5-1.5'
    },
    invoice_status_synced: {
      bg: 'bg-teal-500',
      label: 'Invoice Balance Synced',
      icon: 'M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99'
    },
    document_linked: {
      bg: 'bg-cyan-500',
      label: 'Google Drive Asset Linked',
      icon: 'M18.375 2.25c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h.75c.621 0 1.125-.504 1.125-1.125V3.375c0-.621-.504-1.125-1.125-1.125h-.75zM8.25 2.25c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h.75c.621 0 1.125-.504 1.125-1.125V3.375c0-.621-.504-1.125-1.125-1.125h-.75zM3 10.125c0-.621.504-1.125 1.125-1.125h1.5c.621 0 1.125.504 1.125 1.125v3.75c0 .621-.504 1.125-1.125 1.125h-1.5c-.621 0-1.125-.504-1.125-1.125v-3.75z'
    },
    document_uploaded: {
      bg: 'bg-teal-500',
      label: 'Document Uploaded',
      icon: 'M12 16.5V9.75m0 0l3 3m-3-3l-3 3M6.75 19.5h10.5a2.25 2.25 0 002.25-2.25V6.75a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v10.5a2.25 2.25 0 002.25 2.25z'
    },
    customer_created: {
      bg: 'bg-emerald-500',
      label: 'Customer Created',
      icon: 'M19 7.5L12 3 5 7.5v9L12 21l7-4.5v-9z'
    },
    contact_linked: {
      bg: 'bg-blue-400',
      label: 'Contact Linked',
      icon: 'M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z'
    },
    user_login: {
      bg: 'bg-slate-500',
      label: 'Session Access Logged',
      icon: 'M15.75 5.25a3 3 0 013 3m3 0a6 6 0 01-7.029 5.912c-.563-.097-1.159.026-1.563.43L10.5 17.25H8.25v2.25H6v2.25H2.25v-2.818c0-.597.237-1.17.659-1.591l6.499-6.499c.404-.404.527-.999.43-1.563A6 6 0 1121.75 8.25z'
    },
    user_registered: {
      bg: 'bg-stone-500',
      label: 'User Account Created',
      icon: 'M18 7.5v3m0 0v3m0-3h3m-3 0h-3m-2.25-4.125a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zM3 19.235v-.111c0-1.89 1.437-3.444 3.313-3.55a12.046 12.046 0 019.374 0c1.876.105 3.313 1.66 3.313 3.55v.111c0 .848-.393 1.635-1.042 2.148A11.233 11.233 0 0112 22.5c-3.136 0-6.02-.857-8.47-2.314a2.298 2.298 0 01-1.04-1.951z'
    }
  }
  return configs[action] || {
    bg: 'bg-gray-500',
    label: 'System Update',
    icon: 'M9.813 15.904L9 21l5.904-.813a2 2 0 001.21-.683l4.88-4.88a2.001 2.001 0 00-2.83-2.83l-4.88 4.88a2 2 0 00-.683 1.21z'
  }
}

const formatTimeAgo = (isoString) => {
  if (!isoString) return ''
  const dateObj = new Date(isoString)
  const seconds = Math.floor((new Date() - dateObj) / 1000)
  
  if (seconds < 60) return 'Just now'
  const minutes = Math.floor(seconds / 60)
  if (minutes < 60) return `${minutes}m ago`
  const hours = Math.floor(minutes / 60)
  if (hours < 24) return `${hours}h ago`
  const days = Math.floor(hours / 24)
  if (days === 1) return 'Yesterday'
  if (days < 7) return `${days}d ago`
  
  return dateObj.toLocaleDateString('id-ID', {
    day: 'numeric',
    month: 'short',
    year: 'numeric'
  })
}

const formatLogDetails = (log) => {
  const d = log.details || {}
  switch (log.action) {
    case 'project_created':
      return `Created a new operational project: "${d.title}" under ${d.status || 'inquiry'} status.`
    case 'status_transitioned':
      return `Shifted project status for "${d.title}" from "${d.old_status}" → "${d.new_status}".`
    case 'project_archived':
      return `Deactivated and archived project: "${d.title}".`
    case 'task_allocated':
      return `Allocated a new checklist item: "${d.title}" under operational flow.`
    case 'task_completed':
      return `Completed task checklist item: "${d.title}" and approved milestones.`
    case 'task_status_changed':
      return `Marked task checklist item: "${d.title}" as "${d.status}".`
    case 'invoice_issued':
      return `Issued standard customer Invoice ${d.invoice_number} for total of ${formatMoney(d.amount)}.`
    case 'payment_receipt_posted':
      return `Approved customer Payment receipt reference: ${d.reference_number || 'N/A'} for amount of ${formatMoney(d.amount)} under invoice ${d.invoice_number}.`
    case 'invoice_status_synced':
      return `System synced Invoice ${d.invoice_number} status to "${d.new_status}" based on payment ledger.`
    case 'document_linked':
      return `Linked external Google Drive asset: "${d.title}" to project files.`
    case 'document_uploaded':
      return `Uploaded custom asset file: "${d.title}" (${d.file_type || 'Unknown'}).`
    case 'customer_created':
      return `Registered a new customer: "${d.company_name}" categorized as ${d.category || 'Standard'}.`
    case 'contact_linked':
      return `Linked representative contact point: "${d.name}" (${d.position || 'Staff'}).`
    case 'user_login':
      return `Authenticated and opened session: ${d.email}.`
    case 'user_registered':
      return `Registered a new system employee account: "${d.full_name}" (${d.email}).`
    default:
      return d.notes || `Logged operational change under ${log.entity_type} ID: ${log.entity_id || 'System'}.`
  }
}

const mockRevenueCategory = [
  { category: 'Gathering', amount: 15000000000.0 },
  { category: 'Entertainment', amount: 8000000000.0 },
  { category: 'Production', amount: 4500000000.0 },
  { category: 'Outbound/TB', amount: 3500000000.0 },
  { category: 'Other', amount: 515619883.0 }
]

const mockRevenuePM = [
  { sales: 'OME PIC Manager', amount: 12000000000.0 },
  { sales: 'JIP Sales Director', amount: 10500000000.0 },
  { sales: 'SYS Developer Support', amount: 6500000000.0 },
  { sales: 'TF Operations Lead', amount: 2515619883.0 }
]
</script>

<style scoped>
.glass-panel {
  background: rgba(26, 32, 44, 0.7);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}
.interactive-card {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.interactive-card:hover {
  transform: translateY(-4px);
  border-color: rgba(255, 107, 0, 0.35);
  box-shadow: 0 10px 20px -10px rgba(255, 107, 0, 0.15);
}
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
  height: 4px;
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
