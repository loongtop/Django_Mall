from crud import products
from crud import get_handler


# Create your views here.

class Read(products.Read):
    pass


class Delete(products.Delete):
    pass


class Update(products.Update):
    pass


class Create(products.Create):
    pass


handler_dict = get_handler(read=Read)
