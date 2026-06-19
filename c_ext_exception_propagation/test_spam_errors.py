"""Verify §1.2 exception propagation pattern."""

import spam_errors

result = spam_errors.call(0)
assert result == 84  # 42 * 2 through layer2

try:
    spam_errors.call(1)
    raise AssertionError("expected SpamError")
except spam_errors.SpamError as exc:
    assert "file not found" in str(exc)

print("c_ext_exception_propagation: OK")
