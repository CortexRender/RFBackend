# RFBackend
This repository contains the backend implementation for our Render Farm project. The backend is built using Python and the Django framework.

## Environment Setup
### **1. Prerequisites**
Ensure you have the following installed:
- Python 3.13
- pip (Python package manager)
- PostgreSQL 14+ (for database)
- `psycopg2` or `psycopg` (PostgreSQL driver for Python)

### **2. Runtime Setup**

#### **Step 1: Clone the repository**
```bash
git clone <repository-url>
cd <repository-folder>
```

#### **Step 2: Create a virtual environment**
```bash
python -m venv env
source env/bin/activate # On Windows: env\Scripts\activate
```

#### **Step 3: Install dependencies**
```bash
pip install -r requirements.txt
```

#### **Step 4: Create a `.env` file**
Create a `.env` file in the root directory (same level as `manage.py`) to store environment-specific configurations then export the environment variables all. Below is an example of what your `.env` file should look like:

```env
# Django settings
SECRET_KEY=your_secret_key_here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=email@gmail.com
EMAIL_HOST_PASSWORD=email_password

AWS_ACCESS_KEY_ID=aws_access_key_id
AWS_SECRET_ACCESS_KEY=aws_secret_access_key
AWS_STORAGE_BUCKET_NAME=s3_bucket_name
AWS_S3_REGION_NAME=region

DB_NAME=render_farm
DB_USER=db_user
DB_PASSWORD=db_user_password
DB_HOST=localhost or RDS
DB_PORT=5432

FRONTEND_URL=https://main.d3c81w61pqv4dl.amplifyapp.com/

```
For the secret keys and passwords, ask developers for help.

#### **Step 5: Apply database migrations**
Run the following commands to apply migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

#### **Step 6: Create a superuser**
```bash
python manage.py createsuperuser
```

#### **Step 7: Start the development server**
```bash
python manage.py runserver
```
