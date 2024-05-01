import reflex as rx
from .fonts import Font

text_color = rx.color("gray", 12)

bg_color = "#101011"

base_style = {
    "_dark": {"bg": bg_color},
    "font_family": Font.DEFAULT.value,
    rx.text: {
        "color": text_color,
    },
    rx.button: {
        "_hover": {
            "cursor": "pointer",
        },
    },
    rx.link: {
        "text_decoration": "none !important",
    },
}

base_stylesheets = [
    "styles.css",
    "react-zoom.css",
    "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
]