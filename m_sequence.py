import numpy as np

def autocorrelation(m_seq):
    ac = np.zeros(len(m_seq), dtype=np.int)
    for i in range(len(m_seq)):
        ac[i] = sum(m_seq * np.roll(m_seq, i))
    print(ac)
    return ac

# h(x) = x^7+x^3+1, [211], 符号長127 (= 2^7-1)
def mseq_127_211():
    register = np.ones(7 + 1, dtype=np.int) * -1    # レジスタ(出力を含む)を-1で初期化
    m_seq = np.zeros(127, dtype=np.int)             # m_seqの配列を用意

    for i in range(127):
        m_seq[i] = register[0]                      # 線形帰還シフトレジスタの出力を配列へ代入
        register[7] = register[3] * register[0]     # 生成多項式の計算結果を一番後ろ(配線上)で保持
        register = np.roll(register, -1)            # レジスタの保持した値をシフト

    return m_seq

# h(x) = x^7+x+1, [203], 符号長127 (= 2^7-1)
def mseq_127_203():
    register = np.ones(7 + 1, dtype=np.int) * -1    # レジスタ(出力を含む)を-1で初期化
    m_seq = np.zeros(127, dtype=np.int)             # m_seqの配列を用意

    for i in range(127):
        m_seq[i] = register[0]                      # 線形帰還シフトレジスタの出力を配列へ代入
        register[7] = register[1] * register[0]     # 生成多項式の計算結果を一番後ろ(配線上)で保持
        register = np.roll(register, -1)            # レジスタの保持した値をシフト

    return m_seq