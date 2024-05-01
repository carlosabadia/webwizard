import reflex as rx


def footer() -> rx.Component:
    return rx.el.footer(
        _start_box(),
        rx.box(
            _tools_box(),
            _links_box(),
            class_name="flex flex-col lg:flex-row lg:gap-40 lg:justify-between mt-8 lg:mt-0"
        ),
        class_name="flex flex-col lg:flex-row lg:gap-3 lg:justify-between border-t mt-5 pt-10 pb-10 lg:mt-24 lg:pt-20 lg:pb-20 max-w-[90rem] w-full"
    )


def _start_box() -> rx.Component:
    return rx.box(
        rx.link(
            rx.box(
                rx.image(
                    src="/wizard_hat.svg",
                    decoding="auto",
                    alt="Web Wizard logo",
                    class_name="h-7",
                ),
                rx.text("WebWizard", class_name="text-lg font-bold"),
                class_name="flex flex-row gap-2 items-center lg:justify-start mb-4 justify-center lg:items-start"
            ),
            href="/#",
        ),
        rx.text("Tus herramientas creativas en un solo lugar",
                as_="p", class_name="text-sm opacity-80 mb-3"),
        rx.text(f"Hackathon #HolaMundoDay 2024",
                class_name="text-sm opacity-80"),
        class_name="flex flex-col items-center justify-center lg:justify-start lg:items-start"
    )


link_style = "text-sm opacity-80 hover:underline"


def _tools_box() -> rx.Component:
    return rx.box(
        rx.text("HERRAMIENTAS", as_="p",
                class_name="text-base opacity-80 mb-2 font-medium"),
        rx.link("Logos", href="/logo-generator", class_name=link_style),
        rx.link("Web Feedback", href="/web-criticizer",
                class_name=link_style),
        rx.link("Directorios", href="/directories-list",
                class_name=link_style),
        rx.link("Blogs", href="/blog-generator", class_name=link_style),
        class_name="flex flex-col gap-2 items-center justify-center lg:justify-start lg:items-start"
    )


def _links_box() -> rx.Component:
    return rx.box(
        rx.text("ENLACES", as_="p",
                class_name="text-base opacity-80 mb-2 font-medium"),
        rx.link("Reflex", href="https://reflex.dev/",
                is_external=True, class_name=link_style),
        rx.link("Curso", href="https://github.com/mouredev/python-web", is_external=True,
                class_name=link_style),
        rx.link("HolaMundoDay", href="https://holamundo.day/",
                is_external=True,
                class_name=link_style),
        class_name="flex flex-col gap-2 mt-8 items-center justify-center lg:justify-start lg:mt-0 lg:items-start"
    )
