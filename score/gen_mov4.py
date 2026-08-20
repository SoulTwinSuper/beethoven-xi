#!/usr/bin/env python3
"""
Symphony No. XI "Grenze"
IV. Stille nach dem Sturm  (嵐の後の静寂)

全25パート MusicXML 生成スクリプト（music21 使用）
MC_オーケストラパート別技法要求書 に基づく実装

調性: F-dur (1♭: Bb)
拍子: 6/8  (1小節 = 3.0 quarterLength = 2拍 × 付点四分音符)
テンポ: ♩.=54

特徴的要素:
 - Hr.1-4 コラール (mm.1-20) — ppp, con sordino: Ⅸ番第4楽章 Hr コラールへのオマージュ
 - Vn.I cantabile mf→ppp (mm.21-40)
 - Vn.II pizzicato lontano (mm.21-40)
 - Vc-Fg バロック二重奏 (mm.41-60) — pizz+arco 交替
 - Va + Alto 合唱ユニゾン (mm.41-60) — senza vibrato
 - Soprano 子守唄旋律 (mm.61-70)
 - 全体静寂 (mm.71-80) → attacca V楽章

実行: python gen_mov4.py
出力: beethoven_xi_mov4.xml → MuseScore4 で .mscz に変換
"""

from music21 import (
    stream, note, chord, metadata, key, meter, tempo,
    instrument, clef, dynamics, expressions, articulations
)

# ============================================================
# グローバル設定
# ============================================================
TOTAL_MEASURES = 80
TIME_SIG  = '6/8'      # 1小節 = 3.0 quarterLength
TEMPO_NUM = 54         # ♩.=54
KEY_STR   = 'F'        # F-dur (1♭)

# 6/8拍子の基本音価
DQ = 1.5   # 付点四分音符 (dotted quarter)
E  = 0.5   # 八分音符
Q  = 1.0   # 四分音符
DH = 3.0   # 付点二分音符 (1小節全体)


# ============================================================
# ユーティリティ
# ============================================================

def n(pitch, ql, dyn_str=None):
    nn = note.Note(pitch, quarterLength=ql)
    if dyn_str:
        nn.dynamic = dynamics.Dynamic(dyn_str)
    return nn


def r(ql=DH):
    return note.Rest(quarterLength=ql)


def text_exp(txt, placement='above'):
    te = expressions.TextExpression(txt)
    te.placement = placement
    return te


def rest_measure(mm):
    m = stream.Measure(number=mm)
    m.append(r(DH))
    return m


def add_lyric(nn, text):
    nn.addLyric(text)
    return nn


# ============================================================
# ホルンコラール (mm.1-20) — 楽章の核心
# MC文書 セクション3-1 より
# Hr.1: F5(DQ) E5(DQ) | D5(DH)
# Hr.2: A4(DQ) G4(DQ) | F4(DH)
# Hr.3: D4(DQ) C4(DQ) | A3(DH)
# Hr.4: F2(DQ) C3(DQ) | F2(DH)
# 和声: F-dur → C-dur(属) → F-dur(解決)
# 10回繰り返し (mm.1-20: 各2小節 × 10)
# ============================================================

CHORALE_DATA = {
    1: [('F5', DQ), ('E5', DQ)],    # Hr.1 mm.奇数
    2: [('A4', DQ), ('G4', DQ)],    # Hr.2 mm.奇数
    3: [('D4', DQ), ('C4', DQ)],    # Hr.3 mm.奇数
    4: [('F2', DQ), ('C3', DQ)],    # Hr.4 mm.奇数
}
CHORALE_HOLD = {
    1: 'D5',    # Hr.1 mm.偶数 保続音
    2: 'F4',    # Hr.2
    3: 'A3',    # Hr.3
    4: 'F2',    # Hr.4
}


def build_horn_iv(num):
    """Hr.1-4: con sordino コラール"""
    custom = {}
    for pair in range(10):           # 10ペア × 2小節 = mm.1-20
        mm_odd  = pair * 2 + 1       # 奇数小節: 動き
        mm_even = pair * 2 + 2       # 偶数小節: 保続音

        # 奇数小節
        m_odd = stream.Measure(number=mm_odd)
        if mm_odd == 1:
            m_odd.insert(0, text_exp('con sordino — ppp sempre'))
        dyn_str = 'ppp' if mm_odd == 1 else None
        for pitch, ql in CHORALE_DATA[num]:
            m_odd.append(n(pitch, ql, dyn_str))
        custom[mm_odd] = m_odd

        # 偶数小節: 保続音
        m_even = stream.Measure(number=mm_even)
        m_even.append(n(CHORALE_HOLD[num], DH,
                        'pp' if mm_even == 2 else None))
        custom[mm_even] = m_even

    return custom


