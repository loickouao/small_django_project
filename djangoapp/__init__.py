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
            endpoint = "djangoapp:pricelist-list",
            add = MenuItem(label="New Price", endpoint = "djangoapp:price-list"),
            permission = ItemPermission(
                method = lambda request: request.user.is_staff
            )
        ),
        MenuItem(
            label = "PricesPandas", 
            endpoint = "djangoapp:pandasprice",
            permission = ItemPermission(
                method = lambda request: request.user.is_staff
            )
        ),
        MenuItem(
            label = "Stats Stocks",
            endpoint = "djangoapp:statstock",
            permission = ItemPermission(
                method = lambda request: request.user.is_staff
            )
        )
    ]
)

default_registry.register(djangoapp_menu)

