#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

/* Existing C library — unchanged */
struct ComplexConfig {
    int timeout;
    char *server_url;
    bool enable_ssl;
};

int process_config(const struct ComplexConfig *config)
{
    int result = config->timeout;
    if (config->enable_ssl)
        result += 1000;
    if (config->server_url != NULL)
        result += (int)strlen(config->server_url);
    return result;
}

typedef struct {
    PyObject_HEAD
    int timeout;
    PyObject *server_url;
    bool enable_ssl;
} ConfigObject;

static void
Config_dealloc(ConfigObject *self)
{
    Py_XDECREF(self->server_url);
    Py_TYPE(self)->tp_free((PyObject *)self);
}

static PyObject *
Config_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    ConfigObject *self = (ConfigObject *)type->tp_alloc(type, 0);
    if (self != NULL) {
        self->timeout = 0;
        self->server_url = NULL;
        self->enable_ssl = false;
    }
    return (PyObject *)self;
}

static int
Config_init(ConfigObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"timeout", "url", "ssl", NULL};
    int timeout = 0;
    PyObject *url = NULL;
    int ssl = 0;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|iOi", kwlist,
                                     &timeout, &url, &ssl))
        return -1;

    self->timeout = timeout;
    self->enable_ssl = (bool)ssl;
    if (url) {
        Py_INCREF(url);
        Py_XDECREF(self->server_url);
        self->server_url = url;
    }
    return 0;
}

static PyObject *
Config_get_timeout(ConfigObject *self, void *closure)
{
    return PyLong_FromLong(self->timeout);
}

static int
Config_set_timeout(ConfigObject *self, PyObject *value, void *closure)
{
    if (!PyLong_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "timeout must be int");
        return -1;
    }
    self->timeout = (int)PyLong_AsLong(value);
    return 0;
}

static PyObject *
Config_get_server_url(ConfigObject *self, void *closure)
{
    if (self->server_url == NULL)
        return PyUnicode_FromString("");
    Py_INCREF(self->server_url);
    return self->server_url;
}

static int
Config_set_server_url(ConfigObject *self, PyObject *value, void *closure)
{
    if (!PyUnicode_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "server_url must be str");
        return -1;
    }
    Py_INCREF(value);
    Py_XDECREF(self->server_url);
    self->server_url = value;
    return 0;
}

static PyObject *
Config_get_enable_ssl(ConfigObject *self, void *closure)
{
    return PyBool_FromLong(self->enable_ssl);
}

static int
Config_set_enable_ssl(ConfigObject *self, PyObject *value, void *closure)
{
    if (!PyBool_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "enable_ssl must be bool");
        return -1;
    }
    self->enable_ssl = (value == Py_True);
    return 0;
}

static PyGetSetDef Config_getsetters[] = {
    {"timeout", (getter)Config_get_timeout, (setter)Config_set_timeout,
     "timeout in seconds", NULL},
    {"server_url", (getter)Config_get_server_url, (setter)Config_set_server_url,
     "server URL", NULL},
    {"enable_ssl", (getter)Config_get_enable_ssl, (setter)Config_set_enable_ssl,
     "enable SSL", NULL},
    {NULL}
};

static int
config_to_c(ConfigObject *self, struct ComplexConfig *out)
{
    out->timeout = self->timeout;
    out->enable_ssl = self->enable_ssl;

    if (self->server_url == NULL) {
        out->server_url = NULL;
        return 0;
    }
    if (!PyUnicode_Check(self->server_url)) {
        PyErr_SetString(PyExc_TypeError, "server_url must be str");
        return -1;
    }
    out->server_url = strdup(PyUnicode_AsUTF8(self->server_url));
    if (out->server_url == NULL) {
        PyErr_NoMemory();
        return -1;
    }
    return 0;
}

static void
config_c_free(struct ComplexConfig *cfg)
{
    free(cfg->server_url);
    cfg->server_url = NULL;
}

static PyObject *
Config_process(ConfigObject *self, PyObject *Py_UNUSED(ignored))
{
    struct ComplexConfig cfg;

    if (config_to_c(self, &cfg) < 0)
        return NULL;

    int result = process_config(&cfg);
    config_c_free(&cfg);
    return PyLong_FromLong(result);
}

static PyMethodDef Config_methods[] = {
    {"process", (PyCFunction)Config_process, METH_NOARGS, "Process config via C library"},
    {NULL}
};

static PyTypeObject ConfigType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "mymodule.Config",
    .tp_doc = "Configuration object with marshal boundary",
    .tp_basicsize = sizeof(ConfigObject),
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = Config_new,
    .tp_init = (initproc)Config_init,
    .tp_dealloc = (destructor)Config_dealloc,
    .tp_getset = Config_getsetters,
    .tp_methods = Config_methods,
};

static struct PyModuleDef mymodule_def = {
    PyModuleDef_HEAD_INIT,
    "mymodule",
    "Marshal-at-boundary Config demo.",
    -1,
    NULL
};

PyMODINIT_FUNC
PyInit_mymodule(void)
{
    PyObject *m = PyModule_Create(&mymodule_def);
    if (m == NULL)
        return NULL;

    if (PyType_Ready(&ConfigType) < 0) {
        Py_DECREF(m);
        return NULL;
    }
    Py_INCREF(&ConfigType);
    if (PyModule_AddObject(m, "Config", (PyObject *)&ConfigType) < 0) {
        Py_DECREF(&ConfigType);
        Py_DECREF(m);
        return NULL;
    }
    return m;
}
