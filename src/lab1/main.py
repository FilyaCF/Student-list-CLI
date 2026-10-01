import argparse
import ast
import re
import sys
from pathlib import Path
from typing import Any, Callable

from lab1.utils.csv_io import load_from_csv, save_to_csv
from lab1.utils.converters import parse_dataframe_to_students, parse_students_to_dataframe
from lab1.student import Student
from lab1.cmd.parsing import parse_bool, parse_params, parse_optional, parse_marks
from lab1.cmd import commands as cm

DEFAULT_FILE = "students.csv"

COMMANDS: list[str] = [
    "add",
    "list",
    "average",
    "remove",
    "update"
]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Manage students stored in a CSV file.",
        epilog="Examples:\n"
               '  app.py add name="Anna" marks="[10, None, 8]"\n'
               "  app.py remove id=3\n"
               "  app.py list",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("command", choices=COMMANDS, help="command to run")
    parser.add_argument("args", nargs="*", help="command arguments as key=value")
    parser.add_argument("-f", "--file", type=Path, default=DEFAULT_FILE,
                        help=f"CSV storage file (default: {DEFAULT_FILE})")
    ns = parser.parse_args()

    try:
        raw = parse_params(ns.args)
        students = (
            parse_dataframe_to_students(load_from_csv(ns.file))
            if ns.file.is_file() else []
        )

        if ns.command == "list":
            unknown = raw.keys() - {"count", "group", "sort"}
            if unknown:
                raise ValueError(f"'list' does not accept: {', '.join(sorted(unknown))}")

            count = int(raw["count"]) if "count" in raw else len(students)
            group = int(raw["group"]) if "group" in raw else None
            sort = parse_bool(raw["sort"]) if "sort" in raw else False

            cm.cmd_list(students, cnt=count, group=group, is_sorted=sort)
        elif ns.command == "add":
            unknown = raw.keys() - {"name", "group", "marks"}
            if unknown:
                raise ValueError(f"'add' does not accept: {', '.join(sorted(unknown))}")

            name = parse_optional(raw["name"], str) if "name" in raw else None
            group = parse_optional(raw["group"], int) if "group" in raw else None
            marks = parse_marks(raw["marks"]) if "marks" in raw else []

            student = cm.cmd_add(students, name=name, group=group, marks=marks)
            save_to_csv(parse_students_to_dataframe(students), ns.file)
            print(f"Added student with id={student.id}")
        elif ns.command == "average":
            unknown = raw.keys() - {"count", "group"}
            if unknown:
                raise ValueError(f"'average' does not accept: {', '.join(sorted(unknown))}")

            count = int(raw["count"]) if "count" in raw else len(students)
            group = int(raw["group"]) if "group" in raw else None

            avg = cm.cmd_average(students, cnt=count, group=group)
            if avg is None:
                print("No marks to average.")
            else:
                print(f"Average: {avg:.2f}")
        elif ns.command == "remove":
            unknown = raw.keys() - {"id"}
            if unknown:
                raise ValueError(f"'remove' does not accept: {', '.join(sorted(unknown))}")

            student_id = int(raw["id"]) if "id" in raw else None

            removed = cm.cmd_remove(students, student_id=student_id)
            save_to_csv(parse_students_to_dataframe(students), ns.file)
            print(f"Removed student id={removed.id} ({removed.name})")
        elif ns.command == "update":
            unknown = raw.keys() - {"id", "name", "group", "marks"}
            if unknown:
                raise ValueError(f"'update' does not accept: {', '.join(sorted(unknown))}")

            student_id = int(raw["id"]) if "id" in raw else None

            fields = {}
            if "name" in raw:
                fields["name"] = parse_optional(raw["name"], str)
            if "group" in raw:
                fields["group"] = parse_optional(raw["group"], int)
            if "marks" in raw:
                fields["marks"] = parse_marks(raw["marks"])
            updated = cm.cmd_update(students, student_id=student_id, **fields)
            save_to_csv(parse_students_to_dataframe(students), ns.file)
            print(f"Updated student id={updated.id}")
            
    except (ValueError, TypeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())