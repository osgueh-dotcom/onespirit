<template>
  <div class="w-full max-w-5xl bg-white border border-slate-200 rounded-[28px] shadow-2xl shadow-slate-900/10 relative overflow-hidden select-none grid lg:grid-cols-[0.9fr_1.1fr]">
    <section class="relative hidden lg:flex flex-col justify-between overflow-hidden bg-brand-orange p-10 text-white">
      <div class="absolute inset-0 bg-gradient-to-br from-brand-orange via-brand-orange to-brand-orange-light opacity-95"></div>
      <div class="absolute -top-24 -right-20 h-64 w-64 rounded-full border-[42px] border-white/10"></div>
      <div class="absolute -bottom-32 -left-24 h-72 w-72 rounded-full border-[48px] border-brand-yellow/20"></div>

      <div class="relative">
        <div class="inline-flex rounded-2xl bg-white p-3 shadow-xl shadow-orange-900/10">
          <img :src="brandLogoUrl" alt="One Spirit Asia" class="h-16 w-64 object-contain" />
        </div>
      </div>

      <div class="relative max-w-sm">
        <p class="text-xs font-black uppercase tracking-[0.24em] text-brand-yellow">Operational Workflow System</p>
        <h1 class="mt-4 text-4xl font-black leading-tight tracking-tight">
          Satu ruang kerja untuk mengawal event dari inquiry sampai final report.
        </h1>
        <p class="mt-4 text-sm font-medium leading-relaxed text-white/80">
          Pantau CL, ROS, CK, PNL, readiness, revenue, dan koordinasi project dalam alur yang jelas.
        </p>
      </div>
    </section>

    <section class="p-7 sm:p-10 lg:p-12">
      <div class="lg:hidden mb-8">
        <img :src="brandLogoUrl" alt="One Spirit Asia" class="h-14 w-56 object-contain object-left" />
      </div>

      <div class="mb-8">
        <p class="app-kicker">Akses Workspace</p>
        <h2 class="mt-2 text-3xl font-black tracking-tight text-brand-charcoal">Selamat datang kembali</h2>
        <p class="mt-2 text-sm font-medium text-slate-500">
          Masuk untuk melanjutkan koordinasi project One Spirit Asia.
        </p>
      </div>

      <div
        v-if="auth.error"
        class="mb-5 p-3.5 bg-red-50 border border-red-200 text-red-700 rounded-xl text-xs font-semibold leading-relaxed flex items-center gap-2"
      >
        <span class="h-2 w-2 rounded-full bg-red-500 shrink-0"></span>
        {{ auth.error }}
      </div>

      <form @submit.prevent="handleLogin" class="space-y-5">
        <div>
          <label for="email" class="block text-xs font-extrabold text-slate-600 uppercase tracking-widest mb-2">
            Email Korporat
          </label>
          <input
            v-model="email"
            type="email"
            id="email"
            required
            autocomplete="email"
            placeholder="email@onespirit.asia"
            class="app-form-control"
          />
        </div>

        <div>
          <label for="password" class="block text-xs font-extrabold text-slate-600 uppercase tracking-widest mb-2">
            Kata Sandi
          </label>
          <input
            v-model="password"
            type="password"
            id="password"
            required
            autocomplete="current-password"
            placeholder="Masukkan kata sandi"
            class="app-form-control"
          />
        </div>

        <button type="submit" :disabled="auth.loading" class="app-button-primary w-full py-3.5 text-sm">
          <svg v-if="auth.loading" class="animate-spin h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span>{{ auth.loading ? 'Memasuki sistem...' : 'Masuk ke OneSpirit' }}</span>
        </button>
      </form>

      <div class="mt-8 rounded-2xl border border-brand-orange/15 bg-brand-orange-pastel p-4">
        <p class="text-[10px] font-extrabold text-brand-orange uppercase tracking-wider mb-1.5">
          Akses akun demo
        </p>
        <p class="text-xs text-slate-600 leading-relaxed">
          Gunakan <span class="font-mono font-bold text-brand-charcoal">demo@onespirit.asia</span>.
          Kata sandi diberikan terpisah oleh presenter.
        </p>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'

const auth = useAuthStore()
const router = useRouter()
const brandLogoUrl = `${import.meta.env.BASE_URL}brand/one-spirit-logo.png`

const email = ref('')
const password = ref('')

const handleLogin = async () => {
  const success = await auth.login(email.value, password.value)
  if (success) {
    router.push('/')
  }
}
</script>
