# Truecaller Backend Setup Guide

![Python CI](https://github.com/gnakul2001/truecaller_backend/actions/workflows/build.yml/badge.svg)

## Overview

This backend solution utilizes Django and is integrated with MySQL. It was developed by Nakul Gupta leveraging Python and Django. Follow the steps below for setup and deployment.

## Prerequisites

- Python 3
- MySQL

## Setup Process

### Environment Configuration

1. **Create a Virtual Environment**:
   ```bash
   python3 -m venv myenv
   ```

2. **Activate the Virtual Environment**:
   ```bash
   source myenv/bin/activate
   ```

3. **Install the Required Packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the Database**:
   Update the `settings.py` file with your MySQL credentials. The `DATABASES` section should look like:

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

   For example:
   ```
   Database: truecaller_backend
   User: nakulgupta
   Password: 12345
   host: 127.0.0.1
   ```

   🚨 **Note**: Ensure the MySQL server is running and the specified database exists before starting the Django app.

5. **Execute Database Migrations**:
   ```bash
   python manage.py migrate
   ```

### Launching the Server

To start the Django server:

```bash
python manage.py runserver
```

Visit `http://localhost:8000/` in your browser to access the application.

### Sample User Profiles

For testing, use the sample user credentials provided:

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

For endpoint testing, load the `TruecallerBackend.postman_collection.json` found in the root directory.

#### Routes:

**Base URL**: `{{base_url}}`

- **Accounts**:
  - **Register User**:
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
  - **Mark Number as Spam**:
    - **Endpoint**: POST `/actions/make_number_spam`
    - **Headers**:
      - user-id: `{{user_id}}`
      - Authorization: Bearer `{{login_hash}}`
    - **Parameters**:
      - country_code: `+91`
      - phone_number: `9524765741`

- **Search**:
  - **Search by Name**:
    - **Endpoint**: POST `/search/by_name`
    - **Headers**:
      - user-id: `{{user_id}}`
      - Authorization: Bearer `{{login_hash}}`
    - **Parameters**:
      - name: `User name 1`
      - page_no: `1`
      - max_result: `10`
  - **Search by Phone Number**:
    - **Endpoint**: POST `/search/by_phone_number`
    - **Headers**:
      - user-id: `{{user_id}}`
      - Authorization: Bearer `{{login_hash}}`
    - **Parameters**:
      - country_code: `+91`
      - phone_number: `9524765741`
      - page_no: `1`
      - max_result: `10`
  - **Retrieve Contact Details by Contact ID**:
    - **Endpoint**: POST `/search/details/contact_id`
    - **Headers**:
      - user-id: `{{user_id}}`
      - Authorization: Bearer `{{login_hash}}`
    - **Parameters**:
      - contact_id: `5PMkdCInUk7vBUb1biOa4OHpagS7ZjeDK2Nx2kzHJkMECsZQZ_`
  - **Retrieve Contact Details by User ID**:
    - **Endpoint**: POST `/search/details/user_id`
    - **Headers**:
      - user-id: `{{user_id}}`
      - Authorization: Bearer `{{login_hash}}`
    - **Parameters**:
      - user_id: `njbhjy8tr7ytrfdcvbhgfdr657646578iyugfhuyyt54556734`

### Running Tests

To run the unit tests:

```bash
pytest
```

### Project Cleanup

To reset the project:

```bash
chmod +x clean_project.sh
./clean_project.sh
```
