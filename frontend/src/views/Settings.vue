<template>
  <div class="app-page max-w-7xl mx-auto">
    <section class="rounded-3xl border border-sidebar-theme bg-sidebar-theme p-6 shadow-sm">
      <div class="flex flex-col gap-2 md:flex-row md:items-start md:justify-between">
        <div>
          <p class="text-xs font-black uppercase tracking-[0.25em] text-brand-orange">Pengaturan Akun</p>
          <h2 class="mt-2 text-2xl font-black text-main-theme">Settings</h2>
          <p class="mt-2 text-sm text-muted-theme max-w-3xl">
            Kelola password akun dan akses user dasar untuk demo Zoom serta operasional awal OneSpirit Workflow.
          </p>
        </div>
        <div class="rounded-2xl border border-brand-orange/20 bg-brand-orange/10 px-4 py-3 text-xs text-brand-orange font-bold">
          Backend permission tetap menjadi security gate utama.
        </div>
      </div>
    </section>

    <div class="grid grid-cols-1 xl:grid-cols-3 gap-6">
      <section class="xl:col-span-1 rounded-3xl border border-sidebar-theme bg-sidebar-theme p-6 shadow-sm">
        <h3 class="text-lg font-black text-main-theme">Account Settings</h3>
        <div class="mt-5 space-y-4 text-sm">
          <div>
            <p class="text-xs uppercase tracking-widest text-muted-theme font-black">Email</p>
            <p class="mt-1 text-main-theme font-bold break-all">{{ auth.user?.email }}</p>
          </div>
          <div>
            <p class="text-xs uppercase tracking-widest text-muted-theme font-black">Nama</p>
            <p class="mt-1 text-main-theme font-bold">{{ auth.user?.full_name }}</p>
          </div>
          <div>
            <p class="text-xs uppercase tracking-widest text-muted-theme font-black">Role</p>
            <p class="mt-1 inline-flex rounded-full bg-brand-orange/10 px-3 py-1 text-brand-orange font-black">
              {{ auth.user?.role?.name }}
            </p>
          </div>
        </div>

        <div class="mt-6 rounded-2xl border border-blue-500/20 bg-blue-500/10 p-4">
          <p class="text-xs font-black uppercase tracking-widest text-blue-300">Demo Safety Note</p>
          <ul class="mt-2 space-y-1 text-xs text-muted-theme leading-relaxed">
            <li>Gunakan akun demo untuk presentasi.</li>
            <li>Jangan gunakan data asli saat demo publik.</li>
            <li>Ganti password demo setelah sesi public/tunnel.</li>
          </ul>
        </div>
      </section>

      <section class="xl:col-span-2 rounded-3xl border border-sidebar-theme bg-sidebar-theme p-6 shadow-sm">
        <h3 class="text-lg font-black text-main-theme">Ubah Password</h3>
        <p class="mt-1 text-sm text-muted-theme">Password baru minimal 8 karakter dan mengikuti policy backend.</p>

        <form class="mt-5 grid grid-cols-1 md:grid-cols-3 gap-4" @submit.prevent="changePassword">
          <label class="space-y-2">
            <span class="text-xs font-black uppercase tracking-widest text-muted-theme">Password Lama</span>
            <input
              v-model="passwordForm.current_password"
              type="password"
              autocomplete="current-password"
              required
              class="w-full rounded-xl border border-sidebar-theme bg-app-theme px-4 py-3 text-sm text-main-theme outline-none focus:border-brand-orange"
            />
          </label>
          <label class="space-y-2">
            <span class="text-xs font-black uppercase tracking-widest text-muted-theme">Password Baru</span>
            <input
              v-model="passwordForm.new_password"
              type="password"
              autocomplete="new-password"
              required
              class="w-full rounded-xl border border-sidebar-theme bg-app-theme px-4 py-3 text-sm text-main-theme outline-none focus:border-brand-orange"
            />
          </label>
          <label class="space-y-2">
            <span class="text-xs font-black uppercase tracking-widest text-muted-theme">Konfirmasi</span>
            <input
              v-model="passwordForm.confirm_password"
              type="password"
              autocomplete="new-password"
              required
              class="w-full rounded-xl border border-sidebar-theme bg-app-theme px-4 py-3 text-sm text-main-theme outline-none focus:border-brand-orange"
            />
          </label>
          <div class="md:col-span-3 flex flex-col sm:flex-row sm:items-center gap-3">
            <button
              type="submit"
              :disabled="passwordLoading"
              class="rounded-xl bg-brand-orange px-5 py-3 text-sm font-black text-white shadow-lg shadow-brand-orange/20 disabled:opacity-50"
            >
              {{ passwordLoading ? 'Menyimpan...' : 'Simpan Password Baru' }}
            </button>
            <p v-if="passwordMessage" class="text-sm font-bold text-green-400">{{ passwordMessage }}</p>
            <p v-if="passwordError" class="text-sm font-bold text-red-400">{{ passwordError }}</p>
          </div>
        </form>
      </section>
    </div>

    <section v-if="auth.isAdmin" class="rounded-3xl border border-sidebar-theme bg-sidebar-theme p-6 shadow-sm">
      <div class="flex flex-col gap-2 lg:flex-row lg:items-start lg:justify-between">
        <div>
          <h3 class="text-lg font-black text-main-theme">User Management</h3>
          <p class="mt-1 text-sm text-muted-theme">Hanya Super Admin/Admin yang dapat membuat user, reset password, dan mengubah status aktif.</p>
        </div>
        <button
          type="button"
          @click="loadUserManagement"
          :disabled="usersLoading"
          class="rounded-xl border border-sidebar-theme px-4 py-2 text-xs font-black text-muted-theme hover:text-main-theme disabled:opacity-50"
        >
          {{ usersLoading ? 'Memuat...' : 'Refresh User' }}
        </button>
      </div>

      <form class="mt-6 grid grid-cols-1 md:grid-cols-2 xl:grid-cols-5 gap-4 rounded-2xl border border-sidebar-theme bg-app-theme/40 p-4" @submit.prevent="createUser">
        <label class="space-y-2">
          <span class="text-xs font-black uppercase tracking-widest text-muted-theme">Email</span>
          <input v-model="createForm.email" type="email" required class="w-full rounded-xl border border-sidebar-theme bg-app-theme px-4 py-3 text-sm text-main-theme outline-none focus:border-brand-orange" />
        </label>
        <label class="space-y-2">
          <span class="text-xs font-black uppercase tracking-widest text-muted-theme">Nama</span>
          <input v-model="createForm.full_name" type="text" required class="w-full rounded-xl border border-sidebar-theme bg-app-theme px-4 py-3 text-sm text-main-theme outline-none focus:border-brand-orange" />
        </label>
        <label class="space-y-2">
          <span class="text-xs font-black uppercase tracking-widest text-muted-theme">Role</span>
          <select v-model="createForm.role_id" required class="w-full rounded-xl border border-sidebar-theme bg-app-theme px-4 py-3 text-sm text-main-theme outline-none focus:border-brand-orange">
            <option value="" disabled>Pilih role</option>
            <option v-for="role in roles" :key="role.id" :value="role.id">{{ role.name }}</option>
          </select>
        </label>
        <label class="space-y-2">
          <span class="text-xs font-black uppercase tracking-widest text-muted-theme">Password Awal</span>
          <input v-model="createForm.password" type="password" required autocomplete="new-password" class="w-full rounded-xl border border-sidebar-theme bg-app-theme px-4 py-3 text-sm text-main-theme outline-none focus:border-brand-orange" />
        </label>
        <div class="space-y-2">
          <span class="text-xs font-black uppercase tracking-widest text-muted-theme">Status</span>
          <label class="flex items-center gap-2 rounded-xl border border-sidebar-theme bg-app-theme px-4 py-3 text-sm text-main-theme">
            <input v-model="createForm.is_active" type="checkbox" class="h-4 w-4 accent-brand-orange" />
            Aktif
          </label>
        </div>
        <div class="md:col-span-2 xl:col-span-5 flex flex-col sm:flex-row sm:items-center gap-3">
          <button type="submit" :disabled="createLoading" class="rounded-xl bg-brand-orange px-5 py-3 text-sm font-black text-white disabled:opacity-50">
            {{ createLoading ? 'Membuat...' : 'Tambah User' }}
          </button>
          <p v-if="createMessage" class="text-sm font-bold text-green-400">{{ createMessage }}</p>
          <p v-if="createError" class="text-sm font-bold text-red-400">{{ createError }}</p>
        </div>
      </form>

      <div class="mt-6 overflow-x-auto rounded-2xl border border-sidebar-theme">
        <table class="min-w-full divide-y divide-sidebar-theme text-sm">
          <thead class="bg-app-theme/60 text-xs uppercase tracking-widest text-muted-theme">
            <tr>
              <th class="px-4 py-3 text-left">User</th>
              <th class="px-4 py-3 text-left">Role</th>
              <th class="px-4 py-3 text-left">Status</th>
              <th class="px-4 py-3 text-left">Dibuat</th>
              <th class="px-4 py-3 text-right">Aksi</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-sidebar-theme">
            <tr v-for="user in users" :key="user.id" class="text-main-theme">
              <td class="px-4 py-3">
                <p class="font-black">{{ user.full_name }}</p>
                <p class="text-xs text-muted-theme break-all">{{ user.email }}</p>
              </td>
              <td class="px-4 py-3">{{ user.role?.name || '-' }}</td>
              <td class="px-4 py-3">
                <span class="rounded-full px-3 py-1 text-xs font-black" :class="user.is_active ? 'bg-green-500/10 text-green-400' : 'bg-red-500/10 text-red-400'">
                  {{ user.is_active ? 'Aktif' : 'Nonaktif' }}
                </span>
              </td>
              <td class="px-4 py-3 text-muted-theme">{{ formatDate(user.created_at) }}</td>
              <td class="px-4 py-3">
                <div class="flex flex-wrap justify-end gap-2">
                  <button type="button" @click="beginReset(user)" class="rounded-lg border border-sidebar-theme px-3 py-1.5 text-xs font-black text-muted-theme hover:text-main-theme">
                    Reset Password
                  </button>
                  <button
                    type="button"
                    @click="toggleUserStatus(user)"
                    :disabled="statusLoadingId === user.id || user.id === auth.user?.id"
                    class="rounded-lg border px-3 py-1.5 text-xs font-black disabled:opacity-40"
                    :class="user.is_active ? 'border-red-500/30 text-red-400' : 'border-green-500/30 text-green-400'"
                  >
                    {{ user.is_active ? 'Nonaktifkan' : 'Aktifkan' }}
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <form v-if="resetUser" class="mt-5 rounded-2xl border border-brand-orange/20 bg-brand-orange/10 p-4" @submit.prevent="resetPassword">
        <p class="text-sm font-black text-main-theme">Reset password untuk {{ resetUser.full_name }}</p>
        <div class="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
          <input v-model="resetForm.new_password" type="password" required autocomplete="new-password" placeholder="Password baru" class="w-full rounded-xl border border-sidebar-theme bg-app-theme px-4 py-3 text-sm text-main-theme outline-none focus:border-brand-orange" />
          <input v-model="resetForm.confirm_password" type="password" required autocomplete="new-password" placeholder="Konfirmasi password baru" class="w-full rounded-xl border border-sidebar-theme bg-app-theme px-4 py-3 text-sm text-main-theme outline-none focus:border-brand-orange" />
        </div>
        <div class="mt-4 flex flex-col sm:flex-row sm:items-center gap-3">
          <button type="submit" :disabled="resetLoading" class="rounded-xl bg-brand-orange px-5 py-3 text-sm font-black text-white disabled:opacity-50">
            {{ resetLoading ? 'Menyimpan...' : 'Simpan Reset Password' }}
          </button>
          <button type="button" @click="cancelReset" class="rounded-xl border border-sidebar-theme px-5 py-3 text-sm font-black text-muted-theme">
            Batal
          </button>
          <p v-if="resetMessage" class="text-sm font-bold text-green-400">{{ resetMessage }}</p>
          <p v-if="resetError" class="text-sm font-bold text-red-400">{{ resetError }}</p>
        </div>
      </form>
    </section>

  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import axios from 'axios'
