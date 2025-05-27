# depot_depo_employee_project

## Overview

The Depot Management Employee App is a Django web application designed to manage and display employee salary information for the Depot Management. The application provides a user-friendly interface for viewing and navigating employee data.

## Features

- View employee salaries and related information.
- User-friendly navigation bar.
- Custom styling with CSS.

## Project Structure

```
depot_depo_employee_app/
├── DjangoCrud/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── employee/
│   ├── migrations/
│   │   └── __init__.py
│   ├── fonts/
│   │   └── DejaVuSans.ttf
│   ├── forms/
│   │   ├── __init__.py
│   │   ├── employee_forms.py
│   │   ├── work_forms.py
│   │   ├── piecework_forms.py
│   │   └── monthly_salary_forms.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── employee_models.py
│   │   ├── work_models.py
│   │   ├── piecework_models.py
│   │   └── monthly_salary_models.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── employee/
│   │   │   ├── employee_list.html
│   │   │   ├── employee_create.html
│   │   │   └── employee_update.html
│   │   ├── work/
│   │   │   ├── work_list.html
│   │   │   ├── work_create.html
│   │   │   └── work_update.html
│   |   ├── piecework/
│   │   │   ├── piecework_list.html
│   │   │   ├── piecework_create.html
│   │   │   └── piecework_update.html
│   │   ├── monthly_salary/
│   │   │   ├── monthly_salary_list.html
│   │   │   ├── monthly_salary_create.html
│   │   │   └── monthly_salary_update.html
│   │   ├── forms/
│   │   │   ├── create_form.html
│   │   │   └── update_form.html
│   |   ├── calculations/
│   │   |   └── calculation_materials.html
│   |   └── partials/
│   │       ├── delete_attention.html
│   │       ├── field_error.html
│   │       ├── pagination.html
│   │       └── modals.html
│   ├── views/
│   │   ├── __init__.py
│   │   ├── employee_views.py
│   │   ├── work_views.py
│   │   ├── piecework_views.py
│   │   ├── monthly_salary_views.py
│   │   ├── home_views.py
│   │   ├── calculations_materials.py
│   │   ├── filtered_employee_salaries.py
│   │   ├── employee_salaries_pdf.py
│   │   ├── employee_salaries_excel.py
│   │   └── delete_attention.py
│   ├── static/
│   │   ├── css/
│   │   │   └── custom.css
│   │   ├── js/
│   │   │   ├── theme.js
│   │   │   ├── modals.js
│   │   │   ├── create_form_navigation.js
│   │   │   └── update_form_navigation.js
│   │   └── images/
│   │       └── logo.png
|   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── urls.py
│   ├── tests.py
├── db.sqlite3
├── requirements.txt
├── context_processors.py
├── manage.py
└── README.md
```

## Installation

1. Clone the repository:

   ```
   git clone <repository-url>
   cd depot_depo_employee_app
   ```

2. Create a virtual environment:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

4. Set up the database:
   - Update the database settings in `depot_depo_employee_app/settings.py`.
   - Run migrations:
     ```
     python manage.py migrate
     ```

## Usage

- To start the development server, run:
  ```
  python manage.py runserver
  ```
- Access the application at `http://127.0.0.1:8000/`.

## Logging

The application includes a logging setup to monitor events and errors. Check the logs for any issues during runtime.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
