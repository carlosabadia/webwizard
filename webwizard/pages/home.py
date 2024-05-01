import reflex as rx
from webwizard.views.navbar import navbar_home
from webwizard.views.hero import hero
from webwizard.views.tools import tools
from webwizard.views.footer import footer


@rx.page(route="/", title="WebWizard")
def home() -> rx.Component:
    return rx.box(
        navbar_home(),
        rx.el.main(
            hero(),
            tools(),
            class_name="max-w-7xl w-full",
        ),
        footer(),
        class_name="px-5 max-w-[90rem] mx-auto w-full pb-8",
    )
