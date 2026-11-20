import sqlite3

import numpy as np
import pandas as pd

# COMPARISON WITH SQL. Every pair below runs the SQL query in SQLite AND the pandas version on the same data,
# and checks that both give the same rows. (You know SQL from the SQL course; pandas does the same on tables in memory.)
#   SELECT cols          df[["a", "b"]]                  WHERE            df[cond] or df.query("...")
#   ORDER BY ... LIMIT   df.sort_values(...).head(n)     DISTINCT         df.drop_duplicates()
#   COUNT AVG MAX        len(df)  df.count()  df.mean()   IN / BETWEEN     isin / between
#   LIKE 'A%'            df["c"].str.startswith("A")     IS NULL          df["c"].isna()
#   CASE WHEN            np.where(cond, a, b)             GROUP BY         df.groupby(...).agg(...)   (Module 32)
#   JOIN                 df.merge(other, on=...)          UNION ALL        pd.concat([a, b])           (Module 31)
#   INSERT UPDATE DELETE concat, df.loc[mask, col] = v, df[~mask] or df.drop(...)

emp = pd.DataFrame({
    "id": [1, 2, 3, 4, 5, 6],
    "name": ["Ann", "Bo", "Cy", "Di", "Ed", "Fay"],
    "dept": ["IT", "HR", "IT", "Ops", "IT", "HR"],
    "salary": [52000, 41000, 61000, 38000, np.nan, 45000],
    "hired": ["2020-03-01", "2019-07-15", "2021-01-10", "2018-11-30", "2022-05-05", "2023-02-20"],
})
depts = pd.DataFrame({"dept": ["IT", "HR", "Fin"], "boss": ["Zed", "Yu", "Xi"]})
conn = sqlite3.connect(":memory:")
emp.to_sql("emp", conn, index=False)
depts.to_sql("depts", conn, index=False)


def sql(query):
    return pd.read_sql_query(query, conn)


def rows(frame):
    frame = frame.reset_index(drop=True).astype(object)
    return frame.where(frame.notna(), None).values.tolist()


checks = []


def check(label, query, frame):
    checks.append((label, rows(sql(query)) == rows(frame)))


check("select columns", "SELECT name, salary FROM emp", emp[["name", "salary"]])
check("where and", "SELECT name FROM emp WHERE salary > 40000 AND dept = 'IT'", emp.loc[(emp["salary"] > 40000) & (emp["dept"] == "IT"), ["name"]])
check("where or / not", "SELECT name FROM emp WHERE dept = 'HR' OR NOT salary > 40000", emp.loc[(emp["dept"] == "HR") | (emp["salary"].notna() & ~(emp["salary"] > 40000)), ["name"]])
check("query()", "SELECT name FROM emp WHERE salary >= 45000", emp.query("salary >= 45000")[["name"]])
check("order by limit", "SELECT name, salary FROM emp ORDER BY salary DESC, name LIMIT 3", emp.sort_values(["salary", "name"], ascending=[False, True]).head(3)[["name", "salary"]])
check("distinct", "SELECT DISTINCT dept FROM emp ORDER BY dept", emp[["dept"]].drop_duplicates().sort_values("dept"))
check("in", "SELECT name FROM emp WHERE dept IN ('IT', 'Ops')", emp.loc[emp["dept"].isin(["IT", "Ops"]), ["name"]])
check("between", "SELECT name FROM emp WHERE salary BETWEEN 40000 AND 52000", emp.loc[emp["salary"].between(40000, 52000), ["name"]])
check("like", "SELECT name FROM emp WHERE name LIKE 'A%' OR name LIKE '%y'", emp.loc[emp["name"].str.startswith("A") | emp["name"].str.endswith("y"), ["name"]])
check("is null", "SELECT name FROM emp WHERE salary IS NULL", emp.loc[emp["salary"].isna(), ["name"]])
check("computed column", "SELECT name, ROUND(salary * 1.1, 1) AS raised FROM emp", emp.assign(raised=(emp["salary"] * 1.1).round(1))[["name", "raised"]])
check("case when", "SELECT name, CASE WHEN salary >= 50000 THEN 'high' ELSE 'low' END AS band FROM emp",
      emp.assign(band=np.where(emp["salary"] >= 50000, "high", "low"))[["name", "band"]])
