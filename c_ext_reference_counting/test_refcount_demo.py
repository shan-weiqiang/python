"""Verify §1.3 reference counting patterns."""

import refcount_demo

lst = refcount_demo.new_reference()
assert lst == []

assert refcount_demo.borrowed_reference([]) == -1
assert refcount_demo.borrowed_reference([7]) == 7

lst = [1, 2]
size = refcount_demo.steal_reference(lst, 3)
assert size == 3
assert lst == [1, 2, 3]

assert refcount_demo.marker == "owned_by_module"

print("c_ext_reference_counting: OK")
