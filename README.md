# Python API Development

A FastAPI-based REST API for managing posts and user authentication with SQLAlchemy ORM support for SQLite and PostgreSQL databases.

## 📋 Project Overview

This project demonstrates best practices for building a modern Python REST API with:
- **FastAPI** - High-performance web framework
- **SQLAlchemy** - ORM for database interactions
- **Pydantic** - Data validation and serialization
- **OAuth2 & JWT** - Secure authentication
- **Password Hashing** - Secure credential storage

---

## 📁 Project Structure

```
Python API Development/
├── README.md                 # Project documentation
├── .gitignore               # Git ignore rules (.venv, __pycache__)
├── .venv/                   # Python virtual environment
│
└── app/                     # Main application package
    ├── __init__.py
    ├── main_with_orm.py     # FastAPI app with SQLAlchemy ORM (PRIMARY)
    ├── main_without_orm.py  # Alternative implementation
    ├── database.py          # Database configuration & session management
    ├── models.py            # SQLAlchemy ORM models (Post, User)
    ├── schemas.py           # Pydantic validation schemas (7 schemas)
    ├── oauth2.py            # OAuth2 & JWT token management
    ├── utils.py             # Utility functions (hashing, validation)
    ├── hashUnhash.py        # Password hashing utilities
    │
    └── routers/             # API route handlers
        ├── auth.py          # Authentication endpoints (/login)
        ├── post.py          # Post management endpoints (/posts)
        └── user.py          # User management endpoints (/user)
```

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.8+
- pip or conda package manager

### Installation Steps

1. **Activate Virtual Environment**
   ```bash
   source .venv/bin/activate  # On Linux/Mac
   # OR
   .venv\Scripts\activate      # On Windows
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   # OR view all dependencies
   pip freeze
   ```

3. **Run the Application**
   ```bash
   uvicorn app.main_with_orm:app --reload
   ```

   The API will be available at: `http://localhost:8000`
   - Swagger UI (Interactive Docs): `http://localhost:8000/docs`
   - ReDoc (Alternative Docs): `http://localhost:8000/redoc`

---

## 🗄️ Database Models

### User Model (users table)
```
├── user_id         (PK, Integer)
├── email           (String, Unique, Required)
├── password        (String, Required - bcrypt hashed)
└── created_at      (TIMESTAMP - auto-generated)
```

### Post Model (posts table)
```
├── id              (PK, Integer)
├── title           (String, Required)
├── content         (String, Required)
├── published       (Boolean, Default: True)
├── created_at      (TIMESTAMP - auto-generated)
└── owner_id        (FK → users.user_id, cascade delete)
```

### Supported Databases
- **SQLite** - Default, lightweight option (development)
- **PostgreSQL** - Production-ready option

Configure database connection in `database.py`.

---

## 🔐 Authentication & Security

### OAuth2 with JWT

The API uses OAuth2 Password Bearer scheme with JSON Web Tokens (JWT):

1. **User Login** - Exchange email/password credentials for JWT access token
2. **Token Validation** - Verify JWT signature on protected routes
3. **Password Hashing** - Secure bcrypt-based credential storage

**Key Files:**
- `oauth2.py` - Token creation (`create_access_token`) and validation (`get_current_user`)
- `utils.py` - Password hashing (`hashing`, `rehashing`)
- `hashUnhash.py` - Additional hashing utilities

---

## 🛠️ API Endpoints

### Authentication Routes
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/login` | User login (returns JWT token) | No |

### Post Routes (prefix: `/posts`)
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/` | Get all posts | No |
| GET | `/your_posts` | Get current user's posts | Yes |
| POST | `/create_post` | Create new post | Yes |
| PUT | `/{id}` | Update post | Yes |
| DELETE | `/{id}` | Delete post | Yes |

### User Routes (prefix: `/user`)
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/create_user` | Register new user | No |
| GET | `/` | Get all users | Yes |
| GET | `/{id}` | Get user by ID | No |

---

## 📚 Pydantic Schemas (schemas.py)

Validation and serialization schemas:

| Schema | Purpose |
|--------|---------|
| `CreatePost` | Validate post creation data |
| `UpdatePost` | Validate post update data |
| `PostResponse` | Post response with owner info |
| `UserPostResponse` | Post response without owner |
| `CreateUser` | Validate user registration |
| `UserOut` | User response (no password) |
| `UserLogin` | Login credentials validation |
| `Token` | JWT token response |

**Example:**
```python
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
```

---

## 📂 Core Files Overview

### main_with_orm.py (Entry Point)
- FastAPI application instance
- Database initialization
- Router registration (auth, post, user)
- **Use this for running the application**

### database.py
- SQLAlchemy engine configuration
- Session management
- Base class for ORM models
- `get_db()` dependency for route injection

### models.py
- SQLAlchemy ORM model definitions
- Database table schemas
- Relationships between models
- Constraints and defaults

### oauth2.py
- JWT token creation and signing
- Token expiration settings
- `get_current_user()` dependency for protected routes

### routers/
- `auth.py` - Login endpoint
- `post.py` - Post CRUD operations
- `user.py` - User management

---

## 💾 Key Technologies & Dependencies

| Technology | Version | Purpose |
|-----------|---------|---------|
| FastAPI | Latest | Web framework |
| SQLAlchemy | Latest | ORM & database abstraction |
| Pydantic | v2 | Data validation |
| python-jose | With cryptography | JWT tokens |
| passlib | With bcrypt | Password hashing |
| Uvicorn | Latest | ASGI server |
| Starlette | Included with FastAPI | HTTP utilities |

---

## 📝 Important Notes

### Database Relationships
- **One-to-Many**: One User → Many Posts
- **Cascade Delete**: Deleting a user automatically removes their posts

### Timestamps
- All `created_at` fields use server-side defaults for consistency
- Uses timezone-aware timestamps

### Security
- Passwords are hashed with bcrypt before storage
- JWT tokens secure API access
- Email validation with Pydantic EmailStr

### Development vs Production
- `main_with_orm.py` is the recommended entry point
- `main_without_orm.py` provides an alternative non-ORM approach for comparison

---

## 📖 Usage Examples

### Create User
```bash
curl -X POST "http://localhost:8000/user/create_user" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "email": "user@example.com", "password": "securepass123"}'
```

### Login
```bash
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=securepass123"
```

### Create Post (with authentication)
```bash
curl -X POST "http://localhost:8000/posts/create_post" \
  -H "Authorization: Bearer <your_access_token>" \
  -H "Content-Type: application/json" \
  -d '{"id": 1, "title": "My Post", "content": "Post content"}'
```

---

## 👤 Project Info

- **Type**: FastAPI REST API
- **Purpose**: Learning & Demonstration
- **Database Support**: SQLite, PostgreSQL
- **Last Updated**: May 24, 2026

---

**Happy Coding! 🎉**
