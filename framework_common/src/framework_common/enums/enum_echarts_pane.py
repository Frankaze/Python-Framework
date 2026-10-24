"""Chart panes used when indicators build ECharts options."""

from enum import Enum


class EnumEchartsPane(Enum):
    """Place an indicator series on the price pane or a separate pane."""

    # region Constants

    MAIN: str = "Main"
    SUB: str = "Sub"

    # endregion Constants
