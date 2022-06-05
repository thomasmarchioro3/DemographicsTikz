class TexDocument:

    DEFAULT_PACKAGES = [
                        'inputenc',
                        'amsfonts',
                        'amssymb',
                        'graphicx',
                        'todonotes',
                        'geometry',
                        ]
    DEFAULT_PACKAGES_DICT = {
        'inputenc':'utf8',
        'geometry':'left=2.00cm, right=2.00cm, top=2.00cm, bottom=2.00cm'
    }

    def __init__(self, title=None, author=None, date=None, packages=DEFAULT_PACKAGES, packages_dict=DEFAULT_PACKAGES_DICT):
        self.header = ""
        self.body = ""
        self.footer = ""
        self.title = title
        self.author = author
        self.date = date
        self.packages = packages
        self.packages_dict = packages_dict
        self.initialize_document()

    def clear_document(self):
        self.header = ""
        self.body = ""
        self.footer = ""

    def initialize_document(self):
        self.clear_document()
        self.append_header(r"\documentclass[10pt,a4paper]{article}")
        for package in self.packages:
            if package in self.packages_dict:
                self.append_header(r"\usepackage["+f"{self.packages_dict[package]}"+"]{"+f"{package}"+r"}")
            else:
                self.append_header(r"\usepackage{"+f"{package}"+r"}")

        if self.title is not None:
            self.append_header(r"\title{"+f"{self.title}"+r"}")
        if self.author is not None:
            self.append_header(r"\author{"+f"{self.author}"+r"}")
        if self.date is not None:
            self.append_header(r"\author{"+f"{self.author}"+r"}")

        self.append_header(r"\begin{document}")

        if self.title is not None:
            self.append(r"\maketitle"+"\n")

        self.append_footer(r"\end{document}")

    def append(self, line, place="body"):
        if place=="header":
            self.header += line+"\n"
        elif place=="body":
            self.body += "\t"+line+"\n"
        elif place=="footer":
            self.footer += line+"\n"

        else:
            raise Exception("ERROR: 'in' must be either 'header', 'body' or 'footer'")

    def append_header(self, line):
        self.append(line, place="header")

    def append_footer(self, line):
        self.append(line, place="footer")

    def save_document(self, filename):
        with open(filename, 'w') as f:
            f.write(str(self))

    def add_figure(self, s_fig, floating=None, centering=True):
        self.append("")
        if floating in ["h", "ht"]:
            self.append(r"\begin{figure}["+floating+r"]")
        else:
            self.append(r"\begin{figure}")

        self.append(r"\centering")
        self.append(s_fig)

        self.append(r"\end{figure}")

    def __str__(self):
        return self.header + self.body + self.footer

if __name__ == "__main__":
    filename = "out/testutils.tex"

    doc = TexDocument("Test Document", "Name Surname")

    doc.save_document(filename)
