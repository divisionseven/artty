# Plan for: Fix `test_windows_with_ctypes_available_returns_true` Failing Test

## Task Type
Bug Fix — Incorrect Test Mocking Strategy

---

## 🔍 Root Cause Confirmation

**Confirmed Root Cause:** The test's `monkeypatch.setattr(builtins, "__import__", mock_import)` is insufficient because Python checks `sys.modules` before calling `__import__`. On macOS at pytest start, `ctypes` is already cached in `sys.modules`. When `_supports_ansi()` executes `import ctypes`, Python returns the real cached module from `sys.modules` — the mocked `__import__` is never invoked.

**Evidence:**
- `src/artty/ansi.py:23-24` — `import ctypes` and `from ctypes import wintypes` use the cached module
- `src/artty/ansi.py:26` — `kernel32 = ctypes.windll.kernel32` — `windll` does not exist on macOS ctypes
- `src/artty/ansi.py:47-49` — `except Exception: return False` — catches the AttributeError

**How This Plan Addresses It:**
Replace the `builtins.__import__` monkeypatch with direct `sys.modules` patching. This bypasses Python's module caching mechanism and ensures the mock is used.

---

## Overview

The test incorrectly patches `builtins.__import__` to return a mock ctypes module. However, Python's import system first checks `sys.modules` before calling `__import__`. Since `ctypes` is already imported and cached in `sys.modules` at test time, the mock is never used.

**Fix:** Patch `sys.modules["ctypes"]` and `sys.modules["ctypes.wintypes"]` directly with mock objects.

---

## Success Criteria
- [ ] `test_windows_with_ctypes_available_returns_true` passes
- [ ] `test_windows_with_ctypes_import_failure_returns_false` passes (also uses broken mock)
- [ ] `test_windows_with_SetConsoleMode_failure_returns_false` passes (also uses broken mock)
- [ ] `test_returns_bool` continues to pass (no regression)
- [ ] `test_non_windows_platform_returns_isatty_result` continues to pass (no regression)
- [ ] `test_non_windows_with_isatty_returns_true` continues to pass (no regression)
- [ ] `test_non_windows_with_isatty_returns_false` continues to pass (no regression)

---

## Files to Modify

- **Path:** `tests/test_ansi.py`
- **Current behavior:** Tests at lines 54-81, 83-99, and 101-127 use `builtins.__import__` monkeypatch which fails on macOS/Linux due to module caching
- **Required change:** Replace `builtins.__import__` monkeypatch with direct `sys.modules` patching
- **Why:** `sys.modules` is checked before `__import__` is called, so patching `builtins.__import__` has no effect on already-cached modules

---

## Implementation Steps

### Step 1: Fix `test_windows_with_ctypes_available_returns_true`

**Location:** `tests/test_ansi.py:54-81`

**Change:** Replace the `builtins.__import__` monkeypatch with direct `sys.modules` patching.

**Current code (lines 54-81):**
```python
def test_windows_with_ctypes_available_returns_true(self, monkeypatch):
    """Test that Windows with working ctypes returns True."""
    monkeypatch.setattr(sys, "platform", "win32")

    # Create mock ctypes with working functions
    class MockKernel:
        def GetStdHandle(self, handle):  # noqa: N802
            return 1

        def SetConsoleMode(self, handle, mode):  # noqa: N802
            return True

    class MockCtypes:
        windll = type("windll", (), {"kernel32": MockKernel()})()

    # We need to make ctypes import work with mock
    import builtins

    original_import = builtins.__import__

    def mock_import(name, *args, **kwargs):
        if name == "ctypes":
            return MockCtypes()
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", mock_import)
    result = _supports_ansi()
    assert result is True
```

