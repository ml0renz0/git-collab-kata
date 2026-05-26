#!/usr/bin/env python3
"""Validation harness for the Git collaboration kata.

The script intentionally validates observable outcomes instead of publishing
exercise solutions. It can run locally or in GitHub Actions.
"""
from __future__ import annotations

import ast
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Failure(Exception):
    pass


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=check)


def ok(msg: str) -> None:
    print(f"✅ {msg}")


def fail(msg: str) -> None:
    raise Failure(msg)


def current_branch() -> str:
    env_branch = os.getenv("GITHUB_HEAD_REF") or os.getenv("GITHUB_REF_NAME")
    if env_branch:
        return env_branch
    result = run(["git", "branch", "--show-current"])
    return result.stdout.strip()


def ref_exists(ref: str) -> bool:
    result = run(["git", "rev-parse", "--verify", "--quiet", ref], check=False)
    return result.returncode == 0


def exercise_branch_base(branch: str) -> str | None:
    for expected_branch in EXERCISE_VALIDATORS:
        if branch == expected_branch:
            return expected_branch
        if branch.startswith(f"{expected_branch}-"):
            return expected_branch
    return None


def user_suffix(branch: str) -> str | None:
    expected_branch = exercise_branch_base(branch)
    if expected_branch is None or branch == expected_branch:
        return None
    return branch.removeprefix(f"{expected_branch}-")


def base_candidates(branch: str | None = None) -> list[str]:
    branch = branch or current_branch()
    candidates: list[str] = []

    github_base = os.getenv("GITHUB_BASE_REF")
    if github_base:
        candidates.extend([f"origin/{github_base}", github_base])

    suffix = user_suffix(branch)
    if suffix:
        candidates.extend([f"origin/main-{suffix}", f"main-{suffix}"])

    candidates.extend(["origin/main", "main"])
    return candidates


def first_existing_base(branch: str | None = None) -> str:
    for candidate in base_candidates(branch):
        if ref_exists(candidate):
            return candidate
    fail(f"Could not find a base branch. Tried: {base_candidates(branch)}")


def tracked_files() -> list[str]:
    return run(["git", "ls-files"]).stdout.splitlines()


def read(path: str) -> str:
    p = ROOT / path
    if not p.exists():
        fail(f"Missing required file: {path}")
    return p.read_text(encoding="utf-8")


def parse_module(path: str) -> ast.Module:
    return ast.parse(read(path), filename=path)


def function_names(path: str) -> set[str]:
    tree = parse_module(path)
    return {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}


def assert_function(path: str, name: str) -> None:
    names = function_names(path)
    if name not in names:
        fail(f"Expected function {name!r} in {path}. Found: {sorted(names)}")
    ok(f"Function {name!r} exists in {path}")


def assert_no_text(path: str, pattern: str, description: str) -> None:
    content = read(path)
    if re.search(pattern, content, re.IGNORECASE):
        fail(description)
    ok(description.replace("must not", "does not"))


def assert_file_exists(path: str) -> None:
    if not (ROOT / path).exists():
        fail(f"Expected file to exist: {path}")
    ok(f"File exists: {path}")


def assert_file_absent(path: str) -> None:
    if (ROOT / path).exists():
        fail(f"File should not exist: {path}")
    ok(f"File absent: {path}")


def assert_file_contains(path: str, pattern: str, description: str) -> None:
    content = read(path)
    if not re.search(pattern, content, re.IGNORECASE | re.DOTALL):
        fail(description)
    ok(description.replace("Expected", "Found"))


def assert_test_contains(test_name: str) -> None:
    tests = "\n".join(read(p) for p in tracked_files() if p.startswith("tests/") and p.endswith(".py"))
    if test_name not in tests:
        fail(f"Expected a test named or referencing {test_name!r}")
    ok(f"Tests reference {test_name!r}")


def assert_test_function(name: str, required_text: str | None = None) -> None:
    test_files = [p for p in tracked_files() if p.startswith("tests/") and p.endswith(".py")]
    for path in test_files:
        tree = parse_module(path)
        for node in tree.body:
            if not isinstance(node, ast.FunctionDef) or node.name != name:
                continue
            if required_text is not None:
                references = any(
                    isinstance(child, ast.Name) and child.id == required_text
                    or isinstance(child, ast.Attribute) and child.attr == required_text
                    for child in ast.walk(node)
                )
                if not references:
                    fail(f"Expected test {name!r} to exercise {required_text!r}")
            ok(f"Test function {name!r} exists")
            return
    fail(f"Expected test function {name!r} in tests/")


