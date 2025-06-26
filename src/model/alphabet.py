import re

SPECIAL = [
    # Цифры и латиница
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
    'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
    'w', 'x', 'y', 'z',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
    'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
    'W', 'X', 'Y', 'Z',

    # Операторы
    '+', '-', '*', '/', '=', '<', '>', '!', '^', '_',
    '.', ',', ':', ';', ' ',

    # Греческие буквы
    '\\alpha', '\\beta', '\\gamma', '\\delta', '\\epsilon',
    '\\zeta', '\\eta', '\\theta', '\\iota', '\\kappa',
    '\\lambda', '\\mu', '\\nu', '\\xi', '\\omicron', '\\pi',
    '\\rho', '\\sigma', '\\tau', '\\upsilon', '\\phi',
    '\\chi', '\\psi', '\\omega',

    '\\Gamma', '\\Delta', '\\Theta', '\\Lambda', '\\Xi', '\\Pi',
    '\\Sigma', '\\Upsilon', '\\Phi', '\\Psi', '\\Omega',

    # Математические функции
    '\\sin', '\\cos', '\\tan', '\\cot', '\\sec', '\\csc',
    '\\log', '\\ln', '\\exp',

    # Спецоператоры
    '\\sum', '\\int', '\\prod', '\\lim', '\\infty',
    '\\partial', '\\nabla', '\\cdot', '\\times', '\\div',
    '\\sqrt', '\\frac',

    # Отношения
    '\\leq', '\\geq', '\\neq', '\\approx', '\\equiv',
    '\\sim', '\\propto',

    # Множества и логика
    '\\in', '\\notin', '\\subset', '\\subseteq',
    '\\supset', '\\supseteq', '\\cup', '\\cap', '\\setminus',
    '\\forall', '\\exists', '\\neg', '\\wedge', '\\vee',
    # Скобки
    '(', ')', '[', ']', '{', '}',

    # Модификаторы
    '\\left', '\\right', '|', '\\langle', '\\rangle'
]


VOCAB = SPECIAL + ['<PAD>', '<BOS>', '<EOS>', '<UNK>']

token2idx = {t: i for i, t in enumerate(VOCAB)}
idx2token = {i: t for t, i in token2idx.items()}

def tokenize(latex: str):
    tokens = re.findall(r'\\[a-zA-Z]+|.', latex)
    unknowns = [t for t in tokens if t not in token2idx]
    return [token2idx.get(t, token2idx['<UNK>']) for t in tokens]

def detokenize(indices):
    return ''.join([VOCAB[i] for i in indices])