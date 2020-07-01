import sys

if sys.version_info < (3, 7):
    from ._opacity import OpacityValidator
    from ._fillcolor import FillcolorValidator
else:
    from _plotly_utils.importers import relative_import

    __all__, __getattr__, __dir__ = relative_import(
        __name__, [], ["._opacity.OpacityValidator", "._fillcolor.FillcolorValidator"]
    )
