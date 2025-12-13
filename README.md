# FastAPI Task Manager

REST API do zarządzania projektami i zadaniami z systemem autoryzacji opartym na JWT.

## O Projekcie

Aplikacja stworzona z myślą o nauce modern backend development'u, zaimplementowana w modelu synchronicznym. Task Manager pozwala użytkownikom na:
- Rejestrację i logowanie z tokenami JWT
- Tworzenie i zarządzanie projektami
- Organizowanie zadań w ramach projektów
- Paginację i filtrowanie zasobów

## Stack Technologiczny

| Kategoria | Technologia |
|-----------|-----------|
| **Framework** | FastAPI |
| **Baza danych** | PostgreSQL |
| **ORM** | SQLModel |
| **Migracje** | Alembic |
| **Autentykacja** | JWT + OAuth2 |
| **Testy** | pytest |
| **Deployment** | Docker & Docker Compose |

## Szybki Start

### Wymagania
- Python 3.10+
- Docker & Docker Compose (opcjonalnie)
- PostgreSQL (jeśli bez Docker'a)

### Instalacja & Uruchomienie

**Opcja 1: Z Docker Compose (rekomendowane)**

1. Skonfiguruj .env.docker (patrz przykład poniżej)
2. Uruchom
```bash
docker-compose up --build
```

**Opcja 2: Lokalnie**

1. Zainstaluj zależności
```bash
pip install -r requirements.txt
```

2. Skonfiguruj .env (patrz przykład poniżej)

3. Uruchom migrację 
```bash
alembic upgrade head
```

4. Wystartuj serwer
```bash
uvicorn app.main:app --reload
```

API będzie dostępne na: `http://localhost:8000`  
Dokumentacja interaktywna: `http://localhost:8000/docs`

## Zmienne Środowiskowe

Projekt wykorzystuje dwa pliki konfiguracyjne:

**`.env`** - dla uruchomienia lokalnego (bez Docker)
```env
DATABASE_URL=postgresql://user:password@localhost:5432/db_name
SECRET_KEY=your-secret-key-for-jwt
```

**`.env.docker`** - dla Docker Compose
```env
DATABASE_URL=postgresql://user:password@db:5432/db_name
SECRET_KEY=your-secret-key-for-jwt
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=db_name
```

> Wartości takie jak `user`, `password`, `db_name` oraz `your-secret-key-for-jwt` należy zastąpić własnymi danymi, dostosowanymi do lokalnego środowiska.

## Główne Endpointy

### Autoryzacja
- `POST /api/v1/auth/register` - Rejestracja
- `POST /api/v1/auth/login` - Logowanie (zwraca JWT)
- `GET /api/v1/auth/me` - Dane obecnego użytkownika

### Projekty
- `GET /api/v1/projects` - Lista projektów
- `POST /api/v1/projects` - Utwórz projekt
- `GET /api/v1/projects/{id}` - Wyszukaj projekt po ID
- `PUT /api/v1/projects/{id}` - Aktualizuj projekt
- `DELETE /api/v1/projects/{id}` - Usuń projekt

### Zadania
- `GET /api/v1/tasks` - Lista zadań
- `POST /api/v1/tasks` - Utwórz zadanie
- `GET /api/v1/tasks/{id}` - Wyszukaj zadanie po ID
- `PUT /api/v1/tasks/{id}` - Aktualizuj zadanie
- `DELETE /api/v1/tasks/{id}` - Usuń zadanie

## Testy integracyjne (API / endpoint tests)

```bash
pytest
```

## Architektura Projektu

```
fastapi-task-manager/
├── app/
│   ├── models/        → SQLModel (User, Project, Task)
│   ├── schemas/       → Pydantic (request/response models)
│   ├── routers/       → Endpointy API (auth, projects, tasks)
│   ├── services/      → Logika biznesowa
│   ├── repositories/  → Dostęp do bazy danych
│   ├── core/          → Konfiguracja (security, exceptions)
│   ├── db/            → Sesje i konfiguracja bazy
│   └── utils/         → Pagination
├── alembic/           → Migracje bazy danych
│   └── versions/      → Historia zmian schemy
├── tests/             → Testy integracyjne (pytest)
├── postman/           → Kolekcje API do testowania
```

## Czego się Nauczyłem

**Backend Development:**
- Budowanie synchronicznego REST API z FastAPI
- Modelowanie baz danych z SQLModel
- Migracje bazy danych z Alembic
- Testy integracyjne API (pytest)

**Autoryzacja & Bezpieczeństwo:**
- JWT (access + refresh tokens)
- Hashing haseł z bcrypt
- OAuth2 flow w FastAPI
- Dependency injection dla autoryzacji

**Best Practices:**
- Separacja logiki (service/repository pattern)
- Pydantic schemas do walidacji
- Exception handling
- Docker containerization

**DevOps:**
- Docker & Docker Compose setup
- Zmienne środowiskowe (.env, .env.docker)
- Database migrations automation

## Testowanie API

Projekt zawiera Postman collection w katalogu `postman/`:
- `task-manager.postman_collection.json` - Wszystkie endpointy
- `task-manager.postman_environment.json` - Zmienne środowiskowe

## 📄 Licencja

MIT
