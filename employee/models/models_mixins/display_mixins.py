from employee.constants.constants import (DEFAULT_MATERIAL_TYPE, 
                                          DEFAULT_WAGON_NUMBER,
                                          DEFAULT_WAGON_TYPE)


class TypeMaterialDisplayMixin:
    @property
    def type_material_display(self):
        return self.type_material or DEFAULT_MATERIAL_TYPE


class WagonNumberDisplayMixin:
    @property
    def wagon_number_display(self):
        return DEFAULT_WAGON_NUMBER if not self.wagon_number else self.wagon_number

    
class TypeWagonDisplayMixin:
    @property
    def type_wagon_display(self):
        return self.type_wagon or DEFAULT_WAGON_TYPE
