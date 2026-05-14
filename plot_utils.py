# aquarel_pagx.py
from __future__ import annotations
import os
from typing import Optional, Tuple
from matplotlib import font_manager as fm
from matplotlib.font_manager import FontProperties
from aquarel import Theme
import numpy as np 
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from PIL import Image
import io
import pandas as pd
from matplotlib.patches import Patch

# Default font locations on macOS; adjust if needed
DEFAULT_PAGX_REG = [
    os.path.expanduser("~/Library/Fonts/TeXGyrePagellaX-Regular.otf"),
    "/Library/Fonts/TeXGyrePagellaX-Regular.otf",
]
DEFAULT_PAGX_BOLD = [
    os.path.expanduser("~/Library/Fonts/TeXGyrePagellaX-Bold.otf"),
    "/Library/Fonts/TeXGyrePagellaX-Bold.otf",
]


def _first_existing(paths) -> Optional[str]:
    for p in paths:
        if p and os.path.isfile(p):
            return p
    return None


def _register_pagx_fonts() -> Tuple[str, str, str, str]:
    """Register PagellaX Regular & Bold fonts. Returns (reg_path, bold_path, reg_name, bold_name)."""
    reg = _first_existing(DEFAULT_PAGX_REG)
    bold = _first_existing(DEFAULT_PAGX_BOLD)

    if not reg or not os.path.isfile(reg):
        raise FileNotFoundError(
            "TeXGyrePagellaX-Regular.otf not found. Install in ~/Library/Fonts/ or pass explicit path."
        )
    if not bold or not os.path.isfile(bold):
        raise FileNotFoundError(
            "TeXGyrePagellaX-Bold.otf not found. Install in ~/Library/Fonts/ or pass explicit path."
        )

    fm.fontManager.addfont(reg)
    fm.fontManager.addfont(bold)
    reg_name = FontProperties(fname=reg).get_name()
    bold_name = FontProperties(fname=bold).get_name()
    return reg, bold, reg_name, bold_name


def style_legend(ax, title = "Legend", loc = "lower center", bbox_to_anchor1 = 0.5,
                 bbox_to_anchor2 = -0.35, n_col = 0) -> None:
    """
    Apply 'regular labels + bold title' to the legend on `ax`, using the
    already-installed TeX Gyre PagellaX Regular/Bold fonts.

    - Uses the EXISTING legend if present (keeps its title text).
    - Creates a legend if none exists.
    - Returns None to avoid Jupyter auto-displaying an artist.
    """
    handles, labels = ax.get_legend_handles_labels()
    if n_col == 0:
        ax.legend(
            handles, labels,
            title= title,
            ncol=len(handles),                  # all items in one row
            bbox_to_anchor=(bbox_to_anchor1, bbox_to_anchor2),
            loc=loc
        )
    else: 
        ax.legend(
            handles, labels,
            title= title,
            ncol=n_col,                  # all items in one row
            bbox_to_anchor=(bbox_to_anchor1, bbox_to_anchor2),
            loc=loc
        )

    # Ensure fonts are registered and get file paths for FontProperties
    reg_path, bold_path, _, _ = _register_pagx_fonts()

    reg_prop  = FontProperties(fname=reg_path)
    bold_prop = FontProperties(fname=bold_path)

    leg = ax.get_legend()
    if leg is None:
        # create a legend with default settings; don't pass a title so we
        # don't overwrite later if user sets it afterwards
        leg = ax.legend()

    # Keep the current title text (if any)
    title_text = leg.get_title().get_text()

    # Labels regular
    for txt in leg.get_texts():
        txt.set_fontproperties(reg_prop)

    # Title bold (only if there is a title)
    if title_text:
        leg.get_title().set_fontproperties(bold_prop)

    # Do NOT return the legend artist (prevents Jupyter from displaying it)
    return None

