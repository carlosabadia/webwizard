import reflex as rx
from webwizard.views.navbar import navbar_app
from webwizard.views.footer import footer
from webwizard.components.motion import motion
from webwizard.components.react_zoom import image_zoom
from webwizard.components.sonner import toast, toaster
from webwizard.components.openai_client import get_openai_client_async
from typing import List, Dict

hover_scale = 0.85


@rx.page(route="/logo-generator", title="Genera tu Logo | WebWizard")
def logo_generator() -> rx.Component:
    return rx.box(
        toaster(expand=True),
        navbar_app(),
        rx.el.section(
            _generator_ui(),
            rx.box(
            _image_ui(),
            class_name=""),
            class_name="flex flex-col-reverse lg:flex-row lg:mt-24 mt-5 gap-5 w-full justify-between"
        ),
        footer(),
        class_name="px-5 max-w-[90rem] mx-auto w-full pb-8"
    )


styles_options = ["Glassmorfismo", "Pixel", "Minimalista",
                  "Dibujo", "3D", "Neón", "Gradiente"]


class ColorSwitch(rx.Base):
    name: str
    gradients: str


color_dict: Dict[str, str] = {
    "Rojo": "linear-gradient(45deg, rgb(255, 0, 0), rgb(255, 160, 122))",
    "Verde": "linear-gradient(45deg, rgb(0, 128, 0), rgb(144, 238, 144))",
    "Azul": "linear-gradient(45deg, rgb(0, 0, 255), rgb(135, 206, 250))",
    "Amarillo": "linear-gradient(45deg, rgb(255, 183, 3), rgb(255, 255, 224))",
    "Naranja": "linear-gradient(45deg, rgb(255, 165, 0), rgb(255, 218, 185))",
    "Rosa": "linear-gradient(45deg, rgb(255, 0, 110), rgb(255, 182, 193))",
    "Morado": "linear-gradient(45deg, rgb(128, 0, 128), rgb(221, 160, 221))",
    "Negro": "linear-gradient(45deg, rgb(0, 0, 0), rgb(85, 85, 85))",
}


class DalleState(rx.State):
    """The app state."""

    image_url: str = "/default_img.webp"
    image_processing: bool = False
    image_prompt: str = ""
    _selected_color: str = ""
    _generations_counter: int = 0
    selected_style: str = "Glassmorfismo"

    colors_options: List[ColorSwitch] = [ColorSwitch(
        name=color, gradients=gradient) for color, gradient in color_dict.items()]

    def select_color(self, color_name: str):
        self._selected_color = color_name

    @rx.var
    def check_selected_color(self):
        return self._selected_color

    @rx.background
    async def get_dalle_result(self):
        async with self:
            if self.image_processing:
                return
            if self._generations_counter >= 5:
                yield rx.window_alert("Espera un tiempo para crear mas logos ⌛")
                return
            self.image_processing = True
            yield
        try:
            response = await get_openai_client_async().images.generate(
                prompt=f"ios app icon of a {self.image_prompt}, simple flat vector. Main color is {self._selected_color}, style is {self.selected_style}", n=1, size="1024x1024", quality="hd", model="dall-e-3",
                style="vivid", user=self.router.session.client_token
            )
            async with self:
                self.image_url = response.data[0].url
                self.image_processing = False
                self._generations_counter += 1
        except Exception as ex:
            async with self:
                self.image_processing = False
            yield rx.window_alert(f"Error with OpenAI Execution. {ex}")


def _generator_ui() -> rx.Component:
    return rx.flex(
        rx.box(
            rx.el.h2("🤔 ¿De qué trata tu sitio web o app?",
                     class_name="lg:text-2xl text-xl font-semibold"),
            rx.el.h3("Proporciona una descripción de tu web o app. Puedes añadir lo que quieres que incluya el logo.",
                     class_name="text-base opacity-90 font-normal"),
            rx.input(
                value=DalleState.image_prompt,
                placeholder="Ej: To-Do list App",
                max_length=200,
                type="text",
                size="3",
                class_name="w-full",
                on_change=DalleState.set_image_prompt,
            ),
            class_name="space-y-3 lg:space-y-4"
        ),
        rx.spacer(),
        rx.box(
            rx.el.h2("🎨 Elige el color principal",
                     class_name="lg:text-2xl text-xl font-semibold"),
            _colors_option(),
            class_name="space-y-3 lg:space-y-4"
        ),
        rx.spacer(),
        rx.box(
            rx.el.h2("👨‍🎨 ¿Qué estilo prefieres?",
                     class_name="lg:text-2xl text-xl font-semibold"),
            _styles_options(),
            class_name="space-y-3 lg:space-y-4"
        ),
        rx.spacer(),
        rx.cond(
            ~DalleState.image_processing,
            motion(
                rx.el.button("Generar Logo",
                             class_name="gen-button main px-5 py-3 rounded-lg text-lg w-full",
                             on_click=DalleState.get_dalle_result,
                             ),
                while_tap={"scale": 0.975},
                class_name="w-full"
            ),
            motion(
                rx.el.button("Procesando... ",
                             rx.chakra.spinner(color=rx.color(
                                 "gray", 12), thickness=4, size="md"),
                             align_items="center",
                             class_name="gen-button main px-5 py-3 rounded-lg text-lg opacity-80 w-full items-center",
                             on_click=toast.error('Espera a que termine la generación actual', position="top-center")),
                while_tap={"scale": 0.975},
                class_name="w-full"
            ),
        ),
        bg="#1c1c1e",
        class_name="flex flex-col gap-5 rounded-lg p-7 border lg:h-[600px] lg:w-[650px]"
    )


def _colors_option() -> rx.Component:
    return rx.box(
        rx.foreach(
            DalleState.colors_options,
            display_colors),
        class_name="flex flex-wrap justify-start gap-2.5"
    )


def display_colors(color: ColorSwitch):
    return rx.tooltip(
        motion(
            rx.cond(
                color.name.to(str) == DalleState.check_selected_color,
                rx.box(
                    rx.icon("check", color="white",
                            class_name=""),
                    bg=color.gradients,
                    class_name="lg:h-10 lg:w-10 h-9 w-9 rounded-full shadow-sm cursor-pointer flex items-center justify-center",
                ),
                rx.box(
                    bg=color.gradients,
                    class_name="lg:h-10 lg:w-10 h-9 w-9 rounded-full shadow-sm cursor-pointer flex items-center justify-center",
                ),
            ),
            on_click=DalleState.select_color(
                color.name.to(str)),
            while_tap={"scale": hover_scale},
        ),
        
        content=color.name.to(str),
    )


def _styles_options() -> rx.Component:
    return rx.select(
        styles_options,
        size="3",
        variant="surface",
        radius="large",
        default_value=styles_options[0],
        on_change=DalleState.set_selected_style,
    )


def _image_ui() -> rx.Component:
    return rx.cond(
        ~DalleState.image_processing,
        image_zoom(
            rx.image(src=DalleState.image_url,
                     decoding="auto",
                     class_name="max-h-[600px] w-auto rounded-lg",
                     alt="Output image"),
        ),
        rx.box(
            rx.chakra.spinner(color=rx.color("gray", 12), thickness=4, size="lg",
                              class_name="absolute top-4 right-4 z-10"),
            rx.image(src=DalleState.image_url,
                     decoding="auto",
                     class_name="max-h-[600px] w-auto blur-lg brightness-75 rounded-lg",
                     alt="Output image"),
            class_name="overflow-hidden relative"
        ),
    ),
