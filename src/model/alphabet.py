import re

SPECIAL = [
    '\\frac', '\\sqrt', '\\sum', '\\int', '\\pi',
    '\\alpha', '\\beta', '\\gamma', '\\theta',
    '\\sin', '\\cos', '\\tan', '\\log', '\\ln',
    '\\leq', '\\geq', '\\neq', '\\approx'
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