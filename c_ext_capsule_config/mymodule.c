#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

struct ComplexConfig {
    int timeout;
    char *server_url;
    bool enable_ssl;
    void *internal_data;
};

int process_config(struct ComplexConfig *config)
{
    int result = config->timeout;
    if (config->enable_ssl)
        result += 100;
    if (config->server_url != NULL && config->server_url[0] != '\0')
        result += (int)strlen(config->server_url);
    return result;
}

static void
destroy_config(PyObject *capsule)
{
    struct ComplexConfig *config =
        PyCapsule_GetPointer(capsule, "ComplexConfig");
    if (config) {
        free(config->server_url);
        free(config);
    }
}

static PyObject *
py_create_config(PyObject *self, PyObject *args)
{
    int timeout;
    const char *url;
    int ssl;

    if (!PyArg_ParseTuple(args, "isi", &timeout, &url, &ssl))
        return NULL;

    struct ComplexConfig *config = malloc(sizeof(struct ComplexConfig));
    if (!config) {
        PyErr_NoMemory();
        return NULL;
    }
    config->timeout = timeout;
    config->server_url = strdup(url);
    if (!config->server_url) {
        free(config);
        PyErr_NoMemory();
        return NULL;
    }
    config->enable_ssl = (bool)ssl;
    config->internal_data = NULL;

    return PyCapsule_New(config, "ComplexConfig", destroy_config);
}

static PyObject *
py_process_config(PyObject *self, PyObject *args)
{
    PyObject *capsule;

    if (!PyArg_ParseTuple(args, "O", &capsule))
        return NULL;

    if (!PyCapsule_CheckExact(capsule)) {
        PyErr_SetString(PyExc_TypeError, "Expected Config capsule");
        return NULL;
    }

    struct ComplexConfig *config =
        PyCapsule_GetPointer(capsule, "ComplexConfig");
    if (!config) {
        PyErr_SetString(PyExc_ValueError, "Invalid config capsule");
        return NULL;
    }

    int result = process_config(config);
    return PyLong_FromLong(result);
}

static PyMethodDef CapsuleMethods[] = {
    {"create_config", py_create_config, METH_VARARGS, "Create opaque config capsule."},
    {"process_config", py_process_config, METH_VARARGS, "Process config capsule."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef capsulemodule = {
    PyModuleDef_HEAD_INIT,
    "mymodule",
    "Opaque capsule config demo.",
    -1,
    CapsuleMethods
};

PyMODINIT_FUNC
PyInit_mymodule(void)
{
    return PyModule_Create(&capsulemodule);
}
