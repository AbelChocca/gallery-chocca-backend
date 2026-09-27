import os

os.environ["ENV"] = "test"

from dotenv import load_dotenv

load_dotenv(
    ".env.test",
    override=True,
)

pytest_plugins = [
    "tests.fixtures.database",
    "tests.fixtures.inventory_fixture",
    "tests.fixtures.product_fixtures",
    "tests.fixtures.sale_pricing_fixture",
    "tests.fixtures.catalog_pricing_fixture",
    "tests.fixtures.cart_pricing_fixture",
    "tests.fixtures.http_client",
    "tests.fixtures.dependencies.auth_fixture",
    "tests.fixtures.dependencies.customer",
    "tests.fixtures.dependencies.products",
    "tests.fixtures.dependencies.promotions",
    "tests.fixtures.redis",
    "tests.fixtures.material_fixture",
    "tests.fixtures.dependencies.coupons",
    "tests.fixtures.dependencies.cart",
    "tests.fixtures.dependencies.user",
    "tests.fixtures.dependencies.inventory",
]