def make_theme_light():
    _, _, _, bold_name = _register_pagx_fonts()
    return (
        Theme(name="pagx_bold_light", description="PagellaX bold default (light)")
        .set_axes(width=1.0, top=True, right=True)
        .set_grid(draw=True, width=0.6, style=":", alpha=0.5)
        .set_color(
            palette=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"],
            text_color="#222",
            axes_color="#333",
            tick_color="#666",
            tick_label_color="#333",
            grid_color="#bbb",
            legend_background_color="#fff",
            legend_border_color="#ddd",
            plot_background_color="#fff",
            figure_background_color="#fff",
        )
        .set_overrides({
            "figure.dpi": 300,
            "savefig.dpi": 300,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
            "text.antialiased": True,
            "lines.antialiased": True,
            "legend.frameon": True,
            "legend.framealpha": 1.0,
            "legend.fancybox": True,
            "font.family": bold_name,
            "font.weight": "bold",        # this selects the bold face if available
            "mathtext.fontset": "custom",
            "mathtext.rm": bold_name,
            "axes.titleweight": "bold",
            "axes.labelweight": "bold",
            "figure.titleweight": "bold",
            "axes.titlesize": 14,
            "axes.labelsize": 14,
            "xtick.labelsize": 14,
            "ytick.labelsize": 14,
            "legend.fontsize": 14,
            "axes.edgecolor": "#333",
            "axes.linewidth": 1.2,
            "xtick.top": True,
            "ytick.right": True,
            "xtick.direction": "out",
            "ytick.direction": "out",
        })
    )


def make_theme_dark():
    _, _, _, bold_name = _register_pagx_fonts()
    return (
        Theme(name="pagx_bold_dark", description="PagellaX bold default (dark)")
        .set_axes(width=1.0, top=True, right=True)
        .set_grid(draw=True, width=0.6, style=":", alpha=0.5)
        .set_color(
            palette=["#4cc9f0", "#ffb703", "#80ed99", "#ff6b6b", "#b28dff", "#ffd166"],
            text_color="#e6e6e6",
            axes_color="#d8d8d8",
            tick_color="#bfbfbf",
            tick_label_color="#cccccc",
            grid_color="#ffffff",
            legend_background_color="#1b1e24",
            legend_border_color="#3a3f4b",
            plot_background_color="#0f1116",
            figure_background_color="#0c0e13",
        )
        .set_overrides({
            "figure.dpi": 300,
            "savefig.dpi": 300,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
            "text.antialiased": True,
            "lines.antialiased": True,
            "legend.frameon": True,
            "legend.framealpha": 1.0,
            "legend.fancybox": True,
            "font.family": bold_name,
            "font.weight": "bold",        # this selects the bold face if available
            "mathtext.fontset": "custom",
            "mathtext.rm": bold_name,
            "axes.titleweight": "bold",
            "axes.labelweight": "bold",
            "figure.titleweight": "bold",
            "axes.titlesize": 14,
            "axes.labelsize": 14,
            "xtick.labelsize": 14,
            "ytick.labelsize": 14,
            "legend.fontsize": 14,
            "axes.edgecolor": "#333",
            "axes.linewidth": 1.2,
            "xtick.top": True,
            "ytick.right": True,
            "xtick.direction": "out",
            "ytick.direction": "out",
        })
    )



def _snap_up_to_trading(targets: pd.DatetimeIndex, trading: pd.DatetimeIndex):
    """For each target date, return the first trading day >= target.
       Skip if target is after the last trading day. De-duplicate consecutive hits."""
    snapped = []
    for t in targets:
        i = trading.searchsorted(t, side="left")  # first index with trading[i] >= t
        if i >= len(trading):
            continue  # no trading day on/after target → skip
        chosen = trading[i]
        if not snapped or snapped[-1] != chosen:
            snapped.append(chosen)
    return snapped


def _resolve_fmt(fmt: str, mon_text: bool):
    """Return strftime format string with optional month text conversion."""
    fmt_map = {
        "ymd": "%Y-%m-%d",
        "ym": "%Y-%m",
        "md": "%m-%d",
        "ydm": "%Y-%d-%m",
        "dm": "%d-%m",
        "y": "%Y",
        "m" : "%m"
    }
    if fmt not in fmt_map:
        raise ValueError("fmt ∈ {'ymd','ym','md','ydm','dm','y', 'm'}")

    f = fmt_map[fmt]
    if mon_text:
        # Replace numeric month %m with abbreviated month %b
        f = f.replace("%m", "%b")
    return f