# ============================================================
# 弦楽パート
# ============================================================

def build_violin_i_iv():
    """
    mm.1-20: 全休符 (Hr コラール聴取)
    mm.21-40: cantabile mf→ppp (長い弓、4小節かけて減衰)
    mm.41-80: pp 維持
    """
    custom = {}
    # F長調の主旋律 (cantabile)
    melody = [
        # mm.21-28: 第1フレーズ
        [('A5', DQ), ('G5', DQ)],  # mm.21
        [('F5', DH)],               # mm.22
        [('G5', DQ), ('A5', DQ)],  # mm.23
        [('C6', DH)],               # mm.24
        [('B-5', DQ), ('A5', DQ)], # mm.25
        [('G5', DH)],               # mm.26
        [('F5', DQ), ('E5', DQ)],  # mm.27
        [('F5', DH)],               # mm.28
        # mm.29-36: 第2フレーズ (発展)
        [('C6', DQ), ('D6', DQ)],  # mm.29
        [('C6', DH)],               # mm.30
        [('A5', DQ), ('B-5', DQ)], # mm.31
        [('A5', DH)],               # mm.32
        [('G5', DQ), ('F5', DQ)],  # mm.33
        [('E5', DH)],               # mm.34
        [('D5', DQ), ('C5', DQ)],  # mm.35
        [('F5', DH)],               # mm.36
        # mm.37-40: 消滅
        [('A5', DH)],               # mm.37
        [('F5', DH)],               # mm.38
        [('C5', DH)],               # mm.39
        [('F4', DH)],               # mm.40  (ppp)
    ]
    dyn_labels = {21: 'mf', 25: 'mp', 30: 'p', 37: 'pp', 40: 'ppp'}
    for i, elems in enumerate(melody):
        mm = 21 + i
        m = stream.Measure(number=mm)
        dyn_str = dyn_labels.get(mm)
        if mm == 21:
            m.insert(0, text_exp('cantabile — lunga arcata (長い弓)'))
        for j, (pitch, ql) in enumerate(elems):
            m.append(n(pitch, ql, dyn_str if j == 0 else None))
        custom[mm] = m

    # mm.41-80: pp 維持 (Vc-Fg の対話を背景に)
    for mm in range(41, 81):
        m = stream.Measure(number=mm)
        if mm == 41:
            m.insert(0, text_exp('pp — floating (VcFg dialog behind)'))
        m.append(n('F5', DH, 'pp' if mm == 41 else None))
        if mm == 80:
            m.insert(0, text_exp('ppp — attacca V. Neue Grenze'))
        custom[mm] = m

    return custom


def build_violin_ii_iv():
    """pizzicato lontano — 弱音器付き遠方感 pizz (mm.21-60)"""
    custom = {}
    # F-dur分散和音を pizz で刻む
    pizz_notes = ['F4', 'A4', 'C5', 'A4', 'F4', 'C4']
    for mm in range(21, 61):
        m = stream.Measure(number=mm)
        if mm == 21:
            m.insert(0, text_exp('pizzicato lontano — con sordino, pp'))
        # 6/8: 8分音符6個 = 3.0ql
        for i in range(6):
            p = pizz_notes[(mm * 6 + i) % len(pizz_notes)]
            dyn_str = 'pp' if mm == 21 and i == 0 else None
            nn = n(p, E, dyn_str)
            nn.articulations.append(articulations.Pizzicato() if hasattr(articulations, 'Pizzicato')
                                    else articulations.Staccatissimo())
            m.append(nn)
        custom[mm] = m
    return custom


def build_viola_iv():
    """
    senza vibrato — Va + Alto ユニゾン (mm.41-60)
    透明な内声コラール
    """
    custom = {}
    # mm.1-40: 全休符 (Hr コラール + Vn カンタービレを聴取)
    # mm.41-60: senza vibrato + Alto ユニゾン
    va_melody = [
        'C5', 'B-4', 'A4', 'G4', 'F4', 'G4', 'A4', 'B-4',
        'C5', 'D5',  'C5', 'B-4', 'A4', 'G4', 'F4', 'E4',
        'F4', 'G4',  'A4', 'F4',
    ]
    for i, pitch in enumerate(va_melody):
        mm = 41 + i
        m = stream.Measure(number=mm)
        if mm == 41:
            m.insert(0, text_exp('senza vibrato — unison with Alto'))
        m.append(n(pitch, DH, 'mp' if mm == 41 else 'p' if mm == 51 else None))
        custom[mm] = m
    return custom


