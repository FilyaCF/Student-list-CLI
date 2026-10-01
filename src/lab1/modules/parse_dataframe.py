from student import Student
import pandas as pd

def parse_dataframe_to_students(df: pd.DataFrame) -> list[Student]:
    students = []
    for (idx, row) in df.iterrows():
        students.append(parse_row_to_student(row))
    return students

def parse_row_to_student(row: pd.Series) -> Student:
    name = row['name']
    id = row['id']
    marks = []
    for i in range(len(row) - 2):
        marks.append(row.iloc[i + 2])
    return Student(name, id, marks)