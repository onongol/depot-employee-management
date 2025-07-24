DEPARTMENTS = [
    'Механик', 
    'Авто хяналтын бүс (АКП)', 
    'Засвар 1', 
    'Засвар 2', 
    'Хос дугуй', 
    'Тэргэнцэр', 
    'Авто угсраа'
]


def global_departments(request):
    """Context processor to provide a list of distinct departments."""
    departments_list = DEPARTMENTS

    # Ensure the list is not empty
    if not departments_list:
        departments_list = ['No departments available']
    
    return {
        'departments': departments_list,
        'request': request,
        }


def is_employee(request):
    """Context processor to check if the user is an employee."""
    return {
        'is_employee': request.user.is_authenticated and request.user.groups.filter(name='Employees').exists()
    }


def is_master(request):
    """Context processor to check if the user is a master."""
    return {
        'is_master': request.user.is_authenticated and request.user.groups.filter(name='master').exists()
    }
