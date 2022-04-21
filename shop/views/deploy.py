from crud import products, get_handler


# Create your views here.

class Read(products.Read):
    pass


handler_dict = get_handler(read=Read)
