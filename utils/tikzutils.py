
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
        'geometry':'[left=2.00cm, right=2.00cm, top=2.00cm, bottom=2.00cm]'
    }

    def __init__(self, title=None, author=None, packages=DEFAULT_PACKAGES, packages_dict=DEFAULT_PACKAGES_DICT):
        self.text = ""
        self.title = title
        self.author = author
        self.packages = packages
        self.packages_dict = packages_dict
        pass

    def clear_document(self):
        self.text = ""

    def initialize_document(self):
        self.clear_document()
        self.append(r"\documentclass[10pt,a4paper]{article}")
        for package in self.packages:
            if package in self.packages_dict:
                self.append(r"\usepackage["+f"{self.packages_dict[package]}"+"]{"+f"{package}"+r"}")
            else:
                self.append(r"\usepackage{"+f"{package}"+r"}")

        self.append(r"\begin{document}")

    def append(self, line):
        self.text += line+"\n"
        pass

if __name__ == "__main__":

    pass