def build_cello_iv():
    """
    Vc-Fg バロック二重奏 (mm.41-60)
    pizzicato + arco 交替 (2拍ごと): DQ pizz → DQ arco
    """
    custom = {}
    # コラールベース (F-dur)
    vc_bass = [
        'F2', 'C3', 'F2', 'G2', 'A2', 'B-2', 'C3', 'A2',
        'F2', 'G2', 'A2', 'F2', 'C3', 'B-2', 'A2', 'G2',
        'F2', 'C2', 'F2', 'F2',
    ]
    artic_labels = {0: 'pizz.', 1: 'arco'}
    for i, pitch in enumerate(vc_bass):
        mm = 41 + i
        m = stream.Measure(number=mm)
        if mm == 41:
            m.insert(0, text_exp('Vc-Fg baroque duo — pizz↔arco (2-beat alternation)'))
        # 各小節: pizz DQ + arco DQ
        nn_pizz = n(pitch, DQ, 'mp' if mm == 41 else None)
        nn_pizz.articulations.append(articulations.Staccato())  # pizz 近似
        m.append(nn_pizz)
        m.append(n(pitch, DQ))
        custom[mm] = m
    return custom


def build_contrabass_iv():
    """F ペダルポイント (pp)"""
    custom = {}
    for mm in range(1, 81):
        m = stream.Measure(number=mm)
        if mm == 1:
            m.insert(0, text_exp('pp pedal F — sempre'))
        m.append(n('F1', DH, 'pp' if mm == 1 else None))
        custom[mm] = m
    return custom


# ============================================================
# 木管楽器
# ============================================================

def build_flute_iv():
    """静寂の中の Fl — pp ロングトーン (mm.21-60)"""
    custom = {}
    fl_notes = ['C6', 'B-5', 'A5', 'G5', 'A5', 'C6', 'F6', 'E6',
                'D6', 'C6',  'B-5', 'A5', 'G5', 'F5', 'A5', 'C6',
                'F6', 'E6',  'D6', 'C6',  'B-5', 'A5', 'G5', 'F5',
                'C6', 'B-5', 'A5', 'G5',  'F5',  'E5', 'F5', 'F5',
                'C6', 'B-5', 'A5', 'G5',  'F5',  'E5', 'D5', 'F5']
    for i in range(40):
        mm = 21 + i
        m = stream.Measure(number=mm)
        if mm == 21:
            m.insert(0, text_exp('pp — lunga (長音符)'))
        m.append(n(fl_notes[i % len(fl_notes)], DH,
                   'pp' if mm == 21 else None))
        custom[mm] = m
    return custom


def build_oboe_iv():
    """pp — ロングトーン内声 (mm.21-60)"""
    custom = {}
    ob_notes = ['A4', 'G4', 'F4', 'E4', 'F4', 'G4', 'A4', 'B-4',
                'C5', 'B-4', 'A4', 'G4', 'F4', 'E4', 'F4', 'G4',
                'A4', 'G4', 'F4', 'E4', 'D4', 'E4', 'F4', 'G4',
                'A4', 'B-4', 'C5', 'A4', 'G4', 'F4', 'E4', 'F4',
                'A4', 'G4', 'F4', 'E4', 'D4', 'C4', 'D4', 'F4']
    for i in range(40):
        mm = 21 + i
        m = stream.Measure(number=mm)
        if mm == 21:
            m.insert(0, text_exp('pp dolce'))
        m.append(n(ob_notes[i % len(ob_notes)], DH,
                   'pp' if mm == 21 else None))
        custom[mm] = m
    return custom


def build_clarinet_iv():
    """pp — 内声充填 (mm.21-60)"""
    custom = {}
    cl_notes = ['E4', 'F4', 'G4', 'A4', 'B-4', 'A4', 'G4', 'F4',
                'E4', 'F4', 'G4', 'A4', 'B-4', 'C5', 'B-4', 'A4',
                'G4', 'F4', 'E4', 'D4', 'C4', 'D4', 'E4', 'F4',
                'G4', 'A4', 'B-4', 'G4', 'F4', 'E4', 'D4', 'E4',
                'G4', 'A4', 'B-4', 'A4', 'G4', 'F4', 'E4', 'F4']
    for i in range(40):
        mm = 21 + i
        m = stream.Measure(number=mm)
        if mm == 21:
            m.insert(0, text_exp('pp — inner voice'))
        m.append(n(cl_notes[i % len(cl_notes)], DH,
                   'pp' if mm == 21 else None))
        custom[mm] = m
    return custom


