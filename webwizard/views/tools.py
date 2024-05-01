import reflex as rx
from webwizard.components.motion import motion


def tools() -> rx.Component:
    return rx.el.section(
        motion(
            rx.el.h2("Elige tu herramienta",
                     class_name="lg:text-[3rem] text-2xl font-medium text-center opacity-95"),
            initial={"opacity": 0, "y": 15},
            animate={"opacity": 1, "y": 0},
            transition={"duration": 1},
        ),
        _tools_group(),
        motion(
            rx.text("Más utilidades próximamente...",
                    class_name="text-center opacity-70 lg:text-lg text-sm font-normal"),
            initial={"opacity": 0, },
            while_in_view={"opacity": 1, },
            viewport={"once": True, "amount": 0.5},
            transition={"duration": 1},
        ),
        id="tools",
        class_name="lg:mt-80 mt-24 items-center justify-center w-full lg:space-y-14 space-y-8 pb-8"
    )


def _tools_group() -> rx.Component:
    return rx.box(
        motion(
            _tool(icon="image", comment="Crea logos en segundos",
                  main_color="purple", url="/logo-generator"),
            initial={"opacity": 0, "x": -20},
            while_in_view={"opacity": 1, "x": 0},
            viewport={"once": True, "amount": 0.6},
            transition={"duration": 1},
        ),
        motion(
            _tool(icon="flame", comment="Mejora el diseño de tu web",
                  main_color="orange", url="/web-criticizer"),
            initial={"opacity": 0, "x": -20},
            while_in_view={"opacity": 1, "x": 0},
            viewport={"once": True, "amount": 0.6},
            transition={"duration": 1},
        ),
        motion(
            _tool(icon="rocket", comment="Aumenta la autoridad de tu web",
                  main_color="green", url="/directories-list"),
            initial={"opacity": 0, "x": 20},
            while_in_view={"opacity": 1, "x": 0},
            viewport={"once": True, "amount": 0.6},
            transition={"duration": 1},
        ),
        motion(
            _tool(icon="notebook-pen", comment="Redacta blogs usando IA",
                  main_color="blue", url="/blog-generator"),
            initial={"opacity": 0, "x": 20},
            while_in_view={"opacity": 1, "x": 0},
            viewport={"once": True, "amount": 0.6},
            transition={"duration": 1},
        ),
        columns=["1", "1", "2", "2"],
        class_name="items-center justify-center max-w-6xl align-middle w-full mx-auto space-y-5 gap-5"
    ),


def _tool(icon: str, comment: str, main_color: str, url: str) -> rx.Component:
    return rx.link(
        rx.box(
            rx.box(
                rx.badge(rx.icon(icon, class_name="lg:h-7 lg:w-7"), color_scheme=main_color, variant="soft",
                         cursor="pointer",
                         class_name="lg:h-12 lg:w-12 h-9 w-9 items-center", radius="full"),
                rx.box(
                ),
                rx.el.h3(comment, class_name="lg:text-2xl text-base font-medium",
                         color=rx.color(main_color, 11)),
                rx.spacer(),
                rx.icon("arrow-right", color="white",
                        class_name="-rotate-45 transition-all duration-200 group-hover:rotate-0 opacity-95 lg:h-7 lg:w-7 hidden lg:block"),
                class_name="flex flex-row w-full lg:gap-2 items-center gap-1",
            ),
            bg=rx.color(main_color, 2),
            style={
                "outline": f"1px solid {rx.color(main_color, 11)}",
                "_hover": {
                    "outline": f"2px solid {rx.color(main_color, 11)}",
                    "boxShadow": f"0px 0px 15px 0px {rx.color(main_color, 11)}"
                },
            },
            class_name="h-200 items-center w-full lg:p-5 p-4 cursor-pointer transition-all group rounded-lg ",
        ),
        href=url,
        is_external=False,
    )