**New code:**
```python
def test_windows_with_ctypes_available_returns_true(self, monkeypatch):
    """Test that Windows with working ctypes returns True."""
    monkeypatch.setattr(sys, "platform", "win32")

    # Create mock ctypes with working functions
    class MockKernel:
        def GetStdHandle(self, handle):  # noqa: N802
            return 1

        def GetConsoleMode(self, handle, mode_ptr):  # noqa: N802
            # Simulate successful GetConsoleMode by writing to the DWORD
            mode_ptr._value = 0  # noqa: SLF001

        def SetConsoleMode(self, handle, mode):  # noqa: N802
            return True

    class MockWintypes:
        class HANDLE:
            def __init__(self, value):
                self.value = value

        class DWORD:
            def __init__(self, value=0):
                self.value = value

    class MockCtypes:
        windll = type("windll", (), {"kernel32": MockKernel()})()  # noqa: N816

        @staticmethod
        def byref(obj):
            # Return a mock reference that allows setting _value
            ref = type("ref", (), {"_value": obj.value})()
            return ref

    # Store original modules to restore later
    original_ctypes = sys.modules.get("ctypes")
    original_wintypes = sys.modules.get("ctypes.wintypes")

    try:
        # Directly patch sys.modules to bypass import machinery
        sys.modules["ctypes"] = MockCtypes()
        sys.modules["ctypes.wintypes"] = MockWintypes()
        result = _supports_ansi()
        assert result is True
    finally:
        # Restore original modules
        if original_ctypes is not None:
            sys.modules["ctypes"] = original_ctypes
        elif "ctypes" in sys.modules:
            del sys.modules["ctypes"]
        if original_wintypes is not None:
            sys.modules["ctypes.wintypes"] = original_wintypes
        elif "ctypes.wintypes" in sys.modules:
            del sys.modules["ctypes.wintypes"]
```

---

### Step 2: Fix `test_windows_with_ctypes_import_failure_returns_false`

**Location:** `tests/test_ansi.py:83-99`

**Change:** Replace the `builtins.__import__` monkeypatch with `sys.modules` deletion approach.

**Current code (lines 83-99):**
```python
def test_windows_with_ctypes_import_failure_returns_false(self, monkeypatch):
    """Test that Windows with ctypes import failure returns False."""
    monkeypatch.setattr(sys, "platform", "win32")

    # Mock ctypes import to raise an exception
    import builtins

    original_import = builtins.__import__

    def mock_import(name, *args, **kwargs):
        if name == "ctypes":
            raise ImportError("No module named 'ctypes'")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", mock_import)
    result = _supports_ansi()
    assert result is False
```

**New code:**
```python
def test_windows_with_ctypes_import_failure_returns_false(self, monkeypatch):
    """Test that Windows with ctypes import failure returns False."""
    monkeypatch.setattr(sys, "platform", "win32")

    # Store original module to restore later
    original_ctypes = sys.modules.get("ctypes")
    original_wintypes = sys.modules.get("ctypes.wintypes")

    def mock_import(name, *args, **kwargs):
        raise ImportError(f"No module named '{name}'")

    try:
        # Remove ctypes from sys.modules and patch __import__ to raise
        # This simulates a scenario where ctypes cannot be loaded
        if "ctypes" in sys.modules:
            del sys.modules["ctypes"]
        if "ctypes.wintypes" in sys.modules:
            del sys.modules["ctypes.wintypes"]

        monkeypatch.setattr(builtins, "__import__", mock_import)
        result = _supports_ansi()
        assert result is False
    finally:
        # Restore original modules
        if original_ctypes is not None:
            sys.modules["ctypes"] = original_ctypes
        if original_wintypes is not None:
            sys.modules["ctypes.wintypes"] = original_wintypes
```

---

### Step 3: Fix `test_windows_with_SetConsoleMode_failure_returns_false`

**Location:** `tests/test_ansi.py:101-127`

**Change:** Replace the `builtins.__import__` monkeypatch with direct `sys.modules` patching.

**Current code (lines 101-127):**
```python
def test_windows_with_SetConsoleMode_failure_returns_false(self, monkeypatch):  # noqa: N802
    """Test that Windows when SetConsoleMode fails returns False."""
    monkeypatch.setattr(sys, "platform", "win32")

    # Create mock ctypes where SetConsoleMode raises an exception
    class MockKernel:
        def GetStdHandle(self, handle):  # noqa: N802
            return 1

        def SetConsoleMode(self, handle, mode):  # noqa: N802
            raise Exception("Console mode not supported")

    class MockCtypes:
        windll = type("windll", (), {"kernel32": MockKernel()})()

    import builtins

    original_import = builtins.__import__

    def mock_import(name, *args, **kwargs):
        if name == "ctypes":
            return MockCtypes()
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", mock_import)
    result = _supports_ansi()
    assert result is False
```

