import reflex as rx
from webwizard.views.navbar import navbar_app
from webwizard.views.footer import footer
from webwizard.components.openai_client import get_openai_client
from webwizard.components.motion import motion
from webwizard.components.sonner import toast, toaster


estilos = ["Narrativo", "Descriptivo", "Académico", "Expositivo",
           "Persuasivo", "Creativo", "Técnico", "Periodístico"]


class BlogState(rx.State):

    keyword: str = ""
    processing: bool = False
    blog: str = ""
    estilo: str = estilos[0]
    length: int = 3500
    counter: int = 0

    def set_length(self, length: int):
        self.length = length

    @rx.background
    async def openai_process_question(self):
        try:
            async with self:
                if self.processing:
                    yield rx.window_alert("Ya se esta procesando una solicitud")
                    return
                if self.counter >= 30:
                    yield rx.window_alert("Espera un tiempo para crear mas blogs ⌛")
                    return
                self.processing = True
                self.blog = ""
                yield
            session = get_openai_client().chat.completions.create(
                user=self.router.session.client_token,
                stream=True,
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un asistente especializado en la creación de contenido para blogs, optimizado para SEO. Y respondes en formato markdown."},
                    {"role": "user", "content": f"Escribe un articulo SEO optimizado para {
                        self.keyword}, en menos de {self.length} caracteres y en estilo {self.estilo}."},
                ]
            )
            for item in session:
                if hasattr(item.choices[0].delta, "content"):
                    answer_text = item.choices[0].delta.content
                    async with self:
                        if answer_text is not None:
                            self.blog += answer_text
                        else:
                            answer_text = ""
                            self.blog += answer_text
                    yield
            async with self:
                self.counter += 1
                self.processing = False
        except Exception as ex:
            async with self:
                self.processing = False
            yield rx.window_alert(f"Error with OpenAI Execution. {ex}")


@rx.page(route="/blog-generator", title="Generador de Blogs | WebWizard")
def blog_generator() -> rx.Component:
    return rx.box(
        toaster(expand=True),
        navbar_app(),
        rx.el.section(
            _generator_ui(),
            _blog_ui(),
            class_name="flex flex-col lg:flex-row lg:mt-24 mt-5 w-full gap-5 justify-between"
        ),
        footer(),
        class_name="px-5 max-w-[90rem] mx-auto w-full pb-8"
    )


def _generator_ui() -> rx.Component:
    return rx.flex(
        rx.box(
            rx.el.h2("🤔 ¿De qué tema te gustaría que trate el blog?",
                     class_name="lg:text-2xl text-xl font-semibold"),
            rx.el.h3("Proporciona una breve descripción del tema de tu blog. Puedes añadir lo que quieras que incluya el blog.",
                     class_name="text-base opacity-90 font-normal"),
            rx.input(
                value=BlogState.keyword,
                placeholder="Ej: Los mejores consejos para mejorar tu SEO",
                max_length=500,
                type="text",
                size="3",
                class_name="w-full",
                on_change=BlogState.set_keyword,
            ),
            class_name="space-y-3 lg:space-y-4"
        ),
        rx.spacer(),
        rx.box(
            rx.text(f"📖 Longitud del blog: {BlogState.length} caracteres",
                    class_name="lg:text-2xl text-xl opacity-90 font-semibold"),
            rx.slider(
                min=2000,
                max=5000,
                default_value=3500,
                step=100,
                on_value_commit=BlogState.set_length,
            ),
            class_name="space-y-3 lg:space-y-4"
        ),
        rx.spacer(),
        rx.box(
            rx.el.h2("✍️ ¿Qué estilo prefieres?",
                     class_name="lg:text-2xl text-xl font-semibold"),
            _writing_options(),
            class_name="space-y-3 lg:space-y-4"
        ),
        rx.spacer(),
        rx.cond(
            ~BlogState.processing,
            motion(
                rx.el.button("Generar Blog",
                             class_name="gen-button main px-5 py-3 rounded-lg text-lg w-full",
                             on_click=BlogState.openai_process_question),
                while_tap={"scale": 0.975},
                class_name="w-full"
            ),
            motion(
                rx.el.button("Procesando... ",
                             rx.chakra.spinner(color=rx.color(
                                 "gray", 12), thickness=4, size="md"),
                             class_name="gen-button main px-5 py-3 rounded-lg text-lg opacity-80 w-full items-center",
                             on_click=toast.error('Espera a que termine la generación actual', position="top-center")),
                while_tap={"scale": 0.975},
                class_name="w-full"
            ),
        ),
        bg="#1c1c1e",
        class_name="flex flex-col gap-5 rounded-lg p-7 border lg:h-[600px] lg:w-[650px]"
    )


def _blog_ui() -> rx.Component:
    return rx.box(
        rx.scroll_area(
            rx.button(
                rx.icon("clipboard"),
                variant="soft",
                color_scheme="gray",
                on_click=[rx.set_clipboard(BlogState.blog), toast.success(
                    "Copiado al portapapeles")],
                cursor="pointer",
                class_name="top-5 right-5 z-10 absolute"
            ),
            rx.markdown(BlogState.blog,
                        class_name="text-base opacity-90 font-normal"),
            type="auto",
            scrollbars="vertical",
            class_name="h-full p-7 relative"
        ),
        class_name="border rounded-lg lg:h-[600px] h-[500px] lg:w-[650px]"
    )


def _writing_options() -> rx.Component:
    return rx.select(
        estilos,
        size="3",
        variant="surface",
        radius="large",
        default_value=estilos[0],
        on_change=BlogState.set_estilo,
    )
