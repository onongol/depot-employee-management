DEPARTMENTS = [
    'Механик', 
    'Авто хяналтын бүс (АКП)', 
    'Засвар 1', 
    'Засвар 2', 
    'Хос дугуй', 
    'Тэргэнцэр', 
    'Автоугсраа'
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
