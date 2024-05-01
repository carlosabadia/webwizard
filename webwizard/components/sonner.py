"""Reflex custom component SonnerToast."""

# Imported from https://github.com/ElijahAhianyo/reflex-sonner-toast

from typing import Literal, Any, Dict
import reflex as rx
from reflex.utils.imports import ImportVar
from reflex.vars import BaseVar, VarData
from reflex.components.component import ComponentNamespace
from reflex.utils.serializers import serialize
from reflex.utils import format

toast_var_data = VarData(  # type: ignore
    imports={
        f"sonner": {ImportVar(tag="toast")},
    },
)


class CommonProps(rx.Component):
    theme: rx.Var[Literal["light", "dark", "system"]] = rx.Var.create("light")
    rich_colors: rx.Var[bool] = False
    expand: rx.Var[bool] = False
    visible_toasts: rx.Var[int] = 1
    position: rx.Var[
        Literal["top-left", "top-center", "top-right", "bottom-left", "bottom-center", "bottom-right"]] = rx.Var.create(
        "bottom-right")
    close_button: rx.Var[bool] = False
    offset: rx.Var[str] = "32px"
    dir: rx.Var[Literal["ltr", "rtl"]]
    hot_key: rx.Var[str] = "⌥/alt + T"
    invert: rx.Var[bool] = False
    toast_options: rx.Var[int] = 4000
    gap: rx.Var[int] = 14
    pauses_when_page_is_hidden: rx.Var[bool] = False


class Toast(rx.Fragment, CommonProps):
    method_name: str = "toast"

    @classmethod
    def create(cls, content, **kwargs):
        comp = super().create(*[content], **kwargs)
        return rx.call_script(cls.get_toast_var(content, comp.method_name, comp.render()["props"]))

    @staticmethod
    def format(prop: str):
        new = prop.split("=")
        if (p := new[-1]).startswith("{{"):
            p = p.replace("{{", "{").replace("}}", "}")
        else:
            p = p.strip('{}')
        return ':'.join([new[0], p])

    @classmethod
    def get_toast_var(cls, content, method_name, props):
        prop_str = format.wrap(", ".join([cls.format(p) for p in props]), "{")
        toast_var = BaseVar(
            _var_name=f"{method_name}('{serialize(content)}', {prop_str})",
            _var_type=str,
            _var_data=toast_var_data,
        )
        return toast_var

    def _get_style(self) -> dict:
        return {"style": self.style}

    def _exclude_props(self) -> list[str]:
        return ["method_name"]


open_var_data = VarData(
    hooks={
        "const [open, setOpen] = useState(true)": None,
    },
)

open = BaseVar(
    _var_name="() => setOpen(false)",
    _var_type=str,
    _var_data=open_var_data
)

on_click = rx.call_script(open)


class ToastMessage(Toast):
    method_name = "toast.message"


class ToastError(Toast):
    method_name = "toast.error"


class ToastSuccess(Toast):
    method_name = "toast.success"


class ToastCustom(Toast):
    method_name = "toast.custom"


class ToastLoading(Toast):
    method_name = "toast.loading"


class Toaster(CommonProps, rx.Component):
    library = "sonner"
    # The React component tag.
    tag = "Toaster"


class SonnerToast(ComponentNamespace):
    messaage = staticmethod(ToastMessage.create)
    success = staticmethod(ToastSuccess.create)
    error = staticmethod(ToastError.create)
    loading = staticmethod(ToastLoading.create)
    custom = staticmethod(ToastCustom.create)
    __call__ = staticmethod(Toast.create)


toaster = Toaster.create
toast = SonnerToast()
