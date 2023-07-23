"""
Preface
    Before we go into detail about these special methods, one thing has to be clarified about arguments:
        1. For these methods inside a class(subclass of object)
            a. The first positional arguments: 
                __call__: instance object
                __new__: class of instance that about to be created; by default object only accept this arguments
                __init__: instance object
            b. The rest of positional arguments and keyword arguments
                The rest of positional arguments and keyword arguments will be passed to __new__ and __init__ by 
                metaclass of this class's __call__
        2. For these methods inside a metaclass(subclass of type):
            a. The first positional arguments:
                The same as those inside a class
            b. The rest of positional arguments and keyword arguments:
                classname
                base class tuple
                namespace dict
                any keyword arguments
            c. metaclass of this metaclass(normally type itself)'s __call__ have all those arguments
                __call__ pass arguments in b to __new__
                __new__ pass any keywords arguments to __init_subclass__ of the most close base class
                __call__ pass arguments in b to __init__
                

About __call__ instance method:
    1. __call__ method make instances of the owner class callable
    2. This applies to class and metaclass, and meta-metaclass. 
    3. __call__ is instance method, the first argument is the object who calls this method, whether it's class instance or class
    4. ALL creation of class and variable starts from type.__call__(*args, **kwargs)
        a. For metameta class it returns a class object
        b. For metaclass it returns a variable abject
    5. Whenever a(), a.__class__.__call__ is called, inside this call, type.__call__ is called 
    6. For __call__ of metaclass(subclass of type), should return super().__call__,since the object of metaclass is to create class
    7. For __call__ of class, no requirement on return value
    8. Arguments of __call__ for metaclass:
        a. The first argument is the instance(class object) which calls the method
        b. followed by three positional arguments: class name, base class tuple, namespace dict
        c. followed by any keyword arguments
    9. Arguments of __call__ for class:
        a. The first arguments is the variable instance which calls the method
        b. followed by any positional and keyword arguments that __call__ method defines

About __prepare__ class method(must be explicitly declared using @classmethod):
    When create class using class keyword, __prepare__ method of the metaclass is used to return a namspace dict
    ! No __prepare__ called when creating class dynamically


From https://docs.python.org/3/reference/datamodel.html#object.__new__

About __new__ static method:
    object.__new__(cls[, ...])
    Called to create a new instance of class cls. __new__() is a static method (special-cased so you need not declare it as
    such) that takes the class of which an instance was requested as its first argument. 
    The remaining arguments are those passed to the object constructor expression (the call to the class). 
    The return value of __new__() should be the new object instance (usually an instance of cls).

About __init__ instance method:
    object.__init__(self[, ...])
    Called after the instance has been created (by __new__()), but before it is returned to the caller. 
    The arguments are those passed to the class constructor expression. If a base class has an __init__() method, 
    the derived class’s __init__() method, if any, must explicitly call it to ensure proper initialization of the 
    base class part of the instance; for example: super().__init__([args...]).
"""


class MetaMeta(type):
    """
    Normally this should be type itself, here just used to print info
    """

    def __call__(self, class_name, base_class_tuple, namespace_dict, **kwargs):
        print(
            f"MetaMeta __call__ with {self}, {class_name},{base_class_tuple},{namespace_dict}, {kwargs}")
        # if MetaMeta is used as metaclass for another metaclass, this returns a class object
        ret = super().__call__(class_name, base_class_tuple, namespace_dict, **kwargs)
        print(f"MetaMeta __call__ return")
        return ret