**New code:**
```python
def test_windows_with_SetConsoleMode_failure_returns_false(self, monkeypatch):  # noqa: N802
    """Test that Windows when SetConsoleMode fails returns False."""
    monkeypatch.setattr(sys, "platform", "win32")

    # Create mock ctypes where SetConsoleMode raises an exception
    class MockKernel:
        def GetStdHandle(self, handle):  # noqa: N802
            return 1

        def GetConsoleMode(self, handle, mode_ptr):  # noqa: N802
            # Simulate successful GetConsoleMode
            mode_ptr._value = 0  # noqa: SLF001

        def SetConsoleMode(self, handle, mode):  # noqa: N802
            raise Exception("Console mode not supported")

    class MockWintypes:
        class HANDLE:
            def __init__(self, value):
                self.value = value

        class DWORD:
            def __init__(self, value=0):
                self.value = value

    class MockCtypes:
        windll = type("windll", (), {"kernel32": MockKernel()})()  # noqa: N816

        @staticmethod
        def byref(obj):
            ref = type("ref", (), {"_value": obj.value})()  # noqa: SLF001
            return ref

    # Store original modules to restore later
    original_ctypes = sys.modules.get("ctypes")
    original_wintypes = sys.modules.get("ctypes.wintypes")

    try:
        # Directly patch sys.modules to bypass import machinery
        sys.modules["ctypes"] = MockCtypes()
        sys.modules["ctypes.wintypes"] = MockWintypes()
        result = _supports_ansi()
        assert result is False
    finally:
        # Restore original modules
        if original_ctypes is not None:
            sys.modules["ctypes"] = original_ctypes
        elif "ctypes" in sys.modules:
            del sys.modules["ctypes"]
        if original_wintypes is not None:
            sys.modules["ctypes.wintypes"] = original_wintypes
        elif "ctypes.wintypes" in sys.modules:
            del sys.modules["ctypes.wintypes"]
```

---

## Caller/Consumer Impact Assessment

| File           | Function/Method | Expects | Impact of Change | Action Needed |
|----------------|-----------------|---------|------------------|---------------|
| N/A | N/A | N/A | This is a test-only change | No production code affected |

---

## Testing Strategy

### Regression Tests
All existing tests in `TestSupportsAnsi` class must continue to pass:
- `test_returns_bool`
- `test_non_windows_platform_returns_isatty_result`
- `test_non_windows_with_isatty_returns_true`
- `test_non_windows_with_isatty_returns_false`

### New Behavior Tests (Fixed)
- `test_windows_with_ctypes_available_returns_true` — now correctly mocks ctypes via `sys.modules`
- `test_windows_with_ctypes_import_failure_returns_false` — now correctly simulates import failure
- `test_windows_with_SetConsoleMode_failure_returns_false` — now correctly mocks ctypes via `sys.modules`

### Test Execution
```bash
pytest tests/test_ansi.py -v
```

---

## Other Test Cases That Might Need Similar Fixes

**Identified:** All three Windows-specific tests in `tests/test_ansi.py` use the same broken `builtins.__import__` patching pattern:
1. `test_windows_with_ctypes_available_returns_true` (lines 54-81)
2. `test_windows_with_ctypes_import_failure_returns_false` (lines 83-99)
3. `test_windows_with_SetConsoleMode_failure_returns_false` (lines 101-127)

All three are fixed in this plan.

**Potential future issue:** Any other tests in the codebase that mock `builtins.__import__` to control module imports will have the same problem on macOS/Linux. This pattern should be avoided in favor of `sys.modules` patching.

---

## Key Technical Details

### Why `sys.modules` Patching Works
Python's import system checks `sys.modules` first:
1. `sys.modules` lookup (returns cached module if exists)
2. If not found, call `__import__` (the hook we tried to mock)

By directly setting `sys.modules["ctypes"] = MockCtypes()`, we bypass the need for `__import__` entirely.

### Why `GetConsoleMode` Needs to Modify the Pointer
In the real function at `src/artty/ansi.py:34-35`:
```python
mode = wintypes.DWORD()
if not kernel32.GetConsoleMode(stdout_handle, ctypes.byref(mode)):
```

The `GetConsoleMode` function writes to the `DWORD` via the pointer. Our mock's `GetConsoleMode` must do the same by setting `_value` on the mock reference.

### Cleanup is Critical
Each test uses a `try/finally` block to restore original `sys.modules` entries. This prevents test pollution where one test's mock bleeds into another test.

---

## Estimated Effort
- **Complexity:** Simple
- **Risk level:** Low
- **Files changed:** 1 (tests/test_ansi.py)
- **Lines changed:** ~90 (restructured 3 test methods)
