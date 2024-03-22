from generic_helper import filesystem_helper
from generic_helper import config_helper


if __name__== "__main__":
    collection_name:int =config_helper.get_config_value ("COLLECTION", "name")
    collection_name_list:list[str] = collection_name.split(",")
    collection_name_list = [i for i in collection_name_list if i]
    print (collection_name_list)
    # if (collection_name is None) or  (NAME_COLLECTION not in collection_name):
    #     collection_name = f"{NAME_COLLECTION},{collection_name} "
    #     config_helper.write_config("COLLECTION", "name", collection_name)