def format_date_axis(ax, x, freq: str = "bom", fmt: str = "ymd", rotate: int = 45, ha_mode : str = "left", every: int = 1, mon_text: bool = False):
    """Bottom x-axis: ticks snapped UP to trading days in x."""
    x_s = pd.Series(x)
    x_dt = pd.to_datetime(x_s, errors="coerce").dt.normalize()
    if x_dt.isna().any():
        raise ValueError("Some x values could not be parsed as dates.")
    trading = pd.DatetimeIndex(x_dt.unique()).sort_values()

    start, end = trading[0], trading[-1]
    if freq == "bom":
        targets = pd.date_range(start=start, end=end, freq="MS")
    elif freq == "weekbegin":
        targets = pd.date_range(start=start, end=end, freq="W-MON")
    elif freq == "boy":
        targets = pd.date_range(start=start, end=end, freq="YS")
    else:
        raise ValueError("freq must be one of {'bom','weekbegin','boy'}.")

    snapped = _snap_up_to_trading(targets, trading)
    snapped = snapped[::every] 
    fmt_str = _resolve_fmt(fmt, mon_text)
    labels  = [d.strftime(fmt_str) for d in snapped]

    # Is the axis datetime or categorical?
    is_dt = False
    try:
        lines = ax.get_lines()
        if lines:
            xd = lines[0].get_xdata()
            is_dt = np.issubdtype(np.array(xd).dtype, np.datetime64)
    except Exception:
        pass

    if is_dt:
        ax.set_xticks([pd.Timestamp(d).to_pydatetime() for d in snapped])
        ax.set_xticklabels(labels, rotation=rotate, ha=ha_mode, rotation_mode="anchor")
    else:
        first_idx = {}
        for i, d in enumerate(x_dt):
            if d not in first_idx:
                first_idx[d] = i
        positions = [first_idx[d] for d in snapped if d in first_idx]
        ax.set_xticks(positions)
        ax.set_xticklabels(labels, rotation=rotate, ha=ha_mode, rotation_mode="anchor")

    ax.margins(x=0.01)


def add_date_axis_top(ax, x, freq: str = "bom", fmt: str = "ymd",
                      rotate: int = 45, tick_length: int = 8, ha_mode : str = "left", 
                      every : int = 1, mon_text: bool = False, vlines: bool = False, vline_kw: dict = None):
    """Top x-axis: ticks snapped UP to trading days in x."""
    x_s = pd.Series(x)
    x_dt = pd.to_datetime(x_s, errors="coerce").dt.normalize()
    if x_dt.isna().any():
        raise ValueError("Some x values could not be parsed as dates.")
    trading = pd.DatetimeIndex(x_dt.unique()).sort_values()

    start, end = trading[0], trading[-1]
    if freq == "bom":
        targets = pd.date_range(start=start, end=end, freq="MS")
    elif freq == "weekbegin":
        targets = pd.date_range(start=start, end=end, freq="W-MON")
    elif freq == "boy":
        targets = pd.date_range(start=start, end=end, freq="YS")
    else:
        raise ValueError("freq must be one of {'bom','weekbegin','boy'}.")

    snapped = _snap_up_to_trading(targets, trading)
    snapped = snapped[::every] 
    fmt_str = _resolve_fmt(fmt, mon_text)
    labels  = [d.strftime(fmt_str) for d in snapped]


    ax_top = ax.secondary_xaxis("top")

    is_dt = False
    try:
        lines = ax.get_lines()
        if lines:
            xd = lines[0].get_xdata()
            is_dt = np.issubdtype(np.array(xd).dtype, np.datetime64)
    except Exception:
        pass

    if is_dt:
        xtick_pos = [pd.Timestamp(d).to_pydatetime() for d in snapped]
        ax_top.set_xticks(xtick_pos)
        ax_top.set_xticklabels(labels, rotation=rotate, ha=ha_mode, rotation_mode="anchor")
    else:
        first_idx = {}
        for i, d in enumerate(x_dt):
            if d not in first_idx:
                first_idx[d] = i
        #positions = [first_idx[d] for d in snapped if d in first_idx]
        xtick_pos = [first_idx[d] for d in snapped if d in first_idx]
        ax_top.set_xticks(xtick_pos)
        ax_top.set_xticklabels(labels, rotation=rotate, ha=ha_mode, rotation_mode="anchor")

    ax_top.tick_params(axis="x", which="major", length=tick_length)
    if vlines:
        if vline_kw is None:
            vline_kw = dict(color="grey", linestyle="--", linewidth=0.8, alpha=0.7)
        for xpos in xtick_pos:
            ax.axvline(x=xpos, **vline_kw)

    
    return ax_top


