# RFBackend
This repository contains the backend implementation for our Render Farm project. The backend is built using Python and the Django framework.

## Environment Setup
### **1. Prerequisites**
Ensure you have the following installed:
- Python 3.9
- pip (Python package manager)
- SQLite

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
Create a `.env` file in the root directory (same level as `manage.py`) to store environment-specific configurations. Below is an example of what your `.env` file should look like:

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

DB_NAME=render_farm
DB_USER=db_user
DB_PASSWORD=db_user_password
DB_HOST=localhost or RDS
DB_PORT=5432
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
