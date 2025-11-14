def get_selection_options(entity_list, name_attr='name', surname_attr='surname'):
    options = {}
    for item in entity_list:
        if surname_attr and hasattr(item, surname_attr) and getattr(item, surname_attr):
            label = f"{getattr(item, surname_attr)} {getattr(item, name_attr)} (ID: {item.id})"
        else:
            label = f"{getattr(item, name_attr)} (ID: {item.id})"
        options[label] = item.id
    return options