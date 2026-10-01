from math import nan

from lab1.student import Student
import pandas as pd
import numpy as np

def parse_dataframe_to_students(df: pd.DataFrame) -> list[Student]:
    """Convert a DataFrame into a list of Student objects.

    Each row of the DataFrame is parsed into one Student.

    Args:
        df: The DataFrame to parse. Must contain the columns 'name' and 'id'
            as the first two columns, followed by columns with marks.

    Returns:
        A list of Student objects, one per row, in the original row order.

    Raises:
        TypeError: If any row contains a mark that is not an integer.
    """
    students = []
    for (_, row) in df.iterrows():
        students.append(parse_series_to_student(row))
    return students

def parse_series_to_student(row: pd.Series) -> Student:
    """Convert a single DataFrame row into a Student object.

    The first two values of the row are expected to be 'name' and 'id'
    (accessed by label); all remaining values are treated as marks.

    Args:
        row: A row with 'name' and 'id' as its first two entries, followed
            by the student's marks.

    Returns:
        A Student built from the row's name, id and list of marks.

    Raises:
        TypeError: If any mark is not an integer.
    """
    name = row['name']
    id = row['id']
    group = row['group']
    marks = []
    for i in range(len(row) - 3):
        mark: int | None = row.iloc[i + 3]
        if pd.isna(mark):
            marks.append(None)
            continue
        if not isinstance(mark, (int, np.integer)):
            raise TypeError(
                f'Wrong data format in csv file: Expected number, '
                f'between 0 and 10 or None, found {row.iloc[i + 3]}'
            )
        marks.append(row.iloc[i + 3])
    return Student(name, id, group, marks)

def parse_student_to_series(student: Student, marks_count: int | None = None) -> pd.Series:
    """Convert a Student into a Series: id, name, group, mark_1, mark_2, ...

    Args:
        student: The Student to convert.
        marks_count: Number of mark columns. Missing marks are padded with
            None. Defaults to the length of the student's own marks.
    """
    marks = list(student.marks or [])
    n = len(marks) if marks_count is None else marks_count
    marks += [None] * (n - len(marks))

    index = ['id', 'name', 'group'] + [f'mark_{i}' for i in range(1, n + 1)]
    return pd.Series([student.id, student.name, student.group, *marks],
                     index=index, dtype=object)


def parse_students_to_dataframe(students: list[Student]) -> pd.DataFrame:
    """Convert students into a DataFrame sorted by id.

    The number of mark columns is the maximum number of marks among all
    students; shorter lists are padded with None. The columns id, group and
    mark_N use the nullable dtype 'Int64', so missing values are <NA> and
    numbers stay integers. Students with id=None go last.
    """
    if not students:
        return pd.DataFrame(columns=['id', 'name', 'group'])

    marks_count = max(len(s.marks or []) for s in students)
    ordered = sorted(students, key=lambda s: (s.id is None, s.id or 0))

    df = pd.DataFrame([parse_student_to_series(s, marks_count) for s in ordered])
    df = df.reset_index(drop=True)

    int_columns = ['id', 'group'] + [f'mark_{i}' for i in range(1, marks_count + 1)]
    df[int_columns] = df[int_columns].astype('Int64')
    return df
