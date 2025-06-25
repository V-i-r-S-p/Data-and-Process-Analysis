def tex_package(data: str) -> str:
  return r'''
  \documentclass[12pt, a4paper]{article}

  \usepackage{amsmath}
  \usepackage{amsfonts}
  \usepackage{amssymb}
  \usepackage{booktabs}
  \usepackage{multirow}
  \usepackage{longtable}
  \usepackage[utf8]{inputenc}
  \usepackage[russian]{babel}
  \usepackage[
    left=1cm,
    right=1cm,
    top=2cm,
    bottom=2cm,
    includefoot]{geometry}
  \usepackage{fancyvrb}
  %s
  ''' % data



def tex_longtable(data: str, cols: str, cap: str, *cols_name:str) -> str:
  # if len(cols.replace('|', '')) != len(cols_name):
  #   raise Exception("longtable error")
  cols_name_ = ' & '.join([r'\textbf{%s}' % col_name for col_name in cols_name]) + ' \\\\\n'
  ncol = str(len(cols_name))
  return r'''
\begin{center}
\begin{longtable}{%s}
\caption{%s} \label{tab:%s} \\
\hline
%s
\hline
\endfirsthead

\multicolumn{%s}{c}
{{\bfseries Продолжение таблицы \thetable}} \\
\hline
%s
\hline
\endhead

\hline
\multicolumn{%s}{|c|}{{Продолжение на следующей странице}} \\
\endfoot

\hline
\endlastfoot

%s
\hline
\end{longtable}
\end{center}
\newpage
''' % (cols, cap, cap, cols_name_, ncol, cols_name_, ncol, data)


def tex_verbatim(data: str) -> str:
  return r'''
  \begin{minipage}{\linewidth}
  \centering
  \begin{center}
  \begin{Verbatim}
  %s
  \end{Verbatim}
  \end{center}
  \end{minipage}
  ''' % data


def tex_document(data: str) -> str:
  return r'''
  \begin{document}
  %s
  \end{document}
  ''' % data

def tex_title(data: str, title: str) -> str:
  return r'''
  \title{%s}
  \date{\today}

  \maketitle
  \newpage
  %s
  ''' % (title, data)

def tex_center(data: str) -> str:
  return r'''
  \begin{center}
  %s
  \end{center}
  ''' % data

def tex_math(data: str) -> str:
  return r'''$ %s $''' % data

def tex_displaymath(data: str) -> str:
  return r'''\[%s\]''' % data

def tex_font_mathsf(data: str) -> str:
  return r'''\mathsf{%s}''' % data

def data2tex(data: str) -> str:
  data_ = data

  data_ = tex_font_mathsf(data_)
  data_ = tex_math(data_)

  # data_ = tex_displaymath(data_)
  # data_ = tex_center(data_)
  # data_ = tex_document(data_)

  return data_

def all_data2tex(data: list[str]) -> list[str]:
  tex = []
  for data_ in data:
    tex.append(data2tex(data_))

  return tex
