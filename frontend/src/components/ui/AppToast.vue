<template>
  <div class="pointer-events-none fixed inset-x-0 top-3 z-[70] px-3 sm:left-auto sm:right-4 sm:top-4 sm:w-[26rem] sm:px-0">
    <TransitionGroup name="toast" tag="div" class="flex flex-col gap-2">
      <div
        v-for="toast in ui.toasts"
        :key="toast.id"
        class="pointer-events-auto flex items-start gap-3 rounded-xl border bg-panel-theme px-4 py-3 text-main-theme shadow-2xl backdrop-blur-md"
        :class="toastToneClass(toast.type)"
        :role="toast.type === 'error' ? 'alert' : 'status'"
        aria-live="polite"
      >
        <div
          class="mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-lg border"
          :class="toastIconClass(toast.type)"
        >
          <svg v-if="toast.type === 'success'" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
          </svg>
          <svg v-else-if="toast.type === 'error'" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v4m0 4h.01M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z" />
          </svg>
          <svg v-else-if="toast.type === 'warning'" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v4m0 4h.01M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z" />
          </svg>
          <svg v-else class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M11.25 11.25l.041-.02a.75.75 0 011.063.852l-.708 2.836a.75.75 0 001.063.853l.041-.021M12 8.25h.008v.008H12V8.25z" />
          </svg>
        </div>

        <div class="min-w-0 flex-1">
          <p class="text-sm font-extrabold leading-5">{{ toast.title || fallbackTitle(toast.type) }}</p>
          <p v-if="toast.message" class="mt-0.5 text-xs font-semibold leading-relaxed text-muted-theme">
            {{ toast.message }}
          </p>
        </div>

        <button
          type="button"
          class="mt-0.5 rounded-lg p-1.5 text-muted-theme transition-colors hover:bg-white/10 hover:text-main-theme"
          title="Tutup notifikasi"
          @click="ui.removeToast(toast.id)"
        >
          <span class="sr-only">Tutup notifikasi</span>
          <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </TransitionGroup>
  </div>
</template>

<script setup>
import { useUiStore } from '../../store/ui'

const ui = useUiStore()

const titles = {
  success: 'Berhasil',
  error: 'Gagal',
  warning: 'Perhatian',
  info: 'Informasi'
}

const fallbackTitle = (type) => titles[type] || titles.info

const toastToneClass = (type) => {
  if (type === 'success') return 'border-brand-emerald/30'
  if (type === 'error') return 'border-red-500/35'
  if (type === 'warning') return 'border-amber-500/35'
  return 'border-brand-blue/35'
}

const toastIconClass = (type) => {
  if (type === 'success') return 'border-brand-emerald/20 bg-brand-emerald/10 text-brand-emerald'
  if (type === 'error') return 'border-red-500/25 bg-red-500/10 text-red-400'
  if (type === 'warning') return 'border-amber-500/25 bg-amber-500/10 text-amber-400'
  return 'border-brand-blue/25 bg-brand-blue/10 text-brand-blue'
}
</script>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>
