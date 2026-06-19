#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    PyObject_HEAD
    char *host;
    int port;
    bool use_ssl;
} NetworkConfigObject;

static PyTypeObject NetworkConfigType;

static void
Network_dealloc(NetworkConfigObject *self)
{
    free(self->host);
    Py_TYPE(self)->tp_free((PyObject *)self);
}

static PyObject *
Network_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    NetworkConfigObject *self =
        (NetworkConfigObject *)type->tp_alloc(type, 0);
    if (self) {
        self->host = NULL;
        self->port = 0;
        self->use_ssl = false;
    }
    return (PyObject *)self;
}

static int
Network_init(NetworkConfigObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"host", "port", "use_ssl", NULL};
    const char *host = NULL;
    int port = 0;
    int use_ssl = 0;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|sii", kwlist,
                                     &host, &port, &use_ssl))
        return -1;

    if (host) {
        free(self->host);
        self->host = strdup(host);
        if (!self->host) {
            PyErr_NoMemory();
            return -1;
        }
    }
    self->port = port;
    self->use_ssl = (bool)use_ssl;
    return 0;
}

static PyObject *
Network_get_host(NetworkConfigObject *self, void *closure)
{
    if (self->host == NULL)
        return PyUnicode_FromString("");
    return PyUnicode_FromString(self->host);
}

static int
Network_set_host(NetworkConfigObject *self, PyObject *value, void *closure)
{
    if (!PyUnicode_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "host must be str");
        return -1;
    }
    const char *host = PyUnicode_AsUTF8(value);
    free(self->host);
    self->host = strdup(host);
    if (self->host == NULL) {
        PyErr_NoMemory();
        return -1;
    }
    return 0;
}

static PyObject *
Network_get_port(NetworkConfigObject *self, void *closure)
{
    return PyLong_FromLong(self->port);
}

static int
Network_set_port(NetworkConfigObject *self, PyObject *value, void *closure)
{
    if (!PyLong_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "port must be int");
        return -1;
    }
    self->port = (int)PyLong_AsLong(value);
    return 0;
}

static PyObject *
Network_get_use_ssl(NetworkConfigObject *self, void *closure)
{
    return PyBool_FromLong(self->use_ssl);
}

static int
Network_set_use_ssl(NetworkConfigObject *self, PyObject *value, void *closure)
{
    if (!PyBool_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "use_ssl must be bool");
        return -1;
    }
    self->use_ssl = (value == Py_True);
    return 0;
}

static PyGetSetDef Network_getsetters[] = {
    {"host", (getter)Network_get_host, (setter)Network_set_host, "host", NULL},
    {"port", (getter)Network_get_port, (setter)Network_set_port, "port", NULL},
    {"use_ssl", (getter)Network_get_use_ssl, (setter)Network_set_use_ssl,
     "use_ssl", NULL},
    {NULL}
};

static PyTypeObject NetworkConfigType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "mymodule.NetworkConfig",
    .tp_basicsize = sizeof(NetworkConfigObject),
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = Network_new,
    .tp_init = (initproc)Network_init,
    .tp_dealloc = (destructor)Network_dealloc,
    .tp_getset = Network_getsetters,
};

typedef struct {
    PyObject_HEAD
    int timeout;
    PyObject *server_url;
    bool enable_ssl;
    NetworkConfigObject *network;
    int values[10];
    int values_count;
    PyObject *items;
} ConfigObject;

