from enum import Enum, IntEnum
from types import MappingProxyType


# Group names
class GroupNames(str, Enum):
    PAYROLLS = "Payrolls"
    MASTERS = "Masters"
    EMPLOYEES = "Employees"


# Department list
class Department(str, Enum):
    AUTO_UGSRAA = "Авто угсраа"
    AKP = "Авто хяналтын бүс (АКП)"
    ZASVAR_1 = "Засвар 1"
    ZASVAR_2 = "Засвар 2"
    MECHANIC = "Механик"
    TERGENTSER = "Тэргэнцэр"
    HOS_DUGUI = "Хос дугуй"


DEPARTMENTS = [dept.value for dept in Department]

# Choices for Django model fields
DEPARTMENT_CHOICES = [(dept.value, dept.value) for dept in Department]


# Rank choices for employees
class Rank(IntEnum):
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6


# Choices for Django model fields
RANK_CHOICES = [(rank.value, rank.value) for rank in Rank]


# Type work list
class TypeWork(str, Enum):
    TYPE_84 = "84"
    TYPE_29 = "29"
    TYPE_79 = "79"
    TYPE_03 = "03"
    TUG = "ТҮГ"
    NOOTS = "Нөөц"
    DEPO = "Бүтээгдэхүүн"


# Type work choices
TYPE_WORK_CHOICES = tuple((work_type.value, work_type.value) for work_type in TypeWork)

# Grouped type works by department
TYPE_WORKS_MECHANIC = [TypeWork.DEPO.value]

# АКП, Тэргэнцэр, Авто угсраа
TYPE_WORKS_FULL = [
    TypeWork.TYPE_84.value,
    TypeWork.TYPE_29.value,
    TypeWork.TYPE_79.value,
    TypeWork.TYPE_03.value,
    TypeWork.TUG.value,
    TypeWork.NOOTS.value,
]

# Засвар 1, Засвар 2
TYPE_WORKS_ZASVAR = [
    TypeWork.TYPE_84.value,
    TypeWork.TYPE_29.value,
    TypeWork.TYPE_79.value,
    TypeWork.TYPE_03.value,
]
TYPE_WORKS_HOS_DUGUI = [TypeWork.TYPE_84.value, TypeWork.TYPE_29.value]

# Mapping of departments to their respective type works
_DEPT_TYPE_WORKS_GROUPS = {
    (Department.MECHANIC.value,): TYPE_WORKS_MECHANIC,
    (
        Department.AKP.value,
        Department.TERGENTSER.value,
        Department.AUTO_UGSRAA.value,
    ): TYPE_WORKS_FULL,
    (Department.ZASVAR_1.value, Department.ZASVAR_2.value): TYPE_WORKS_ZASVAR,
    (Department.HOS_DUGUI.value,): TYPE_WORKS_HOS_DUGUI,
}

DEPARTMENT_TYPE_WORKS = MappingProxyType(
    {
        dept: values
        for group, values in _DEPT_TYPE_WORKS_GROUPS.items()
        for dept in group
    }
)


def get_type_work_choices(department: str | None):
    """
    Return choices list for type_work limited by department; fallback to all.
    """
    values = DEPARTMENT_TYPE_WORKS.get(department)
    if not values:
        return TYPE_WORK_CHOICES
    return tuple((v, v) for v in values)


# Default wagon number, only UI display value
DEFAULT_WAGON_NUMBER = "-"

# Default material type, only UI display value
DEFAULT_MATERIAL_TYPE = "-"


# Position list
class JobTitle(str, Enum):
    TOKARCHIN = "Токарьчин"
    BELTGELEL_TOKARCHIN = "Бэлтгэл токарьчин"
    DARHAN_LANTUUCHIN = "Дархан лантуучин"
    GAGNUURCHIN = "Гагнуурчин"
    ZASVARCHIN = "Засварчин"
    BUDAGCHIN = "Будагчин"
    NEELKHI = "Нээлхий"


JOB_TITLES = [title.value for title in JobTitle]

JOB_TITLE_CHOICES = tuple((title.value, title.value) for title in JobTitle)

# Grouped job titles by department
# Механик
JOB_TITLES_MECHANIC = [
    JobTitle.TOKARCHIN.value,
    JobTitle.BELTGELEL_TOKARCHIN.value,
    JobTitle.DARHAN_LANTUUCHIN.value,
    JobTitle.GAGNUURCHIN.value,
]
# АКП
JOB_TITLES_SINGLE_ZASVARCHIN = [JobTitle.ZASVARCHIN.value]
# Хос дугуй
JOB_TITLES_HOS_DUGUI = [
    JobTitle.TOKARCHIN.value,
    JobTitle.ZASVARCHIN.value,
]
# Засвар 1,2
JOB_TITLES_ZASVAR = [
    JobTitle.ZASVARCHIN.value,
    JobTitle.GAGNUURCHIN.value,
    JobTitle.BUDAGCHIN.value,
    JobTitle.NEELKHI.value,
]
# Тэргэнцэр, Авто угсраа
JOB_TITLES_ZASV_GAGNUUR = [
    JobTitle.ZASVARCHIN.value,
    JobTitle.GAGNUURCHIN.value,
]

# Mapping of departments to their respective job titles
_DEPT_JOB_TITLE_GROUPS = {
    (Department.MECHANIC.value,): JOB_TITLES_MECHANIC,
    (Department.AKP.value,): JOB_TITLES_SINGLE_ZASVARCHIN,
    (Department.HOS_DUGUI.value,): JOB_TITLES_HOS_DUGUI,
    (Department.ZASVAR_1.value, Department.ZASVAR_2.value): JOB_TITLES_ZASVAR,
    (
        Department.TERGENTSER.value,
        Department.AUTO_UGSRAA.value,
    ): JOB_TITLES_ZASV_GAGNUUR,
}

DEPARTMENT_JOB_TITLES = MappingProxyType(
    {dept: values for group, values in _DEPT_JOB_TITLE_GROUPS.items() for dept in group}
)


def get_job_title_choices(department: str | None):
    """Return choices list for JobTitle limited by department; fallback to all."""
    values = DEPARTMENT_JOB_TITLES.get(department, JOB_TITLES)
    return tuple((v, v) for v in values)


# Type wagon
class TypeWagon(str, Enum):
    HAGAS = "Хагас-84"
    CHINGELG = "Чингэлэг"
    TAVTSANT = "Тавцант"
    BITUU = "Битүү"
    HOPPER_DOSATOR = "Хоппер-Дозатор"
    DUMPCAR = "Думпкар"
    CISTERNA = "Цистерн"
    TUSGAI_HEREGTSIIN = "Тусгай хэрэгцээний"
    ICH_ZASVAR = "Их засвар"
    URSGAL = "Урсгал"


TYPE_WAGONS = [wagon.value for wagon in TypeWagon]

TYPE_WAGON_CHOICES = [(wagon.value, wagon.value) for wagon in TypeWagon]

ALLOWED_WAGON_DEPARTMENTS = (Department.ZASVAR_1.value, Department.ZASVAR_2.value)

MECHANIC = Department.MECHANIC.value

# Default type wagon, only UI display value
DEFAULT_WAGON_TYPE = "-"

# Default select choice, only UI display value
EMPTY_SELECT = [("", "---------")]

# Grouping constants
GROUP_DEFAULT = ""
GROUP_MONTH = "month"
GROUP_YEAR = "year"
GROUP_WAGON = "wagon"
