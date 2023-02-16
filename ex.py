from bokeh.plotting import curdoc, figure, show
from bokeh.sampledata.periodic_table import elements
from bokeh.transform import dodge, factor_cmap

periods = ["I", "II", "III", "IV", "V", "VI", "VII"]
groups = [str(x) for x in range(1, 19)]

df = elements.copy()
df["atomic mass"] = df["atomic mass"].astype(str)
df["group"] = df["group"].astype(str)
df["period"] = [periods[x - 1] for x in df.period]
df = df[df.group != "-"]
df = df[df.symbol != "Lr"]
df = df[df.symbol != "Lu"]

cmap = {
    "alkali metal": "#a6cee3",
    "alkaline earth metal": "#1f78b4",
    "metal": "#d93b43",
    "halogen": "#999d9a",
    "metalloid": "#e08d49",
    "noble gas": "#eaeaea",
    "nonmetal": "#f1d4Af",
    "transition metal": "#599d7A",
}

TOOLTIPS = [
    ("Name", "@name"),
    ("Atomic number", "@{atomic number}"),
    ("Atomic mass", "@{atomic mass}"),
    ("Type", "@metal"),
    ("CPK color", "$color[hex, swatch]:CPK"),
    ("Electronic configuration", "@{electronic configuration}"),
]

p = figure(
    title="Periodic Table (omitting LA and AC Series)",
    width=1000,
    height=450,
    x_range=groups,
    y_range=list(reversed(periods)),
    tools="hover",
    toolbar_location=None,
    tooltips=TOOLTIPS,
)

r = p.rect(
    "group",
    "period",
    0.95,
    0.95,
    source=df,
    fill_alpha=0.6,
    legend_field="metal",
    color=factor_cmap("metal", palette=list(cmap.values()), factors=list(cmap.keys())),
)

text_props = dict(source=df, text_align="left", text_baseline="middle")

x = dodge("group", -0.4, range=p.x_range)

p.text(x=x, y="period", text="symbol", text_font_style="bold", **text_props)

p.text(
    x=x,
    y=dodge("period", 0.3, range=p.y_range),
    text="atomic number",
    text_font_size="11px",
    **text_props
)

p.text(
    x=x,
    y=dodge("period", -0.35, range=p.y_range),
    text="name",
    text_font_size="7px",
    **text_props
)

p.text(
    x=x,
    y=dodge("period", -0.2, range=p.y_range),
    text="atomic mass",
    text_font_size="7px",
    **text_props
)

p.text(
    x=["3", "3"],
    y=["VI", "VII"],
    text=["LA", "AC"],
    text_align="center",
    text_baseline="middle",
)

p.outline_line_color = None
p.grid.grid_line_color = None
p.axis.axis_line_color = None
p.axis.major_tick_line_color = None
p.axis.major_label_standoff = 0
p.legend.orientation = "horizontal"
p.legend.location = "top_center"
p.hover.renderers = [r]  # only hover element boxes

show(p)


import pandas as pd
from bokeh.layouts import column, row
from bokeh.models import Select
from bokeh.palettes import Spectral5
from bokeh.sampledata.autompg import autompg_clean as df

df = df.copy()

SIZES = list(range(6, 22, 3))
COLORS = Spectral5
N_SIZES = len(SIZES)
N_COLORS = len(COLORS)

# data cleanup
df.cyl = df.cyl.astype(str)
df.yr = df.yr.astype(str)
del df["name"]

columns = sorted(df.columns)
discrete = [x for x in columns if df[x].dtype == object]
continuous = [x for x in columns if x not in discrete]


def create_figure():
    xs = df[x.value].values
    ys = df[y.value].values
    x_title = x.value.title()
    y_title = y.value.title()

    kw = dict()
    if x.value in discrete:
        kw["x_range"] = sorted(set(xs))
    if y.value in discrete:
        kw["y_range"] = sorted(set(ys))
    kw["title"] = "%s vs %s" % (x_title, y_title)

    p = figure(height=600, width=800, tools="pan,box_zoom,hover,reset", **kw)
    p.xaxis.axis_label = x_title
    p.yaxis.axis_label = y_title

    if x.value in discrete:
        p.xaxis.major_label_orientation = pd.np.pi / 4

    sz = 9
    if size.value != "None":
        if len(set(df[size.value])) > N_SIZES:
            groups = pd.qcut(df[size.value].values, N_SIZES, duplicates="drop")
        else:
            groups = pd.Categorical(df[size.value])
        sz = [SIZES[xx] for xx in groups.codes]

    c = "#31AADE"
    if color.value != "None":
        if len(set(df[color.value])) > N_COLORS:
            groups = pd.qcut(df[color.value].values, N_COLORS, duplicates="drop")
        else:
            groups = pd.Categorical(df[color.value])
        c = [COLORS[xx] for xx in groups.codes]

    p.circle(
        x=xs,
        y=ys,
        color=c,
        size=sz,
        line_color="white",
        alpha=0.6,
        hover_color="white",
        hover_alpha=0.5,
    )

    return p


def update(attr, old, new):
    layout.children[1] = create_figure()


x = Select(title="X-Axis", value="mpg", options=columns)
x.on_change("value", update)

y = Select(title="Y-Axis", value="hp", options=columns)
y.on_change("value", update)

size = Select(title="Size", value="None", options=["None"] + continuous)
size.on_change("value", update)

color = Select(title="Color", value="None", options=["None"] + continuous)
color.on_change("value", update)

controls = column(x, y, color, size, width=200)
layout = row(controls, create_figure())
doc = curdoc()
doc.add_root(layout)
doc.title = "Crossfilter"

show(doc)
