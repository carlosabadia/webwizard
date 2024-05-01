import reflex as rx
import webwizard.styles.styles as styles
from webwizard.components.motion import motion


def hero() -> rx.Component:
    return rx.el.section(
        rx.image(src="/grid.webp",
                     class_name="opacity-80 overflow-hidden absolute -z-10 top-0 align-middle lg:-mt-40 w-full rotate-90 lg:rotate-0 scale-150 lg:scale-100 mt-10"),
        motion(
            rx.box(
                rx.logo(opacity=0.85),
                rx.box(
                    rx.el.h1(
                        "Diseña,", class_name="bg-gradient-to-t from-gray-500 via-gray-100 to-gray-100 bg-clip-text text-transparent"),
                    rx.el.h1(
                        "Mejora,", class_name="bg-gradient-to-t from-gray-500 via-gray-100 to-gray-100 bg-clip-text text-transparent"),
                    rx.el.h1(
                        "Inspira", class_name="bg-gradient-to-t from-gray-500 via-gray-100 to-gray-100 bg-clip-text text-transparent"),
                    class_name="flex flex-col lg:flex-row lg:text-[5.35rem] text-[3.35rem] font-semibold text-center leading-tight -mt-7 gap-1 lg:gap-3.5"
                ),
                rx.el.h2(
                    "Emplea la IA para mejorar tu web o aplicación en segundos. Tus herramientas creativas en un solo lugar",
                    class_name="lg:text-xl text-base font-normal text-center text-balance max-w-xl opacity-80"
                ),
                rx.el.button(
                    "Ver herramientas", class_name="gen-button-hero main rounded-lg lg:text-xl text-lg px-5 py-3 hover:opacity-80 transition-opacity",
                    on_click=rx.scroll_to("tools"),
                    width="215px",),
                _avatar_group(),
                class_name="flex flex-col items-center text-center lg:gap-14 gap-9 lg:mt-36 relative"
            ),
            initial={"opacity": 0, "y": 15},
            animate={"opacity": 1, "y": 0},
            transition={"duration": 1},
        ),
        class_name="lg:-mt-10 items-center max-w-4xl w-full mx-auto relative"
    )


def _avatar_group() -> rx.Component:
    return rx.box(
        rx.box(
            _avatar(src="/people/bezos.webp", fallback="JB",
                    comment="Desde que utilizo WebWizard, mi empresa ha crecido un 200%"),
            _avatar(src="/people/zuck.webp", fallback="MZ",
                    comment="¡Increíble! WebWizard ha mejorado la experiencia de mis usuarios"),
            _avatar(src="/people/bill.webp", fallback="BG",
                    comment="Me encanta la simplicidad de WebWizard. ¡Gracias!"),
            _avatar(src="/people/elon.webp", fallback="EM",
                    comment="¡Gracias WebWizard! Ahora puedo dedicar más tiempo a mi familia"),
            class_name="flex flex-row -space-x-2 rtl:space-x-reverse items-center"
        ),
        rx.box(
            _stars_group(),
            rx.text(
                "Utilizado por los mejores ",
                rx.text.span("seniors", as_="s"),
                " juniors",
                as_="p",
                class_name="text-base font-normal opacity-60"
            ),
            class_name="flex flex-col lg:gap-0.5 gap-1 items-center lg:items-start"
        ),
        class_name="flex lg:flex-row flex-col items-center gap-4"
    )


def _avatar(src: str, fallback: str, comment: str):
    return rx.tooltip(
        motion(
            rx.avatar(src=src, radius="full", fallback=fallback,
                      class_name=f"ring-2 ring-[{styles.bg_color}]"),
            while_hover={"scale": 1.3, "rotate": 5},
        ),
        side="bottom",
        content=comment,
    )


def _stars_group():
    return rx.box(
        rx.image(src="star.svg", class_name="h-4 w-5"),
        rx.image(src="star.svg", class_name="h-4 w-5"),
        rx.image(src="star.svg", class_name="h-4 w-5"),
        rx.image(src="star.svg", class_name="h-4 w-5"),
        rx.image(src="star.svg", class_name="h-4 w-5"),
        class_name="flex flex-row gap-1"
    )
