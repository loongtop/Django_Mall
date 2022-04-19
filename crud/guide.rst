"""

1. Copy the crud component to the root directory of the project


2.在工程主目录增加*_crud,文件， 内容如下：
    userinfo_handler_dict = {
    'read': userinfo.Read,
    'update': userinfo.Update,
    'create': userinfo.Create,
    'delete': userinfo.Delete}


    factory = get_create_factory(app_name='CRUD', namespace='Shop')


    factory.register((UserInfo, userinfo_handler_dict),
                 (Host, host_handler_dict),
                 (Department, department_handler_dict),)


    def get_shop_urls():
        return [re_path('', factory.urls)]


3. 增加views内容
    class Read(products.Read):
        pass


    class Delete(products.Delete):
        pass


    class Update(products.Update):
        pass


    class Create(products.Create):
        pass


4. 修改urls文件，在文件中增加
    ～from *.*_crud import get_*_urls
    ～path('', include(get_*_urls())),



