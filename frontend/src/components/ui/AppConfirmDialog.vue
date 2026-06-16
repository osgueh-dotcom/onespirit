<template>
  <Teleport to="body">
    <Transition name="confirm-dialog">
      <div
        v-if="dialog"
        class="fixed inset-0 z-[80] flex items-end justify-center bg-black/60 p-4 backdrop-blur-sm sm:items-center"
        @click.self="cancel"
      >
        <section
          ref="dialogPanel"
          role="dialog"
          aria-modal="true"
          :aria-labelledby="titleId"
          :aria-describedby="messageId"
          tabindex="-1"
          class="w-full max-w-md rounded-2xl border bg-panel-theme p-5 text-main-theme shadow-2xl"
          :class="dialogToneClass"
          @keydown.esc.prevent="cancel"
        >
          <div class="flex items-start gap-3">
            <div
              class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl border"
              :class="dialogIconClass"
            >
              <svg v-if="dialog.tone === 'danger'" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v4m0 4h.01M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z" />
              </svg>
              <svg v-else-if="dialog.tone === 'warning'" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v4m0 4h.01M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z" />
              </svg>
              <svg v-else class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M8.625 9.75a3.375 3.375 0 116.75 0c0 2.25-3.375 2.25-3.375 4.5m0 3.75h.008v.008H12V18z" />
              </svg>
            </div>

            <div class="min-w-0 flex-1">
              <h2 :id="titleId" class="text-base font-black tracking-tight">
                {{ dialog.title }}
              </h2>
              <p :id="messageId" class="mt-1 text-sm font-medium leading-relaxed text-muted-theme">
                {{ dialog.message }}
              </p>
            </div>
          </div>

          <div class="mt-5 flex flex-col-reverse gap-2 sm:flex-row sm:justify-end">
            <button
              type="button"
              class="app-button-secondary min-h-10"
              @click="cancel"
            >
              {{ dialog.cancelText }}
            </button>
            <button
              type="button"
              class="inline-flex min-h-10 items-center justify-center rounded-xl px-4 py-2.5 text-xs font-extrabold text-white shadow-card transition-all active:scale-[0.98]"
              :class="confirmButtonClass"
              @click="confirmAction"
            >
              {{ dialog.confirmText }}
            </button>
          </div>
        </section>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { computed, nextTick, ref, watch } from 'vue'
import { useUiStore } from '../../store/ui'

const ui = useUiStore()
const dialogPanel = ref(null)
const titleId = 'app-confirm-title'
const messageId = 'app-confirm-message'

const dialog = computed(() => ui.confirmDialog)

watch(dialog, async (value) => {
  if (!value) return
  await nextTick()
  dialogPanel.value?.focus()
})

const dialogToneClass = computed(() => {
  if (dialog.value?.tone === 'danger') return 'border-red-500/35'
  if (dialog.value?.tone === 'warning') return 'border-amber-500/35'
  return 'border-panel-theme'
})

const dialogIconClass = computed(() => {
  if (dialog.value?.tone === 'danger') return 'border-red-500/25 bg-red-500/10 text-red-400'
  if (dialog.value?.tone === 'warning') return 'border-amber-500/25 bg-amber-500/10 text-amber-400'
  return 'border-brand-blue/25 bg-brand-blue/10 text-brand-blue'
})

const confirmButtonClass = computed(() => {
  if (dialog.value?.tone === 'danger') return 'bg-red-500 hover:bg-red-600'
  if (dialog.value?.tone === 'warning') return 'bg-amber-500 hover:bg-amber-600'
  return 'bg-brand-orange hover:bg-brand-orange-dark'
})

const cancel = () => {
  ui.resolveConfirm(false)
}

const confirmAction = () => {
  ui.resolveConfirm(true)
}
</script>

<style scoped>
.confirm-dialog-enter-active,
.confirm-dialog-leave-active {
  transition: opacity 0.2s ease;
}

.confirm-dialog-enter-active section,
.confirm-dialog-leave-active section {
  transition: transform 0.2s ease, opacity 0.2s ease;
}

.confirm-dialog-enter-from,
.confirm-dialog-leave-to {
  opacity: 0;
}

.confirm-dialog-enter-from section,
.confirm-dialog-leave-to section {
  opacity: 0;
  transform: translateY(12px);
}
</style>
