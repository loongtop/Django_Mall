from crud import products
from crud import get_handler
from crud import Operation


# Create your views here.

class Read(products.Read):

    display_list = [Operation.checkbox, 'first_name', 'phone', 'gender', Operation.update, Operation.delete]


class Delete(products.Delete):
    pass


class Update(products.Update):
    pass


class Create(products.Create):
    pass


handler_dict = get_handler(Create, Read, Update, Delete)