import { useAuthStore } from '../store/auth'

const auth = useAuthStore()

const passwordLoading = ref(false)
const passwordMessage = ref('')
const passwordError = ref('')
const passwordForm = reactive({
  current_password: '',
  new_password: '',
  confirm_password: ''
})

const users = ref([])
const roles = ref([])
const usersLoading = ref(false)
const createLoading = ref(false)
const createMessage = ref('')
const createError = ref('')
const createForm = reactive({
  email: '',
  full_name: '',
  role_id: '',
  password: '',
  is_active: true
})

const resetUser = ref(null)
const resetLoading = ref(false)
const resetMessage = ref('')
const resetError = ref('')
const resetForm = reactive({
  new_password: '',
  confirm_password: ''
})

const statusLoadingId = ref(null)

const selectedRole = computed(() => roles.value.find((role) => role.id === createForm.role_id))

const preferredCreateRole = () => {
  return roles.value.find((role) => role.name === 'Staff') || roles.value[0]
}

const ensureCreateRoleSelected = () => {
  if (!createForm.role_id && roles.value.length > 0) {
    createForm.role_id = preferredCreateRole()?.id || ''
  }
}

const readError = (error, fallback) => {
  const detail = error.response?.data?.detail
  if (Array.isArray(detail)) {
    return detail.map((item) => item.msg || item.message || String(item)).join(' ')
  }
  if (typeof detail === 'string') return detail
  return fallback
}

