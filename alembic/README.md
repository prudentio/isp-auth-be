# 🛠️ Running Alembic CLI

- Generate a new migration file

  ```sh
  alembic revision -m "MIGRATION_NAME"
  ```

- Apply all pending migrations

  ```sh
  alembic upgrade head
  ```

- Apply migrations up to a specific revision

  ```sh
  alembic upgrade <revision_id>
  ```

- Rollback last applied migration

  ```sh
  alembic downgrade -1
  ```

- Rollback last 10 applied migrations

  ```sh
  alembic downgrade -10
  ```

- Rollback all applied migrations

  ```sh
  alembic downgrade base
  ```

- Drop all tables (manually or with SQLAlchemy) then reapply all migrations

  ```sh
  alembic downgrade base
  alembic upgrade head
  ```

- Check the current migration version

  ```sh
  alembic current
  ```

- Show full migration history
  ```sh
  alembic history --verbose
  ```
