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


def release_tag(version: str, branch: str | None = None) -> str:
    suffix = user_suffix(branch or current_branch())
    return f"{version}-{suffix}" if suffix else version


def assert_annotated_tag(tag: str) -> None:
    ref = f"refs/tags/{tag}"
    if not ref_exists(ref):
        fail(f"Expected annotated release tag {tag!r}")
    result = run(["git", "cat-file", "-t", ref], check=False)
    if result.stdout.strip() != "tag":
        fail(f"Expected {tag!r} to be an annotated tag, not a lightweight tag")
    ok(f"Annotated release tag {tag!r} exists")


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


def append_base_ref(candidates: list[str], ref: str) -> None:
    if not ref:
        return
    if ref.startswith("origin/"):
        candidates.append(ref)
        return
    candidates.extend([f"origin/{ref}", ref])


def base_candidates(branch: str | None = None) -> list[str]:
    branch = branch or current_branch()
    candidates: list[str] = []

    kata_base = os.getenv("KATA_BASE_REF")
    if kata_base:
        append_base_ref(candidates, kata_base)

    github_base = os.getenv("GITHUB_BASE_REF")
    if github_base:
        append_base_ref(candidates, github_base)

    expected_branch = exercise_branch_base(branch)
    suffix = user_suffix(branch)
    if expected_branch == "hotfix/backport-factorial":
        release_branch = f"release/v1-{suffix}" if suffix else "release/v1"
        append_base_ref(candidates, release_branch)

    if suffix:
        candidates.extend([f"origin/main-{suffix}", f"main-{suffix}"])

    candidates.extend(["origin/main", "main"])

    deduped: list[str] = []
    for candidate in candidates:
        if candidate not in deduped:
            deduped.append(candidate)
    return deduped


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


def read_from_ref(ref: str, path: str) -> str | None:
    result = run(["git", "show", f"{ref}:{path}"], check=False)
    if result.returncode != 0:
        return None
    return result.stdout


def function_names(path: str) -> set[str]:
    tree = parse_module(path)
    return {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}


def has_final_release_shape() -> bool:
    try:
        names = function_names("app/calculator.py")
        if "calculate_tax" not in names:
            return False
        if function_arg_names("app/calculator.py", "add")[:2] != ["left", "right"]:
            return False
        if function_arg_names("app/calculator.py", "subtract")[:2] != ["left", "right"]:
            return False
    except (Failure, SyntaxError):
        return False
    return True


def function_arg_names(path: str, name: str) -> list[str]:
    tree = parse_module(path)
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            args = [*node.args.posonlyargs, *node.args.args]
            return [arg.arg for arg in args]
    fail(f"Expected function {name!r} in {path}")


def assert_function(path: str, name: str) -> None:
    names = function_names(path)
    if name not in names:
        fail(f"Expected function {name!r} in {path}. Found: {sorted(names)}")
    ok(f"Function {name!r} exists in {path}")


def assert_function_absent(path: str, name: str) -> None:
    names = function_names(path)
    if name in names:
        fail(f"Function {name!r} should not exist in {path}")
    ok(f"Function {name!r} is absent from {path}")


def assert_function_args(path: str, name: str, expected: list[str]) -> None:
    actual = function_arg_names(path, name)
    if actual[: len(expected)] != expected:
        fail(f"Expected {name} arguments to start with {expected}, found {actual}")
    ok(f"Function {name!r} uses expected argument names")


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


def tree_function_has_explicit_raise(tree: ast.Module, name: str, expected_exception: str) -> bool:
    for node in tree.body:
        if not isinstance(node, ast.FunctionDef) or node.name != name:
            continue
        for child in ast.walk(node):
            if not isinstance(child, ast.Raise) or child.exc is None:
                continue
            raised = child.exc.func if isinstance(child.exc, ast.Call) else child.exc
            if isinstance(raised, ast.Name) and raised.id == expected_exception:
                return True
            if isinstance(raised, ast.Attribute) and raised.attr == expected_exception:
                return True
        return False
    return False


def function_has_explicit_raise(path: str, name: str, expected_exception: str) -> bool:
    tree = parse_module(path)
    if tree_function_has_explicit_raise(tree, name, expected_exception):
        return True
    if name not in function_names(path):
        fail(f"Expected function {name!r} in {path}")
    return False


