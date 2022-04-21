from crud import get_handler
from crud.factory.products import Read as CRUDRead


# Create your views here.

class Read(CRUDRead):

    display_list = [CRUDRead.checkbox, 'name', 'email', CRUDRead.update, CRUDRead.delete]


#########################
handler_dict = get_handler(read=Read)
