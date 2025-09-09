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

# Mapping of rank to corresponding monetary values
RANK_TO_MONEY = {
    Rank.THREE.value: Decimal('8448.55'),
    Rank.FOUR.value: Decimal('9616.24'),
    Rank.FIVE.value: Decimal('11127.36'),
    Rank.SIX.value: Decimal('13187.98'),
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