def build_fagotto_iv():
    """
    Vc-Fg バロック二重奏 (mm.41-60) — Vcとユニゾン or 3度下
    """
    custom = {}
    fg_notes = [
        'F2', 'C3', 'F2', 'G2', 'A2', 'B-2', 'C3', 'A2',
        'F2', 'G2', 'A2', 'F2', 'C3', 'B-2', 'A2', 'G2',
        'F2', 'C2', 'F2', 'F2',
    ]
    for i, pitch in enumerate(fg_notes):
        mm = 41 + i
        m = stream.Measure(number=mm)
        if mm == 41:
            m.insert(0, text_exp('Vc-Fg baroque duo — staccato leggiero'))
        # staccato 8分音符で刻む (baroque 様式)
        for _ in range(6):
            nn = n(pitch, E, 'mp' if mm == 41 and _ == 0 else None)
            nn.articulations.append(articulations.Staccato())
            m.append(nn)
        custom[mm] = m
    return custom


# ============================================================
# 金管楽器 (Tp, Tb, Tuba: 第Ⅳ楽章は静寂・全休符)
# Tp のみ mm.70 でpppp長音
# ============================================================

def build_horn_done(num):
    """Hr: コラール後 (mm.21-80) は静寂"""
    return {}


def build_trumpet_iv(num):
    """第Ⅳ楽章: 全休符 (嵐の後の静寂には金管不在)"""
    return {}


def build_trombone_iv(num):
    return {}


def build_tuba_iv():
    return {}


def build_timpani_iv():
    """pp tremolo — Cb との共鳴 (mm.41-80)"""
    custom = {}
    for mm in range(41, 81):
        m = stream.Measure(number=mm)
        if mm == 41:
            m.insert(0, text_exp('pp — soft felt mallet tremolo'))
        # 8分音符でtremolo近似
        for i in range(6):
            m.append(n('F2', E, 'pp' if mm == 41 and i == 0 else None))
        custom[mm] = m
    return custom


# ============================================================
# 合唱パート
# ============================================================

def build_soprano_iv():
    """
    子守唄的旋律 (mm.61-70) — 6/8拍子 legato
    F-dur でシンプルな歌曲風
    """
    custom = {}
    # 歌詞なし (vocalize — "Ah")
    sop_notes = ['F5', 'G5', 'A5', 'B-5', 'C6', 'B-5', 'A5', 'G5', 'F5', 'E5']
    for i, pitch in enumerate(sop_notes):
        mm = 61 + i
        m = stream.Measure(number=mm)
        if mm == 61:
            m.insert(0, text_exp('子守唄 (Wiegenlied) — legato, pp'))
        nn = n(pitch, DH, 'pp' if mm == 61 else 'ppp' if mm == 70 else None)
        nn.addLyric('Ah' if i == 0 else '')
        m.append(nn)
        custom[mm] = m
    return custom


def build_alto_iv():
    """
    Va とユニゾン (mm.41-60) — senza vibrato
    """
    custom = {}
    va_melody = [
        'C5', 'B-4', 'A4', 'G4', 'F4', 'G4', 'A4', 'B-4',
        'C5', 'D5', 'C5', 'B-4', 'A4', 'G4', 'F4', 'E4',
        'F4', 'G4', 'A4', 'F4',
    ]
    for i, pitch in enumerate(va_melody):
        mm = 41 + i
        m = stream.Measure(number=mm)
        if mm == 41:
            m.insert(0, text_exp('Alt — unison with Va, senza vibrato, mp'))
        nn = n(pitch, DH, 'mp' if mm == 41 else 'p' if mm == 51 else None)
        nn.addLyric('(Mm)' if i == 0 else '')
        m.append(nn)
        custom[mm] = m
    return custom


def build_tenor_iv():
    """第Ⅳ楽章: テノール全休符"""
    return {}


def build_bass_iv():
    """第Ⅳ楽章: バス全休符"""
    return {}


# ============================================================
# パート設定テーブル
# ============================================================

