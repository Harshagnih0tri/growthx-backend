# GrowthX Backend — Authentication Module: Full Summary

## Project Context
- **Stack:** Python, FastAPI, SQLAlchemy, PostgreSQL, Pydantic, Uvicorn
- **Architecture:** Clean/layered (routers → services → repositories → models)
- **Version control:** Git, connected to GitHub (`Harshagnih0tri/growthx-backend`)

---

## What Was Built (File by File)

### 1. `app/config.py` (modified, not replaced)
Added JWT-related settings to your existing `Settings` class (which already used `os.getenv()` + `python-dotenv`):
```python
SECRET_KEY: str = os.getenv("SECRET_KEY", "CHANGE_THIS_IN_PRODUCTION")
ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
```
**Why:** Centralizes JWT config, keeps secrets out of code, casts `ACCESS_TOKEN_EXPIRE_MINUTES` to `int` since `os.getenv()` always returns strings.

### 2. `.env` (updated)
Added:
```
SECRET_KEY=<generated via secrets.token_hex(32)>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```
Confirmed `.env` was **never committed to git** — it was `.gitignore`d before the first commit, so no secrets ever reached GitHub.

### 3. `app/core/security.py` (extended your existing hashing code)
You already had `hash_password` / `verify_password` (bcrypt via passlib). We added:
```python
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str
def decode_access_token(token: str) -> dict
```
**Why:** Signs and verifies JWTs using `SECRET_KEY` + `HS256`, with an `exp` (expiry) claim. Uses UTC timestamps to avoid timezone bugs.

**Bug fixed along the way:** `bcrypt 5.0.0` broke `passlib`'s version detection (`AttributeError: module 'bcrypt' has no attribute '__about__'`), which then caused a misleading "password too long" error. Fixed by pinning `bcrypt==4.0.1`.

### 4. `app/core/dependencies.py` (new)
```python
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(get_db)) -> User
```
**Why:** The bridge between an incoming request's `Authorization` header and "who is logged in." Decodes the JWT, looks up the user by email (the `sub` claim), and checks `is_active`.

**Iteration:** Started with `OAuth2PasswordBearer` (which renders a username/password/client_id form in Swagger — built for form-encoded OAuth2 flows). Since your `/auth/login` accepts JSON, not form data, this was incompatible. Switched to `HTTPBearer`, which gives a simple "paste your token" box in Swagger and matches a JSON API correctly.

### 5. `app/models/user.py` (already existed — reviewed, not changed)
Confirmed structure: UUID primary key, `name`, `email` (unique), `hashed_password`, `is_active` (bool, default `True`), `created_at`, `updated_at` (auto-managed timestamps).

