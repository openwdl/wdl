#!/usr/bin/env python3
from argparse import ArgumentParser
from collections import defaultdict
from enum import Enum
import json
import os
from pathlib import Path
import shutil
import subby
from typing import Optional


class Result(Enum):
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"
    INVALID = "invalid"
    IGNORE = "ignore"


def resolve_miniwdl(path: Optional[Path]) -> Path:
    if path is None:
        path = Path(shutil.which("miniwdl"))
    if path is None:
        raise Exception("Cannot find miniwdl on system path")
    if not path.exists():
        raise Exception(f"Executable does not exist: {path}")
    if not os.access(path, os.X_OK):
        raise Exception(f"Path is not executable: {path}")
    return path


def check(
    config: dict,
    miniwdl_path: Path,
    test_dir: Path,
    strict: bool,
    no_warn: bool,
    deprecated_optional: bool,
) -> Result:
    command = [str(miniwdl_path), "check"]
    if strict:
        command.append("--strict")
    command.append(str(config["path"]))
    p = subby.cmd(command, shell=True, cwd=test_dir, raise_on_error=False)
    if p.returncode == 0:
        return Result.PASS
    elif config["priority"] == "ignore":
        return Result.IGNORE
    elif config["fail"] and no_warn:
        return Result.WARN
    elif deprecated_optional and "deprecated" in config["tags"]:
        return Result.WARN
    else:
        fail = config["fail"]
        title = f"{config['path']}: {'WARNING' if fail else 'ERROR'}"
        print(title)
        print("-" * len(title))
        print(p.output or p.error)
        print()
        return Result.WARN if fail else Result.FAIL


def run_test(
    config: dict,
    miniwdl_path: Path,
    test_dir: Path,
    data_dir: Path,
    output_dir: Optional[Path],
    no_warn: bool,
    deprecated_optional: bool,
) -> Result:
    if config["priority"] == "ignore":
        return Result.IGNORE

    input_json = json.dumps(config["input"])
    command = [miniwdl_path, "run", "-p", test_dir, "-i", input_json]
    if output_dir is not None:
        command.extend(["-d", str(output_dir)])
    if config["type"] == "task":
        command.extend(["--task", str(config["target"])])
    command.append(str(config["path"]))
    p = subby.cmd(command, shell=True, cwd=data_dir)
    output = json.loads(p.output)

    fail = False
    if p.returncode == 0:
        fail = config["fail"]
    elif config["fail"]:
        if config["return_code"] == "*":
            pass
        else:
            rc = config["return_code"]
            if isinstance(rc, int):
                rc = [rc]
            if not p.returncode in rc:
                fail = True
    else:
        fail = True

    invalid = []
    if not fail:
        for key, value in output.items():
            if key not in config["exclude_output"]:
                if key not in config["output"]:
                    invalid.append((key, value, None))
                elif config["output"][key] != value:
                    invalid.append((key, value, config["output"][key]))

    if fail or invalid:
        warn = config["priority"] == "optional"
        if warn and no_warn:
            return Result.WARN

        title = f"{config['path']}: {'WARNING' if warn else 'ERROR'}"
        print(title)
        print("-" * len(title))
        print(f"Return code:")
        if fail:
            print(json.dumps(output))
        else:
            print("Invalid output(s):")
            for key, expected, actual in invalid:
                print(f"  {key}: {expected} != {actual}")

        if warn:
            return Result.WARN
        elif fail:
            return Result.FAIL
        else:
            return Result.INVALID
    else:
        return Result.PASS


def main():
    parser = ArgumentParser()
    parser.add_argument("-T", "--test-dir", type=Path, default=Path("."))
    parser.add_argument("-c", "--test-config", type=Path, default=None)
    parser.add_argument("-D", "--data-dir", type=Path, default=None)
    parser.add_argument("-O", "--output-dir", type=Path, default=None)
    parser.add_argument("-n", "--num-tests", type=int, default=None)
    parser.add_argument("--miniwdl-path", type=Path, default=None)
    parser.add_argument("--check-only", action="store_true", default=False)
    parser.add_argument("--strict", action="store_true", default=False)
    parser.add_argument("--no-warn", action="store_true", default=False)
    parser.add_argument("--deprecated-optional", action="store_true", default=False)
    args = parser.parse_args()

    miniwdl_path = resolve_miniwdl(args.miniwdl_path)
    test_dir = args.test_dir
    data_dir = args.data_dir or test_dir / "data"
    test_config = args.test_config or test_dir / "test_config.json"
    with open(test_config, "r") as i:
        configs = json.load(i)
    if args.num_tests is not None:
        configs = configs[: args.num_tests]
    results = defaultdict(int)
    for config in configs:
        if args.check_only:
            result = check(
                config,
                miniwdl_path,
                test_dir,
                args.strict,
                args.no_warn,
                args.deprecated_optional,
            )
            results[result] += 1
        else:
            result = run_test(
                config,
                miniwdl_path,
                test_dir,
                data_dir,
                args.output_dir,
                args.no_warn,
                args.deprecated_optional,
            )
            results[result] += 1

    print(f"Total tests: {sum(results.values())}")
    print(f"Passed: {results.get(Result.PASS, 0)}")
    print(f"Warnings: {results.get(Result.WARN, 0)}")
    print(f"Failures: {results.get(Result.FAIL, 0)}")
    print(f"Invalid outputs: {results.get(Result.INVALID, 0)}")
    print(f"Ignored: {results.get(Result.IGNORE, 0)}")


if __name__ == "__main__":
    main()
