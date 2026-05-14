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


def assert_test_contains(test_name: str) -> None:
    tests = "\n".join(read(p) for p in tracked_files() if p.startswith("tests/") and p.endswith(".py"))
    if test_name not in tests:
        fail(f"Expected a test named or referencing {test_name!r}")
    ok(f"Tests reference {test_name!r}")


def commit_messages_since_base(base: str = "origin/main") -> list[str]:
    result = run(["git", "log", "--format=%s", f"{base}..HEAD"], check=False)
    if result.returncode != 0:
        result = run(["git", "log", "--format=%s", "main..HEAD"], check=False)
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def commit_count_since_base(base: str = "origin/main") -> int:
    result = run(["git", "rev-list", "--count", f"{base}..HEAD"], check=False)
    if result.returncode != 0:
        result = run(["git", "rev-list", "--count", "main..HEAD"], check=False)
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
    assert_test_contains("multiply")
    assert_no_text("app/calculator.py", r"print\(", "calculator.py must not contain debug print calls")


def validate_divide() -> None:
    assert_function("app/calculator.py", "divide")
    assert_test_contains("divide")


def validate_division_by_zero() -> None:
    assert_function("app/calculator.py", "divide")
    code = read("app/calculator.py")
    if "ZeroDivisionError" not in code and "ValueError" not in code:
        fail("divide should explicitly handle division by zero with a clear exception")
    ok("divide handles division by zero explicitly")
    assert_test_contains("zero")


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


def validate_tax() -> None:
    assert_function("app/calculator.py", "calculate_tax")
    assert_test_contains("calculate_tax")


EXERCISE_VALIDATORS = {
    "feature/multiply-operation": validate_multiply,
    "feature/divide-operation": validate_divide,
    "hotfix/division-by-zero": validate_division_by_zero,
    "feature/clean-history": validate_clean_history,
    "feature/squash-demo": validate_squash_demo,
    "feature/fixup-demo": validate_fixup_demo,
    "feature/tax-calculation": validate_tax,
}


def main() -> int:
    branch = current_branch()
    print(f"🔎 Validating branch: {branch}")
    generic_checks()
    validator = EXERCISE_VALIDATORS.get(branch)
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
