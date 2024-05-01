import reflex as rx
from webwizard.views.navbar import navbar_app
from webwizard.views.footer import footer
from webwizard.components.motion import motion
from webwizard.components.sonner import toast, toaster
from webwizard.components.openai_client import get_openai_client_async
from PIL.Image import Image
from typing import List, Dict, Union
import base64
from io import BytesIO
import PIL
import json
import httpx

hover_scale = 0.85


async def get_screenshot(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f'https://shotapi.arshadyaseen.com/take?url={
                url}&format=base64&width=1280&height=800&full_page=false&mobile=false&dark_mode=false&delay=0',
            headers={'accept': 'application/json'}, timeout=60
        )
        return response


class WebState(rx.State):
    web_image: Union[Image,
                     str] = ""
    web_url: str = ""
    processing: bool = False

    score: str = ""
    feedback: str = ""
    counter: int = 0

    @rx.background
    async def get_web_image(self):
        
        if self.counter >= 5:
            yield rx.window_alert("Espera un tiempo para criticar más webs ⌛")
            return

        if not self.web_url.startswith("http"):
            async with self:
                self.web_url = f"https://{self.web_url}"
        async with self:
            self.processing = True
            yield
        try:
            response = await get_screenshot(self.web_url)
            if response.status_code == 429:
                async with self:
                    self.processing = False
                yield rx.window_alert("Demasiadas solicitudes, espera un tiempo para criticar tu web ⌛")
            if response.status_code != 200:
                async with self:
                    self.processing = False
                yield rx.window_alert("Error al obtener la imagen de la web 🤔")
                return
            base64_string = response.text
            response = await get_openai_client_async().chat.completions.create(
                response_format={"type": "json_object"},
                model="gpt-4-turbo",
                user=self.router.session.client_token,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Eres un crítico de diseño web especializado en la evaluación de la calidad de la interfaz de usuario, el texto y el diseño de una web. Por favor, evalúa la web en la imagen adjunta y proporciona un puntaje de 1 a 100 sobre la calidad de la interfaz de usuario, el texto y el diseño. Además, proporciona comentarios sobre la interfaz de usuario, el texto y el diseño. ¿Qué se puede mejorar? ¿Qué es bueno? ¿Qué es malo? En menos de 5000 caracteres. Responde en formato json con las claves 'score' y 'feedback. El 'feedback' proporcionalo en formato markdown."},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_string}",
                                },
                            },
                        ],
                    }
                ],
                max_tokens=2000,
            )
            json_response = json.loads(response.choices[0].message.content)
            image_bytes = base64.b64decode(base64_string)
            image_buffer = BytesIO(image_bytes)
            async with self:
                self.score = json_response["score"]
                self.feedback = json_response["feedback"]
                self.web_image = PIL.Image.open(image_buffer)
                self.processing = False
                self.counter += 1
        except Exception as ex:
            async with self:
                self.processing = False
            yield rx.window_alert(f"Error al generar la respuesta 🤔 {ex}")


@rx.page(route="/web-criticizer", title="Critica tu web | Webwizard")
def web_criticizer() -> rx.Component:
    return rx.box(
        toaster(expand=True),
        navbar_app(),
        rx.el.section(
            _input_ui(),
            class_name="flex flex-col justify-between lg:gap-10 gap-5 lg:mt-10 mt-5"
        ),
        footer(),
        class_name="px-5 max-w-[90rem] mx-auto w-full pb-8"
    )


def _input_ui() -> rx.Component:
    return rx.box(
        rx.center(
            rx.el.h1("Introduce la URL de tu web para recibir feedback sobre ella.",
                     class_name="lg:text-3xl text-lg font-semibold text-start text-balance"),
            rx.el.h2("Páginas con protecciones de seguridad o que requieran login no funcionarán.",
                     class_name="lg:text-base text-sm font-medium text-start text-balance opacity-90"),
            rx.input(
                value=WebState.web_url,
                placeholder="URL de tu web",
                max_length=100,
                type="text",
                size="3",
                width="300px",
                class_name="lg:w-[300px]",
                on_change=WebState.set_web_url,
            ),
            rx.cond(
                ~WebState.processing,
                motion(
                    rx.el.button("Criticar Web",
                                 widht="250px",
                                 class_name="gen-button main px-5 py-3 rounded-lg text-lg lg:w-[300px] w-full",
                                 on_click=WebState.get_web_image),
                    while_tap={"scale": 0.975},
                    class_name="w-full"
                ),
                motion(
                    rx.el.button("Procesando... ",
                                 rx.chakra.spinner(color=rx.color(
                                     "gray", 12), thickness=4, size="md"),
                                 class_name="gen-button main px-5 py-3 rounded-lg text-lg opacity-80 lg:w-[300px] w-full items-center",
                                 on_click=toast.error('Espera a que termine la generación actual', position="top-center")),
                    while_tap={"scale": 0.975},
                    class_name="w-full"
                ),
            ),
            bg="#1c1c1e",
            class_name="flex flex-col gap-7 items-center text-center rounded-lg p-7 border"
        ),
        rx.center(
            rx.image(src=WebState.web_image,
                     class_name="max-h-[600px] w-auto rounded-lg",
                     ),
        ),
        rx.cond(
            WebState.score != "",
            rx.box(
                rx.box(
                    rx.text(f"Puntuación: {WebState.score}/100",
                            class_name="text-2xl font-semibold"),
                    rx.chakra.circular_progress(
                        value=WebState.score.to(int)),
                    class_name="flex flex-row gap-5 items-center mb-7"
                ),
                rx.markdown(WebState.feedback),
                bg="#1c1c1e",
                class_name="flex flex-col rounded-lg p-7 border"
            ),
            rx.box(),
        ),
        class_name="flex flex-col gap-5"
    )