PARTS_CONFIG = [
    ('Flute',          'Fl.',   instrument.Flute(),       'treble', build_flute_iv),
    ('Oboe',           'Ob.',   instrument.Oboe(),         'treble', build_oboe_iv),
    ('Clarinet in Bb', 'Cl.',   instrument.Clarinet(),     'treble', build_clarinet_iv),
    ('Fagotto',        'Fg.',   instrument.Bassoon(),      'bass',   build_fagotto_iv),
    ('Horn in F 1',    'Hr.1',  instrument.Horn(),         'treble', lambda: build_horn_iv(1)),
    ('Horn in F 2',    'Hr.2',  instrument.Horn(),         'treble', lambda: build_horn_iv(2)),
    ('Horn in F 3',    'Hr.3',  instrument.Horn(),         'treble', lambda: build_horn_iv(3)),
    ('Horn in F 4',    'Hr.4',  instrument.Horn(),         'bass',   lambda: build_horn_iv(4)),
    ('Trumpet in C 1', 'Tp.1',  instrument.Trumpet(),      'treble', lambda: build_trumpet_iv(1)),
    ('Trumpet in C 2', 'Tp.2',  instrument.Trumpet(),      'treble', lambda: build_trumpet_iv(2)),
    ('Trumpet in C 3', 'Tp.3',  instrument.Trumpet(),      'treble', lambda: build_trumpet_iv(3)),
    ('Trombone 1',     'Tb.1',  instrument.Trombone(),     'bass',   lambda: build_trombone_iv(1)),
    ('Trombone 2',     'Tb.2',  instrument.Trombone(),     'bass',   lambda: build_trombone_iv(2)),
    ('Trombone 3',     'Tb.3',  instrument.Trombone(),     'bass',   lambda: build_trombone_iv(3)),
    ('Tuba',           'Tuba',  instrument.Tuba(),         'bass',   build_tuba_iv),
    ('Timpani',        'Timp.', instrument.Timpani(),      'bass',   build_timpani_iv),
    ('Soprano',        'S.',    instrument.Soprano(),      'treble', build_soprano_iv),
    ('Alto',           'A.',    instrument.Alto(),         'treble', build_alto_iv),
    ('Tenor',          'T.',    instrument.Tenor(),        'treble', build_tenor_iv),
    ('Bass',           'B.',    instrument.Bass(),         'bass',   build_bass_iv),
    ('Violin I',       'Vn.I',  instrument.Violin(),       'treble', build_violin_i_iv),
    ('Violin II',      'Vn.II', instrument.Violin(),       'treble', build_violin_ii_iv),
    ('Viola',          'Va.',   instrument.Viola(),        'alto',   build_viola_iv),
    ('Violoncello',    'Vc.',   instrument.Violoncello(),  'bass',   build_cello_iv),
    ('Contrabass',     'Cb.',   instrument.Contrabass(),   'bass',   build_contrabass_iv),
]


CLEF_MAP = {
    'treble': clef.TrebleClef,
    'bass':   clef.BassClef,
    'alto':   clef.AltoClef,
    'tenor':  clef.TenorClef,
}


def build_part(name, abbrev, instr, clef_type, custom_measures_dict):
    part = stream.Part()
    part.partName = name
    part.partAbbreviation = abbrev
    part.insert(0, instr)

    for mm in range(1, TOTAL_MEASURES + 1):
        if mm in custom_measures_dict:
            m = custom_measures_dict[mm]
        else:
            m = rest_measure(mm)

        m.number = mm

        if mm == 1:
            m.insert(0, CLEF_MAP[clef_type]())
            m.insert(0, key.Key(KEY_STR))
            m.insert(0, meter.TimeSignature(TIME_SIG))
            m.insert(0, tempo.MetronomeMark(
                text='Andante sereno', number=TEMPO_NUM,
                referent=note.Note(type='quarter', dots=1)))

        part.append(m)

    return part


# ============================================================
# メイン
# ============================================================

def main():
    score = stream.Score()

    md = metadata.Metadata()
    md.title = 'Symphony No. XI "Grenze" — IV. Stille nach dem Sturm'
    md.composer = 'Music TWIN Collective (Soul-Twin Society, 2026)'
    score.insert(0, md)

    for name, abbrev, instr, clef_t, builder in PARTS_CONFIG:
        print(f'  Building part: {name}')
        custom = builder()
        part = build_part(name, abbrev, instr, clef_t, custom)
        score.insert(0, part)

    out_path = 'beethoven_xi_mov4.xml'
    score.write('musicxml', fp=out_path)
    print(f'\nMusicXML saved: {out_path}')


if __name__ == '__main__':
    main()
