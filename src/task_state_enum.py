import enum


class TaskStateEnum(enum.Enum):
    DRAFT = "DRAFT"  # черновик
    WORKS = "WORKS"  # в работе
    COMPLETED = "COMPLETED"  # Завершена
