from bridger.menus import Menu, MenuItem, ItemPermission, default_registry


djangoapp_menu = Menu(
    label = "Global Stock Price",
    items = [
        MenuItem(
            label = "Stocks", 
            endpoint = "djangoapp:stock-list",
            add = MenuItem(label = "New Stock", endpoint = "djangoapp:stock-list"),
            permission = ItemPermission(
                method = lambda request: request.user.is_staff
            )
        ),
        MenuItem(
            label = "Prices", 
            endpoint = "djangoapp:price-list",
            add = MenuItem(label="New Price", endpoint = "djangoapp:price-list"),
            permission = ItemPermission(
                method = lambda request: request.user.is_staff
            )
        ),
        MenuItem(
            label = "Prices Pandas", 
            endpoint = "djangoapp:pandasprice",
            permission = ItemPermission(
                method = lambda request: request.user.is_staff
            )
        ),
        MenuItem(
            label = "NB Prices Stocks",
            endpoint = "djangoapp:nbpricestock-list",
            permission = ItemPermission(
                method = lambda request: request.user.is_staff
            )
        )
    ]
)

default_registry.register(djangoapp_menu)

