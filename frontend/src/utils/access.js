const ADMIN_ROLES = ['Super Admin', 'Admin']

const permissionsFor = (user) => user?.role?.permissions || []

export const hasRole = (user, roleName) => user?.role?.name === roleName

export const hasAnyRole = (user, roleNames = []) => {
  if (roleNames.length === 0) return true
  return roleNames.includes(user?.role?.name)
}

export const isAdminUser = (user) => {
  return permissionsFor(user).includes('admin') || hasAnyRole(user, ADMIN_ROLES)
}

export const hasPermission = (user, permission) => {
  if (!permission) return true
  return isAdminUser(user) || permissionsFor(user).includes(permission)
}

export const canAccessItem = (user, item = {}) => {
  if (!hasPermission(user, item.permission)) return false
  if (!item.roles || item.roles.length === 0 || isAdminUser(user)) return true
  return hasAnyRole(user, item.roles)
}

export const canViewPnl = (user) => {
  return isAdminUser(user) || hasAnyRole(user, ['Management', 'Finance'])
}

export const canUseDeveloperTools = (user) => isAdminUser(user)
