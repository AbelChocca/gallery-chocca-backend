pytest_plugins = [
    "tests.fixtures.database",
    "tests.fixtures.inventory_fixture",
    "tests.fixtures.product_fixtures",
    "tests.fixtures.sale_pricing_fixture",
    "tests.fixtures.catalog_pricing_fixture",
    "tests.fixtures.dependencies.customer",
    "tests.fixtures.dependencies.products",
    "tests.fixtures.dependencies.promotions"
]