### 6. `app/schemas/user.py` (extended your existing file)
You already had `UserBase`, `UserCreate`, `UserRead`. We added:
```python
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
```
**Why:** `UserLogin` is deliberately separate from `UserCreate` (login doesn't need `name`). `Token` matches the required login response shape.

**Dependency installed:** `email-validator` (required for Pydantic's `EmailStr` to actually validate email format).

### 7. `app/repositories/user_repository.py` (new)
```python
def get_user_by_email(db: Session, email: str) -> User | None
def create_user(db: Session, name: str, email: str, hashed_password: str) -> User
```
**Why:** Isolates raw SQLAlchemy queries from business logic — the only file allowed to query the `User` table directly.

### 8. `app/services/auth_service.py` (new)
```python
def register_user(db: Session, payload: UserCreate) -> User
def authenticate_user(db: Session, payload: UserLogin) -> str
```
**Why:** Business logic layer. `register_user` checks duplicate email → hashes password → persists. `authenticate_user` verifies password → checks `is_active` → issues a JWT. Uses identical error messages for "user not found" vs "wrong password" (`401`) to prevent email enumeration attacks; uses `403` specifically for deactivated accounts.

### 9. `app/routers/auth.py` (new)
```python
POST /auth/register  → response_model=UserRead, status_code=201
POST /auth/login      → response_model=Token
```

### 10. `app/routers/users.py` (new)
```python
GET /users/me  → protected via Depends(get_current_user)
```

### 11. `app/main.py` (modified)
- Imported and included both new routers (`auth.router`, `users.router`)
- Added `Base.metadata.create_all(bind=engine)` to the startup event, so SQLAlchemy models actually create their tables in PostgreSQL on boot (this fixed a `relation "users" does not exist` error we hit during testing)

**Bug fixed:** Original draft called `app.include_router(...)` *before* `app = FastAPI(...)` was defined — moved to correct order.

---

## Bugs Encountered & Fixed (in order)

| # | Issue | Root Cause | Fix |
|---|---|---|---|
| 1 | `AttributeError: module 'bcrypt' has no attribute '__about__'` | `bcrypt 5.0.0` incompatible with `passlib`'s version check | Pinned `bcrypt==4.0.1` |
| 2 | `ModuleNotFoundError: No module named 'email_validator'` | `EmailStr` needs a separate package | `pip install email-validator` |
| 3 | `ImportError: cannot import name 'UserLogin'` | Assumed schema before seeing real file | Added `UserLogin`/`Token` to actual `schemas/user.py` |
| 4 | `NameError: name 'app' is not defined` | `include_router()` called before `app = FastAPI()` | Reordered `main.py` |
| 5 | `relation "users" does not exist` | Tables never created in PostgreSQL — models only describe structure, don't auto-create | Added `Base.metadata.create_all()` on startup |
| 6 | OAuth2 login form in Swagger didn't match JSON API | `OAuth2PasswordBearer` expects form-encoded login | Switched to `HTTPBearer` |

---

## Testing Performed (All Passed)

- ✅ `hash_password` / `verify_password` — correct hash, correct/incorrect password checks
- ✅ `create_access_token` / `decode_access_token` — valid token round-trip
- ✅ Invalid/garbage token correctly raises `JWTError`
- ✅ All modules import cleanly (`register_user`, `authenticate_user`, `get_current_user`)
- ✅ Full app boots without errors
- ✅ `POST /auth/register` → `201 Created`, correct user shape, no password leaked
- ✅ `POST /auth/login` → `200`, returns `access_token` + `token_type: bearer`
- ✅ `GET /users/me` with valid token → `200`, correct user data returned
- ⏳ `GET /users/me` with no/invalid token → expected `401` (final check pending confirmation)

---

## Git History

```
6596478  chore: initial commit
2561547  feat(auth): implement complete JWT authentication module
<pending> fix(auth): switch from OAuth2PasswordBearer to HTTPBearer
```

Repo: `https://github.com/Harshagnih0tri/growthx-backend` (connected, `main` branch, pushed)
`.env` confirmed never committed at any point.

---

## Final Folder Structure

```text
app/
├── config.py                    ✅ JWT settings added
├── database.py                  (untouched — already had get_db, Base, engine)
├── main.py                      ✅ routers wired, create_all() on startup
├── core/
│   ├── security.py              ✅ hashing + JWT create/decode
│   └── dependencies.py          ✅ get_current_user (HTTPBearer-based)
├── models/
│   └── user.py                  (untouched — UUID pk, is_active, timestamps)
├── repositories/
│   └── user_repository.py       ✅ new
├── routers/
│   ├── auth.py                  ✅ new — /auth/register, /auth/login
│   └── users.py                 ✅ new — /users/me
├── schemas/
│   └── user.py                  ✅ UserLogin, Token added
└── services/
    └── auth_service.py          ✅ new — register_user, authenticate_user
```

## Authentication Flow Diagram

```
REGISTER
  Client → POST /auth/register {name, email, password}
    → UserCreate validation (Pydantic)
    → check duplicate email (repository)
    → hash_password (bcrypt)
    → create_user (insert into PostgreSQL)
    → return UserRead (no password hash)

LOGIN
  Client → POST /auth/login {email, password}
    → UserLogin validation
    → get_user_by_email (repository)
    → verify_password (bcrypt)
    → check is_active
    → create_access_token (JWT, signed, 60 min expiry)
    → return {access_token, token_type: "bearer"}

PROTECTED ROUTE
  Client → GET /users/me
    Header: Authorization: Bearer <token>
    → HTTPBearer extracts token
    → decode_access_token (verify signature + expiry)
    → extract email from "sub" claim
    → look up user in DB
    → check is_active
    → return user data (or 401/403 if any check fails)
```

---

## Continuation Prompt — Next Module: Habit CRUD

Use this prompt to continue in the same incremental, mentor-style workflow:

> We're continuing the GrowthX FastAPI backend. The Authentication Module is complete and tested: `/auth/register`, `/auth/login`, and `/users/me` all work end-to-end with JWT (HTTPBearer scheme), bcrypt password hashing, and an `is_active` check via `get_current_user` in `app/core/dependencies.py`.
>
> Now implement the **Habit CRUD module**, following the same rules as before:
> - Never regenerate the whole project or rewrite working files
> - Only generate one file at a time, explain why it's needed and where it goes before writing it
> - Show complete code for that file only, then explain every function/import and the request flow
> - Wait for me to integrate and confirm before moving to the next file
> - All Habit endpoints must be scoped per-user via `Depends(get_current_user)`, so users only ever see/edit their own habits
>
> Requirements for the module:
> - `Habit` SQLAlchemy model (id, user_id FK, name, description, frequency, created_at, updated_at)
> - Pydantic schemas: `HabitCreate`, `HabitUpdate`, `HabitRead`
> - Repository layer for DB access
> - Service layer for business logic (e.g., verify habit belongs to current user before update/delete)
> - Router with:
>   - `POST /habits` — create
>   - `GET /habits` — list current user's habits
>   - `GET /habits/{id}` — get one (404 if not found or not owned)
>   - `PUT /habits/{id}` — update
>   - `DELETE /habits/{id}` — delete
> - Proper HTTP status codes and error handling (404 for not found/not owned, 422 for validation)
>
> Start with the first required file.

---

## Key Concepts Learned Along the Way

- **Hashing vs. encryption:** hashing (bcrypt) is one-way and irreversible — correct for passwords. Encryption is reversible and wrong for this use case.
- **JWT structure:** header.payload.signature — payload is readable by anyone (base64, not encrypted), only the signature is protected. Never put sensitive data in the payload.
- **Why `401` vs `403`:** `401` = not authenticated (bad/missing credentials). `403` = authenticated but not permitted (e.g., deactivated account).
- **Why same error message for "no such user" and "wrong password":** prevents attackers from enumerating valid emails.
- **Why re-query the DB in `get_current_user` instead of trusting the JWT payload alone:** a deleted/deactivated user's old token would otherwise stay functional until expiry.
- **Local git vs. GitHub:** `git commit` only saves locally; `git push` is a separate, required step to sync with GitHub.
- **Why `Base.metadata.create_all()` was needed:** SQLAlchemy models only describe table structure in Python — they don't create real database tables until something explicitly triggers it.
