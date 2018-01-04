import os
import json

# download zip file from https://fontawesome.com/ and extract into fontawesome directory.
INPUT_FILE = os.path.join("fontawesome", "advanced-options", "metadata", "icons.json")
OUTPUT_FILE = 'fontawesome5.sty'

OUTPUT_HEADER = r'''
% Identify this package.
\NeedsTeXFormat{LaTeX2e}
\ProvidesPackage{fontawesome5}[2018/01/04 v5.0.2 font awesome icons]
% Requirements to use.
\usepackage{fontspec}
% Configure a directory location for fonts(default: 'fonts/')
\newcommand*{\fontdir}[1][fonts/]{\def\@fontdir{#1}}
\fontdir
% Define pro option
\DeclareOption{pro}{
  % Define shortcut to load the Font Awesome pro font.
  \newfontfamily\FA[
    Path=\@fontdir,
    UprightFont=*-Regular-400,
    ItalicFont=*-Light-300,
    BoldFont=*-Solid-900,
  ]{Font Awesome 5 Pro}
}
\ProcessOptions\relax
% Define shortcut to load the Font Awesome font for brands.
\newfontfamily{\FAbrands}[Path=\@fontdir]{Font Awesome 5 Brands-Regular-400}
% Define shortcut to load the Font Awesome font.
\@ifundefined{FA}{%
\newfontfamily\FA[
  Path=\@fontdir,
  UprightFont=*-Regular-400,
  BoldFont=*-Solid-900,
]{Font Awesome 5 Free}
}{}
% Generic command displaying an icon by its name.
\newcommand*{\faicon}[1]{{
  \csname faicon@#1\endcsname
}}
'''

OUTPUT_LINE = '\expandafter\def\csname faicon@%(name)s\endcsname {%(font)s\symbol{"%(symbol)s}} \n'

def main():
    with open(INPUT_FILE, 'r') as json_data:
        icons = json.load(json_data)
        with open(OUTPUT_FILE, 'w') as w:
            w.write(OUTPUT_HEADER)
            for icon_name in sorted(icons.keys()):
                font = "\FA" if "brands" not in icons[icon_name]["styles"] else "\FAbrands"
                w.write(
                    OUTPUT_LINE % {
                        'name': icon_name, 'symbol': icons[icon_name]["unicode"].upper(), "font": font
                    }
                )
            w.write(r'\endinput')


if __name__ == "__main__":
    main()