const clearPasswordForm = () => {
  passwordForm.current_password = ''
  passwordForm.new_password = ''
  passwordForm.confirm_password = ''
}

const changePassword = async () => {
  passwordLoading.value = true
  passwordMessage.value = ''
  passwordError.value = ''
  try {
    const response = await axios.patch('/api/v1/auth/me/password', { ...passwordForm })
    passwordMessage.value = response.data.message || 'Password berhasil diperbarui.'
    clearPasswordForm()
  } catch (error) {
    passwordError.value = readError(error, 'Gagal memperbarui password.')
  } finally {
    passwordLoading.value = false
  }
}

const loadUserManagement = async () => {
  if (!auth.isAdmin) return
  usersLoading.value = true
  createError.value = ''
  try {
    const [usersResponse, rolesResponse] = await Promise.all([
      axios.get('/api/v1/auth/users'),
      axios.get('/api/v1/auth/roles')
    ])
    users.value = usersResponse.data
    roles.value = rolesResponse.data
    ensureCreateRoleSelected()
  } catch (error) {
    createError.value = readError(error, 'Gagal memuat user management.')
  } finally {
    usersLoading.value = false
  }
}

const clearCreateForm = () => {
  createForm.email = ''
  createForm.full_name = ''
  createForm.password = ''
  createForm.is_active = true
  if (!selectedRole.value && roles.value.length > 0) {
    createForm.role_id = preferredCreateRole()?.id || ''
  }
}

