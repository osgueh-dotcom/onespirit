<template>
  <div class="p-6 bg-red-500/10 border border-red-500/20 rounded-3xl text-center space-y-4 select-none">
    <div class="flex flex-col items-center justify-center gap-2">
      <svg class="w-10 h-10 text-red-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
      </svg>
      <h4 class="text-sm font-extrabold text-white light:text-gray-900">{{ title }}</h4>
      <p class="text-xs text-gray-400 font-semibold max-w-md mx-auto light:text-gray-600">
        {{ message }}
      </p>
    </div>
    <div>
      <button 
        @click="$emit('retry')"
        class="py-2 px-6 bg-red-500 hover:bg-red-600 text-white text-xs font-black uppercase tracking-wider rounded-xl transition-all duration-200"
      >
        Coba Muat Ulang
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    default: 'Gagal Memuat Data'
  },
  message: {
    type: String,
    default: 'Gagal memuat data dari server. Periksa koneksi internet Anda atau coba kembali beberapa saat lagi.'
  }
})
defineEmits(['retry'])
</script>