def ref_function_has_explicit_raise(ref: str, path: str, name: str, expected_exception: str) -> bool:
    content = read_from_ref(ref, path)
    if content is None:
        return False
    try:
        tree = ast.parse(content, filename=f"{ref}:{path}")
    except SyntaxError:
        return False
    return tree_function_has_explicit_raise(tree, name, expected_exception)


def assert_explicit_raise(path: str, name: str, expected_exception: str) -> None:
    if not function_has_explicit_raise(path, name, expected_exception):
        fail(f"Expected {name!r} to explicitly raise {expected_exception}")
    ok(f"{name!r} explicitly raises {expected_exception}")


def assert_tests_match(pattern: str, description: str) -> None:
    tests = "\n".join(read(p) for p in tracked_files() if p.startswith("tests/") and p.endswith(".py"))
    if not re.search(pattern, tests, re.IGNORECASE | re.DOTALL):
        fail(description)
    ok(description.replace("Expected", "Found"))


def commit_messages_since_base(base: str | None = None) -> list[str]:
    base = base or first_existing_base()
    result = run(["git", "log", "--format=%s", f"{base}..HEAD"], check=False)
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def commit_bodies_since_base(base: str | None = None) -> str:
    base = base or first_existing_base()
    result = run(["git", "log", "--format=%B", f"{base}..HEAD"], check=False)
    return result.stdout


def commit_messages_for_ref(ref: str = "HEAD") -> list[str]:
    result = run(["git", "log", "--format=%s", ref], check=False)
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def commit_count_since_base(base: str | None = None) -> int:
    base = base or first_existing_base()
    result = run(["git", "rev-list", "--count", f"{base}..HEAD"], check=False)
    try:
        return int(result.stdout.strip())
    except ValueError:
        return 0


def assert_commit_count(expected: int, description: str) -> None:
    count = commit_count_since_base()
    if count != expected:
        fail(f"{description}: expected {expected}, found {count}")
    ok(description)


def merge_commit_count_since_base(base: str | None = None) -> int:
    base = base or first_existing_base()
    result = run(["git", "rev-list", "--merges", "--count", f"{base}..HEAD"], check=False)
    try:
        return int(result.stdout.strip())
    except ValueError:
        return 0


def assert_no_merge_commits_since_base(description: str) -> None:
    count = merge_commit_count_since_base()
    if count != 0:
        fail(f"{description}: expected 0 merge commits over the base branch, found {count}")
    ok(description)


def changed_files_since_base(base: str | None = None) -> list[str]:
    base = base or first_existing_base()
    result = run(["git", "diff", "--name-only", f"{base}...HEAD"], check=False)
    if result.returncode != 0:
        result = run(["git", "diff", "--name-only", f"{base}..HEAD"], check=False)
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def assert_max_changed_files(max_files: int) -> None:
    changed_files = changed_files_since_base()
    if len(changed_files) > max_files:
        fail(
            f"Expected at most {max_files} changed files in the PR, "
            f"found {len(changed_files)}: {changed_files}"
        )
    ok(f"PR changes at most {max_files} files")


def assert_commit_messages_absent(pattern: str, description: str) -> None:
    messages = commit_messages_since_base()
    offenders = [message for message in messages if re.search(pattern, message, re.IGNORECASE)]
    if offenders:
        fail(f"{description}: {offenders}")
    ok(description)


def generic_checks() -> None:
    forbidden = []
    forbidden_solution_files = {"solutions.md", "answers.md", "docs/solutions.md", "docs/answers.md"}
    for file in tracked_files():
        if file == ".env" or file.endswith(".pem") or file.endswith(".key"):
            forbidden.append(file)
        if file.startswith(("solutions/", "answers/")) or file in forbidden_solution_files:
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
    assert_commit_count(1, "Multiply branch contains exactly one commit over main")


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
    assert_no_merge_commits_since_base("Modulus branch was updated without merge commits")


def validate_exponentiation() -> None:
    assert_function("app/calculator.py", "exponentiation")
    assert_test_function("test_exponentiation", "exponentiation")
    assert_python_result("exponentiation(2, 3)", "8")
    assert_no_text("app/calculator.py", r"print\(", "calculator.py must not contain debug print calls")
    assert_commit_count(2, "Exponentiation branch contains exactly two commits over main")