const createUser = async () => {
  createLoading.value = true
  createMessage.value = ''
  createError.value = ''
  try {
    await axios.post('/api/v1/auth/users', { ...createForm })
    createMessage.value = 'User berhasil ditambahkan.'
    clearCreateForm()
    await loadUserManagement()
  } catch (error) {
    createError.value = readError(error, 'Gagal menambahkan user.')
  } finally {
    createLoading.value = false
  }
}

const beginReset = (user) => {
  resetUser.value = user
  resetMessage.value = ''
  resetError.value = ''
  resetForm.new_password = ''
  resetForm.confirm_password = ''
}

const cancelReset = () => {
  resetUser.value = null
  resetForm.new_password = ''
  resetForm.confirm_password = ''
  resetMessage.value = ''
  resetError.value = ''
}

const resetPassword = async () => {
  if (!resetUser.value) return
  resetLoading.value = true
  resetMessage.value = ''
  resetError.value = ''
  try {
    const response = await axios.patch(`/api/v1/auth/users/${resetUser.value.id}/password`, { ...resetForm })
    resetMessage.value = response.data.message || 'Password user berhasil diperbarui.'
    resetForm.new_password = ''
    resetForm.confirm_password = ''
  } catch (error) {
    resetError.value = readError(error, 'Gagal reset password user.')
  } finally {
    resetLoading.value = false
  }
}

const toggleUserStatus = async (user) => {
  statusLoadingId.value = user.id
  createError.value = ''
  try {
    await axios.patch(`/api/v1/auth/users/${user.id}/status`, {
      is_active: !user.is_active
    })
    await loadUserManagement()
  } catch (error) {
    createError.value = readError(error, 'Gagal mengubah status user.')
  } finally {
    statusLoadingId.value = null
  }
}

const formatDate = (value) => {
  if (!value) return '-'
  return new Intl.DateTimeFormat('id-ID', {
    year: 'numeric',
    month: 'short',
    day: '2-digit'
  }).format(new Date(value))
}

onMounted(() => {
  loadUserManagement()
})
</script>
