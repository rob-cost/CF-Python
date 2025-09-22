
class ShoppingList(object):
    def __init__(self, list_name):
        self.list_name = list_name
        self.shopping_list = []

    def add_item(self, item):
        if not item in self.shopping_list:
            self.shopping_list.append(item)

    def remove_item(self, item):
        for i in self.shopping_list:
            if i == item:
                self.shopping_list.remove(item)

    def view_list(self):
        print("Items in " + str(self.list_name) + "\n" + 30*"-")
        for item in self.shopping_list:
            print(" - " + str(item))

    def merge_list(self, obj):
        merged_lists_name = "Merged list between: " + str(self.list_name) + " and " + str(obj.list_name)

        merged_list_object = ShoppingList(merged_lists_name)

        merged_list_object.shopping_list = self.shopping_list.copy()


pet_store_list = ShoppingList("Pet Store Shopping List")


pet_store_list.add_item("dog food")
pet_store_list.add_item("frisbee")
pet_store_list.add_item("bowl")
pet_store_list.add_item("collars")
pet_store_list.add_item("flea collars")

pet_store_list.view_list()

pet_store_list.remove_item("flea collars")
pet_store_list.view_list()

pet_store_list.add_item("frisbee")
pet_store_list.view_list()

