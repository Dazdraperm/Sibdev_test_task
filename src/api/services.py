from api.models import FileCSV, Customer, PurchaseDate, Item, ItemAndCustomer


def save_objects(data):
    """ Сохранение данных в бд """

    # Сохранение Customer
    try:
        customer = Customer.objects.get(login=data[0])
    except Customer.DoesNotExist:
        Customer(login=data[0]).save()
        customer = Customer.objects.get(login=data[0])

    # Сохранение Item
    try:
        item = Item.objects.get(name=data[1])
    except Item.DoesNotExist:
        Item(name=data[1], total=data[2]).save()
        item = Item.objects.get(name=data[1])

    # Сохранение Даты покупки Customer-ом

    try:
        instance = PurchaseDate.objects.create(date=data[4].replace('\n', ''))
        instance.customer.add(customer)

    except RuntimeWarning:
        pass
    # Сохранение ItemAndCustomer
    try:
        item_and_customer = ItemAndCustomer.objects.get(customer=customer, item=item)
        item_and_customer.quantity += int(data[3])
        item_and_customer.save()
    except ItemAndCustomer.DoesNotExist:
        ItemAndCustomer(quantity=data[3], customer=customer, item=item).save()


def create_data_deal(id_file_csv):
    """ Проход по файлу и сохранение данных в бд """

    file = FileCSV.objects.get(id=id_file_csv).file

    with open(str(file), encoding="utf8") as file:
        skip_first_line = 0
        for line in file:
            if skip_first_line == 0:
                skip_first_line += 1
            else:
                data = line.split(',')

                save_objects(data)
