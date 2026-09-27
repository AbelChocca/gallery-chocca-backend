import asyncio
import random

from sqlalchemy import select

from app.infra.db.config import async_session_factory
from app.features.customer.models.customer import Customer
from app.features.sales.types.customer import (
    CustomerDocumentType,
    CustomerType,
)


FIRST_NAMES = [
    "Carlos",
    "Andrea",
    "Luis",
    "Valeria",
    "Diego",
    "Camila",
    "Jorge",
    "Daniela",
    "Sebastian",
    "Luciana",
    "Mateo",
    "Sofia",
    "Renzo",
    "Alejandra",
    "Fernando",
    "Maria",
    "Alonso",
    "Gabriela",
    "Nicolas",
    "Paola",
]

LAST_NAMES = [
    "Garcia",
    "Torres",
    "Flores",
    "Rojas",
    "Mendoza",
    "Chavez",
    "Vargas",
    "Castillo",
    "Ramirez",
    "Quispe",
    "Huaman",
    "Salazar",
    "Paredes",
    "Medina",
    "Reyes",
]


def build_customer(index: int) -> Customer:
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)

    document_number = str(
        70_000_000 + index
    )

    customer_type = random.choices(
        population=[
            CustomerType.REGULAR,
            CustomerType.WHOLESALE,
            CustomerType.VIP,
        ],
        weights=[
            70,
            20,
            10,
        ],
        k=1,
    )[0]

    return Customer(
        document_type=CustomerDocumentType.DNI,
        document_number=document_number,
        name=f"{first_name} {last_name}",
        email=f"customer{index}@chocca.test",
        phone=str(910_000_000 + index),
        address=f"Dirección de prueba #{index}",
        customer_type=customer_type,
        user_id=None,
    )


async def seed_customers() -> None:
    async with async_session_factory() as session:

        document_numbers = {
            str(70_000_000 + index)
            for index in range(1, 51)
        }

        result = await session.scalars(
            select(Customer.document_number).where(
                Customer.document_number.in_(
                    document_numbers
                )
            )
        )

        existing_documents = set(
            result.all()
        )

        customers = [
            build_customer(index)
            for index in range(1, 51)
            if str(70_000_000 + index)
            not in existing_documents
        ]

        session.add_all(customers)

        await session.commit()

        print()
        print("🌱 Customer seed terminado")
        print(f"✅ Creados: {len(customers)}")
        print(
            f"⏭️ Existentes: "
            f"{50 - len(customers)}"
        )
        print("📦 Total procesados: 50")
        print()


if __name__ == "__main__":
    asyncio.run(seed_customers())