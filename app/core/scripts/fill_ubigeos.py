import asyncio
import re
from pathlib import Path

import pandas as pd
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.locations.models.ubigeo import UbigeoTable

from app.infra.db.config import async_session_factory


ROOT_DIR = Path(__file__).resolve().parents[3]
EXCEL_PATH = ROOT_DIR / "data" / "ubigeos.xlsx"


def normalize_text(value: str | None) -> str | None:
    if pd.isna(value):
        return None

    value = str(value).strip()

    if not value:
        return None

    return re.sub(r"\s+", " ", value)


def load_ubigeos() -> list[dict]:
    if not EXCEL_PATH.exists():
        raise FileNotFoundError(
            f"Ubigeo Excel file not found: {EXCEL_PATH}"
        )

    dataframe = pd.read_excel(
        EXCEL_PATH,
        dtype={
            "Departamento": str,
            "Provincia": str,
            "Distrito": str,
            "Nombre de Ciudad": str,
            "UBIGEO": str,
        },
    )

    dataframe = dataframe.dropna(how="all")

    ubigeos: dict[str, dict] = {}

    for index, row in dataframe.iterrows():
        # +2 porque Excel empieza en 1 y además tenemos el header
        excel_row = index + 2

        code = normalize_text(row["UBIGEO"])
        department = normalize_text(row["Departamento"])
        province = normalize_text(row["Provincia"])
        district = normalize_text(row["Distrito"])
        city_name = normalize_text(row["Nombre de Ciudad"])

        # Campos obligatorios
        if not all([
            code,
            department,
            province,
            district,
        ]):
            raise ValueError(
                f"Incomplete required data at Excel row {excel_row}: "
                f"UBIGEO={code!r}, "
                f"Departamento={department!r}, "
                f"Provincia={province!r}, "
                f"Distrito={district!r}"
            )

        if not re.fullmatch(r"\d{6}", code):
            raise ValueError(
                f"Invalid UBIGEO code at Excel row {excel_row}: "
                f"{code!r}. Expected exactly 6 digits."
            )

        ubigeos[code] = {
            "code": code,
            "department": department,
            "province": province,
            "district": district,
            "city_name": city_name,
        }

    if not ubigeos:
        raise ValueError(
            "No valid UBIGEO records were found in the Excel file."
        )

    return list(ubigeos.values())


async def fill_ubigeos(
    session: AsyncSession,
) -> None:
    ubigeos = load_ubigeos()

    statement = insert(UbigeoTable).values(ubigeos)

    statement = statement.on_conflict_do_update(
        index_elements=[UbigeoTable.code],
        set_={
            "department": statement.excluded.department,
            "province": statement.excluded.province,
            "district": statement.excluded.district,
            "city_name": statement.excluded.city_name,
        },
    )

    await session.execute(statement)
    await session.commit()

    print(f"Processed {len(ubigeos)} ubigeos successfully.")


async def main() -> None:
    async with async_session_factory() as session:
        try:
            await fill_ubigeos(session)

        except Exception:
            await session.rollback()
            raise


if __name__ == "__main__":
    asyncio.run(main())