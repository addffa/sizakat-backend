# Sistem Informasi Zakat (SiZakat)

Si Zakat merupakan sistem informasi untuk membantu masjid dalam mengelola transaksi zakat. Sistem ini dibuat oleh tim lab 1231, yang dipimpin oleh Prof. Dr. Wisnu Jatmiko.

## Environment Configuration:
1. Buat file `.db.env`:
    ```
    POSTGRES_DB=sizakat
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    ```
2. Buat file `.env`:
    ```
    SECRET_KEY=foobarbarfoo
    ALLOWED_HOSTS=*
    SQL_DATABASE=sizakat
    SQL_USER=postgres
    SQL_PASSWORD=postgres
    SQL_HOST=db
    SQL_PORT=5432
    DEBUG=1
    ```
## Development Guide
### Installation:
1. Pastikan semua environment file sudah dibuat.

2. Build dan run docker images: `docker-compose up -d --build`.

3. Lakukan migrasi model pada backend:
    - `docker-compose exec backend python manage.py makemigrations`
    - `docker-compose exec backend python manage.py migrate`

4. Aplikasi backend dapat diakses pada `{docker_host}:8000`.

5. Load dummy data pada backend: `docker-compose exec backend python manage.py loaddata dataseed.json`.

### Graphql Documentation & Playground:
`graphiql` dapat diakses pada aplikasi backend: `{docker_host}:8000/graphql`

## Production Installation
todo

## Dummy User:
- username: admin, pass: admin123, role: Admin
