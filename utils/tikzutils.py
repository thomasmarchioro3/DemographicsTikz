from .texutils import TexDocument


def make_histogram(hist_dict, colors, title=None, wbar=0.4, add_percent=True, scale=1):
    assert len(hist_dict) <= len(colors)
    s = ""
    s_scale =  "" if scale != 1 else f"[scale={scale:.2f}]"
    s = s_append(s, r"\begin{tikzpicture}"+s_scale, tab="")
    s = s_append(s, r"\begin{axis}[")
    s = s_append(s, r"tick align=outside,")
    s = s_append(s, r"tick pos=left,")
    xmin = -0.59
    xmax = len(hist_dict)-1+.59
    ymin = 0
    ymax = max(hist_dict.values())+2
    s = s_append(s, f"xmin={xmin:.2f}, xmax={xmax:.2f},")
    s = s_append(s, f"ymin={ymin:.0f}, ymax={ymax:.0f},")
    s = s_append(s, r"xtick={"+", ".join([str(i) for i in range(len(hist_dict))])+r"},")
    s = s_append(s, r"xticklabels={"+", ".join(hist_dict.keys())+r"},")
    if title is not None:
        s = s_append(s, r"title={"+title+r"},")
    s = s_append(s, r"]")
    for i, (count, color) in enumerate(zip(hist_dict.values(), colors)):
        htemp = r"\draw[draw=black, "
        htemp += f"fill={color}, "
        htemp += f"opacity=\opacity] "
        htemp += f"(axis cs:{i-wbar},0) rectangle "
        if add_percent:
            percent = count * 100 / sum(hist_dict.values())
            htemp += r"node[label=below:{\small $("+f"{percent:.2f}"+r"\%)$}] {$"+f"{count}"+r"$}"
        else:
            htemp += r"node {$"+f"{count}"+r"$}"
        htemp += f"(axis cs:{i+wbar},{count});"

        s = s_append(s, htemp)
    s = s_append(s, r"\end{axis}")
    s = s_append(s, r"\end{tikzpicture}")

    return s

def s_append(s, line, tab="\t"):
    return s+tab+line+"\n"


class TikzDocument(TexDocument):

    DEFAULT_PACKAGES = TexDocument.DEFAULT_PACKAGES + [
                        'tikz',
                        'pgfplots'
                        ]
    DEFAULT_PACKAGES_DICT = TexDocument.DEFAULT_PACKAGES_DICT

    DEFAULT_PALETTE = {
                'tabblue':'1f77b4',
                'taborange':'ff7f0e',
                'tabgreen':'2ca02c',
                'tabred':'d62728',
                'tapurple':'9467bd',
                'tabbrown':'8c564b',
                'tabpink':'e377c2',
                'tabgray':'7f7f7f',
                'tabolive':'bcbd22',
                'tabcyan':'17becf'
                }

    def __init__(self, title=None, author=None, date=None, packages=DEFAULT_PACKAGES, packages_dict=DEFAULT_PACKAGES_DICT, palette=DEFAULT_PALETTE):
        super().__init__(title=title, author=author, date=date, packages=packages, packages_dict=packages_dict)
        self.palette = palette
        self.add_colors(self.palette)
        self.append(r"\newcommand{\opacity}{0.8}")

    def add_colors(self, palette):
        for color, hex in palette.items():
            self.append(r"\definecolor{"+color+"}{HTML}{"+hex+"}")

    def add_histogram(self, hist_dict, title=None, wbar=0.4, floating=None):
        self.add_figure(make_histogram(hist_dict, self.palette.keys(), title, wbar), floating)




if __name__ == '__main__':

    filename = "out/testtikz.tex"

    doc = TikzDocument("Test Document", "Name Surname")

    hist_dict = {'Male':40, 'Female':40}

    doc.add_histogram(hist_dict)
    doc.save_document(filename)
