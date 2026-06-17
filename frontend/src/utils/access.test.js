import { describe, expect, it } from 'vitest'
import {
  canAccessItem,
  canUseDeveloperTools,
  canViewPnl,
  hasPermission
} from './access'

const userWith = (roleName, permissions = []) => ({
  role: { name: roleName, permissions }
})

describe('role-aware access helpers', () => {
  it('allows the admin permission to bypass item restrictions', () => {
    const admin = userWith('Super Admin', ['admin'])
    const namedAdmin = userWith('Admin', [])

    expect(hasPermission(admin, 'finance:write')).toBe(true)
    expect(hasPermission(namedAdmin, 'finance:write')).toBe(true)
    expect(canAccessItem(admin, {
      permission: 'projects:write',
      roles: ['Management']
    })).toBe(true)
    expect(canAccessItem(namedAdmin, {
      permission: 'projects:write',
      roles: ['Management']
    })).toBe(true)
    expect(canUseDeveloperTools(admin)).toBe(true)
    expect(canUseDeveloperTools(namedAdmin)).toBe(true)
  })

  it('requires both permission and allowed role for restricted navigation', () => {
    const management = userWith('Management', ['projects:write'])
    const staff = userWith('Staff', ['projects:write'])

    const importItem = {
      permission: 'projects:write',
      roles: ['Management']
    }

    expect(canAccessItem(management, importItem)).toBe(true)
    expect(canAccessItem(staff, importItem)).toBe(false)
  })

  it('allows formal PO and PM roles into their workflow control centers', () => {
    const po = userWith('PO', ['projects:read'])
    const pm = userWith('PM', ['projects:read'])

    expect(canAccessItem(po, {
      permission: 'projects:read',
      roles: ['Super Admin', 'Admin', 'Management', 'PO', 'Staff']
    })).toBe(true)
    expect(canAccessItem(pm, {
      permission: 'projects:read',
      roles: ['Super Admin', 'Admin', 'Management', 'PM', 'Staff']
    })).toBe(true)
  })

  it('limits PNL visibility to approved roles', () => {
    expect(canViewPnl(userWith('Finance', ['projects:read']))).toBe(true)
    expect(canViewPnl(userWith('Management', ['projects:read']))).toBe(true)
    expect(canViewPnl(userWith('Staff', ['projects:read']))).toBe(false)
  })
})
