import enum


class TaskStateEnum(enum.Enum):
    DRAFT = "DRAFT"  # черновик
    WORKS = "WORKS"  # в работе
    STOPPED = "STOPPED"  # остановлена
    COMPLETED = "COMPLETED"  # Завершена
    TERMINATED = "TERMINATED"  # Прекращена
    IN_ACCEPTANCE = "IN_ACCEPTANCE"  # НА приемке
