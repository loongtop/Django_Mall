
def get_handler_dict(*args):
    handler_dict = {'create': args[0], 'read': args[1], 'update': args[2], 'delete': args[3]}
    return handler_dict
