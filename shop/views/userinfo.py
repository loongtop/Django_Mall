from crud import get_handler, Operation
from crud.factory.products import Read as CRUDRead


# Create your views here.

class Read(CRUDRead):

    display_list = [Operation.checkbox, 'name', 'email', Operation.delete]


#########################
handler_dict = get_handler(read=Read)
