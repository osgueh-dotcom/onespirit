import { defineStore } from 'pinia'

let toastId = 0

const TOAST_TYPES = ['success', 'error', 'warning', 'info']
const CONFIRM_TONES = ['danger', 'warning', 'default']

const normalizeToastType = (type) => {
  return TOAST_TYPES.includes(type) ? type : 'info'
}

const normalizeConfirmTone = (tone) => {
  return CONFIRM_TONES.includes(tone) ? tone : 'default'
}

const toMessage = (value, fallback = '') => {
  if (typeof value === 'string') return value
  if (value?.message && typeof value.message === 'string') return value.message
  return fallback
}

const DEFAULT_CONFIRM = {
  title: 'Konfirmasi Tindakan',
  message: 'Tindakan ini akan memengaruhi data operasional.',
  confirmText: 'Lanjutkan',
  cancelText: 'Batal',
  tone: 'default'
}

export const useUiStore = defineStore('ui', {
  state: () => ({
    toasts: [],
    confirmDialog: null
  }),
  actions: {
    showToast(options = {}) {
      const payload = typeof options === 'string' ? { message: options } : options
      const duration = Number.isFinite(payload.duration) ? payload.duration : 4200
      const toast = {
        id: ++toastId,
        type: normalizeToastType(payload.type),
        title: toMessage(payload.title),
        message: toMessage(payload.message),
        duration
      }

      this.toasts.push(toast)

      if (duration > 0) {
        window.setTimeout(() => {
          this.removeToast(toast.id)
        }, duration)
      }

      return toast.id
    },
    success(message, options = {}) {
      return this.showToast({
        ...options,
        type: 'success',
        title: options.title || 'Berhasil',
        message
      })
    },
    error(message, options = {}) {
      return this.showToast({
        ...options,
        type: 'error',
        title: options.title || 'Gagal',
        message
      })
    },
    warning(message, options = {}) {
      return this.showToast({
        ...options,
        type: 'warning',
        title: options.title || 'Perhatian',
        message
      })
    },
    info(message, options = {}) {
      return this.showToast({
        ...options,
        type: 'info',
        title: options.title || 'Informasi',
        message
      })
    },
    removeToast(id) {
      this.toasts = this.toasts.filter((toast) => toast.id !== id)
    },
    confirm (options = {}) {
      if (this.confirmDialog?.resolve) {
        this.confirmDialog.resolve(false)
      }

      return new Promise((resolve) => {
        this.confirmDialog = {
          ...DEFAULT_CONFIRM,
          ...options,
          tone: normalizeConfirmTone(options.tone),
          resolve
        }
      })
    },
    resolveConfirm(result) {
      if (!this.confirmDialog) return
      const resolve = this.confirmDialog.resolve
      this.confirmDialog = null
      resolve(Boolean(result))
    }
  }
})