check("year of a date", "SELECT name, CAST(strftime('%Y', hired) AS INTEGER) AS year FROM emp", emp.assign(year=pd.to_datetime(emp["hired"]).dt.year)[["name", "year"]])
check("count avg max", "SELECT COUNT(*) AS n, COUNT(salary) AS with_salary, AVG(salary) AS mean_salary, MAX(salary) AS top FROM emp",
      pd.DataFrame({"n": [len(emp)], "with_salary": [emp["salary"].count()], "mean_salary": [emp["salary"].mean()], "top": [emp["salary"].max()]}))
check("group by", "SELECT dept, COUNT(*) AS n, AVG(salary) AS avg_salary FROM emp GROUP BY dept ORDER BY dept",
      emp.groupby("dept").agg(n=("id", "count"), avg_salary=("salary", "mean")).reset_index())
grouped = emp.groupby("dept").agg(n=("id", "count")).reset_index()
check("having", "SELECT dept, COUNT(*) AS n FROM emp GROUP BY dept HAVING COUNT(*) > 1 ORDER BY dept", grouped[grouped["n"] > 1])
check("inner join", "SELECT e.name, d.boss FROM emp e JOIN depts d ON e.dept = d.dept ORDER BY e.id", emp.merge(depts, on="dept")[["name", "boss"]])
check("left join", "SELECT e.name, d.boss FROM emp e LEFT JOIN depts d ON e.dept = d.dept ORDER BY e.id", emp.merge(depts, on="dept", how="left")[["name", "boss"]])
check("union all", "SELECT name FROM emp WHERE dept = 'HR' UNION ALL SELECT name FROM emp WHERE dept = 'Ops'",
      pd.concat([emp.loc[emp["dept"] == "HR", ["name"]], emp.loc[emp["dept"] == "Ops", ["name"]]]))
for label, ok in checks:
    print(f"{label:<16} {ok}")

# NULL LOGIC: in SQL, NULL > 40000 is "unknown", and NOT unknown is unknown, so the row is left out.
# In pandas NaN > 40000 is False, and ~False is True, so the row is KEPT unless you test notna() yourself.
naive = emp.loc[(emp["dept"] == "HR") | ~(emp["salary"] > 40000), ["name"]]
print(rows(sql("SELECT name FROM emp WHERE dept = 'HR' OR NOT salary > 40000")) == rows(naive), len(naive))

# CHANGING DATA: SQL changes the table, pandas builds a new table (or changes your copy)
table = emp.copy()
conn.execute("UPDATE emp SET salary = salary + 1000 WHERE dept = 'HR'")
table.loc[table["dept"] == "HR", "salary"] += 1000
conn.execute("DELETE FROM emp WHERE salary IS NULL")
table = table.dropna(subset=["salary"])
conn.execute("INSERT INTO emp VALUES (7, 'Gus', 'Fin', 50000, '2024-01-01')")
table = pd.concat([table, pd.DataFrame([{"id": 7, "name": "Gus", "dept": "Fin", "salary": 50000, "hired": "2024-01-01"}])])
conn.commit()
print(rows(sql("SELECT id, name, salary FROM emp ORDER BY id")) == rows(table[["id", "name", "salary"]]), len(table))
print(rows(sql("SELECT dept, SUM(salary) AS total FROM emp GROUP BY dept ORDER BY dept")) == rows(table.groupby("dept")["salary"].sum().reset_index(name="total")))
conn.close()

# EXPECTED OUTPUT
# select columns   True
# where and        True
# where or / not   True
# query()          True
# order by limit   True
# distinct         True
# in               True
# between          True
# like             True
# is null          True
# computed column  True
# case when        True
# year of a date   True
# count avg max    True
# group by         True
# having           True
# inner join       True
# left join        True
# union all        True
# False 4
# True 6
# True