import os
def delete_all_file(path):
    "delete all folers and files"
    if os.path.isfile(path):
        try:
            os.remove(path)
        except:
            pass
    elif os.path.isdir(path):
        for item in os.listdir(path):
            itemsrc = os.path.join(path, item)
            delete_all_file(itemsrc)
        try:
            os.rmdir(path)
        except:
            pass