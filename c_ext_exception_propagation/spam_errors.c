#define PY_SSIZE_T_CLEAN
#include <Python.h>

static PyObject *SpamError = NULL;

static PyObject *
layer3_func(PyObject *self, PyObject *args)
{
    int fail;
    if (!PyArg_ParseTuple(args, "i", &fail))
        return NULL;
    if (fail) {
        PyErr_SetString(SpamError, "Specific error: file not found");
        return NULL;
    }
    return PyLong_FromLong(42);
}

static PyObject *
layer2_func(PyObject *self, PyObject *args)
{
    PyObject *obj = layer3_func(self, args);
    if (obj == NULL)
        return NULL;
  /* process: double the value */
    long value = PyLong_AsLong(obj);
    Py_DECREF(obj);
    return PyLong_FromLong(value * 2);
}

static PyObject *
layer1_func(PyObject *self, PyObject *args)
{
    PyObject *result = layer2_func(self, args);
    if (result == NULL)
        return NULL;
    return result;
}

static PyMethodDef SpamMethods[] = {
    {"call", layer1_func, METH_VARARGS, "Call through three C layers."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef spammodule = {
    PyModuleDef_HEAD_INIT,
    "spam_errors",
    "Exception propagation demo.",
    -1,
    SpamMethods
};

PyMODINIT_FUNC
PyInit_spam_errors(void)
{
    PyObject *m = PyModule_Create(&spammodule);
    if (m == NULL)
        return NULL;

    SpamError = PyErr_NewException("spam_errors.SpamError", NULL, NULL);
    if (SpamError == NULL) {
        Py_DECREF(m);
        return NULL;
    }
    Py_INCREF(SpamError);
    if (PyModule_AddObject(m, "SpamError", SpamError) < 0) {
        Py_DECREF(SpamError);
        Py_DECREF(m);
        return NULL;
    }
    return m;
}
