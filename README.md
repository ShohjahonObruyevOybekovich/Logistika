# Logistika Project

This project is a logistics management system consisting of a backend and frontend application. The backend is built with Django, and the frontend is developed using a modern JavaScript framework. Both are containerized with Docker for easy deployment.

---

## Project Repositories

- **Backend:** [Logistika Backend Repository](https://github.com/ShohjahonObruyevOybekovich/Logistika.git)
- **Frontend:** [Logistics Dashboard Repository](https://github.com/Sadriddin0124/logistics-dashboard.git)

---

## Environment Setup

### Backend

#### 1. Clone the Repository
```bash
git clone https://github.com/ShohjahonObruyevOybekovich/Logistika.git
cd Logistika
```

#### 2. Create a `.env` File
Create a `.env` file in the root directory with the following variables:
```env
SECRET_KEY='your-secret-key'
ALLOWED_HOSTS='your-allowed-hosts'

POSTGRES_DB='postgres_db_name'
POSTGRES_USER='postgres_user'
POSTGRES_PASSWORD='1'
POSTGRES_HOST='postgres_host'
POSTGRES_PORT=5432
```

#### 3. Run the Backend with Docker Compose
```bash
sudo docker compose up -d --build
```

#### 4. Apply Database Migrations
```bash
docker exec -it django python manage.py makemigrations
```
```bash
docker exec -it django python manage.py migrate
```

#### 5. Access the Backend
Once the backend is running, you can access it at your specified domain or IP (configured in `ALLOWED_HOSTS`).

---

### Frontend

#### 1. Clone the Repository
```bash
git clone https://github.com/Sadriddin0124/logistics-dashboard.git
cd logistics-dashboard
```

#### 2. Install Dependencies
```bash
pnpm i
```

#### 3. Build the Frontend
```bash
pnpm build
```

#### 4. Run the Frontend with PM2
```bash
pm2 start "pnpm start" --name "front"
```

#### 5. Check PM2 Status
```bash
pm2 status
```

---

### Nginx Configuration
Ensure that your Nginx is configured to route requests to both the backend and frontend appropriately. Example configuration:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location / {
        root /path/to/frontend/build;
        index index.html;
        try_files $uri /index.html;
    }
}
```

---

## Accessing the Application

1. Open your browser and navigate to your configured domain or IP address.
2. The first page you will see is the login page.
3. Log in using the superuser credentials you created during setup.

---

## Screenshots

### Login Page
![Login Page](./file-3gdz6KkfDrjgXBedS2pS74)

### Dashboard
![Dashboard](./dashboard-screenshot.png)

---

## Notes
- Ensure Docker, PM2, and Nginx are installed and properly configured on your server.
- Replace placeholders (e.g., `your-domain.com`, `your-secret-key`) with actual values.
- For any issues, refer to the respective repository documentation or raise an issue on GitHub.

---

## Credits
- Backend Developer: ShohjahonObruyevOybekovich
- Frontend Developer: Sadriddin0124

