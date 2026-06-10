import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../store/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: () => import('../views/Login.vue'),
      meta: { guest: true }
    },
    {
      path: '/',
      name: 'Dashboard',
      component: () => import('../views/Dashboard.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/crm',
      name: 'CRM',
      component: () => import('../views/CRM.vue'),
      meta: { requiresAuth: true, permission: 'crm:read' }
    },
    {
      path: '/projects',
      name: 'Projects',
      component: () => import('../views/Projects.vue'),
      meta: { requiresAuth: true, permission: 'projects:read' }
    },
    {
      path: '/projects/:id',
      name: 'ProjectDetail',
      component: () => import('../views/ProjectDetail.vue'),
      meta: { requiresAuth: true, permission: 'projects:read' }
    },
    {
      path: '/finance',
      name: 'Finance',
      component: () => import('../views/Finance.vue'),
      meta: { requiresAuth: true, permission: 'finance:read' }
    },
    {
      path: '/documents',
      name: 'Documents',
      component: () => import('../views/Documents.vue'),
      meta: { requiresAuth: true, permission: 'documents:read' }
    },
    {
      path: '/imports',
      name: 'Imports',
      component: () => import('../views/Imports.vue'),
      meta: { requiresAuth: true, permission: 'projects:write' }
    },
    {
      path: '/pm-control-center',
      name: 'PMControlCenter',
      component: () => import('../views/PmControlCenter.vue'),
      meta: { requiresAuth: true, permission: 'projects:read' }
    },
    {
      path: '/po-control-center',
      name: 'POControlCenter',
      component: () => import('../views/PoControlCenter.vue'),
      meta: { requiresAuth: true, permission: 'projects:read' }
    },
    {
      path: '/source-vendor-performance',
      name: 'SourceVendorPerformance',
      component: () => import('../views/SourceVendorPerformance.vue'),
      meta: { requiresAuth: true, permission: 'projects:read' }
    }
  ]
})

// Navigation Guard
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  // Seed the store token on load
  if (authStore.token && !authStore.user) {
    await authStore.fetchMe()
  }

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return next({ name: 'Login' })
  }

  if (to.meta.guest && authStore.isAuthenticated) {
    return next({ name: 'Dashboard' })
  }

  if (to.meta.permission && !authStore.hasPermission(to.meta.permission)) {
    return next({ name: 'Dashboard' }) // Redirect back if unauthorized
  }

  next()
})

export default router
