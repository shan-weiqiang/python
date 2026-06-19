#define PY_SSIZE_T_CLEAN
#include <Python.h>

/*
 * Demonstrates owned vs borrowed references and reference stealing
 * from §1.3.
 */
static PyObject *
demo_new_reference(PyObject *self, PyObject *Py_UNUSED(ignored))
{
    PyObject *obj = PyList_New(0);
    if (obj == NULL)
        return NULL;
    /* new reference — caller receives ownership */
    return obj;
}

static PyObject *
demo_borrowed_reference(PyObject *self, PyObject *args)
{
    PyObject *list;
    if (!PyArg_ParseTuple(args, "O", &list))
        return NULL;
    if (!PyList_Check(list)) {
        PyErr_SetString(PyExc_TypeError, "expected list");
        return NULL;
    }
    if (PyList_GET_SIZE(list) == 0) {
        return PyLong_FromLong(-1);
    }
    /* borrowed — do not decref item */
    PyObject *item = PyList_GetItem(list, 0);
    return PyLong_FromLong(PyLong_AsLong(item));
}

static PyObject *
demo_steal_reference(PyObject *self, PyObject *args)
{
    PyObject *list;
    PyObject *value;
    if (!PyArg_ParseTuple(args, "OO", &list, &value))
        return NULL;
    if (!PyList_Check(list) || !PyLong_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "expected (list, int)");
        return NULL;
    }
    if (PyList_Append(list, value) < 0)
        return NULL;
    /* PyList_Append does not steal; we still own value and must decref */
    Py_DECREF(value);
    return PyLong_FromLong(PyList_GET_SIZE(list));
}

static PyMethodDef RefcountMethods[] = {
    {"new_reference", demo_new_reference, METH_NOARGS,
     "Return a new empty list (owned reference)."},
    {"borrowed_reference", demo_borrowed_reference, METH_VARARGS,
     "Read first list element via borrowed reference."},
    {"steal_reference", demo_steal_reference, METH_VARARGS,
     "Append int to list (owned reference lifecycle)."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef refcountmodule = {
    PyModuleDef_HEAD_INIT,
    "refcount_demo",
    "Reference counting demo.",
    -1,
    RefcountMethods
};

PyMODINIT_FUNC
PyInit_refcount_demo(void)
{
    PyObject *m = PyModule_Create(&refcountmodule);
    if (m == NULL)
        return NULL;

    /* PyModule_AddObject steals reference to obj */
    PyObject *marker = PyUnicode_FromString("owned_by_module");
    if (marker == NULL) {
        Py_DECREF(m);
        return NULL;
    }
    if (PyModule_AddObject(m, "marker", marker) < 0) {
        Py_DECREF(marker);
        Py_DECREF(m);
        return NULL;
    }
    return m;
}