def validate_division_by_zero() -> None:
    assert_function("app/calculator.py", "divide")
    assert_python_result("divide(10, 2)", "5.0")
    assert_python_raises("divide(10, 0)", "ZeroDivisionError")
    assert_explicit_raise("app/calculator.py", "divide", "ZeroDivisionError")
    assert_tests_match(r"zero", "Expected tests to cover division by zero")


def validate_subtract_none_validation() -> None:
    assert_function("app/calculator.py", "subtract")
    assert_python_result("subtract(5, 3)", "2")
    assert_python_raises("subtract(None, 3)", "ValueError")
    assert_tests_match(
        r"subtract\s*\(\s*None\s*,\s*3\s*\)",
        "Expected tests to cover subtract rejecting None",
    )


def validate_add_cast_int() -> None:
    assert_function("app/calculator.py", "add")
    assert_python_result("add('2', '3')", "5")
    assert_tests_match(r"add\s*\(\s*['\"]2['\"]\s*,\s*['\"]3['\"]\s*\)", "Expected tests to cover add casting string inputs")


def validate_add_none_validation() -> None:
    assert_function("app/calculator.py", "add")
    assert_python_result("add('2', '3')", "5")
    assert_python_raises("add(None, 3)", "ValueError")
    assert_tests_match(r"add\s*\(\s*None\s*,\s*3\s*\)", "Expected tests to cover add rejecting None")
    assert_no_merge_commits_since_base("Add None validation branch was updated without merge commits")


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
    assert_file_contains("docs/recovery.md", r"\bclean\b", "Expected docs/recovery.md to mention git clean")
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


def validate_pr_template() -> None:
    assert_file_exists("docs/pr-template.md")
    assert_file_contains(
        "docs/pr-template.md",
        r"##\s+Qu[eé]\s+cambia",
        "Expected docs/pr-template.md to include Qué cambia",
    )
    assert_file_contains(
        "docs/pr-template.md",
        r"##\s+Por\s+qu[eé]",
        "Expected docs/pr-template.md to include Por qué",
    )
    assert_file_contains(
        "docs/pr-template.md",
        r"##\s+C[oó]mo\s+se\s+ha\s+probado",
        "Expected docs/pr-template.md to include Cómo se ha probado",
    )
    assert_file_contains(
        "docs/pr-template.md",
        r"##\s+Riesgos",
        "Expected docs/pr-template.md to include Riesgos",
    )
    count = commit_count_since_base()
    if count != 1:
        fail(f"Expected PR template branch to end as 1 commit over main, found {count}")
    ok("PR template branch contains exactly one commit over main")
    assert_max_changed_files(3)


def validate_review_cleanup() -> None:
    assert_file_exists("docs/review-workflow.md")
    assert_file_contains(
        "docs/review-workflow.md",
        r"funcional",
        "Expected review workflow to mention functional feedback",
    )
    assert_file_contains(
        "docs/review-workflow.md",
        r"naming",
        "Expected review workflow to mention naming feedback",
    )
    assert_file_contains(
        "docs/review-workflow.md",
        r"diseñ|disen",
        "Expected review workflow to mention design feedback",
    )
    assert_file_contains(
        "docs/review-workflow.md",
        r"pytest\s+-q",
        "Expected review workflow to mention pytest -q",
    )
    assert_file_contains(
        "docs/review-workflow.md",
        r"validate\.py",
        "Expected review workflow to mention validate.py",
    )
    assert_file_contains(
        "docs/review-workflow.md",
        r"range-diff",
        "Expected review workflow to mention git range-diff",
    )
    assert_no_text(
        "docs/review-workflow.md",
        r"(^|\n)##\s+Notes\b",
        "docs/review-workflow.md must not keep the old Notes heading",
    )
    count = commit_count_since_base()
    if count != 1:
        fail(f"Expected review cleanup branch to end as 1 commit over main, found {count}")
    ok("Review cleanup branch contains exactly one commit over main")
    assert_commit_messages_absent(r"address review comments", "No Address review comments commit remains")
    assert_max_changed_files(3)


