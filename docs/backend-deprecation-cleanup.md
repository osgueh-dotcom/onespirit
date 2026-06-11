# Backend Deprecation Cleanup - Sprint 14 Phase 1

Phase 1 hanya mengubah API internal yang mekanis dan mempertahankan response contract.

## Warning Ditemukan

- Pydantic class-based `Config`.
- Pydantic `.dict()`.
- Pydantic `.from_orm()`.
- `datetime.utcnow()`.
- FastAPI `@app.on_event("startup")`.
- Starlette TestClient/httpx compatibility warning.

## Diperbaiki

- Settings memakai `SettingsConfigDict`.
- Service update payload memakai `model_dump(exclude_unset=True)`.
- Token dan timestamp terpilih memakai UTC timezone-aware source.
- Base model memakai helper `utc_now()` sambil mempertahankan naive UTC database compatibility.
- Project response schemas memakai `ConfigDict(from_attributes=True)`.
- Project router memakai `model_validate()`.
- FastAPI startup memakai lifespan.
- Warning total turun dari baseline Sprint 13 `919` menjadi `39`.

## Ditunda

- `ConfigDict` migration untuk auth, CRM, events, tasks, documents, finance, imports, event sources, dan dashboard.
- Full timezone-aware database column strategy.
- Starlette/httpx test client upgrade.

## Risiko

- Migrasi schema-wide dapat mengubah serialization jika dilakukan tanpa contract tests.
- Perubahan timezone column membutuhkan migration dan audit data lama.
- Dependency upgrade FastAPI/Starlette/httpx perlu diuji sebagai satu paket.

## Validation

```bash
cd backend
python -m pytest app/tests -q
```

Hasil Sprint 14: `29 passed, 39 warnings`.

## Phase 2

1. Migrasikan schema per modul dengan response contract tests.
2. Selesaikan seluruh `class Config`.
3. Putuskan strategi timezone database.
4. Selaraskan FastAPI, Starlette, dan httpx test stack.
