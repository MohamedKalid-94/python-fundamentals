CREATE TABLE departments (
    name  TEXT PRIMARY KEY,
    floor INTEGER NOT NULL
);

CREATE TABLE employees (
    id     INTEGER PRIMARY KEY,
    name   TEXT    NOT NULL UNIQUE,
    dept   TEXT    NOT NULL REFERENCES departments (name),
    salary INTEGER NOT NULL CHECK (salary > 0)
);

CREATE INDEX idx_employees_dept ON employees (dept);