def validate_tax() -> None:
    assert_function("app/calculator.py", "calculate_tax")
    assert_test_function("test_calculate_tax", "calculate_tax")
    assert_python_result("calculate_tax(100, 0.21)", "21.0")
    base = first_existing_base()
    if ref_function_has_explicit_raise(base, "app/calculator.py", "subtract", "ValueError"):
        assert_python_raises("subtract(None, 3)", "ValueError")
        assert_tests_match(
            r"subtract\s*\(\s*None\s*,\s*3\s*\)",
            "Expected tax branch to preserve the subtract None hotfix from its base",
        )
    assert_no_merge_commits_since_base("Tax feature branch was updated without merge commits")


def validate_calculator_names() -> None:
    assert_function("app/calculator.py", "add")
    assert_function("app/calculator.py", "subtract")
    assert_function("app/calculator.py", "calculate_tax")
    assert_function_args("app/calculator.py", "add", ["left", "right"])
    assert_function_args("app/calculator.py", "subtract", ["left", "right"])
    assert_python_result("add(2, 3)", "5")
    assert_python_result("add('2', '3')", "5")
    assert_python_raises("add(None, 3)", "ValueError")
    assert_python_result("subtract(5, 3)", "2")
    assert_python_raises("subtract(None, 3)", "ValueError")
    assert_python_result("calculate_tax(100, 0.21)", "21.0")
    assert_test_function("test_calculate_tax", "calculate_tax")
    assert_tests_match(
        r"subtract\s*\(\s*None\s*,\s*3\s*\)",
        "Expected tests to cover subtract rejecting None",
    )
    assert_no_merge_commits_since_base("Calculator names branch was updated without merge commits")


def validate_final_incident() -> None:
    assert_annotated_tag(release_tag("v1.0.0"))
    assert_file_absent("release-blocker.txt")
    count = commit_count_since_base()
    if count < 2:
        fail(f"Expected final incident branch to contain at least 2 commits over main, found {count}")
    ok("Final incident branch contains at least two commits over main")
    messages = commit_messages_since_base()
    if not any(re.search(r"\brevert\b", message, re.IGNORECASE) for message in messages):
        fail(f"Expected at least one revert commit message, found: {messages}")
    ok("Revert commit message found")


def validate_factorial_regression() -> None:
    assert_function("app/calculator.py", "factorial")
    assert_python_result("factorial(0)", "1")
    assert_python_result("factorial(5)", "120")
    assert_python_raises("factorial(-1)", "ValueError")
    assert_tests_match(r"factorial\s*\(\s*0\s*\)", "Expected tests to cover factorial(0)")
    assert_tests_match(r"factorial\s*\(\s*5\s*\)", "Expected tests to cover factorial(5)")
    assert_tests_match(r"factorial\s*\(\s*-1\s*\)", "Expected tests to cover factorial(-1)")
    assert_file_exists("docs/bisect-report.md")
    assert_file_contains("docs/bisect-report.md", r"git\s+blame", "Expected bisect report to mention git blame")
    assert_file_contains("docs/bisect-report.md", r"git\s+log\s+-S", "Expected bisect report to mention git log -S")
    assert_file_contains("docs/bisect-report.md", r"git\s+log\s+-G", "Expected bisect report to mention git log -G")
    assert_file_contains("docs/bisect-report.md", r"git\s+bisect", "Expected bisect report to mention git bisect")
    assert_file_contains("docs/bisect-report.md", r"factorial\s*\(\s*0\s*\)", "Expected bisect report to mention factorial(0)")
    assert_file_contains(
        "docs/bisect-report.md",
        r"([0-9a-f]{7,40}|refactor|simplify|culpable)",
        "Expected bisect report to identify the culprit commit",
    )
    assert_file_contains(
        "docs/bisect-report.md",
        r"fix\s+forward|forward",
        "Expected bisect report to explain the fix forward decision",
    )
    count = commit_count_since_base()
    if count < 5:
        fail(f"Expected factorial bisect branch to preserve at least 5 commits over main, found {count}")
    ok("Factorial bisect branch preserves enough history for diagnosis")
    merge_count = merge_commit_count_since_base()
    if merge_count < 1:
        fail("Expected factorial bisect branch to contain at least one merge commit")
    ok("Factorial bisect branch contains a merge commit")


