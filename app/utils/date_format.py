# ==============================
# Library imports
# ==============================

from datetime import date


# ==============================
# Month translations
# ==============================

MONTHS = {
    "en": {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December",
    },
    "ru": {
        1: "января",
        2: "февраля",
        3: "марта",
        4: "апреля",
        5: "мая",
        6: "июня",
        7: "июля",
        8: "августа",
        9: "сентября",
        10: "октября",
        11: "ноября",
        12: "декабря",
    },
    "lv": {
        1: "janvāra",
        2: "februāra",
        3: "marta",
        4: "aprīļa",
        5: "maija",
        6: "jūnija",
        7: "jūlija",
        8: "augusta",
        9: "septembra",
        10: "oktobra",
        11: "novembra",
        12: "decembra",
    },
}


# ==============================
# Date formatting
# ==============================

def format_month_year(
    value: date,
    language: str,
) -> str:
    """Format a date as month and year in the selected language."""
    months = MONTHS.get(language)

    if months is None:
        raise ValueError(
            f"Unsupported language: {language}"
        )

    return f"{months[value.month]} {value.year}"


def format_year(
    value: date,
) -> str:
    """Format a date as a year."""
    return str(value.year)