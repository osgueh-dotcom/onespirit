<template>
  <div class="w-full max-w-md bg-brand-charcoal border border-brand-charcoal-light/35 rounded-3xl shadow-2xl p-8 relative overflow-hidden select-none">
    <!-- Glow effect -->
    <div class="absolute -top-40 -right-40 w-80 h-80 bg-brand-orange/10 rounded-full blur-3xl pointer-events-none"></div>
    <div class="absolute -bottom-40 -left-40 w-80 h-80 bg-brand-blue/5 rounded-full blur-3xl pointer-events-none"></div>

    <div class="text-center mb-8 relative">
      <div class="h-14 w-14 bg-gradient-to-tr from-brand-orange to-brand-orange-light rounded-2xl flex items-center justify-center shadow-lg shadow-brand-orange/30 mx-auto mb-4 animate-bounce">
        <span class="text-white font-extrabold text-2xl font-sans">1</span>
      </div>
      <h2 class="text-2xl font-extrabold text-white tracking-wide font-sans">ONE<span class="text-brand-orange">SPIRIT</span> ASIA</h2>
      <p class="text-xs text-gray-400 mt-1.5 font-medium">Operational Management Ledger</p>
    </div>

    <!-- Error Callout -->
    <div v-if="auth.error" class="mb-5 p-3.5 bg-red-500/10 border border-red-500/20 text-red-400 rounded-xl text-xs font-semibold leading-relaxed flex items-center gap-2">
      <span class="h-2 w-2 rounded-full bg-red-500 shrink-0"></span>
      {{ auth.error }}
    </div>

    <form @submit.prevent="handleLogin" class="space-y-5 relative">
      <div>
        <label for="email" class="block text-xs font-bold text-gray-300 uppercase tracking-widest mb-2">Email Korporat</label>
        <input 
          v-model="email" 
          type="email" 
          id="email" 
          required 
          placeholder="email@onespirit.asia"
          class="w-full px-4 py-3 rounded-xl bg-brand-charcoal-dark border border-brand-charcoal-light/45 hover:border-brand-orange/30 focus:border-brand-orange/90 text-white placeholder-gray-500 outline-none transition-all text-sm font-medium"
        />
      </div>

      <div>
        <div class="flex items-center justify-between mb-2">
          <label for="password" class="block text-xs font-bold text-gray-300 uppercase tracking-widest">Kata Sandi</label>
        </div>
        <input 
          v-model="password" 
          type="password" 
          id="password" 
          required 
          placeholder="••••••••"
          class="w-full px-4 py-3 rounded-xl bg-brand-charcoal-dark border border-brand-charcoal-light/45 hover:border-brand-orange/30 focus:border-brand-orange/90 text-white placeholder-gray-500 outline-none transition-all text-sm font-medium"
        />
      </div>

      <button 
        type="submit" 
        :disabled="auth.loading"
        class="w-full py-3.5 rounded-xl bg-gradient-to-r from-brand-orange to-brand-orange-light text-white font-bold text-sm tracking-wide shadow-lg shadow-brand-orange/20 hover:shadow-brand-orange/45 hover:from-brand-orange-light hover:to-brand-orange transition-all duration-300 active:scale-[0.98] disabled:opacity-50 select-none flex items-center justify-center gap-2"
      >
        <svg v-if="auth.loading" class="animate-spin h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <span>{{ auth.loading ? 'Memasuki Sistem...' : 'Masuk' }}</span>
      </button>
    </form>

    <!-- Demo account helper -->
    <div class="mt-8 pt-6 border-t border-brand-charcoal-light/25 text-center">
      <div class="inline-block px-4 py-3 bg-brand-charcoal-light/15 border border-brand-charcoal-light/20 rounded-xl text-left max-w-xs">
        <p class="text-[10px] font-extrabold text-brand-orange uppercase tracking-wider mb-1 flex items-center gap-1.5">
          <span class="h-1.5 w-1.5 rounded-full bg-brand-orange animate-ping"></span>
          Akses Akun Demo
        </p>
        <p class="text-[11px] text-gray-400 leading-relaxed">
          Email: <span class="text-white font-mono font-medium">demo@onespirit.asia</span><br/>
          Kata sandi diberikan oleh presenter dan tidak ditampilkan di aplikasi.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'

const auth = useAuthStore()
const router = useRouter()

const email = ref('')
const password = ref('')

const handleLogin = async () => {
  const success = await auth.login(email.value, password.value)
  if (success) {
    router.push('/')
  }
}
</script>