def validate_backport_factorial() -> None:
    assert_function("app/calculator.py", "factorial")
    assert_python_result("factorial(0)", "1")
    assert_python_result("factorial(5)", "120")
    assert_python_raises("factorial(-1)", "ValueError")
    assert_python_raises("factorial(2.5)", "TypeError")
    assert_tests_match(r"factorial\s*\(\s*2\.5\s*\)", "Expected tests to cover factorial rejecting non-integers")
    assert_file_exists("docs/worktree-notes.md")
    assert_file_contains("docs/worktree-notes.md", r"git\s+worktree\s+add", "Expected worktree notes to mention git worktree add")
    assert_file_contains("docs/worktree-notes.md", r"git\s+worktree\s+list", "Expected worktree notes to mention git worktree list")
    assert_file_contains("docs/worktree-notes.md", r"git\s+worktree\s+remove", "Expected worktree notes to mention git worktree remove")
    assert_file_contains("docs/worktree-notes.md", r"cherry-pick\s+-x", "Expected worktree notes to mention git cherry-pick -x")
    messages = commit_bodies_since_base()
    if "cherry picked from commit" not in messages.lower():
        fail(f"Expected a cherry-pick -x commit message, found: {messages}")
    ok("Cherry-pick -x commit message found")


def validate_revert_merge_demo() -> None:
    assert_function_absent("app/calculator.py", "experimental_discount")
    merge_count = merge_commit_count_since_base()
    if merge_count < 1:
        fail("Expected revert merge demo branch to contain at least one merge commit")
    ok("Revert merge demo branch contains a merge commit")
    messages = commit_messages_since_base()
    if not any(re.search(r"\brevert\b", message, re.IGNORECASE) for message in messages):
        fail(f"Expected at least one revert commit message, found: {messages}")
    ok("Revert commit message found")
    assert_file_exists("docs/merge-revert.md")
    assert_file_contains("docs/merge-revert.md", r"git\s+merge\s+--no-ff", "Expected merge revert notes to mention git merge --no-ff")
    assert_file_contains("docs/merge-revert.md", r"git\s+revert\s+-m\s+1", "Expected merge revert notes to mention git revert -m 1")
    assert_file_contains("docs/merge-revert.md", r"primer\s+padre", "Expected merge revert notes to explain the first parent")


def validate_personal_main_release_if_present(branch: str) -> bool:
    if not branch.startswith("main-") or not has_final_release_shape():
        return False

    suffix = branch.removeprefix("main-")
    validate_calculator_names()
    assert_annotated_tag(f"v1.0.0-{suffix}")

    messages = commit_messages_for_ref("HEAD")
    incident_branch = f"chore/final-incident-{suffix}"
    incident_was_merged = (
        any(re.search(r"release marker|release-blocker", message, re.IGNORECASE) for message in messages)
        or ref_exists(incident_branch)
        or ref_exists(f"origin/{incident_branch}")
        or ref_exists(f"refs/tags/v1.0.1-{suffix}")
    )
    if incident_was_merged:
        assert_file_absent("release-blocker.txt")
        assert_annotated_tag(f"v1.0.1-{suffix}")

    ok("Personal main release checks passed")
    return True


EXERCISE_VALIDATORS = {
    "feature/multiply": validate_multiply,
    "feature/exponentiation": validate_exponentiation,
    "feature/divide-operation": validate_divide,
    "feature/modulus-operation": validate_modulus,
    "hotfix/division-by-zero": validate_division_by_zero,
    "hotfix/subtract-none-validation": validate_subtract_none_validation,
    "feature/add-cast-int": validate_add_cast_int,
    "feature/add-none-validation": validate_add_none_validation,
    "feature/clean-history": validate_clean_history,
    "feature/squash-demo": validate_squash_demo,
    "feature/fixup-demo": validate_fixup_demo,
    "feature/recovery-sandbox": validate_recovery_sandbox,
    "rescue/reflog": validate_reflog_rescue,
    "chore/revert-demo": validate_revert_demo,
    "feature/pr-template": validate_pr_template,
    "feature/review-cleanup": validate_review_cleanup,
    "feature/tax-calculation": validate_tax,
    "refactor/calculator-names": validate_calculator_names,
    "chore/final-incident": validate_final_incident,
    "hotfix/factorial-regression": validate_factorial_regression,
    "hotfix/backport-factorial": validate_backport_factorial,
    "chore/revert-merge-demo": validate_revert_merge_demo,
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
        if validate_personal_main_release_if_present(branch):
            print("🎉 Final release validation passed")
            return 0
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
