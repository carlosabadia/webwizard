import reflex as rx
from typing import Any, Dict, List, Optional, Set, Union

# Imported from https://github.com/Alek99/reflex-motion

class Motion(rx.Component):
    """Motion component."""

    # The React library to wrap.
    library = "framer-motion"

    # The React component tag.
    tag = "motion.div"

    # The initial state of the component.
    initial: rx.Var[Union[Dict[str, Union[float, str]], str]]

    # The animate state of the component.
    animate: rx.Var[Dict[str, Union[float, str]]]

    # The transition
    transition: rx.Var[Union[Dict[str, Union[float, str]], str]]

    # What the component does when it's hovered.
    while_hover: rx.Var[Union[Dict[str, Union[float, str]], str]]

    # What the component does when it's tapped.
    while_tap: rx.Var[Union[Dict[str, Union[float, str]], str]]

    # What the component does when it's in view.
    while_in_view: rx.Var[Union[Dict[str, Union[float, str]], str]]

    # What the component does when its focused.
    while_focus: rx.Var[Union[Dict[str, Union[float, str]], str]]

    # What the component does when it's out of view.
    viewport: rx.Var[Union[str, List[str], Dict[str, Union[float, str]]]]

motion = Motion.create
