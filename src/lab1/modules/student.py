
class Student:
    name: str
    id: int
    marks: list[int]

    def __init__(self, name, id, marks) -> None:
        self.name = name
        self.id = id