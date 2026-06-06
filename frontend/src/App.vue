<template>
  <!-- Guest Layout (Login Screen) -->
  <div v-if="isGuest" class="h-full bg-app-theme text-main-theme flex items-center justify-center p-4">
    <router-view />
  </div>

  <!-- Authenticated Shell Layout -->
  <div v-else class="h-full flex bg-app-theme text-main-theme overflow-hidden font-sans">
    <!-- Sidebar navigation -->
    <aside 
      class="bg-sidebar-theme border-r border-sidebar-theme transition-all duration-300 flex flex-col z-25 relative shrink-0"
      :class="sidebarCollapsed ? 'w-20' : 'w-64'"
    >
      <!-- Brand Logo Header -->
      <div class="h-16 flex items-center gap-3 px-5 border-b border-sidebar-theme overflow-hidden select-none">
        <div class="h-9 w-9 bg-gradient-to-tr from-brand-orange to-brand-orange-light rounded-xl flex items-center justify-center shadow-lg shadow-brand-orange/20 shrink-0">
          <span class="text-white font-extrabold text-lg font-sans">1</span>
        </div>
        <span v-if="!sidebarCollapsed" class="text-main-theme font-extrabold text-lg tracking-wider font-sans whitespace-nowrap">
          ONE<span class="text-brand-orange">SPIRIT</span>
        </span>
      </div>

      <!-- Navigation Links -->
      <nav class="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
        <router-link 
          v-for="item in navItems" 
          :key="item.name"
          :to="item.path"
          v-show="item.permission ? auth.hasPermission(item.permission) : true"
          class="flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all duration-200 group text-muted-theme hover:text-main-theme hover:bg-brand-charcoal-light/10"
          active-class="bg-brand-orange/10 !text-brand-orange border-l-2 border-brand-orange"
        >
          <component :is="item.icon" class="h-5 w-5 shrink-0 group-hover:scale-105 transition-transform" />
          <span v-if="!sidebarCollapsed" class="font-bold text-sm whitespace-nowrap">{{ item.name }}</span>
        </router-link>
      </nav>

      <!-- Sidebar Footer User Profile -->
      <div class="p-3 border-t border-sidebar-theme overflow-hidden">
        <div class="flex items-center gap-3 p-2 rounded-xl bg-brand-charcoal-light/5">
          <div class="h-9 w-9 bg-brand-orange-soft/10 text-brand-orange rounded-lg font-bold flex items-center justify-center shrink-0">
            {{ userInitial }}
          </div>
          <div v-if="!sidebarCollapsed" class="min-w-0 flex-1">
            <p class="text-xs font-bold text-main-theme truncate">{{ auth.user?.full_name }}</p>
            <p class="text-[10px] text-brand-orange font-semibold truncate">{{ auth.user?.role?.name }}</p>
          </div>
        </div>
      </div>
    </aside>

    <!-- Main Content Workspace -->
    <div class="flex-1 flex flex-col min-w-0 overflow-hidden">
      <!-- Top header panel -->
      <header class="h-16 bg-header-theme border-b border-sidebar-theme backdrop-blur-md px-6 flex items-center justify-between shrink-0">
        <div class="flex items-center gap-4">
          <button 
            @click="sidebarCollapsed = !sidebarCollapsed"
            class="p-1.5 rounded-lg bg-brand-charcoal-light/10 border border-sidebar-theme hover:border-brand-orange/40 text-muted-theme hover:text-main-theme transition-all shrink-0"
          >
            <span class="sr-only">Toggle Sidebar</span>
            <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
          <h1 class="text-lg font-bold text-main-theme tracking-wide font-sans shrink-0">{{ currentPageName }}</h1>
        </div>

        <div class="flex items-center gap-4 shrink-0">
          <span class="px-2.5 py-1 text-[10px] uppercase font-extrabold tracking-widest rounded bg-brand-orange/10 text-brand-orange border border-brand-orange/20 select-none">
            {{ auth.user?.role?.name }}
          </span>

          <!-- Light / Dark Mode Toggle Button -->
          <button 
            @click="toggleTheme"
            class="p-2 rounded-xl bg-brand-charcoal-light/10 border border-sidebar-theme hover:border-brand-orange/40 text-muted-theme hover:text-main-theme transition-all shrink-0 flex items-center justify-center"
            title="Toggle Light/Dark Theme"
          >
            <!-- Sun Icon (Show in dark mode to switch to light) -->
            <svg v-if="darkMode" class="w-4.5 h-4.5 text-brand-orange" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 3v2.25m6.364.386l-1.591 1.591M21 12h-2.25m-.386 6.364l-1.591-1.591M12 18.75V21m-4.773-4.227l-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z" />
            </svg>
            <!-- Moon Icon (Show in light mode to switch to dark) -->
            <svg v-else class="w-4.5 h-4.5 text-brand-blue" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M21.752 15.002A9.718 9.718 0 0118 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 003 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 009.002-5.998z" />
            </svg>
          </button>

          <button 
            @click="logout"
            class="px-3.5 py-1.5 rounded-lg border border-sidebar-theme hover:border-red-500/40 text-xs font-bold text-muted-theme hover:text-red-400 hover:bg-red-500/5 transition-all select-none"
          >
            Sign Out
          </button>
        </div>
      </header>

      <!-- Router Content -->
      <main class="flex-1 overflow-y-auto p-6 min-w-0 relative">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from './store/auth'