def combine_plots(
    plots,
    suptitle="",
    nrow=1,
    ncol=2,
    dpi=300,
    base_figsize=(8, 6),
    show=False,
    *,
    title_fontsize=16,
    title_y_offset=0.98,
    gridlines=None,          # None | "grid" | "h" | "v"
    grid_lw=0.8,
    grid_lc="0.7",
):
    total_width = base_figsize[0] * ncol
    total_height = base_figsize[1] * nrow

    fig, axs = plt.subplots(
        nrow, ncol,
        figsize=(total_width, total_height),
        dpi=dpi
    )
    axs = np.array(axs).reshape(nrow, ncol)

    for idx, plot in enumerate(plots):
        r, c = divmod(idx, ncol)
        ax = axs[r, c]

        buf = io.BytesIO()
        plot.savefig(buf, format="png", bbox_inches="tight")
        buf.seek(0)
        img = Image.open(buf)

        ax.imshow(img)
        ax.axis("off")

    # Turn off unused axes
    for idx in range(len(plots), nrow * ncol):
        r, c = divmod(idx, ncol)
        axs[r, c].axis("off")

    if suptitle:
        fig.suptitle(
            suptitle,
            fontsize=title_fontsize,
            y=title_y_offset
        )

    fig.tight_layout(rect=[0, 0, 1, title_y_offset - 0.02])

    # --- GRIDLINES (figure-level, layout-aware) ---
    # --- GRIDLINES (respect suptitle area) ---
    if gridlines is not None:
        if gridlines not in {"grid", "h", "v"}:
            raise ValueError("gridlines must be one of None, 'grid', 'h', 'v'.")

        # get subplot area bounds AFTER tight_layout
        top = fig.subplotpars.top
        bottom = fig.subplotpars.bottom
        left = fig.subplotpars.left
        right = fig.subplotpars.right

        # vertical separators
        if gridlines in {"grid", "v"}:
            for c in range(1, ncol):
                x = left + (right - left) * c / ncol
                fig.add_artist(
                    plt.Line2D(
                        [x, x], [bottom, top],
                        transform=fig.transFigure,
                        linewidth=grid_lw,
                        color=grid_lc,
                        zorder=10,
                    )
                )

        # horizontal separators
        if gridlines in {"grid", "h"}:
            for r in range(1, nrow):
                y = top - (top - bottom) * r / nrow
                fig.add_artist(
                    plt.Line2D(
                        [left, right], [y, y],
                        transform=fig.transFigure,
                        linewidth=grid_lw,
                        color=grid_lc,
                        zorder=10,
                    )
                )

    if show:
        plt.show()

    return fig, axs



