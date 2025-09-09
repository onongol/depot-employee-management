from decimal import Decimal

# Department list
DEPARTMENTS = [
    'Механик', 
    'Авто хяналтын бүс (АКП)', 
    'Засвар 1', 
    'Засвар 2', 
    'Хос дугуй', 
    'Тэргэнцэр', 
    'Авто угсраа'
]

# Choices for Django model fields
DEPARTMENT_CHOICES = [
    ('Механик', 'Механик'),
    ('Авто хяналтын бүс (АКП)', 'Авто хяналтын бүс (АКП)'),
    ('Засвар 1', 'Засвар 1'),
    ('Засвар 2', 'Засвар 2'),
    ('Хос дугуй', 'Хос дугуй'),
    ('Тэргэнцэр', 'Тэргэнцэр'),
    ('Авто угсраа', 'Авто угсраа'),
]

# Rank choices for employees
RANK_CHOICES = [
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
]

# Mapping of rank to corresponding monetary values
RANK_TO_MONEY = {
    3: Decimal('8448.55'),
    4: Decimal('9616.24'),
    5: Decimal('11127.36'),
    6: Decimal('13187.98'),
}

# Work type choices
TYPE_WORK_CHOICES = [
    ('84', '84'),
    ('29', '29'),
    ('ТҮГ', 'ТҮГ'),
    ('Нөөц', 'Нөөц'),
    ('Завод', 'Завод'),
    ('Депо', 'Депо'),
]
