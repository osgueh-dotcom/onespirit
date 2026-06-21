# Frontend Agent Rules

- Follow existing Vue 3, Pinia, Vue Router, Tailwind, and shared UI conventions.
- Reuse `frontend/src/utils/access.js` for UI access decisions; never treat UI
  guards as a substitute for backend authorization.
- Keep CL, ROS, CK, PNL, status, owner, risk, and next action visible where they
  drive the workflow.
- Include loading, empty, error, validation, and unauthorized states where
  relevant.
- Preserve mobile/tablet usability and avoid adding more logic to oversized
  views when a focused component or composable clearly owns the behavior.
- Add or update Vitest coverage for shared logic and critical rendering changes.
- Validate from `frontend/` with `npm run lint`, `npm run test`,
  `npm run quality:scan`, `npm audit`, and `npm run build`.
