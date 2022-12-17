def select_item(items, prompt, display_key="name", value_key=None):
    for i, item in enumerate(items):
        print(f"{i+1}. {item[display_key]}")

    selection = input(prompt)

    try:
        selection = int(selection) - 1
        if selection >= 0 and selection < len(items):
            selected = items[selection]
            return selected if value_key is None else selected[value_key]
        else:
            print("Invalid selection. Please try again.")
            return select_item(items)
    except ValueError:
        print("Invalid selection. Please try again.")
        return select_item(items)
