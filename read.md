# Django Engineering College Application

This Django project is designed to manage various aspects of an engineering college, including departments, faculty, and student information. This guide will walk you through setting up the project environment, running the application, and applying initial migrations to populate the database with predefined department data.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

#### 1. Clone the Repository

First, clone this repository to your local machine using Git:

```sh
git clone https://github.com/VirajChetanDesai/ITproject.git
cd ITproject
'''

2. Create a Virtual Environment
It's recommended to create a virtual environment to isolate project dependencies:
'''
# Create a virtual environment named 'env'
python -m venv env

# Activate the virtual environment
# On Windows
env\Scripts\activate
# On Unix or MacOS
source env/bin/activate
'''

3. Apply Migrations
Before running the application, you need to apply migrations to create the database schema:
'''
python manage.py migrate
'''

This command applies all migrations, including an initial data migration for populating the Department model with predefined data.

