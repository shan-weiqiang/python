"""Verify §1.1 / §1.4 spam_system extension."""

import spam

# true exits 0 on all Unix shells
status = spam.system("true")
assert status == 0

# false exits non-zero
status = spam.system("false")
assert status != 0

print("c_ext_spam_system: OK")
