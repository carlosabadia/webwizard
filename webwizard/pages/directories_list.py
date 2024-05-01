import reflex as rx
from webwizard.views.navbar import navbar_app
from webwizard.views.footer import footer

hover_scale = 0.85

data = [
    {"Website": "https://producthunt.com", "Link Strength": "21"},
    {"Website": "https://theresanaiforthat.com", "Link Strength": "17"},
    {"Website": "https://indiepa.ge", "Link Strength": "5"},
    {"Website": "https://devhunt.org", "Link Strength": "1"},
    {"Website": "https://freestuff.dev", "Link Strength": "46"},
    {"Website": "https://yourstory.com", "Link Strength": "22"},
    {"Website": "https://pitchwall.co", "Link Strength": "10"},
    {"Website": "https://landingfolio.com", "Link Strength": "9"},
    {"Website": "https://uneed.best", "Link Strength": "5"},
    {"Website": "https://spotsaas.com", "Link Strength": "8"},
    {"Website": "https://toolify.ai", "Link Strength": "9"},
    {"Website": "https://obt.ai", "Link Strength": "2"},
    {"Website": "https://aitoptools.com", "Link Strength": "9"},
    {"Website": "https://airepo.io", "Link Strength": "2"},
    {"Website": "https://list.ly", "Link Strength": "14"},
    {"Website": "https://read.cv", "Link Strength": "10"},
    {"Website": "https://trackawesomelist.com", "Link Strength": "7"},
    {"Website": "https://appsumo.com", "Link Strength": "18"},
    {"Website": "https://futurepedia.io", "Link Strength": "12"},
    {"Website": "https://ctrlalt.cc", "Link Strength": "6"},
    {"Website": "https://webwiki.com", "Link Strength": "13"},
    {"Website": "https://launched.io", "Link Strength": "7"},
    {"Website": "https://microsaasaffiliate.com", "Link Strength": "23"},
    {"Website": "https://medium.com", "Link Strength": "11"},
    {"Website": "https://dev.to", "Link Strength": "18"},
    {"Website": "https://news.ycombinator.com", "Link Strength": "35"},
    {"Website": "https://alternativeto.net", "Link Strength": "19"}
]



@rx.page(route="/directories-list", title="Directorios | WebWizard")
def directories_list() -> rx.Component:
    return rx.box(
        navbar_app(),
        rx.el.section(
            rx.el.h1("Amplía tu audiencia y mejora la autoridad de tu web al publicar en múltiples plataformas seleccionadas (con requisitos específicos para cada una)",
                     class_name="lg:text-xl text-base font-medium text-start text-balance"),
            _directories_display(),
            class_name="flex flex-col justify-between lg:gap-10 gap-5 lg:mt-10 mt-5"
        ),
        footer(),
        class_name="px-5 max-w-[90rem] mx-auto w-full pb-8"
    )

def _directories_display() -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("Nombre"),
                rx.table.column_header_cell("Link Strength"),
                rx.table.column_header_cell("Web"),
            ),
        ),
        rx.table.body(
            *[
                _table_row(page["Website"], page["Link Strength"])
                for page in data
            ],
        ),
    )
    

def _table_row(name: str, ls: str) -> rx.Component:
    return rx.table.row(
        rx.table.row_header_cell(rx.box(rx.image(src=name+"/favicon.ico", width=22,
                                 height=22), name.replace("https://", ""), class_name="flex flex-row items-center gap-2"),),
        rx.table.cell(ls),
        rx.table.cell(rx.button("Visitar", on_click=rx.redirect(name))),
    )
