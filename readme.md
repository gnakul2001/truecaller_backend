# Truecaller Backend Setup Guide

## Overview

This backend solution is constructed using Django paired with MySQL. Developed by Nakul Gupta using Python and Django. To set it up and get it running, follow the instructions outlined below.

## Prerequisites

- Python 3
- MySQL

## Setup Process

### Environment Configuration

1. **Initialize a Virtual Environment**:
   ```bash
   python3 -m venv myenv
   ```

2. **Enter the Virtual Environment**:
   ```bash
   source myenv/bin/activate
   ```

3. **Add Django to the Environment**:
   ```bash
   pip install django
   ```

4. **Incorporate MySQL Client**:
   ```bash
   pip install mysqlclient
   ```

5. **Embed Django REST Framework and Bcrypt**:
   ```bash
   pip install djangorestframework bcrypt
   ```

6. **Database Configuration**:\
Adjust the `settings.py` database settings to match your MySQL details. The `DATABASES` section should resemble:

   ```python
   DATABASES = {
      'default': {
         'ENGINE': 'django.db.backends.mysql',
         'NAME': 'your_database_name',
         'USER': 'your_mysql_username',
         'PASSWORD': 'your_mysql_password',
         'HOST': 'localhost',
         'PORT': '3306',
      }
   }
   ```

   Substitute with your specific MySQL credentials. Example:
   ```
   Database: truecaller_backend
   User: nakulgupta
   Password: 12345
   ```

   🚨 **Important**: Ensure your MySQL server is active and the mentioned database is available before running the Django app.

7. **Initiate Database Migrations**:
   ```bash
   python manage.py migrate
   ```

### Launching the Server

To activate the Django server:

```bash
python manage.py runserver
```

Open `http://localhost:8000/` in your preferred browser to interact with the application.

### Sample User Profiles

For testing purposes, utilize the sample user details below:

- **User 1**:
  - Mobile: +918802631740
  - Password: Nakul@12345
- **User 2**:
  - Mobile: +918888888888
  - Password: TrueCaller@12345
- **User 3**:
  - Mobile: +917777777777
  - Password: TrueCaller1@12345

### Testing with Postman

Use the provided `TruecallerBackend.postman_collection.json` in the root directory for testing endpoints.

#### Routes:

**Base URL**: `{{base_url}}`

- **Accounts**:
  - **User Register**:
    - **Endpoint**: POST `/user/create`
    - **Parameters**:
      - name: `Nakul Gupta`
      - phone_number: `8802631740`
      - country_code: `+91`
      - password: `Nakul@12345`
      - email: `gnakul2001@gmail.com`
  - **User Login**:
    - **Endpoint**: POST `/user/login`
    - **Parameters**:
      - phone_number: `8802631740`
      - country_code: `+91`
      - password: `Nakul@12345`

- **Actions**:
  - **Mark Number Spam**:
    - **Endpoint**: POST `/actions/make_number_spam`
    - **Headers**:
      - user-id: `{{user_id}}`
      - Authorization: Bearer `{{login_hash}}`
    - **Parameters**:
      - country_code: `+91`
      - phone_number: `9524765741`

- **Search**:
  - **Search By Name**:
    - **Endpoint**: POST `/search/by_name`
    - **Headers**:
      - user-id: `{{user_id}}`
      - Authorization: Bearer `{{login_hash}}`
    - **Parameters**:
      - name: `User name 1`
      - page_no: `1`
      - max_result: `10`
  - **Search By Phone Number**:
    - **Endpoint**: POST `/search/by_phone_number`
    - **Headers**:
      - user-id: `{{user_id}}`
      - Authorization: Bearer `{{login_hash}}`
    - **Parameters**:
      - country_code: `+91`
      - phone_number: `9524765741`
      - page_no: `1`
      - max_result: `10`
  - **Get Contact Detail By Contact ID**:
    - **Endpoint**: POST `/search/details/contact_id`
    - **Headers**:
      - user-id: `{{user_id}}`
      - Authorization: Bearer `{{login_hash}}`
    - **Parameters**:
      - contact_id: `5PMkdCInUk7vBUb1biOa4OHpagS7ZjeDK2Nx2kzHJkMECsZQZ_`
  - **Get Contact Detail By User ID**:
    - **Endpoint**: POST `/search/details/user_id`
    - **Headers**:
      - user-id: `{{user_id}}`
      - Authorization: Bearer `{{login_hash}}`
    - **Parameters**:
      - user_id: `njbhjy8tr7ytrfdcvbhgfdr657646578iyugfhuyyt54556734`

### Running Tests

To execute all unit tests:

```bash
python manage.py test truecaller_backend
```

### Cleaning the Project

To clean the project, run the provided script:

```bash
chmod +x clean_project.sh
./clean_project.sh
```
