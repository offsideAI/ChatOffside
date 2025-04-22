# Alembic Migrations

The project is using Alembic for database migrations. 

Alembic configuration is at `alembic.ini` 

The migrations are stored in the "alembic" directory and are versioned using the ".alembic_version" file.

## Running the migrations correctly

Here's how to run the migrations correctly:

1. First, make sure you're in the app directory:
```
cd /Users/coder/repos/offsideAI/githubrepos/ChatOffside/app
```

2. Create a new migration for the is_admin field:

```
alembic revision --autogenerate -m "add is_admin field to user"
``

This will create a new migration file in the alembic/versions directory. Let's verify what migrations exist: