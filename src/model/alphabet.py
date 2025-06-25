import re

SPECIAL = [
    '\\rceil', '\\gcd', '\\vdash', '\\subset', '\\arccos', '\\Gamma', '\\lnx', '\\liminf',
    '\\lg', '\\Rightarrow', '\\nrightarrow', '\\sinu', '\\limsup', '\\kappa', '\\rfloor', '\\Pr',
    '\\ni', '\\Downarrow', '\\eta', '\\dots', '\\downdownarrows', '\\sqrt', '\\triangle', '\\xi',
    '\\nu', '\\nLeftrightarrow', '\\Omega', '\\tob', '\\tow', '\\hom', '\\cong', '\\%',
    '\\tor', '\\epsilon', '\\mathbb{R}', '\\sinh', '\\cdotk', '\\lfloor', '\\ln', '\\varrho',
    '\\Pi', '\\rightrightarrows', '\\Xi', '\\phi', '\\arctan', '\\tanv', '\\pi', '\\psi',
    '\\rangle', '\\cdotx', '\\pm', '\\mathbb{Q}', '\\top', '\\tos', '\\tant', '\\Phi',
    '\\in', '\\lng', '\\odot', '\\rightleftarrows', '\\cscu', '\\cfrac', '\\arcsin', '\\varpi',
    '\\leftrightarrow', '\\tanp', '\\varepsilon', '\\oplus', '\\lambda', '\\thetac', '\\sinv', '\\tan',
    '\\leftarrow', '\\thetap', '\\right', '\\cosu', '\\lnp', '\\rho', '\\lnz', '\\leftleftarrows',
    '\\neg', '\\lim', '\\sinw', '\\alpha', '\\lny', '\\toy', '\\cup', '\\varphi',
    '\\thetak', '\\updownarrow', '\\nparallel', '\\siny', '\\tans', '\\det', '\\toe', '\\lnw',
    '\\toz', '\\Leftarrow', '\\vee', '\\varnothing', '\\{', '\\lna', '\\exists', '\\models',
    '\\subseteq', '\\&', '\\left', '\\ton', '\\theta', '\\cdotv', '\\gamma', '\\omicron',
    '\\sim', '\\le', '\\tog', '\\arg', '\\lnb', '\\breve', '\\ker', '\\sigma',
    '\\leftrightarrows', '\\nLeftarrow', '\\infty', '\\mathbb{Z}', '\\Leftrightarrow', '\\sinx', '\\thetae', '\\supset',
    '\\lnv', '\\notin', '\\lnu', '\\sinr', '\\omega', '\\vdots', '\\ne', '\\times',
    '\\lnr', '\\thetag', '\\angle', '\\sing', '\\cdotz', '\\cdot', '\\Upsilon', '\\digamma',
    '\\toh', '\\Sigma', '\\tok', '\\Theta', '\\varsigma', '\\wedge', '\\propto', '\\prod',
    '\\sum', '\\$', '\\tot', '\\nleftrightarrow', '\\cdota', '\\cos', '\\coth', '\\dim',
    '\\csck', '\\zeta', '\\upuparrows', '\\cdoth', '\\log', '\\lnc', '\\Updownarrow', '\\hat',
    '\\tank', '\\cscg', '\\vartheta', '\\sec', '\\mu', '\\lns', '\\delta', '\\ast',
    '\\setminus', '\\perp', '\\int', '\\lnh', '\\toa', '\\gg', '\\secx', '\\nleftarrow',
    '\\cap', '\\|', '\\tov', '\\otimes', '\\to', '\\cot', '\\beta', '\\exp',
    '\\lnk', '\\ominus', '\\dot', '\\Uparrow', '\\equiv', '\\chi', '\\parallel', '\\mathbb{C}',
    '\\upsilon', '\\langle', '\\ddot', '\\cosv', '\\Delta', '\\ddots', '\\csc', '\\rightarrow',
    '\\cdotb', '\\degree', '\\mathbb{N}', '\\Lambda', '\\sinz', '\\bar', '\\iota', '\\vec',
    '\\cosh', '\\sint', '\\tanh', '\\ll', '\\#', '\\toc', '\\varkappa', '\\uparrow',
    '\\forall', '\\ge', '\\approx', '\\mid', '\\tau', '\\div', '\\frac', '\\cdotc',
    '\\cdots', '\\downarrow', '\\lceil', '\\lnt', '\\tilde', '\\supseteq', '\\cscx', '\\mp',
    '\\sin', '\\deg', '\\Psi', '\\nRightarrow', '\\}', '\\thetav', '\\tou', '\\overline'
]

SYMBOLS = list("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+-*/=^{}_()[] ")

VOCAB = SPECIAL + SYMBOLS + ['<PAD>', '<BOS>', '<EOS>', '<UNK>']

token2idx = {t: i for i, t in enumerate(VOCAB)}
idx2token = {i: t for t, i in token2idx.items()}

def tokenize(latex: str):
    tokens = re.findall(r'\\[a-zA-Z]+|.', latex)
    unknowns = [t for t in tokens if t not in token2idx]
    return [token2idx.get(t, token2idx['<UNK>']) for t in tokens]

def detokenize(indices):
    return ''.join([VOCAB[i] for i in indices])
