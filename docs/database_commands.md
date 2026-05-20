# Database dump and load commands

All commands assume MySQL is installed and the MySQL client is on your PATH. Replace `root` and the password prompt as needed for your environment.

**Project root** = parent of `exskilence_project/` (e.g. `e_commerce_naive/`).

---

## 1. Create database and tables (schema)

The schema file creates all tables, including **products**, **orders**, and **order_items**. Run the commands below to create or update the database and tables.

From **project root**:

```bash
mysql -u root -p e_commerce_db < exskilence_project/database/db_schema.sql
```

This creates all tables (including **products**, **orders**, **order_items**). On an existing database, re-running it is safe—`CREATE TABLE IF NOT EXISTS` will add any missing tables.

Or run the schema file so it also creates the database (schema file contains `CREATE DATABASE IF NOT EXISTS e_commerce_db`):

```bash
mysql -u root -p < exskilence_project/database/db_schema.sql
```

From **exskilence_project** directory:

```bash
mysql -u root -p e_commerce_db < database/db_schema.sql
```

```bash
mysql -u root -p < database/db_schema.sql
```

---

## 2. Load seed data

Seed data inserts sample users and a test record. Run **after** the schema.

From **project root**:

```bash
mysql -u root -p e_commerce_db < exskilence_project/database/seed_data.sql
```

From **exskilence_project** directory:

```bash
mysql -u root -p e_commerce_db < database/seed_data.sql
```

---

## 3. Dump (export) database

**Note:** The table must exist in the database before you can dump it. If you get `Couldn't find table: "products"`, run the schema first (section 1) to create the `products`, `orders`, and `order_items` tables:

```bash
mysql -u root -p e_commerce_db < exskilence_project/database/db_schema.sql
```

**Schema only** (structure, no data):

```bash
mysqldump -u root -p --no-data e_commerce_db > exskilence_project/database/dump_schema.sql
```

**Full dump** (schema + data):

```bash
mysqldump -u root -p e_commerce_db > exskilence_project/database/dump_full.sql
```

**Single table** (e.g. users):

```bash
mysqldump -u root -p e_commerce_db users > exskilence_project/database/dump_users.sql
```

**Products table** (schema + data; run section 1 first if the table does not exist):

```bash
mysqldump -u root -p e_commerce_db products > exskilence_project/database/dump_products.sql
```

---

## 4. Restore from a dump

```bash
mysql -u root -p e_commerce_db < exskilence_project/database/dump_full.sql
```

If the database does not exist yet:

```bash
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS e_commerce_db;"
mysql -u root -p e_commerce_db < exskilence_project/database/dump_full.sql
```

---

## 5. Fresh setup (schema + seed)

From **project root**:

```bash
mysql -u root -p < exskilence_project/database/db_schema.sql
mysql -u root -p e_commerce_db < exskilence_project/database/seed_data.sql
```
