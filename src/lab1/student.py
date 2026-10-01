
class Student:
    name: str | None
    id: int
    group: int | None
    marks: list[int | None]

    def __init__(self, name: str | None, id: int, group: int | None, marks: list[int | None]) -> None:
        self.name = name
        self.id = id
        self.group = group
        self.marks = marks

    def mean_mark(self) -> float:
        result: float = 0
        cnt: int = 0
        for mark in self.marks:
            if mark is not None:
                result += mark
                cnt += 1
        return result / (1 if cnt == 0 else cnt)
        