def assert_python_result(expression: str, expected: str) -> None:
    result = run([sys.executable, "-c", f"from app.calculator import *; print({expression})"], check=False)
    actual = result.stdout.strip()
    if result.returncode != 0 or actual != expected:
        detail = result.stderr.strip() or actual or f"exit code {result.returncode}"
        fail(f"Expected {expression} to print {expected!r}; got {detail!r}")
    ok(f"{expression} returns {expected}")


def assert_python_raises(expression: str, expected_exception: str) -> None:
    code = f"""
from app.calculator import *

try:
    {expression}
except {expected_exception}:
    pass
else:
    raise AssertionError("Expected {expected_exception}")
"""
    result = run([sys.executable, "-c", code], check=False)
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or f"exit code {result.returncode}"
        fail(f"Expected {expression} to raise {expected_exception}; got {detail!r}")
    ok(f"{expression} raises {expected_exception}")


def assert_tests_match(pattern: str, description: str) -> None:
    tests = "\n".join(read(p) for p in tracked_files() if p.startswith("tests/") and p.endswith(".py"))
    if not re.search(pattern, tests, re.IGNORECASE | re.DOTALL):
        fail(description)
    ok(description.replace("Expected", "Found"))


def commit_messages_since_base(base: str | None = None) -> list[str]:
    base = base or first_existing_base()
    result = run(["git", "log", "--format=%s", f"{base}..HEAD"], check=False)
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def commit_count_since_base(base: str | None = None) -> int:
    base = base or first_existing_base()
    result = run(["git", "rev-list", "--count", f"{base}..HEAD"], check=False)
    try:
        return int(result.stdout.strip())
    except ValueError:
        return 0


def generic_checks() -> None:
    forbidden = []
    for file in tracked_files():
        if file == ".env" or file.endswith(".pem") or file.endswith(".key"):
            forbidden.append(file)
        if file.startswith("solutions/"):
            forbidden.append(file)
    if forbidden:
        fail(f"Forbidden tracked files found: {forbidden}")
    ok("No forbidden tracked files")

    secret_patterns = [r"TOKEN\s*=", r"SECRET\s*=", r"BEGIN [A-Z]+ PRIVATE KEY"]
    for file in tracked_files():
        path = ROOT / file
        if not path.is_file() or path.stat().st_size > 500_000:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in secret_patterns:
            if re.search(pattern, text):
                fail(f"Possible secret-like content found in tracked file {file}: {pattern}")
    ok("No obvious secret-like content in tracked files")

    bad_messages = [m for m in commit_messages_since_base() if re.search(r"\b(wip|stuff|tmp|temp|fix later)\b", m, re.I)]
    if bad_messages:
        fail(f"Clean up commit messages before PR: {bad_messages}")
    ok("No obvious WIP commit messages in branch history")


def validate_multiply() -> None:
    assert_function("app/calculator.py", "multiply")
    assert_test_function("test_multiply", "multiply")
    assert_python_result("multiply(2, 3)", "6")
    assert_no_text("app/calculator.py", r"print\(", "calculator.py must not contain debug print calls")


def validate_divide() -> None:
    assert_function("app/calculator.py", "divide")
    assert_test_function("test_divide", "divide")
    assert_python_result("divide(10, 2)", "5.0")


def validate_modulus() -> None:
    assert_function("app/calculator.py", "divide")
    assert_function("app/calculator.py", "modulus")
    assert_test_function("test_divide", "divide")
    assert_test_function("test_modulus", "modulus")
    assert_python_result("divide(10, 2)", "5.0")
    assert_python_result("modulus(10, 3)", "1")


def validate_exponentiation() -> None:
    assert_function("app/calculator.py", "exponentiation")
    assert_test_function("test_exponentiation", "exponentiation")
    assert_python_result("exponentiation(2, 3)", "8")
    assert_no_text("app/calculator.py", r"print\(", "calculator.py must not contain debug print calls")