def legend_separate_fig(
    ax=None,
    fig=None,
    *,
    title=None,
    figsize=(8, 1),
    dpi=300,
    ncol=None,
    loc="center",
    handlelength=2.8,
    columnspacing=1.0,
    handletextpad=0.6,
    borderaxespad=0.0,
    sort_legend=None,   # <-- NEW: None | "alphabetical" | "reverse"
    **kwargs
):
    """
    Internal constructor: Creates the figure and calculates the
    exact bounding box of the legend frame.

    sort_legend:
      - None: keep original order
      - "alphabetical": sort labels A->Z (case-insensitive)
      - "reverse": reverse alphabetical 
    """
    if (ax is None) == (fig is None):
        raise ValueError("Provide exactly one of ax=... or fig=...")

    axes = [ax] if ax is not None else list(fig.axes)

    seen = set()
    handles, labels = [], []
    for a in axes:
        h, l = a.get_legend_handles_labels()
        for hh, ll in zip(h, l):
            if not ll or ll.startswith("_") or ll in seen:
                continue
            seen.add(ll)
            handles.append(hh)
            labels.append(ll)

    if not handles:
        raise ValueError("No legend entries found.")

    # --- sorting (keeps handle-label pairing) ---
    if sort_legend is not None:
        if sort_legend not in {"alphabetical", "reverse"}:
            raise ValueError("sort_legend must be None, 'alphabetical', or 'reverse'.")

        pairs = list(zip(labels, handles))

        if sort_legend == "alphabetical":
            pairs.sort(key=lambda x: x[0].casefold())
        elif sort_legend == "reverse":
            pairs.sort(key=lambda x: x[0].casefold(), reverse=True)

        labels, handles = zip(*pairs)
        labels, handles = list(labels), list(handles)

    if ncol is None:
        ncol = len(handles)

    fig_leg = plt.figure(figsize=figsize, dpi=dpi)
    ax_leg = fig_leg.add_subplot(111)
    ax_leg.axis("off")

    leg = ax_leg.legend(
        handles,
        labels,
        title=title,
        loc=loc,
        ncol=ncol,
        frameon=True,
        handlelength=handlelength,
        columnspacing=columnspacing,
        handletextpad=handletextpad,
        borderaxespad=borderaxespad,
        **kwargs
    )

    fig_leg.canvas.draw()
    bbox = leg.get_window_extent().transformed(fig_leg.dpi_scale_trans.inverted())

    return fig_leg, bbox

def get_legend_trimmed(ax=None, fig=None, filepath=None, show=True, **kwargs):
    """
    Wrapper function: 
    - Calls the constructor.
    - Saves to 'filepath' if provided (acts as boolean indicator).
    - Shows the figure if 'show' is True.
    """
    # 1. Generate the figure and the calculated crop box
    legfig, tight_bbox = legend_separate_fig(ax=ax, fig=fig, **kwargs)

    # 2. Save only if filepath is provided
    if filepath:
        legfig.savefig(
            filepath, 
            bbox_inches=tight_bbox, 
            pad_inches=0
        )
        print(f"Legend saved to: {filepath}")

    # 3. Show logic
    if show:
        plt.show()
    else:
        plt.close(legfig)

    return legfig

def combine_plots_and_legend_row(
    plots,
    legend_fig,
    *,
    nrow_plots,
    ncol,
    legend_row,              # <-- NEW: explicit row index
    suptitle="",
    dpi=300,
    base_figsize=(8, 6),
    legend_height_ratio=0.25,
    show=False,
    title_fontsize=16,
    title_y_offset=0.98,
):
    """
    Combine plots in a grid and place a legend on its own row
    specified by legend_row (0-indexed).

    Total rows = nrow_plots + 1
    Legend spans all columns.
    """

    import matplotlib.pyplot as plt
    import numpy as np
    import io
    from PIL import Image
    from matplotlib.gridspec import GridSpec

    total_rows = nrow_plots + 1
    if not (0 <= legend_row < total_rows):
        raise ValueError("legend_row must be between 0 and nrow_plots (inclusive).")

    total_width = base_figsize[0] * ncol
    total_height = base_figsize[1] * (nrow_plots + legend_height_ratio)

    fig = plt.figure(figsize=(total_width, total_height), dpi=dpi)

    # Build height ratios with legend row inserted
    height_ratios = []
    for r in range(total_rows):
        if r == legend_row:
            height_ratios.append(legend_height_ratio)
        else:
            height_ratios.append(1.0)

    gs = GridSpec(
        nrows=total_rows,
        ncols=ncol,
        height_ratios=height_ratios,
        figure=fig,
    )

    def _fig_to_image(fig_obj):
        buf = io.BytesIO()
        fig_obj.savefig(buf, format="png", bbox_inches="tight", pad_inches=0)
        buf.seek(0)
        return Image.open(buf)

    # --- fill plot rows (skip legend_row) ---
    plot_idx = 0
    for r in range(total_rows):
        if r == legend_row:
            continue
        for c in range(ncol):
            ax = fig.add_subplot(gs[r, c])
            if plot_idx < len(plots):
                img = _fig_to_image(plots[plot_idx])
                ax.imshow(img)
                ax.axis("off")
                plot_idx += 1
            else:
                ax.axis("off")

    # --- legend row ---
    ax_leg = fig.add_subplot(gs[legend_row, :])
    img_leg = _fig_to_image(legend_fig)
    ax_leg.imshow(img_leg)
    ax_leg.axis("off")

    if suptitle:
        fig.suptitle(suptitle, fontsize=title_fontsize, y=title_y_offset)

    plt.tight_layout(rect=[0, 0, 1, title_y_offset - 0.02])

    if show:
        plt.show()

    return fig

