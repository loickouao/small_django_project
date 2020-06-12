from bridger.menus import Menu, MenuItem, ItemPermission, default_registry


djangoapp_menu = Menu(
    label="Global Stock Price",
    items=[
        MenuItem(
            label="Stocks", 
            endpoint="djangoapp:stock-list",
            add=MenuItem(label="New Stock", endpoint="djangoapp:stock-list"),
        ),
        MenuItem(
            label="Prices", 
            endpoint="djangoapp:pricelist-list",
            add=MenuItem(label="New Price", endpoint="djangoapp:price-list"),
        ),
    ]
)
default_registry.register(djangoapp_menu)
