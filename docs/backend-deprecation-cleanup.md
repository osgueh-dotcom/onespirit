# Backend Deprecation Cleanup - Sprint 17

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
- Warning total turun dari baseline Sprint 13 `919` menjadi `37`.
- Auth, CRM, events, tasks, documents, finance, imports, event sources, dan dashboard schemas memakai `ConfigDict(from_attributes=True)`.
- Pydantic class-based `Config` warning sudah selesai.
- Starlette TestClient memakai `httpx2` sehingga warning compatibility test stack selesai.

## Ditunda

- Full timezone-aware database column strategy.

## Risiko

- Migrasi schema-wide dapat mengubah serialization jika dilakukan tanpa contract tests.
- Perubahan timezone column membutuhkan migration dan audit data lama.
- Dependency upgrade FastAPI/Starlette/httpx/httpx2 perlu diuji sebagai satu paket.

## Validation

```bash
cd backend
python -m pytest app/tests -q
```

Hasil terkini setelah Sprint 20: `38 passed`.

## Remaining Cleanup

1. Putuskan strategi timezone database.