def save_pub(fig, path, *, transparent=False, pad=0, tight=True, dpi=None):
    kw = {}
    if tight:
        kw["bbox_inches"] = "tight"
        kw["pad_inches"] = pad
    if transparent:
        kw["transparent"] = True
        kw["facecolor"] = "none"
        kw["edgecolor"] = "none"
    if dpi is not None:
        kw["dpi"] = dpi
    fig.savefig(path, **kw)

    import io
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from textwrap import fill

def annotate_fig_text(
    fig,
    text,
    *,
    where="bottom",          # "bottom" | "top" | "right" | "left" | "overlay"
    dpi=300,
    wrap_chars=110,          # naive but effective for paragraphs
    text_fontsize=12,
    text_ha="left",
    text_va="top",
    text_pad=0.03,           # padding inside text axes (axes coords)
    text_ratio=0.22,         # fraction of figure reserved for text panel (non-overlay)
    box=True,
    box_alpha=0.08,
    box_pad=0.4,
    bbox_inches="tight",
    pad_inches=0,
):
    """
    Return a NEW figure that contains the rendered input figure plus a text panel.

    Notes:
    - This rasterizes the original figure into an image (consistent with your combine workflow).
    - Use where="overlay" to draw text on top of the image instead of adding a new panel.
    """

    # render original fig to image
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches=bbox_inches, pad_inches=pad_inches, dpi=dpi)
    buf.seek(0)
    img = Image.open(buf).copy()
    buf.close()

    wrapped = fill(text, width=wrap_chars) if wrap_chars else text

    if where == "overlay":
        # same size as original image
        w_px, h_px = img.size
        figsize = (w_px / dpi, h_px / dpi)
        out = plt.figure(figsize=figsize, dpi=dpi)
        ax = out.add_axes([0, 0, 1, 1])
        ax.imshow(img)
        ax.axis("off")

        bbox = None
        if box:
            bbox = dict(boxstyle=f"round,pad={box_pad}", fc="white", ec="none", alpha=box_alpha)

        ax.text(
            text_pad, 1 - text_pad, wrapped,
            transform=ax.transAxes,
            ha=text_ha, va=text_va,
            fontsize=text_fontsize,
            bbox=bbox
        )
        return out

    # non-overlay: add a dedicated text panel
    w_px, h_px = img.size
    base_w, base_h = (w_px / dpi, h_px / dpi)

    if where in {"bottom", "top"}:
        out = plt.figure(figsize=(base_w, base_h * (1 + text_ratio)), dpi=dpi)
        if where == "top":
            ax_text = out.add_axes([0, 1 - text_ratio, 1, text_ratio])
            ax_img  = out.add_axes([0, 0, 1, 1 - text_ratio])
        else:
            ax_img  = out.add_axes([0, text_ratio, 1, 1 - text_ratio])
            ax_text = out.add_axes([0, 0, 1, text_ratio])

    elif where in {"right", "left"}:
        out = plt.figure(figsize=(base_w * (1 + text_ratio), base_h), dpi=dpi)
        if where == "left":
            ax_text = out.add_axes([0, 0, text_ratio, 1])
            ax_img  = out.add_axes([text_ratio, 0, 1 - text_ratio, 1])
        else:
            ax_img  = out.add_axes([0, 0, 1 - text_ratio, 1])
            ax_text = out.add_axes([1 - text_ratio, 0, text_ratio, 1])
    else:
        raise ValueError("where must be one of 'bottom','top','right','left','overlay'.")

    ax_img.imshow(img)
    ax_img.axis("off")

    ax_text.axis("off")
    bbox = None
    if box:
        bbox = dict(boxstyle=f"round,pad={box_pad}", fc="white", ec="none", alpha=box_alpha)

    ax_text.text(
        text_pad, 1 - text_pad, wrapped,
        transform=ax_text.transAxes,
        ha=text_ha, va=text_va,
        fontsize=text_fontsize,
        bbox=bbox
    )

    return out

