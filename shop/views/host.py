
from crud.factory import products
from crud.common.get_handler_dict import get_handler_dict


# Create your views here.

class Read(products.Read):
    pass


class Delete(products.Delete):
    pass


class Update(products.Update):
    pass


class Create(products.Create):
    pass


handler_dict = get_handler_dict(Create, Read, Update, Delete)