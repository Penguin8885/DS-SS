import numpy as np
import m_sequence

# 通信するデータの生成 (1bit)
def create_data():
    if np.random.rand() < 0.5:
        return +1
    else:
        return -1


# 拡散
def spread(data, PN):
    return data * PN


# 通信路 他局間干渉及びノイズ干渉
remainder = None
def add_channel_interference(sp1, sp2, delay, SIR, EbNo):
    global remainder # グローバル変数を操作する宣言

    # EbNoを設定 (amp1 = 1.0 を仮定)
    AWGN_amp = 10.0 ** (EbNo / 10.0) # 電力
    AWGN = np.random.normal(loc=0 , scale=np.sqrt(len(sp1) / (2.0*AWGN_amp)), size=len(sp1))

    # SIRを設定 (amp1 = 1.0 を仮定)
    amp2 = 10.0 ** (-SIR / 20.0) # 電圧
    sp2 * amp2

    # 遅延を設定
    delay_sp2 = np.hstack([remainder, sp2])[delay : -(len(sp2)-delay)] # 遅延した信号を生成
    remainder = sp2                                                    # 今の信号を次回用に保存

    # 加算して返却
    return sp1 + delay_sp2 + AWGN


# 逆拡散
def despread(received, PN):
    if np.sum(received * PN) > 0:
        return +1
    else:
        return -1


######## 通信実験・BER特性評価 ########
def evaluate(repeatNum, PN1, PN2, delay, SIR, EbNo):
    err_count = 0

    global remainder
    remainder = spread(1, PN2)  # 遅延計算のために干渉側は先に1ビットだけ通信を記録しておく

    for i in range(repeatNum):

        # 送信機1 自分のデータを拡散
        data1 = create_data()
        spreaded1 = spread(data1, PN1)

        # 送信機2 他人のデータを拡散
        data2 = create_data()
        spreaded2 = spread(data2, PN2)

        # 通信路干渉
        received = add_channel_interference(spreaded1, spreaded2, delay, SIR, EbNo)

        # 受信機1 自分のデータを逆拡散
        DATA1 = despread(received, PN1)

        # BERを計算
        if data1 != DATA1:
            err_count += 1

    return err_count / repeatNum # BERを返却




if __name__ == '__main__':
    PN1 = m_sequence.mseq_127_211()     # 自局拡散系列
    PN2 = np.zeros(127, dtype=np.int)   # 干渉なし
    # PN2 = m_sequence.mseq_127_203()     # 他局拡散系列

    print(evaluate(int(1e5), PN1, PN2, delay=0, SIR=0, EbNo=6.8))