def _rgba_from_facecolor(fc):
    fc = np.asarray(fc)
    if fc.size == 0:
        return None
    if fc.ndim == 1:
        return tuple(fc.tolist()) if fc.shape[0] == 4 else None
    return tuple(fc[0].tolist()) if fc.shape[-1] == 4 else None

def legend_separate_fig_area(
    ax,
    *,
    title=None,
    figsize=(14, 1),          # wider default
    dpi=300,
    ncol=1,
    loc="center",
    handlelength=2.8,
    columnspacing=1.0,
    handletextpad=0.6,
    borderaxespad=0.0,
    sort_legend=None,
    prefer_existing_legend=True,
    force_ncol=True,          # NEW
    **kwargs
):
    seen = set()
    handles, labels = [], []

    if prefer_existing_legend and ax.get_legend() is not None:
        leg0 = ax.get_legend()
        for h, t in zip(leg0.legend_handles, leg0.get_texts()):
            label = t.get_text()
            if not label or label.startswith("_") or label in seen:
                continue
            seen.add(label)

            if hasattr(h, "get_facecolor"):
                rgba = _rgba_from_facecolor(h.get_facecolor())
                handles.append(Patch(facecolor=rgba, edgecolor="none") if rgba else h)
            else:
                handles.append(h)
            labels.append(label)

    if not handles:
        for coll in getattr(ax, "collections", []):
            label = getattr(coll, "get_label", lambda: None)()
            if not label or label.startswith("_") or label in seen:
                continue
            rgba = _rgba_from_facecolor(coll.get_facecolor())
            if rgba is None:
                continue
            handles.append(Patch(facecolor=rgba, edgecolor="none"))
            labels.append(label)
            seen.add(label)

    if not handles:
        raise ValueError("No legend entries found.")

    if sort_legend is not None:
        if sort_legend not in {"alphabetical", "reverse"}:
            raise ValueError("sort_legend must be None, 'alphabetical', or 'reverse'.")
        pairs = list(zip(labels, handles))
        pairs.sort(key=lambda x: x[0].casefold(), reverse=(sort_legend == "reverse"))
        labels, handles = map(list, zip(*pairs))

    fig_leg = plt.figure(figsize=figsize, dpi=dpi)
    ax_leg = fig_leg.add_subplot(111)
    ax_leg.axis("off")

    # Key: mode="expand" + bbox_to_anchor spanning the axes width
    legend_kwargs = dict(
        title=title,
        loc=loc,
        ncol=ncol,
        frameon=True,
        handlelength=handlelength,
        columnspacing=columnspacing,
        handletextpad=handletextpad,
        borderaxespad=borderaxespad,
    )

    if force_ncol:
        legend_kwargs.update(
            mode="expand",
            bbox_to_anchor=(0, 0, 1, 1),   # fill full axes
            bbox_transform=ax_leg.transAxes
        )

    legend_kwargs.update(kwargs)

    leg = ax_leg.legend(handles, labels, **legend_kwargs)

    fig_leg.canvas.draw()
    bbox = leg.get_window_extent().transformed(fig_leg.dpi_scale_trans.inverted())
    return fig_leg, bbox

def get_legend_trimmed_area(ax, filepath=None, show=True, **kwargs):
    legfig, tight_bbox = legend_separate_fig_area(ax=ax, **kwargs)

    if filepath:
        legfig.savefig(filepath, bbox_inches=tight_bbox, pad_inches=0)
        print(f"Legend saved to: {filepath}")

    if show:
        plt.show()
    else:
        plt.close(legfig)

    return legfig
