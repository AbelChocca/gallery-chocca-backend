from datetime import date


PERU_HOLIDAYS_2026: frozenset[date] = frozenset({
    date(2026, 1, 1),    # Año Nuevo

    date(2026, 4, 2),    # Jueves Santo
    date(2026, 4, 3),    # Viernes Santo

    date(2026, 5, 1),    # Día del Trabajo

    date(2026, 6, 7),    # Batalla de Arica
    date(2026, 6, 29),   # San Pedro y San Pablo

    date(2026, 7, 23),   # Día de la Fuerza Aérea
    date(2026, 7, 28),   # Fiestas Patrias
    date(2026, 7, 29),   # Fiestas Patrias

    date(2026, 8, 6),    # Batalla de Junín
    date(2026, 8, 30),   # Santa Rosa de Lima

    date(2026, 10, 8),   # Combate de Angamos

    date(2026, 11, 1),   # Todos los Santos

    date(2026, 12, 8),   # Inmaculada Concepción
    date(2026, 12, 9),   # Batalla de Ayacucho
    date(2026, 12, 25),  # Navidad
})
