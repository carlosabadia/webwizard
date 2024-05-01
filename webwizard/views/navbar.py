import reflex as rx
from webwizard.components.motion import motion
import webwizard.styles.styles as styles


def navbar_home() -> rx.Component:
    return rx.el.header(
        motion(
            rx.mobile_and_tablet(
                navbar_mobile()
            ),
            rx.desktop_only(
                navbar_desktop(),
            ),
            initial={"opacity": 0, "y": -15},
            animate={"opacity": 1, "y": 0},
            transition={"duration": 1},
        ),
        class_name="w-full py-4 max-w-[90rem]"
    )


def navbar_app() -> rx.Component:
    return rx.el.header(
        rx.mobile_and_tablet(
            navbar_app_mobile()
        ),
        rx.desktop_only(
            navbar_app_desktop(),
        ),
        class_name="w-full py-4 max-w-[90rem] border-b"
    )


def navbar_desktop() -> rx.Component:
    return rx.el.nav(
        rx.link(
            rx.box(
                motion(
                    rx.image(src="/wizard_hat.svg", width=36, height=36),
                    while_hover={"scale": 1.2, "rotate": 5},
                ),
                rx.text("WebWizard", as_='span', class_name="text-2xl"),
                class_name="flex gap-2 items-center font-semibold flex-row"
            ),
            href="/",
            is_external=False,
        ),
        rx.box(
            rx.el.button(
                "Empezar", class_name="gen-button main rounded-lg px-5 py-2 text-lg",
                width="150px",
                on_click=rx.scroll_to("tools"),),
            class_name="flex gap-5 items-center"
        ),
        class_name="w-full flex flex-row justify-between items-center h-16"
    )


def navbar_mobile() -> rx.Component:
    return rx.el.nav(
        rx.link(
            rx.box(
                motion(
                    rx.image(src="/wizard_hat.svg", width=30, height=30),
                    while_hover={"scale": 1.2, "rotate": 5},
                ),
                rx.text("WebWizard", as_='span', class_name="text-xl"),
                class_name="flex gap-2 items-center font-semibold flex-row"
            ),
            href="/",
            is_external=False,
        ),
        class_name="w-full flex flex-row justify-center items-center h-10"
    )


def navbar_app_desktop() -> rx.Component:
    return rx.el.nav(
        motion(
            rx.link(
                rx.image(src="/wizard_hat.svg", width=36, height=36),
                href="/",
                is_external=False,
            ),
            while_hover={"scale": 1.2, "rotate": 5},
        ),
        rx.spacer(),
        rx.box(
            nav_link(text="Logos", icon="image",
                     main_color="purple", url="/logo-generator"),
            nav_link(text="Web Feedback", icon="flame",
                     main_color="orange", url="/web-criticizer"),
            nav_link(text="Directorios", icon="rocket",
                     main_color="green", url="/directories-list"),
            nav_link(text="Blogs", icon="notebook-pen",
                     main_color="blue", url="/blog-generator"),
            class_name="flex flex-row gap-8 items-center"
        ),
        class_name="w-full flex flex-row justify-between items-center h-16"
    )


def nav_link(text: str, icon: str, main_color: str, url: str) -> rx.Component:
    return rx.link(
        rx.box(
            rx.badge(
                rx.icon(icon, color=rx.color(main_color, 11)),
                color_scheme=main_color,
                cursor="pointer",
                variant="soft",
                class_name="h-11 w-11 items-center justify-center", radius="full"
            ),
            rx.text(text, class_name=rx.cond(
                rx.State.router.page.path == url,
                "text-xl font-semibold",
                "lg:hidden text-xl font-medium"),
                color=rx.color(main_color, 11)),
            class_name="flex gap-2 items-center transition-all"
        ),
        class_name=rx.cond(
            rx.State.router.page.path == url,
            "opacity-100 cursor-pointer",
            "opacity-70 hover:opacity-95 transition-opacity cursor-pointer"
        ),
        href=url,
        is_external=False,
    )


def navbar_app_mobile() -> rx.Component:
    return rx.el.nav(
        rx.link(
            rx.image(src="/wizard_hat.svg", width=30, height=30),
            href="/",
            is_external=False,
        ),
        _drawer(),
        class_name="w-full flex flex-row justify-between items-center h-10"
    )


def _drawer() -> rx.Component:
    return rx.drawer.root(
        rx.drawer.trigger(rx.icon("align-justify", size=30,
                                  color="white")),
        rx.drawer.overlay(),
        rx.drawer.portal(
            rx.drawer.content(
                rx.box(
                    rx.spacer(),
                    rx.drawer.close(
                        rx.icon("x", size=30, color="white", class_name="justify-end")),
                    class_name="w-full flex flex-row justify-between items-center h-10"
                ),
                rx.box(
                    nav_link(text="Logos", icon="image",
                             main_color="purple", url="/logo-generator"),
                    nav_link(text="Web Feedback", icon="flame",
                             main_color="orange", url="/web-criticizer"),
                    nav_link(text="Directorios", icon="rocket",
                             main_color="green", url="/directories-list"),
                    nav_link(text="Blogs", icon="notebook-pen",
                             main_color="blue", url="/blog-generator"),
                    class_name="flex flex-col gap-10 items-end justify-end mt-12"
                ),
                bg=styles.bg_color,
                class_name="w-full py-4 px-5 h-full flex flex-col focus:outline-none",
            ),
        ),
        modal=True,
        direction="right",
        autofocus=False
    )
