# Aplikasi Talenta Mahasiswa UMS – Backend API

Backend untuk platform Talenta Mahasiswa UMS yang menampilkan profil, skill, portofolio, dan pengalaman mahasiswa secara publik melalui REST API. Backend ini dibangun menggunakan Django REST Framework dengan autentikasi JWT.

---

## 🚀 Teknologi

* **Framework**: Django & Django REST Framework
* **Autentikasi**: JWT (SimpleJWT)
* **Database**: PostgreSQL
* **Upload Media**: ImageField (Foto Profil)
* **Testing API**: Thunder Client

---

## 📁 Struktur Relasi Data

```
User (Django)
   │ OneToOne
   ▼
 Profile
   │   \
   │    \
   ▼     ▼
 Skill  Experience
```

---

## 🔐 Autentikasi (JWT)

### Login

**POST** `/api/token/`

**Request**

```json
{
  "username": "andika",
  "password": "123456"
}
```

**Response**

```json
{
  "refresh": "xxxx",
  "access": "yyyy"
}
```

Gunakan semua request API dengan header:

```
Authorization: Bearer <ACCESS_TOKEN>
```

---

## 👤 Profile API

### GET Profile User Login

**GET** `/api/profiles/`

**Response**

```json
[
  {
    "id": 1,
    "nama": "Yoga Andika",
    "prodi": "Informatika",
    "angkatan": "2022",
    "bio": "Backend Developer",
    "foto": "/media/foto/foto1.jpg",
    "kontak_email": "andika@gmail.com",
    "instagram": "@andika",
    "linkedin": "andika",
    "is_active": true
  }
]
```

---

### Update Profile + Upload Foto

**PATCH** `/api/profiles/<id>/`

Gunakan **form-data**:

| key   | type | value       |
| ----- | ---- | ----------- |
| nama  | text | Andika      |
| prodi | text | Informatika |
| foto  | file | gambar.jpg  |
| bio   | text | Backend Dev |

---

## 🧠 Skill API

### GET Skill

**GET** `/api/skills/`

Query Opsional:

* `?search=python`
* `?level=Mahir`
* `?page=2`

**Response**

```json
{
  "count": 3,
  "results": [
    {"id": 5, "nama_skill": "Python", "level": "Mahir"}
  ]
}
```

---

### POST Skill

**POST** `/api/skills/`

```json
{
  "nama_skill": "React",
  "level": "Menengah"
}
```

Jika duplikat:

```json
{
  "nama_skill": ["Skill ini sudah ada untuk profil kamu."]
}
```

---

### PATCH Skill

**PATCH** `/api/skills/<id>/`

```json
{
  "level": "Mahir"
}
```

---

### DELETE Skill

**DELETE** `/api/skills/<id>/`

---

## 🏢 Experience API

### GET Experience

**GET** `/api/experiences/`

Query Opsional:

* `?search=backend`
* `?tahun=2024`
* `?page=2`

---

### POST Experience

**POST** `/api/experiences/`

```json
{
  "judul": "Magang Backend",
  "deskripsi": "Mengerjakan REST API",
  "tahun": "2024"
}
```

---

### PATCH Experience

**PATCH** `/api/experiences/<id>/`

---

### DELETE Experience

**DELETE** `/api/experiences/<id>/`

Jika user lain menghapus:

```json
{
  "detail": "Kamu tidak boleh menghapus data ini."
}
```

---

## ✅ Akses Media

Setelah upload foto, bisa diakses melalui:

```
http://127.0.0.1:8000/media/foto/nama_file.jpg
```

---

## 🔒 Keamanan API

* Semua endpoint dilindungi JWT
* Setiap user hanya bisa mengakses datanya sendiri
* Skill tidak boleh duplikat per profile

---

## 📌 Endpoint Ringkas

### Auth

* POST `/api/token/`
* POST `/api/token/refresh/`

### Profile

* GET `/api/profiles/`
* PATCH `/api/profiles/<id>/`

### Skill

* GET `/api/skills/`
* POST `/api/skills/`
* PATCH `/api/skills/<id>/`
* DELETE `/api/skills/<id>/`

### Experience

* GET `/api/experiences/`
* POST `/api/experiences/`
* PATCH `/api/experiences/<id>/`
* DELETE `/api/experiences/<id>/`

---

## ⚙️ Cara Menjalankan Backend

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## 🧪 Testing API

Gunakan **Thunder Client** atau **Postman** dengan token JWT.

---

> Dokumentasi ini dibuat untuk keperluan pengembangan frontend dan penilaian tugas backend Aplikasi Talenta Mahasiswa UMS.