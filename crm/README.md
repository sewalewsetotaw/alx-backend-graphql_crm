# CRM Project Setup Guide (Windows)

This guide explains how to set up Redis, install dependencies, run Django migrations, start Celery workers and Beat, and verify logs for the CRM project on Windows.

---

## 1. Install Redis and Dependencies

### Install Redis
1. Download Redis for Windows: [Redis Releases](https://github.com/microsoftarchive/redis/releases)  
2. Extract Redis (e.g., `C:\Redis`) and run:
   ```powershell
   redis-server.exe

    Verify Redis is running:

    redis-cli ping

    Expected output: PONG

Install Python Dependencies

Open a terminal in your project directory and run:

pip install celery django-celery-beat redis

2. Run Django Migrations

Apply migrations for the project database:

python manage.py migrate

3. Start Celery Worker

Open a terminal in your project directory and run:

celery -A crm worker -l info

4. Start Celery Beat (Scheduler)

Open another terminal and run:

celery -A crm beat -l info

5. Verify Logs

By default, Celery logs are written to:

C:\tmp\crm_report_log.txt

    Note: Windows does not have /tmp, so make sure your Celery logging config points to a Windows-friendly path.

To monitor logs in real-time (PowerShell):

Get-Content C:\tmp\crm_report_log.txt -Wait