def validate_division_by_zero() -> None:
    assert_function("app/calculator.py", "divide")
    assert_python_result("divide(10, 2)", "5.0")
    assert_python_raises("divide(10, 0)", "ZeroDivisionError")
    assert_tests_match(r"zero", "Expected tests to cover division by zero")


def validate_add_cast_int() -> None:
    assert_function("app/calculator.py", "add")
    assert_python_result("add('2', '3')", "5")
    assert_tests_match(r"add\s*\(\s*['\"]2['\"]\s*,\s*['\"]3['\"]\s*\)", "Expected tests to cover add casting string inputs")


def validate_add_none_validation() -> None:
    assert_function("app/calculator.py", "add")
    assert_python_result("add('2', '3')", "5")
    assert_python_raises("add(None, 3)", "ValueError")
    assert_tests_match(r"add\s*\(\s*None\s*,\s*3\s*\)", "Expected tests to cover add rejecting None")


def validate_clean_history() -> None:
    assert_file_exists("docs/usage.md")
    assert_file_absent("temp.txt")
    count = commit_count_since_base()
    if count != 1:
        fail(f"Expected exactly 1 commit over main after cleanup, found {count}")
    ok("Branch contains exactly one commit over main")


def validate_squash_demo() -> None:
    assert_file_exists("docs/squash.md")
    count = commit_count_since_base()
    if count != 1:
        fail(f"Expected the squash demo to end as 1 commit over main, found {count}")
    ok("Squash demo branch contains exactly one commit over main")


def validate_fixup_demo() -> None:
    assert_file_exists("docs/api.md")
    count = commit_count_since_base()
    if count != 1:
        fail(f"Expected fixup/autosquash branch to end as 1 commit over main, found {count}")
    ok("Fixup demo branch contains exactly one commit over main")


def validate_recovery_sandbox() -> None:
    assert_file_exists("app/calculator.py")
    assert_file_exists("docs/recovery.md")
    assert_file_contains("docs/recovery.md", r"restore", "Expected docs/recovery.md to mention restore")
    assert_file_contains("docs/recovery.md", r"staged?", "Expected docs/recovery.md to mention staged")
    assert_file_absent("debug.conf")


def validate_reflog_rescue() -> None:
    assert_file_exists("important.txt")
    assert_file_contains("important.txt", r"important", "Expected important.txt to contain important")


def validate_revert_demo() -> None:
    assert_file_absent("production.txt")
    count = commit_count_since_base()
    if count < 2:
        fail(f"Expected revert demo branch to contain at least 2 commits over main, found {count}")
    ok("Revert demo branch contains at least two commits over main")
    messages = commit_messages_since_base()
    if not any(re.search(r"\brevert\b", message, re.IGNORECASE) for message in messages):
        fail(f"Expected at least one revert commit message, found: {messages}")
    ok("Revert commit message found")


def validate_tax() -> None:
    assert_function("app/calculator.py", "calculate_tax")
    assert_test_contains("calculate_tax")


EXERCISE_VALIDATORS = {
    "feature/multiply": validate_multiply,
    "feature/exponentiation": validate_exponentiation,
    "feature/divide-operation": validate_divide,
    "feature/modulus-operation": validate_modulus,
    "hotfix/division-by-zero": validate_division_by_zero,
    "feature/add-cast-int": validate_add_cast_int,
    "feature/add-none-validation": validate_add_none_validation,
    "feature/clean-history": validate_clean_history,
    "feature/squash-demo": validate_squash_demo,
    "feature/fixup-demo": validate_fixup_demo,
    "feature/recovery-sandbox": validate_recovery_sandbox,
    "rescue/reflog": validate_reflog_rescue,
    "chore/revert-demo": validate_revert_demo,
    "feature/tax-calculation": validate_tax,
}


def branch_validator(branch: str):
    for expected_branch, validator in EXERCISE_VALIDATORS.items():
        if branch == expected_branch or branch.startswith(f"{expected_branch}-"):
            return validator
    return None


def main() -> int:
    branch = current_branch()
    print(f"🔎 Validating branch: {branch}")
    generic_checks()
    validator = branch_validator(branch)
    if validator is None:
        print("ℹ️ No branch-specific kata validator for this branch. Running generic checks only.")
        return 0
    validator()
    print("🎉 Exercise validation passed")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Failure as exc:
        print(f"❌ {exc}", file=sys.stderr)
        raise SystemExit(1)
