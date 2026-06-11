# Frontend Quality Baseline - Sprint 14

Sprint 14 menambahkan quality gate frontend tanpa refactor UI besar.

## Scripts

```bash
npm run lint
npm run test
npm run quality:scan
npm run build
```

- `lint`: ESLint flat config untuk JavaScript dan Vue 3.
- `test`: Vitest baseline.
- `quality:scan`: guard tambahan untuk debugger, `console.log`, local file URL, dan token secret di frontend.
- `build`: Vite production build.

GitHub Pages workflow menjalankan seluruh command tersebut sebelum deploy.

## ESLint Baseline

Konfigurasi berada di `frontend/eslint.config.js`.

Blocking rules:

- `no-debugger`
- `no-undef`

Non-blocking baseline:

- unused variables
- `console` selain `warn` dan `error`
- unused Vue template variables

Hasil Sprint 14: `0 errors`, `26 warnings`. Warning tidak disembunyikan dan menjadi cleanup backlog.

## Vitest Baseline

Test awal berada di `frontend/src/utils/access.test.js`.

Coverage baseline:

- admin bypass
- kombinasi permission dan allowed role
- visibility PNL

Hasil Sprint 14: `3 passed`.

## Dependency Audit

- `npm audit --omit=dev`: `0 vulnerabilities`.
- Full `npm audit`: dua advisory moderate pada Vite 5/esbuild development server.
- Advisory kritis Vitest telah diperbaiki dengan patch `3.2.6`.

Upgrade Vite major ditunda karena memerlukan compatibility test dan update Node image.

## Limitations

- Belum ada component test dengan Vue Test Utils.
- Belum ada coverage threshold.
- Warning lint legacy belum menjadi blocking.
- TypeScript/typecheck belum digunakan oleh project.