static void
Config_dealloc(ConfigObject *self)
{
    Py_XDECREF(self->server_url);
    Py_XDECREF(self->network);
    Py_XDECREF(self->items);
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
        self->network = NULL;
        self->values_count = 0;
        self->items = NULL;
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

static PyObject *
Config_get_network(ConfigObject *self, void *closure)
{
    if (self->network == NULL) {
        self->network = (NetworkConfigObject *)
            NetworkConfigType.tp_new(&NetworkConfigType, NULL, NULL);
        if (self->network == NULL)
            return NULL;
    }
    Py_INCREF(self->network);
    return (PyObject *)self->network;
}

static int
Config_set_network(ConfigObject *self, PyObject *value, void *closure)
{
    if (!PyObject_TypeCheck(value, &NetworkConfigType)) {
        PyErr_SetString(PyExc_TypeError, "network must be NetworkConfig");
        return -1;
    }
    Py_INCREF(value);
    Py_XDECREF(self->network);
    self->network = (NetworkConfigObject *)value;
    return 0;
}

static PyObject *
Config_get_value(ConfigObject *self, PyObject *args)
{
    int index;
    if (!PyArg_ParseTuple(args, "i", &index))
        return NULL;
    if (index < 0 || index >= self->values_count) {
        PyErr_SetString(PyExc_IndexError, "index out of range");
        return NULL;
    }
    return PyLong_FromLong(self->values[index]);
}

static PyObject *
Config_set_value(ConfigObject *self, PyObject *args)
{
    int index;
    PyObject *value;
    if (!PyArg_ParseTuple(args, "iO", &index, &value))
        return NULL;
    if (!PyLong_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "value must be int");
        return NULL;
    }
    if (index < 0 || index >= 10) {
        PyErr_SetString(PyExc_IndexError, "index out of range");
        return NULL;
    }
    self->values[index] = (int)PyLong_AsLong(value);
    if (index >= self->values_count)
        self->values_count = index + 1;
    Py_RETURN_NONE;
}

static PyObject *
Config_get_values(ConfigObject *self, PyObject *Py_UNUSED(ignored))
{
    PyObject *list = PyList_New(self->values_count);
    if (list == NULL)
        return NULL;
    for (int i = 0; i < self->values_count; i++)
        PyList_SET_ITEM(list, i, PyLong_FromLong(self->values[i]));
    return list;
}

static PyObject *
Config_get_items(ConfigObject *self, void *closure)
{
    if (self->items == NULL)
        return PyList_New(0);
    Py_INCREF(self->items);
    return self->items;
}

static int
Config_set_items(ConfigObject *self, PyObject *value, void *closure)
{
    if (!PyList_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "items must be a list");
        return -1;
    }
    Py_INCREF(value);
    Py_XDECREF(self->items);
    self->items = value;
    return 0;
}

static PyGetSetDef Config_getsetters[] = {
    {"timeout", (getter)Config_get_timeout, (setter)Config_set_timeout,
     "timeout in seconds", NULL},
    {"server_url", (getter)Config_get_server_url, (setter)Config_set_server_url,
     "server URL", NULL},
    {"enable_ssl", (getter)Config_get_enable_ssl, (setter)Config_set_enable_ssl,
     "enable SSL", NULL},
    {"network", (getter)Config_get_network, (setter)Config_set_network,
     "network settings", NULL},
    {"items", (getter)Config_get_items, (setter)Config_set_items,
     "items list", NULL},
    {NULL}
};

static PyMethodDef Config_methods[] = {
    {"get_value", (PyCFunction)Config_get_value, METH_VARARGS, "Get value by index"},
    {"set_value", (PyCFunction)Config_set_value, METH_VARARGS, "Set value by index"},
    {"get_values", (PyCFunction)Config_get_values, METH_NOARGS, "Get all values"},
    {NULL}
};

static PyTypeObject ConfigType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "mymodule.Config",
    .tp_doc = "Configuration object with nested struct and arrays",
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
    "Nested Config type demo.",
    -1,
    NULL
};

PyMODINIT_FUNC
PyInit_mymodule(void)
{
    PyObject *m = PyModule_Create(&mymodule_def);
    if (m == NULL)
        return NULL;

    if (PyType_Ready(&NetworkConfigType) < 0) {
        Py_DECREF(m);
        return NULL;
    }
    Py_INCREF(&NetworkConfigType);
    if (PyModule_AddObject(m, "NetworkConfig",
                           (PyObject *)&NetworkConfigType) < 0) {
        Py_DECREF(m);
        return NULL;
    }

    if (PyType_Ready(&ConfigType) < 0) {
        Py_DECREF(m);
        return NULL;
    }
    Py_INCREF(&ConfigType);
    if (PyModule_AddObject(m, "Config", (PyObject *)&ConfigType) < 0) {
        Py_DECREF(m);
        return NULL;
    }
    return m;
}
