from typing import Any
from lab1.student import Student

def cmd_list(
    students: list[Student],
    cnt: int,
    group: int | None = None,
    is_sorted: bool = False,
) -> None:
    if cnt < 0:
        raise ValueError("cnt must be non-negative")

    # 1. фильтр по группе
    rows = [s for s in students if group is None or s.group == group]

    # 2. сортировка по среднему баллу (лучшие первыми, без оценок в конце)
    if is_sorted:
        rows.sort(key=lambda s: (s.mean_mark() is None, -(s.mean_mark() or 0)))

    # 3. ограничение по количеству
    rows = rows[:cnt]

    if not rows:
        print("No students.")
        return

    headers = ["ID", "Name", "Group", "Marks", "Avg"]
    data = []
    for s in rows:
        avg = s.mean_mark()
        data.append([
            str(s.id),
            s.name,
            str(s.group),
            ", ".join("-" if m is None else str(m) for m in s.marks),
            "-" if avg is None else f"{avg:.2f}",
        ])

    widths = [max(len(h), *(len(r[i]) for r in data)) for i, h in enumerate(headers)]

    def fmt(cells: list[str]) -> str:
        return " | ".join(c.ljust(w) for c, w in zip(cells, widths))

    print(fmt(headers))
    print("-+-".join("-" * w for w in widths))
    for r in data:
        print(fmt(r))

def mex(values: set[int], start: int = 1) -> int:
    """Наименьшее целое >= start, которого нет в values."""
    n = start
    while n in values:
        n += 1
    return n


def cmd_add(
    students: list[Student],
    marks: list[int | None],
    name: str | None = None,
    group: int | None = None,
) -> Student:
    used = {s.id for s in students if s.id is not None}
    student = Student(name=name, id=mex(used), group=group, marks=marks)
    students.append(student)
    return student

def cmd_average(
    students: list[Student],
    cnt: int,
    group: int | None = None,
) -> float | None:
    """Средний балл по всем оценкам выбранных студентов.

    Выбор: фильтр по группе (если задана), затем первые cnt студентов.
    Возвращает None, если у выбранных студентов нет ни одной оценки.
    """
    if cnt < 0:
        raise ValueError("cnt must be non-negative")

    rows = [s for s in students if group is None or s.group == group][:cnt]

    marks = [m for s in rows for m in (s.marks or []) if m is not None]
    return sum(marks) / len(marks) if marks else None

def cmd_remove(students: list[Student], student_id: int | None = None) -> Student:
    """Удаляет студента по id и возвращает его.

    Если student_id не задан, удаляется студент с наибольшим id.

    Raises:
        ValueError: если список пуст или студента с таким id нет.
    """
    if student_id is None:
        ids = [s.id for s in students if s.id is not None]
        if not ids:
            raise ValueError("no students to remove")
        student_id = max(ids)

    for i, s in enumerate(students):
        if s.id == student_id:
            return students.pop(i)

    raise ValueError(f"student with id={student_id} not found")

class _Unset:
    def __repr__(self) -> str:
        return "UNSET"

UNSET = _Unset()


def _find_student(students: list[Student], student_id: int | None) -> Student:
    """Студент по id; при student_id=None берётся студент с наибольшим id."""
    if student_id is None:
        ids = [s.id for s in students if s.id is not None]
        if not ids:
            raise ValueError("no students to update")
        student_id = max(ids)

    for s in students:
        if s.id == student_id:
            return s
    raise ValueError(f"student with id={student_id} not found")


def cmd_update(
    students: list[Student],
    student_id: int | None = None,
    name: str | None | _Unset = UNSET,
    group: int | None | _Unset = UNSET,
    marks: list[int | None] | _Unset = UNSET,
) -> Student:
    """Обновляет поля студента с заданным id (по умолчанию с наибольшим).

    Поля, которые не переданы (UNSET), остаются без изменений.
    Переданное None записывается как значение None.
    """
    if name is UNSET and group is UNSET and marks is UNSET:
        raise ValueError("nothing to update: specify name, group or marks")

    student = _find_student(students, student_id)
    if not isinstance(name, _Unset):
        student.name = name
    if not isinstance(group, _Unset):
        student.group = group
    if not isinstance(marks, _Unset):
        student.marks = marks
    return student