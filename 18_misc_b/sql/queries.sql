-- name: count
SELECT COUNT(*) FROM employees;

-- name: all_employees
SELECT id, name, dept, salary FROM employees ORDER BY id;

-- name: by_dept
SELECT name FROM employees WHERE dept = ? ORDER BY name;

-- name: by_dept_named
SELECT name, salary
FROM employees
WHERE dept = :dept AND salary >= :min_salary
ORDER BY name;

-- name: stats_by_dept
SELECT dept, COUNT(*) AS n, AVG(salary) AS avg_salary
FROM employees
GROUP BY dept
ORDER BY dept;

-- name: with_floor
SELECT e.name, d.floor
FROM employees AS e
JOIN departments AS d ON d.name = e.dept
ORDER BY e.name;

-- name: insert_employee
INSERT INTO employees (name, dept, salary) VALUES (?, ?, ?);

-- name: raise_salary
UPDATE employees SET salary = salary + ? WHERE dept = ?;

-- name: delete_employee
DELETE FROM employees WHERE name = ?;

-- name: salary_of
SELECT salary FROM employees WHERE name = ?;

-- name: by_name
SELECT id, name, dept, salary FROM employees WHERE name = ?;

-- name: list_tables
SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name;

-- name: columns
PRAGMA table_info(employees);