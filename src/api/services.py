import json

from api.models import FileCSV, Customer, PurchaseDate, Item, ItemAndCustomer

""" Начало фукнций для GET поинта FileCSV """


def save_objects(data):
    """ Сохранение данных в бд """

    login = data[0]
    name = data[1]
    total = int(data[2])
    quantity = int(data[3])
    spent_money = total * quantity
    date = data[4].replace('\n', '')

    # Сохранение Customer
    try:
        customer = Customer.objects.get(login=login)
    except Customer.DoesNotExist:
        Customer(login=login, spent_money=spent_money).save()
        customer = Customer.objects.get(login=login)

    # Сохранение Item
    try:
        item = Item.objects.get(name=name)
    except Item.DoesNotExist:
        Item(name=name, total=total).save()
        item = Item.objects.get(name=name)

    # Сохранение Даты покупки Customer-ом

    try:
        instance = PurchaseDate.objects.create(date=date)
        instance.customer.add(customer)

    except RuntimeWarning:
        pass
    # Сохранение ItemAndCustomer
    try:
        item_and_customer = ItemAndCustomer.objects.get(customer=customer, item=item)
        item_and_customer.quantity += int(quantity)
        item_and_customer.save()
    except ItemAndCustomer.DoesNotExist:
        ItemAndCustomer(quantity=quantity, customer=customer, item=item).save()


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


""" Конец фукнций для GET поинта FileCSV """

""" Начало фукнций для GET поинта info-top-client """


def get_gems_of_customers(customers, gems_of_customers, list_gems_of_customers):
    spent_money_of_customers = {}
    for customer in customers:
        spent_money_of_customers[customer.login] = customer.spent_money
        purchases = ItemAndCustomer.objects.filter(customer=customer).select_related('item')
        gems = []

        for purchase in purchases:
            gems.append(purchase.item.name)
            list_gems_of_customers.append(purchase.item.name)

        gems_of_customers[customer.login] = gems
    return gems_of_customers, list_gems_of_customers, spent_money_of_customers


def clear_gems_without_instance(list_gems) -> list:
    """ Если гем есть у > 2 customer, то здесь мы это поймем, ведь в списке list_gems содержаться все гемы с
    повторениями """

    # с последнего индекса length -1 | до последнего элемента(доходит не до последнего а до предпоследнего) | с шагом -1
    for index_gem in range(len(list_gems) - 1, -1, -1):
        gem = list_gems.pop(index_gem)
        if gem in list_gems:
            list_gems.append(gem)

    return list_gems


def clear_gems_with_instance(list_gems, instance_list_gems) -> list:
    print(list_gems)
    # с последнего индекса length -1 | до последнего элемента(доходит не до последнего а до предпоследнего) | с шагом -1
    for index_gem in range(len(list_gems) - 1, -1, -1):
        gem = list_gems.pop(index_gem)
        if gem in instance_list_gems:
            list_gems.append(gem)

    return list_gems


def generate_json(dict_gems_of_customers, spent_money_of_customers):
    print(dict_gems_of_customers)
    final_data = {}
    info_users = {}
    index = 0
    for gem_of_customer in dict_gems_of_customers:
        index += 1
        username = {'username': gem_of_customer}
        gems = {'gems': dict_gems_of_customers[gem_of_customer]}
        spent_money = {'spent_money': spent_money_of_customers[gem_of_customer]}
        info_users[f'user_{index}'] = username, spent_money, gems
    final_data['response'] = info_users
    return final_data


def get_data():
    top_count = 5
    customers = Customer.objects.all().order_by('-spent_money')[:top_count]
    dict_gems_of_customers = {}
    list_gems_of_customers = []

    dict_gems_of_customers, list_gems_of_customers, spent_money_of_customers = get_gems_of_customers(
        customers,
        dict_gems_of_customers,
        list_gems_of_customers)

    list_gems_of_customers = clear_gems_without_instance(list_gems_of_customers)

    for customer in dict_gems_of_customers:
        dict_gems_of_customers[customer] = list(
            set(clear_gems_with_instance(dict_gems_of_customers[customer], list_gems_of_customers)))

    print(generate_json(dict_gems_of_customers, spent_money_of_customers))
    return generate_json(dict_gems_of_customers, spent_money_of_customers)


""" Конец фукнций для GET поинта info-top-client """
