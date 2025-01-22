## Django CRM
A web app for managing contacts using Django for the backend, HTMX for SPA functionality, and TailwindCSS, featuring role-based access control (RBAC) and employee management, 2-Factor Authentication and email invitations, contact promotion workflow allowing users to manage leads, prospects, and customers.

**Live Demo:** https://dj-crm-v3.el.r.appspot.com/

### Tech Stack
- Django
- TailwindCSS
- HTMX
- Alpine.js

### To run the project locally
1. **Clone the repository**:
   ```bash
    git clone https://github.com/Shreehar-KE/django-crm.git

    cd django-crm
   ```
2. **Activate a virtual environment & install the packages**
   ```bash
    # These are for Unix based OS(Linux/MacOS)
    python3 -m venv .venv
    source .venv/bin/activate
    python3 -m pip install -r requirements.txt
   ```
3. **Add your own .env file inside a_core/**
   ```bash
    ENVIRONMENT=development
    # use `python3 -c "import secrets; print(secrets.token_urlsafe())"` in the terminal for the keys
    SECRET_KEY=
    ENCRYPT_KEY=
    DATABASE_URL= #required only if your are connecting to a db other than db.sqlite3
    RUN_POSTGRES_LOCALLY=False
   ```
4. **Run the project**
   ```
   python manage.py makemigrations accounts
   python manage.py migrate
   python manage.py makemigrations a_contacts
   python manage.py makemigrations analytics
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```
5. **Tailwind Config, if you want to modify the CSS**
   ```bash
   # In a separate terminal
   cd node
   npm install
   npm run tailwind
   
   # To run tailwind in watch mode
   npm run tailwind-watch

   # To minify the CSS
   npm run minify
   ```
6. **Open your browser and navigate to** ``http://localhost:8000/`` or ``http://127.0.0.1:8000/``