class Meta(type, metaclass=MetaMeta):
    """
    This is a metaclass, because it's subclass of type; also it use MetaMeta as metaclass, so metaclass can also has metaclass, but normally
    metaclass's metaclass is type, here just to print infomation; if we change to metaclass=type, it's also ok:
    Meta(type, metaclass=MetaMeta) == Meta(type) == Meta(type, metaclass=type)
    We can see that metaclass do not have multiple hierachy, since all metaclass directly subclass type itself
    """

    @classmethod
    def __prepare__(cls, class_name, base_class, **kwargs):
        print(
            f"Meta __prepare__ with {cls}, {class_name},{base_class} {kwargs}")

        class VerboseDict(dict):
            def __init__(self, name):
                self.name = name

            def __setitem__(self, name, value):
                print(f"{self.name} assignment {name}={value}")
                if name == "__annotations__":
                    value = VerboseDict("   annotations")
                super().__setitem__(name, value)
        print(f"Meta __prepare__ return")
        return VerboseDict("ns")

    def __call__(self, *args, **kwargs):
        """
        Always return a instance of class(which is instance of Meta), since the instance of metaclass is class, class are callable to return
        a class instance
        """
        print(
            f'Meta class __call__ with {self}, {args}, {kwargs}')
        # when class created by Meta is instantiated, this line return the created variable
        ret = super().__call__(*args, **kwargs)
        print(f'Meta __call__ method return')
        return ret

    def __new__(cls, class_name, base_class_tuple, namespace_dict, **kwargs):
        print(
            f"Meta __new__ with {cls}, {class_name}, {base_class_tuple}, {namespace_dict}, {kwargs}")
        ret = super().__new__(cls, class_name, base_class_tuple, namespace_dict, **kwargs)
        print(f"Meta __new__ return")
        return ret

    def __init__(self, class_name, base_class_tuple, namespace_dict, **kwargs):
        """
        Unlike __init__ of class object, __init__ of metaclass's positional arguments is fixed:
            1. self: class being created
            2. args:
                class name
                base class tuple
                namespace dict
            3. keyword argument provided by user class definition
        """
        print(
            f"Meta __init__ with {self}, {class_name}, {base_class_tuple}, {namespace_dict}, {kwargs}")
        print(f"Meta __init__ return")


class Base:
    def __init_subclass__(cls, **kwargs):
        """
        This is classmethod, when subclass are created, type.__call__ method will call this method and pass class object created as cls
        """
        print(f"Base __init_subclass__ with {cls}, {kwargs}")
        super().__init_subclass__()
        print(f"Base __init_subclass__ return")


print(f">>>>>>> dynamcally creating class<<<<<<<<<<<<<<", end='\n\n')


def f(self, *args, **kwargs):
    print(f"someclass __init__ with {args} {kwargs}")


SomeClass = Meta('SomeClass', (Base,), {'x': 10, '__init__': f}, foo='bar')
"""
This line dynamically create class SomeClass, this will call MetaMeta.__call__ and pass all arguments to it:
Parameters：
    positional arguments:
        'SomeClass':            class name
        (Base,):                tuple containing all base classes
        {'x':..}:               namespace dict containing all class variables and methods

    keyword arguments:
        foo='bar'
    
    The number and meaning of positional arguments is fixed for metaclass's __call__
    keywords parameter can be user defined. __call__ will pass these positional and keyword arguments to __new__
    and __init__, and inside __new__,  keyword arguments will be passed to __init_subclass__ in base class

    Meta.__prepare__ will NOT be called in dynamically created class!!
"""

print(f">>>>>>> using class keyword creating class<<<<<<<<<<<<<<", end='\n\n')


class MyClass(Base, metaclass=Meta, bar='foo'):
    """
    Equals to MyClass = Meta('MyClass', ('Base',),{'data':10, '__call__':...},{'bar':'foo'})
    """
    data = 10

    def __call__(self, *args, **kwargs):
        """
        Might not return a value, since instance of class is normal variable, callable variable might not need to return
        anything
        """
        print(f'MyClass __call__ with {self}, {args}, {kwargs}')
        """
        For normal classes, whose base class is 'object', which does not have __call__ method
        For metaclass, whose base class is 'type', the __call__ method must be called to return a class instance
        """
        # Cannot access member "__call__" for type "object"   Member "__call__" is unknown
        # ret = super().__call__(*args, **kwargs)
        print(f'MyClass __call__ method return')

    def __new__(cls, *args, **kwargs):
        print(f"MyClass __new__ with {cls} {args} {kwargs}")
        ret = super().__new__(cls)
        print(f"MyClass __new__ return")
        return ret

    def __init__(self, *args, **kwargs):
        """
        Will be called by Meta.__call__ method, and pass all user arguments inside MyClass(..) to this
        If there there are no matching __init__ to accept these arguments there will be TypeError
        """
        print(f"MyClass __init__ with {self}, {args}, {kwargs}")
        print(f"MyClass __init__ return")


print(f">>>>>>> class instantiation<<<<<<<<<<<<<<", end='\n\n')
# This calls __call__ of Meta, since the __class__ of MyClass is Meta, and pass instance MyClass as first argument
a = MyClass('Bonjure', foo='Nihao')
print(f">>>>>>> callable instance<<<<<<<<<<<<<<", end='\n\n')
# This calls __call__ of MyClass, since the __class__ of a is MyClass, and pass instance a as first argument
a(foo='Hello')
