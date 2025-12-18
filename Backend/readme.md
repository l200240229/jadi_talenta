** Deskripsi Proyek
Backend Aplikasi Talenta Mahasiswa UMS adalah REST API berbasis Django REST Framework yang digunakan untuk mengelola data talenta mahasiswa, meliputi profil, skill, dan pengalaman. Sistem ini menerapkan autentikasi JWT (JSON Web Token) dan dirancang dengan arsitektur frontend–backend terpisah.
Backend ini digunakan oleh frontend berbasis React untuk menampilkan dan mengelola data talenta mahasiswa.

** Teknologi yang Digunakan

Python 3.12+
Django
Django REST Framework
PostgreSQL
JWT Authentication (djangorestframework-simplejwt)
API Documentation: drf-spectacular (Swagger / OpenAPI)

** Struktur Aplikasi
Backend/
├── accounts/       # Autentikasi (register, login, JWT)
├── profiles/       # Data profil mahasiswa
├── skills/         # Data skill mahasiswa
├── experiences/    # Data pengalaman mahasiswa
├── config/         # Konfigurasi project Django
└── manage.py

** User Flow

1.User melakukan registrasi
2.User login dan mendapatkan JWT
3.User melengkapi profil
4.User menambahkan skill
5.User menambahkan pengalaman
6.Semua data hanya dapat diakses oleh user yang login

** Dokumentasi API

Dokumentasi API tersedia melalui Swagger:
Swagger UI:
http://127.0.0.1:8000/api/docs/

OpenAPI Schema:
http://127.0.0.1:8000/api/schema/

