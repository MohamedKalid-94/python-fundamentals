# A C extension module: `fastmath`

## fastmath.c

```c
#define PY_SSIZE_T_CLEAN
#include <Python.h>

/* fastmath.add(a, b) -> a + b, for two integers */
static PyObject *fastmath_add(PyObject *self, PyObject *args)
{
    long a, b;
    if (!PyArg_ParseTuple(args, "ll", &a, &b)) {   /* "ll" = two C longs */
        return NULL;                               /* an exception is already set */
    }
    return PyLong_FromLong(a + b);
}

static PyMethodDef FastmathMethods[] = {
    {"add", fastmath_add, METH_VARARGS, "Return a + b."},
    {NULL, NULL, 0, NULL}                          /* end of the table */
};

static struct PyModuleDef fastmathmodule = {
    PyModuleDef_HEAD_INIT, "fastmath", "A tiny C extension.", -1, FastmathMethods
};

PyMODINIT_FUNC PyInit_fastmath(void)
{
    return PyModule_Create(&fastmathmodule);
}
```

## pyproject.toml

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "fastmath"
version = "0.1.0"
```

## setup.py

```python
from setuptools import Extension, setup

setup(ext_modules=[Extension("fastmath", sources=["fastmath.c"])])
```

## Build and use

```bash
python -m pip install .          # needs a C compiler (Visual Studio Build Tools, gcc or clang)
python -c "import fastmath; print(fastmath.add(2, 3))"      # 5
```

## The same idea with Cython (`fastmath.pyx`)

```cython
def add(long a, long b):
    return a + b
```

## What the C API makes you do

| Task | C API |
|---|---|
| Read arguments | `PyArg_ParseTuple` |
| Return a Python value | `PyLong_FromLong`, `PyUnicode_FromString`, `Py_BuildValue` |
| Raise an exception | `PyErr_SetString(PyExc_ValueError, "text")` then `return NULL` |
| Manage memory | Reference counting: `Py_INCREF` and `Py_DECREF` |
| Release the GIL for long work | `Py_BEGIN_ALLOW_THREADS ... Py_END_ALLOW_THREADS` |

Reference-counting mistakes cause leaks or crashes, which is why most people choose
`ctypes`, Cython, `pybind11` or Rust (`PyO3`) instead of the raw C API.