import { 
  Squares2X2Icon, 
  UserGroupIcon, 
  BriefcaseIcon, 
  CurrencyDollarIcon, 
  FolderIcon,
  ArrowUpTrayIcon,
  ClipboardDocumentCheckIcon
} from '@heroicons/vue/24/outline'

const auth = useAuthStore()
const route = useRoute()
const router = useRouter()

const sidebarCollapsed = ref(false)
const darkMode = ref(true)

const isGuest = computed(() => route.meta.guest)

const userInitial = computed(() => {
  if (!auth.user?.full_name) return 'U'
  return auth.user.full_name.charAt(0).toUpperCase()
})

const currentPageName = computed(() => {
  return String(route.name || 'One Spirit Asia')
})

const navItems = [
  { name: 'Dashboard', path: '/', icon: Squares2X2Icon },
  { name: 'CRM Module', path: '/crm', icon: UserGroupIcon, permission: 'crm:read' },
  { name: 'Projects Workflow', path: '/projects', icon: BriefcaseIcon, permission: 'projects:read' },
  { name: 'Finance Tracker', path: '/finance', icon: CurrencyDollarIcon, permission: 'finance:read' },
  { name: 'Documents Hub', path: '/documents', icon: FolderIcon, permission: 'documents:read' },
  { name: 'Excel Importer', path: '/imports', icon: ArrowUpTrayIcon, permission: 'projects:write' },
  { name: 'PM Control Center', path: '/pm-control-center', icon: ClipboardDocumentCheckIcon, permission: 'projects:read' }
]

const toggleTheme = () => {
  darkMode.value = !darkMode.value
  if (darkMode.value) {
    document.documentElement.classList.remove('light')
    localStorage.setItem('theme', 'dark')
  } else {
    document.documentElement.classList.add('light')
    localStorage.setItem('theme', 'light')
  }
}

// On mount, load user theme preference
onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'light') {
    darkMode.value = false
    document.documentElement.classList.add('light')
  } else {
    darkMode.value = true
    document.documentElement.classList.remove('light')
  }
})

const logout = () => {
  auth.logout()
  router.push('/login')
}
</script>

<style scoped>
.bg-app-theme {
  transition: background-color 0.3s ease;
}
.bg-sidebar-theme {
  transition: background-color 0.3s ease, border-color 0.3s ease;
}
.border-sidebar-theme {
  transition: border-color 0.3s ease;
}
</style>
