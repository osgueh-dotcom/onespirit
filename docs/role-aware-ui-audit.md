# Role-aware UI Audit - Sprint 14

## Prinsip

- Backend permission adalah security gate utama.
- Frontend visibility adalah UX layer.
- Menu tersembunyi atau tombol disabled tidak boleh dianggap sebagai authorization.

## Role Saat Ini

| Role bisnis | Status implementasi |
|---|---|
| Super Admin | Seeded, permission `admin`, full bypass. |
| Admin | Seeded, permission `admin`, full bypass untuk user management dan workflow guard. |
| Management | Seeded, read/write lintas workflow; dipakai demo user. |
| PO | Seeded sebagai role komersial untuk CRM, project, finance read, documents, dan PO Control Center. |
| PM | Seeded sebagai role operasional untuk project, events, tasks, documents, dan PM Control Center. |
| Finance | Seeded dengan projects read, finance read/write, documents read. |
| Staff | Seeded sebagai role operasional umum. |
| Demo user | Role Management; credential diberikan melalui environment/presenter. |

## Menu Visibility Matrix

| Menu | Backend gate | UI Sprint 14 |
|---|---|---|
| Dashboard | Authenticated | Semua user terautentikasi. |
| Projects / Detail | `projects:read` | Berdasarkan permission. |
| PM Control | Authenticated backend | Super Admin/Admin/Management/PM/Staff + `projects:read`. |
| PO Control | Authenticated backend | Super Admin/Admin/Management/PO/Staff + `projects:read`. |
| Source & Vendor | Authenticated backend | Super Admin/Admin/Management/PO/Staff + `projects:read`. |
| Finance | `finance:read` | Berdasarkan permission. |
| Imports | `admin` atau `projects:write` | UI dibatasi Super Admin/Admin/Management. |
| CRM | `crm:read` | Berdasarkan permission. |
| Documents | `documents:read` | Berdasarkan permission. |
| Settings | Authenticated | Semua user; User Management hanya Admin/Super Admin. |

Finance tidak lagi melihat control center operasional hanya karena memiliki `projects:read`.

## Action Visibility Matrix

| Area | Action | UI gate | Backend gate |
|---|---|---|---|
| CRM | Create/delete customer/contact | `crm:write` | `crm:write` |
| Projects | Create/archive/quick transition | `projects:write` | `projects:write` |
| Project Detail | Status transition | Disabled tanpa `projects:write` | `projects:write` + readiness/role checks |
| ROS/event schedule | Create/update | `events:write` | `events:write` |
| CK/tasks | Create/update/delete | `tasks:write` | `tasks:write` |
| Documents | Add/delete | `documents:write` | `documents:write` |
| Instruments | Generate/create/update/delete | `projects:write` | `projects:write` |
| PNL link | View | Super Admin/Management/Finance | Backend response masking |
| Finance | Add/delete invoice/payment | `finance:write` | `finance:write` |
| Settings | Change own password | Authenticated | Current authenticated user |
| User Management | List/create/reset/status | Admin only | Permission `admin` |
| Developer tools | View | Admin only | Legacy dashboard endpoint authenticated |

## Backend Audit

- CRUD router utama memakai `PermissionChecker`.
- Tujuh endpoint dashboard modular yang sebelumnya tidak memiliki auth telah diberi `get_current_user`.
- Test memastikan endpoint tersebut mengembalikan 401 tanpa token.
- `/auth/users` dilindungi permission `admin`; `/auth/users/options` hanya menyediakan safe user reference data untuk workflow.
- `/auth/users` menerima alias role formal `admin`, `po`, dan `pm` saat admin membuat user.
- `PermissionChecker` memakai semantics "salah satu permission", bukan seluruh permission.

## Limitations

- Backend control center belum memiliki role-specific permission; UI restriction belum menjadi security restriction.
- Import backend masih dapat dipakai semua user dengan `projects:write`.
- `Staff` dengan `projects:write` masih dapat mengubah metadata/status instrumen PNL walaupun link response dimasking.
- Belum ada project-level ownership enforcement untuk PO/PM.
- Dashboard analytics belum dipisahkan berdasarkan sensitivitas role.

## Rekomendasi Sprint 21

1. Tambahkan permission khusus seperti `imports:write`, `pnl:read`, dan `pnl:write`.
2. Terapkan ownership gate per project untuk assigned PO/PM.
3. Tambahkan backend permission matrix tests untuk seluruh write endpoint.
4. Tentukan dashboard metrics yang boleh dilihat Finance, Staff, PO, dan PM.
