from decimal import Decimal
from enum import Enum


# Group names
class GroupNames(str, Enum):
    PAYROLLS = 'Payrolls'
    MASTERS = 'Masters'
    EMPLOYEES = 'Employees'


# Department list
class Department(str, Enum):
    MECHANIC = 'Механик'
    AKP = 'Авто хяналтын бүс (АКП)'
    ZASVAR_1 = 'Засвар 1'
    ZASVAR_2 = 'Засвар 2'
    HOS_DUGUI = 'Хос дугуй'
    TERGENTSER = 'Тэргэнцэр'
    AUTO_UGSRAA = 'Авто угсраа'

DEPARTMENTS = [dept.value for dept in Department]

# Choices for Django model fields
DEPARTMENT_CHOICES = [(dept.value, dept.value) for dept in Department]


# Rank choices for employees
class Rank(Enum):
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6

# Choices for Django model fields
RANK_CHOICES = [(rank.value, rank.value) for rank in Rank]

# Monetary values associated with each rank
class MoneyHourChoices(str, Enum):
    MONEY_THREE = Decimal('9715.83')
    MONEY_FOUR = Decimal('11058.67')
    MONEY_FIVE = Decimal('12796.46')
    MONEY_SIX = Decimal('15166.18')


# Mapping of rank to corresponding monetary values
RANK_TO_MONEY = {
    Rank.THREE.value: MoneyHourChoices.MONEY_THREE.value,
    Rank.FOUR.value: MoneyHourChoices.MONEY_FOUR.value,
    Rank.FIVE.value: MoneyHourChoices.MONEY_FIVE.value,
    Rank.SIX.value: MoneyHourChoices.MONEY_SIX.value,
}


# Type work list
class TypeWork(Enum):
    TYPE_84 = '84'
    TYPE_29 = '29'
    TUG = 'ТҮГ'
    NOOTS = 'Нөөц'
    ZAVOD = 'Завод'
    DEPO = 'Депо'

# Type work choices
TYPE_WORK_CHOICES = [(work_type.value, work_type.value) for work_type in TypeWork]

# Default wagon number
DEFAULT_WAGON_NUMBER = "0"

# Default material type
DEFAULT_MATERIAL_TYPE = "-"


# Position list
class job_title(str, Enum):
    TOKARCHIN = 'Токарьчин'
    BELTGELEL_TOKARCHIN = 'Бэлтгэл токарьчин'
    DARHAN_LANTUUCHIN = 'Дархан лантуучин'
    GAGNUURCHIN = 'Гагнуурчин'
    ZASVARCHIN = 'Засварчин'
    BUDAGCHIN = 'Будагчин'
    NEELKHI = 'Нээлхий'

JOB_TITLES = [title.value for title in job_title]

JOB_TITLE_CHOICES = [(title.value, title.value) for title in job_title]

# Per-department job titles mapping (каждый цех — отдельный ключ)
DEPARTMENT_JOB_TITLES = {
    Department.MECHANIC.value: [
        job_title.TOKARCHIN.value,
        job_title.BELTGELEL_TOKARCHIN.value,
        job_title.DARHAN_LANTUUCHIN.value,
        job_title.GAGNUURCHIN.value,
    ],
    Department.AKP.value: [
        job_title.ZASVARCHIN.value,
    ],
    Department.HOS_DUGUI.value: [
        job_title.ZASVARCHIN.value,
    ],
    Department.ZASVAR_1.value: [
        job_title.ZASVARCHIN.value,
        job_title.GAGNUURCHIN.value,
        job_title.BUDAGCHIN.value,
        job_title.NEELKHI.value,
    ],
    Department.ZASVAR_2.value: [
        job_title.ZASVARCHIN.value,
        job_title.GAGNUURCHIN.value,
        job_title.BUDAGCHIN.value,
        job_title.NEELKHI.value,
    ],
    Department.TERGENTSER.value: [
        job_title.ZASVARCHIN.value,
        job_title.GAGNUURCHIN.value,
    ],
    Department.AUTO_UGSRAA.value: [
        job_title.ZASVARCHIN.value,
        job_title.GAGNUURCHIN.value,
    ],
}

def get_job_title_choices(department: str | None):
    """Return choices list for job_title limited by department; fallback to all."""
    values = DEPARTMENT_JOB_TITLES.get(department, JOB_TITLES)
    return [(v, v) for v in values]


# Type wagon
class TypeWagon(str, Enum):
    HAGAS = 'Хагас-84'
    CHINGELG = 'Чингэлэг'
    TAVTSANT = 'Тавцант'
    BITUU = 'Битүү'
    HOPPER_DOSATOR = 'Хоппер-Дозатор'
    DUMPCAR = 'Думпкар'
    CISTERNA = 'Цистерн'
    TUSGAI_HEREGTSIIN = 'Тусгай хэрэгцээний'
    ICH_ZASVAR = 'Их засвар'
    URSGAL = 'Урсгал' 

TYPE_WAGONS = [wagon.value for wagon in TypeWagon]

TYPE_WAGON_CHOICES = [(wagon.value, wagon.value) for wagon in TypeWagon]
