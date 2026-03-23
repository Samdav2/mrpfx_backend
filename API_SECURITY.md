# API Security Documentation

To ensure the highest level of security, all API endpoints now require two layers of authentication.

## 1. Private API Key (Mandatory for ALL Requests)

Every request sent to the backend must include the `X-API-KEY` header. Requests without this header or with an invalid key will return `403 Forbidden`.

**Header Name**: `X-API-KEY`
**Value**: `bdbd0da428c30a13e7f8a9a11a259204b210847da7a8473dbeee62c65387c3bc`

> [!IMPORTANT]
> This key should be stored securely in your frontend environment variables (.env) and never hardcoded in the source code if the bundle is public. For web apps, ensure it is only used in server-side requests if possible, or understand that it is a shared secret for the client application.

## 2. JWT Authentication (Mandatory for Protected Endpoints)

In addition to the API Key, all user-specific and admin endpoints require a valid JWT token.

**Header Name**: `Authorization`
**Value**: `Bearer <your_jwt_token>`

### Workflow Examples

#### A. Public Endpoints (e.g., Login, Signup, Health)
Only the API Key is required.

```http
POST /api/v1/auth/login
X-API-KEY: bdbd0da428c30a13e7f8a9a11a259204b210847da7a8473dbeee62c65387c3bc
Content-Type: application/json

{
  "login": "username",
  "password": "password"
}
```

#### B. Protected Endpoints (e.g., Profile, Services, Traders)
Both the API Key and the Bearer token are required.

```http
GET /api/v1/auth/me
X-API-KEY: bdbd0da428c30a13e7f8a9a11a259204b210847da7a8473dbeee62c65387c3bc
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### C. Admin Endpoints
Both the API Key and an Admin Bearer token are required.

```http
GET /api/v1/admin/learnpress/courses
X-API-KEY: bdbd0da428c30a13e7f8a9a11a259204b210847da7a8473dbeee62c65387c3bc
Authorization: Bearer <admin_token>
```

---

## Error Codes
| Status Code | Description |
| :--- | :--- |
| `403 Forbidden` | Invalid or missing `X-API-KEY` header, or insufficient privileges (e.g. non-admin accessing admin route). |
| `401 Unauthorized` | Missing, invalid, or expired JWT token in `Authorization` header. |
