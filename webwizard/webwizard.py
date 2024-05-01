from webwizard.styles import styles
import reflex as rx

import dotenv
dotenv.load_dotenv()

# Import all the pages.
from webwizard.pages import *


app = rx.App(style=styles.base_style,
             html_lang="es",
             html_custom_attrs={"className": "!scroll-smooth"},
             stylesheets=styles.base_stylesheets,
             theme=rx.theme(
                 appearance="dark",
                 has_background=True,
                 scaling="100%",
                 radius="large",
                 accent_color="yellow")
             )
