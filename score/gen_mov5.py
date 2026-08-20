#!/usr/bin/env python3
"""
Symphony No. XI "Grenze"
V. Neue Grenze  (新たな限界 — 大ロンド形式)

全25パート MusicXML 生成スクリプト（music21 使用）
MC_オーケストラパート別技法要求書 サンプル3 (mm.420-450) を中核に実装

調性: D-dur (2♯: F#, C#)
拍子: 4/4 (mm.1-40) → 5/4 (mm.41-55) → 7/4 (mm.56-65) → 4/4 (mm.66-80 Coda)
テンポ: ♩=96 Maestoso → ♩=152 Maestoso-Presto (mm.66 Coda)

楽章構成:
 mm.1-10  : 4/4 ♩=96  導入（第Ⅰ楽章 Ur-Motiv の augmentation）
 mm.11-40 : 4/4 ♩=96  ロンド主題A（弦+木管+合唱 Strophe 1/2）
 mm.41-55 : 5/4 ♩=96  エピソード（全楽章統合）
 mm.56-65 : 7/4 ♩=96  クライマックス前の溜め
 mm.66-80 : 4/4 ♩=152 Coda SATB（サンプル3より）
   mm.66: S/T/B 入り (ff)
   mm.67: A 入り (ff, 1小節遅れ)
   mm.68: E5→F5→E5 フレーズ + Tp d''' 入り (ffff)
   mm.69-76: S c''' 8小節維持 (ffff) + A a'' + T b' + B D1
   mm.77-80: 解決和音 → 終止

実行: python gen_mov5.py
出力: beethoven_xi_mov5.xml → MuseScore4 で .mscz に変換
"""

from music21 import (
    stream, note, chord, metadata, key, meter, tempo,
    instrument, clef, dynamics, expressions, articulations
)

# ============================================================
# グローバル設定
# ============================================================
TOTAL_MEASURES = 80
KEY_STR = 'D'       # D-dur (2♯)

# 変拍子パターン
def get_ts(mm):
    if mm <= 40:
        return '4/4'
    elif mm <= 55:
        return '5/4'
    elif mm <= 65:
        return '7/4'
    else:
        return '4/4'  # Coda

def measure_len(mm):
    ts = get_ts(mm)
    return {'4/4': 4.0, '5/4': 5.0, '7/4': 7.0}[ts]

CODA_START   = 66    # mm.66 から Coda (♩=152)
SOPRANO_HIGH = 'C6'  # c'' (ソプラノ最高音、C6 = 実用的限界点)
TP_HIGH      = 'D6'  # d''' (Tp 最高音宣言)


# ============================================================
# ユーティリティ
# ============================================================

def n(pitch, ql, dyn_str=None):
    nn = note.Note(pitch, quarterLength=ql)
    if dyn_str:
        nn.dynamic = dynamics.Dynamic(dyn_str)
    return nn


def r(ql=4.0):
    return note.Rest(quarterLength=ql)


def text_exp(txt, placement='above'):
    te = expressions.TextExpression(txt)
    te.placement = placement
    return te


def add_lyric(nn, text):
    if text:
        nn.addLyric(text)
    return nn


def rest_measure(mm):
    m = stream.Measure(number=mm)
    m.append(r(measure_len(mm)))
    return m


# ============================================================
# ロンド主題 A (4/4, D-dur) — mm.11-40
# D-dur スケール上昇 + 合唱的フレーズ
# ============================================================

RONDO_A = [
    # D-dur 分散和音上昇
    [('D4', 1.0), ('F#4', 1.0), ('A4', 1.0), ('D5', 1.0)],
    [('E5', 2.0), ('D5', 2.0)],
    [('C#5', 1.0), ('B4', 1.0), ('A4', 2.0)],
    [('G4', 1.0), ('F#4', 1.0), ('E4', 1.0), ('D4', 1.0)],
    [('A4', 2.0), ('D5', 2.0)],
    [('C#5', 1.0), ('E5', 1.0), ('A5', 2.0)],
    [('G5', 2.0), ('F#5', 2.0)],
    [('E5', 2.0), ('D5', 2.0)],
]


def rondo_measure(mm, offset=0):
    elems = RONDO_A[(mm - 11 + offset) % len(RONDO_A)]
    m = stream.Measure(number=mm)
    for pitch, ql in elems:
        m.append(n(pitch, ql))
    return m


# ============================================================
# Coda 実装 (mm.66-80, 4/4 ♩=152)
# MC文書 サンプル3 LilyPond をそのまま music21 に変換
# ============================================================

def build_soprano_coda():
    """
    サンプル3 sopranoV:
    mm.66: f2(h=2) g4(q=1) a4(q=1)         ff  "das Un-"
    mm.67: b4(h=2) c5(q=1) d5(q=1)         ff  "-mög-li-che"
    mm.68: e5(h=2) f5(q=1) e5(q=1)         fff "es zer-"
    mm.69-76: c6(wn=4) × 8小節              ffff "-bricht!"
    mm.77: c6(3.0) rest(1.0)               ffff → diminuendo
    """
    measures = {}

    # mm.66
    m = stream.Measure(number=66)
    m.insert(0, text_exp('CODA — ffff, tutta forza'))
    m.append(add_lyric(n('F5', 2.0, 'ff'), 'das'))
    m.append(add_lyric(n('G5', 1.0), 'Un-'))
    m.append(add_lyric(n('A5', 1.0), ''))
    measures[66] = m

    # mm.67
    m = stream.Measure(number=67)
    m.append(add_lyric(n('B5', 2.0, 'ff'), '-mög-'))
    m.append(add_lyric(n('C6', 1.0), '-li-'))
    m.append(add_lyric(n('D6', 1.0), '-che'))
    measures[67] = m

    # mm.68
    m = stream.Measure(number=68)
    m.append(add_lyric(n('E6', 2.0, 'fff'), 'es'))
    m.append(add_lyric(n('F6', 1.0), 'zer-'))
    m.append(add_lyric(n('E6', 1.0), ''))
    measures[68] = m

    # mm.69-76: c''' (C6) 8小節持続
    for mm in range(69, 77):
        m = stream.Measure(number=mm)
        if mm == 69:
            m.insert(0, text_exp(f'c\'\'\' ({SOPRANO_HIGH}) — 8mm. 物理的限界点 ffff'))
        dyn_str = 'ffff' if mm == 69 else None
        m.append(add_lyric(n(SOPRANO_HIGH, 4.0, dyn_str), '-bricht!' if mm == 69 else ''))
        measures[mm] = m

    # mm.77-80: 解決 → ppp
    for mm, (pitch, dyn_str) in enumerate([('A5', 'fff'), ('F#5', 'ff'),
                                            ('D5', 'f'), ('D4', 'ppp')],
                                           start=77):
        m = stream.Measure(number=mm)
        if mm == 77:
            m.insert(0, text_exp('dim. — D-dur 最終解決'))
        m.append(n(pitch, 4.0, dyn_str))
        measures[mm] = m

    return measures


def build_alto_coda():
    """
    サンプル3 altoV:
    mm.66: 全休符
    mm.67: f2(h=2) g4(q=1) a4(q=1)  ff  "das Un-"
    mm.68: b4(h=2) c5(q=1) d5(q=1)  ff  "-mög-li-che"
    mm.69: e5(h=2) f5(q=1) e5(q=1)  fff "es zer-"
    mm.70-76: a5(wn) × 7小節         ffff "-bricht!"
    mm.77-80: 解決
    """
    measures = {}

    # mm.67 (1小節遅れ)
    m = stream.Measure(number=67)
    m.append(add_lyric(n('F5', 2.0, 'ff'), 'das'))
    m.append(add_lyric(n('G5', 1.0), 'Un-'))
    m.append(add_lyric(n('A5', 1.0), ''))
    measures[67] = m

    m = stream.Measure(number=68)
    m.append(add_lyric(n('B5', 2.0, 'ff'), '-mög-'))
    m.append(add_lyric(n('C6', 1.0), '-li-'))
    m.append(add_lyric(n('D6', 1.0), '-che'))
    measures[68] = m

    m = stream.Measure(number=69)
    m.append(add_lyric(n('E6', 2.0, 'fff'), 'es'))
    m.append(add_lyric(n('F6', 1.0), 'zer-'))
    m.append(add_lyric(n('E6', 1.0), ''))
    measures[69] = m

    for mm in range(70, 77):
        m = stream.Measure(number=mm)
        dyn_str = 'ffff' if mm == 70 else None
        m.append(add_lyric(n('A5', 4.0, dyn_str), '-bricht!' if mm == 70 else ''))
        measures[mm] = m

    for mm, (pitch, dyn_str) in enumerate([('F#5', 'fff'), ('D5', 'ff'),
                                            ('A4', 'f'), ('D4', 'ppp')],
                                           start=77):
        m = stream.Measure(number=mm)
        m.append(n(pitch, 4.0, dyn_str))
        measures[mm] = m

    return measures


def build_tenor_coda():
    """
    サンプル3 tenorV (treble_8 clef):
    mm.66: d2(h=2) f4(q=1) a4(q=1)   ff  "Neu-e"
    mm.67: b4(h=2) a4(q=1) g4(q=1)   ff  "Gren-ze"
    mm.68: fis4(h=2) g4(q=1) a4(q=1) fff "neu-es"
    mm.69-74: b4(wn) × 6小節          ffff "Licht!"
    mm.75-80: 解決
    """
    measures = {}

    m = stream.Measure(number=66)
    m.append(add_lyric(n('D4', 2.0, 'ff'), 'Neu-'))
    m.append(add_lyric(n('F#4', 1.0), '-e'))
    m.append(add_lyric(n('A4', 1.0), ''))
    measures[66] = m

    m = stream.Measure(number=67)
    m.append(add_lyric(n('B4', 2.0, 'ff'), 'Gren-'))
    m.append(add_lyric(n('A4', 1.0), '-ze'))
    m.append(add_lyric(n('G4', 1.0), ''))
    measures[67] = m

    m = stream.Measure(number=68)
    m.append(add_lyric(n('F#4', 2.0, 'fff'), 'neu-'))
    m.append(add_lyric(n('G4', 1.0), '-es'))
    m.append(add_lyric(n('A4', 1.0), ''))
    measures[68] = m

    for mm in range(69, 75):
        m = stream.Measure(number=mm)
        dyn_str = 'ffff' if mm == 69 else None
        m.append(add_lyric(n('B4', 4.0, dyn_str), 'Licht!' if mm == 69 else ''))
        measures[mm] = m

    for mm, (pitch, dyn_str) in enumerate([('A4', 'fff'), ('F#4', 'ff'),
                                            ('E4', 'f'), ('D4', 'p'),
                                            ('D4', 'pp'), ('D4', 'ppp')],
                                           start=75):
        m = stream.Measure(number=mm)
        m.append(n(pitch, 4.0, dyn_str))
        measures[mm] = m

    return measures


def build_bass_coda():
    """
    サンプル3 bassV:
    mm.66: d2(h=2) c4(q=1) b,4(q=1)  ff  "das Un-"
    mm.67: a,2(h=2) g,4(q=1) fis,4(q=1) ff "-mög-li-che"
    mm.68-80: d,1 (持続)               ffff "es zerbricht!"
    """
    measures = {}

    m = stream.Measure(number=66)
    m.append(add_lyric(n('D3', 2.0, 'ff'), 'das'))
    m.append(add_lyric(n('C3', 1.0), 'Un-'))
    m.append(add_lyric(n('B2', 1.0), ''))
    measures[66] = m

    m = stream.Measure(number=67)
    m.append(add_lyric(n('A2', 2.0, 'ff'), '-mög-'))
    m.append(add_lyric(n('G2', 1.0), '-li-'))
    m.append(add_lyric(n('F#2', 1.0), '-che'))
    measures[67] = m

    for mm in range(68, 81):
        m = stream.Measure(number=mm)
        dyn_str = 'ffff' if mm == 68 else 'ppp' if mm == 79 else None
        m.append(add_lyric(n('D2', 4.0, dyn_str),
                            'zer-bricht!' if mm == 68 else ''))
        measures[mm] = m

    return measures


# ============================================================
# 各パート完全実装
# ============================================================

def build_violin_i_v():
    custom = {}
    # mm.1-10: Ur-Motiv augmentation (D-C#-C) in D-dur
    for mm in range(1, 11):
        m = stream.Measure(number=mm)
        if mm == 1:
            m.insert(0, text_exp('Ur-Motiv augmentation: D–C#–C (fff)'))
        aug_seq = [('D5', 1.0), ('C#5', 1.0), ('C5', 2.0),
                   ('D5', 1.0), ('C#5', 1.0), ('C5', 2.0),
                   ('D5', 2.0), ('E5', 2.0),
                   ('F#5', 2.0), ('G5', 2.0),
                   ('A5', 4.0)]
        pitch, ql = aug_seq[mm - 1]
        m.append(n(pitch, ql, 'mf' if mm == 1 else None))
        # 残りを埋める
        remaining = 4.0 - ql
        if remaining > 0:
            m.append(r(remaining))
        custom[mm] = m

    # mm.11-40: ロンド主題
    for mm in range(11, 41):
        m = rondo_measure(mm)
        if mm == 11:
            m.insert(0, text_exp('Rondo Theme A — fff, tutta forza'))
            m.elements[0].dynamic = dynamics.Dynamic('fff')
        custom[mm] = m

    # mm.41-55: 5/4 エピソード
    for mm in range(41, 56):
        ml = measure_len(mm)
        m = stream.Measure(number=mm)
        if mm == 41:
            m.insert(0, text_exp('5/4 Episode — 全楽章統合'))
        # 第Ⅰ楽章動機 + 上行
        m.append(n('D5', 1.0, 'f'))
        m.append(n('C#5', 1.0))
        m.append(n('C5', 1.0))
        m.append(n('E5', 1.0))
        m.append(n('F#5', 1.0))
        custom[mm] = m

    # mm.56-65: 7/4 クライマックス前
    for mm in range(56, 66):
        ml = measure_len(mm)
        m = stream.Measure(number=mm)
        if mm == 56:
            m.insert(0, text_exp('7/4 — 溜め (Auftakt zum Coda)'))
        # D-dur 和音分散 × 7拍
        pitches = ['D5', 'F#5', 'A5', 'D6', 'A5', 'F#5', 'D5']
        for p in pitches:
            m.append(n(p, 1.0, 'ff' if mm == 56 else None))
        custom[mm] = m

    # mm.66-80: Coda (サンプル3)
    # サンプル3 violinIV より:
    # mm.66: d2(h=2) e4(q=1) fis4(q=1)  fff
    # mm.67: g2(h=2) fis4(q=1) e4(q=1)  fff
    # mm.68-76: d5(4.0) ffff
    m = stream.Measure(number=66)
    m.insert(0, text_exp('Coda — ♩=152 Maestoso-Presto'))
    m.append(n('D5', 2.0, 'fff'))
    m.append(n('E5', 1.0))
    m.append(n('F#5', 1.0))
    custom[66] = m

    m = stream.Measure(number=67)
    m.append(n('G5', 2.0, 'fff'))
    m.append(n('F#5', 1.0))
    m.append(n('E5', 1.0))
    custom[67] = m

    for mm in range(68, 77):
        m = stream.Measure(number=mm)
        dyn_str = 'ffff' if mm == 68 else None
        m.append(n('D5', 4.0, dyn_str))
        custom[mm] = m

    # mm.77-80: 終止
    for mm, (pitch, dyn_str) in enumerate([('A4', 'fff'), ('F#4', 'ff'),
                                            ('D4', 'f'), ('D4', 'ppp')],
                                           start=77):
        m = stream.Measure(number=mm)
        m.append(n(pitch, 4.0, dyn_str))
        custom[mm] = m

    return custom


def build_violin_ii_v():
    custom = {}
    # mm.11-40: ロンド主題（3度下）
    vn2_notes = ['B4', 'D5', 'F#5', 'B5', 'C#5', 'B4', 'A4', 'G4',
                 'B4', 'A4', 'G4', 'F#4', 'F#4', 'A4', 'E5', 'D5',
                 'D5', 'C#5', 'B4', 'A4', 'G4', 'A4', 'B4', 'F#4',
                 'G4', 'F#4', 'E4', 'D4', 'A4', 'D5']
    for mm in range(11, 41):
        m = stream.Measure(number=mm)
        pitch = vn2_notes[(mm - 11) % len(vn2_notes)]
        m.append(n(pitch, 4.0, 'f' if mm == 11 else None))
        custom[mm] = m
    # mm.41-55: 5/4
    for mm in range(41, 56):
        m = stream.Measure(number=mm)
        for p in ['F#4', 'A4', 'D5', 'F#5', 'A4']:
            m.append(n(p, 1.0, 'f' if mm == 41 else None))
        custom[mm] = m
    # mm.56-65: 7/4
    for mm in range(56, 66):
        m = stream.Measure(number=mm)
        for p in ['F#4', 'A4', 'D5', 'F#5', 'D5', 'A4', 'F#4']:
            m.append(n(p, 1.0, 'ff' if mm == 56 else None))
        custom[mm] = m
    # mm.66-80: Coda
    for mm in range(66, 81):
        m = stream.Measure(number=mm)
        m.append(n('F#4', 4.0, 'ffff' if mm == 68 else 'ppp' if mm == 80 else None))
        custom[mm] = m
    return custom


def build_viola_v():
    custom = {}
    for mm in range(11, 66):
        ml = measure_len(mm)
        m = stream.Measure(number=mm)
        if mm == 11:
            m.insert(0, text_exp('f — inner voice'))
        # A-D-F#-A のアルペジオ（Va 音域）
        num_beats = int(ml)
        pitches = ['A3', 'D4', 'F#4', 'A4']
        for i in range(num_beats):
            m.append(n(pitches[i % 4], 1.0, 'f' if mm == 11 and i == 0 else None))
        custom[mm] = m
    # Coda
    for mm in range(66, 81):
        m = stream.Measure(number=mm)
        m.append(n('F#3', 4.0, 'ffff' if mm == 68 else 'ppp' if mm == 80 else None))
        custom[mm] = m
    return custom


def build_cello_v():
    custom = {}
    # mm.11-65: D ペダル + ロンド主題低音
    for mm in range(11, 66):
        ml = measure_len(mm)
        m = stream.Measure(number=mm)
        # D3 → A2 → D3 繰り返し
        for i in range(int(ml)):
            pitch = 'D3' if i % 2 == 0 else 'A2'
            m.append(n(pitch, 1.0, 'f' if mm == 11 and i == 0 else None))
        custom[mm] = m
    # Coda
    for mm in range(66, 81):
        m = stream.Measure(number=mm)
        m.append(n('D2', 4.0, 'ffff' if mm == 68 else 'ppp' if mm == 80 else None))
        custom[mm] = m
    return custom


def build_contrabass_v():
    custom = {}
    for mm in range(1, 81):
        m = stream.Measure(number=mm)
        if mm == 1:
            m.insert(0, text_exp('D — pedal point, f sempre'))
        dyn_str = 'f' if mm == 1 else 'ffff' if mm == 68 else 'ppp' if mm == 80 else None
        m.append(n('D1', measure_len(mm), dyn_str))
        custom[mm] = m
    return custom


def build_flute_v():
    custom = {}
    for mm in range(11, 66):
        ml = measure_len(mm)
        m = stream.Measure(number=mm)
        if mm == 11:
            m.insert(0, text_exp('ff — D-dur 高音スケール'))
        # D5-E5-F#5-G5-A5-B5 スケール
        pitches = ['D5', 'E5', 'F#5', 'G5', 'A5', 'B5', 'A5', 'G5']
        for i in range(int(ml)):
            m.append(n(pitches[(mm + i) % len(pitches)], 1.0,
                       'ff' if mm == 11 and i == 0 else None))
        custom[mm] = m
    # Coda
    for mm in range(66, 81):
        m = stream.Measure(number=mm)
        m.append(n('D6', 4.0, 'ffff' if mm == 68 else 'ppp' if mm == 80 else None))
        custom[mm] = m
    return custom


def build_oboe_v():
    custom = {}
    for mm in range(11, 66):
        ml = measure_len(mm)
        m = stream.Measure(number=mm)
        pitches = ['A4', 'B4', 'C#5', 'D5', 'E5', 'F#5', 'E5', 'D5']
        for i in range(int(ml)):
            m.append(n(pitches[(mm + i) % len(pitches)], 1.0,
                       'ff' if mm == 11 and i == 0 else None))
        custom[mm] = m
    for mm in range(66, 81):
        m = stream.Measure(number=mm)
        m.append(n('A4', 4.0, 'ffff' if mm == 68 else 'ppp' if mm == 80 else None))
        custom[mm] = m
    return custom


def build_clarinet_v():
    custom = {}
    for mm in range(11, 66):
        ml = measure_len(mm)
        m = stream.Measure(number=mm)
        pitches = ['F#4', 'G4', 'A4', 'B4', 'C#5', 'D5', 'C#5', 'B4']
        for i in range(int(ml)):
            m.append(n(pitches[(mm + i) % len(pitches)], 1.0,
                       'ff' if mm == 11 and i == 0 else None))
        custom[mm] = m
    for mm in range(66, 81):
        m = stream.Measure(number=mm)
        m.append(n('C#5', 4.0, 'ffff' if mm == 68 else 'ppp' if mm == 80 else None))
        custom[mm] = m
    return custom


def build_fagotto_v():
    custom = {}
    for mm in range(11, 66):
        ml = measure_len(mm)
        m = stream.Measure(number=mm)
        for i in range(int(ml)):
            m.append(n('D3', 1.0, 'f' if mm == 11 and i == 0 else None))
        custom[mm] = m
    for mm in range(66, 81):
        m = stream.Measure(number=mm)
        m.append(n('D2', 4.0, 'ffff' if mm == 68 else 'ppp' if mm == 80 else None))
        custom[mm] = m
    return custom


def build_horn_v(num):
    custom = {}
    pitches = {1: 'D5', 2: 'A4', 3: 'F#4', 4: 'D3'}
    for mm in range(11, 66):
        ml = measure_len(mm)
        m = stream.Measure(number=mm)
        if mm == 11:
            m.insert(0, text_exp(f'Hr.{num} — ff, offen'))
        m.append(n(pitches[num], ml, 'ff' if mm == 11 else 'ffff' if mm == 56 else None))
        custom[mm] = m
    for mm in range(66, 81):
        m = stream.Measure(number=mm)
        m.append(n(pitches[num], 4.0, 'ffff' if mm == 68 else 'ppp' if mm == 80 else None))
        custom[mm] = m
    return custom


def build_trumpet_v(num):
    """
    サンプル3 trumpetV:
    mm.66-67: 全休符
    mm.68-76: d''' (D6) ffff 持続
    """
    custom = {}
    # mm.30-65: 金管参加
    for mm in range(30, 66):
        m = stream.Measure(number=mm)
        if mm == 30:
            m.insert(0, text_exp(f'Tp.{num} — fff subito'))
        ml = measure_len(mm)
        pitches = {1: 'D5', 2: 'C#5', 3: 'A4'}
        m.append(n(pitches[num], ml, 'fff' if mm == 30 else 'ffff' if mm == 56 else None))
        custom[mm] = m
    # mm.66-67: 全休符（Coda 準備）
    # mm.68: d''' (D6) 宣言
    for mm in range(68, 81):
        m = stream.Measure(number=mm)
        if mm == 68:
            m.insert(0, text_exp(f'Tp.{num} — d\'\'\'({TP_HIGH}) FFFF 限界突破宣言'))
        dyn_str = 'ffff' if mm == 68 else 'ppp' if mm == 80 else None
        m.append(n(TP_HIGH if num == 1 else ('A5' if num == 2 else 'F#5'),
                   4.0, dyn_str))
        custom[mm] = m
    return custom


def build_trombone_v(num):
    custom = {}
    for mm in range(30, 81):
        m = stream.Measure(number=mm)
        ml = measure_len(mm)
        pitches = {1: 'B-2', 2: 'F2', 3: 'D2'}
        dyn_str = 'fff' if mm == 30 else 'ffff' if mm == 56 or mm == 68 else 'ppp' if mm == 80 else None
        m.append(n(pitches[num], ml if mm < 66 else 4.0, dyn_str))
        custom[mm] = m
    return custom


def build_tuba_v():
    custom = {}
    for mm in range(30, 81):
        m = stream.Measure(number=mm)
        ml = measure_len(mm)
        dyn_str = 'fff' if mm == 30 else 'ffff' if mm == 68 else 'ppp' if mm == 80 else None
        m.append(n('D1', ml if mm < 66 else 4.0, dyn_str))
        custom[mm] = m
    return custom


def build_timpani_v():
    """
    サンプル3 timpV:
    mm.66: d8 d d d4 d d2   fff (「運命」動機変容リズム)
    mm.67: d8 d d d4 d d2   fff
    mm.68-76: d1 ffff
    """
    custom = {}
    for mm in range(11, 66):
        ml = measure_len(mm)
        m = stream.Measure(number=mm)
        if mm == 11:
            m.insert(0, text_exp('Timp — fff, 第Ⅱ楽章 tremolo 4台→1台に収束'))
        for _ in range(int(ml * 2)):  # 8分音符で刻む
            m.append(n('D2', 0.5, 'fff' if mm == 11 and _ == 0 else None))
        custom[mm] = m

    # mm.66-67: 「運命」動機リズム (♪♪♪♩ 変容)
    for mm in [66, 67]:
        m = stream.Measure(number=mm)
        if mm == 66:
            m.insert(0, text_exp('「運命」リズム変容: ♪♪♪♩♩♩𝅗𝅥 — fff'))
        m.append(n('D2', 0.5, 'fff'))
        m.append(n('D2', 0.5))
        m.append(n('D2', 0.5))
        m.append(n('D2', 1.0))
        m.append(n('D2', 1.0))
        m.append(n('D2', 0.5))
        custom[mm] = m

    for mm in range(68, 81):
        m = stream.Measure(number=mm)
        dyn_str = 'ffff' if mm == 68 else 'ppp' if mm == 80 else None
        m.append(n('D2', 4.0, dyn_str))
        custom[mm] = m

    return custom


def build_soprano_v():
    custom = {}
    # mm.11-40: Strophe 1 (S/A canon)
    strophe1_sop = [
        # "Die Grenze ist nicht Ende,"
        ('D5', 1.0, 'Die'), ('F#5', 1.0, 'Gren-'), ('A5', 1.0, '-ze'), ('B5', 1.0, 'ist'),
        ('C6', 2.0, 'nicht'), ('A5', 2.0, 'En-'),
        ('G5', 2.0, '-de,'), (None, 2.0, ''),
        # "sie ist der Ort, wo wir beginnen."
        ('F#5', 1.0, 'sie'), ('E5', 1.0, 'ist'), ('D5', 1.0, 'der'), ('E5', 1.0, 'Ort,'),
        ('F#5', 2.0, 'wo'), ('G5', 2.0, 'wir'),
        ('A5', 2.0, 'be-'), ('D5', 2.0, '-gin-'),
        ('D5', 4.0, '-nen.'),
        (None, 4.0, ''),
    ]
    for i, (pitch, ql, lyric) in enumerate(strophe1_sop):
        mm = 11 + i
        if mm > 40:
            break
        m = stream.Measure(number=mm)
        if mm == 11:
            m.insert(0, text_exp('Strophe 1 — S leading'))
        if pitch:
            m.append(add_lyric(n(pitch, ql, 'f' if mm == 11 else None), lyric))
            if ql < 4.0:
                m.append(r(4.0 - ql))
        else:
            m.append(r(4.0))
        custom[mm] = m

    # mm.41-65: 5/4 + 7/4 区間
    for mm in range(41, 66):
        ml = measure_len(mm)
        m = stream.Measure(number=mm)
        m.append(n('D5', ml, 'ff' if mm == 56 else None))
        custom[mm] = m

    # mm.66-80: Coda
    coda = build_soprano_coda()
    custom.update(coda)
    return custom


def build_alto_v():
    custom = {}
    # mm.16-40: Strophe 1 カノン（S の5小節遅れ）
    strophe1_alt = [
        ('D5', 1.0, 'Die'), ('F#5', 1.0, 'Gren-'), ('A5', 1.0, '-ze'), ('B5', 1.0, 'ist'),
        ('C6', 2.0, 'nicht'), ('A5', 2.0, 'En-'),
        ('G5', 2.0, '-de,'), (None, 2.0, ''),
        ('F#5', 1.0, 'sie'), ('E5', 1.0, 'ist'), ('D5', 1.0, 'der'), ('E5', 1.0, 'Ort,'),
        ('F#5', 2.0, 'wo'), ('G5', 2.0, 'wir'),
        ('A5', 2.0, 'be-'), ('D5', 2.0, '-gin-'),
        ('D5', 4.0, '-nen.'),
        (None, 4.0, ''),
        (None, 4.0, ''),
        (None, 4.0, ''),
        (None, 4.0, ''),
        (None, 4.0, ''),
        (None, 4.0, ''),
        (None, 4.0, ''),
        (None, 4.0, ''),
    ]
    for i, (pitch, ql, lyric) in enumerate(strophe1_alt):
        mm = 16 + i
        if mm > 40:
            break
        m = stream.Measure(number=mm)
        if mm == 16:
            m.insert(0, text_exp('Strophe 1 — A (5mm. canon after S)'))
        if pitch:
            m.append(add_lyric(n(pitch, ql, 'f' if mm == 16 else None), lyric))
            if ql < 4.0:
                m.append(r(4.0 - ql))
        else:
            m.append(r(4.0))
        custom[mm] = m

    for mm in range(41, 66):
        ml = measure_len(mm)
        m = stream.Measure(number=mm)
        m.append(n('A4', ml, 'ff' if mm == 56 else None))
        custom[mm] = m

    coda = build_alto_coda()
    custom.update(coda)
    return custom


def build_tenor_v():
    custom = {}
    # mm.11-40: Strophe 2 (T/B)
    strophe2_ten = [
        # "Im Schweigen hörten wir die Welt,"
        ('D4', 1.0, 'Im'), ('E4', 1.0, 'Schwei-'), ('F#4', 1.0, '-gen'), ('G4', 1.0, 'hör-'),
        ('A4', 2.0, '-ten'), ('G4', 2.0, 'wir'),
        ('F#4', 2.0, 'die'), ('E4', 2.0, 'Welt,'),
        # "im Sturm erkannten wir uns selbst."
        ('F#4', 1.0, 'im'), ('G4', 1.0, 'Sturm'), ('A4', 1.0, 'er-'), ('B4', 1.0, 'kann-'),
        ('C#5', 2.0, '-ten'), ('B4', 2.0, 'wir'),
        ('A4', 2.0, 'uns'), ('G4', 2.0, 'selbst.'),
        ('F#4', 4.0, ''),
        (None, 4.0, ''),
        (None, 4.0, ''),
        (None, 4.0, ''),
        (None, 4.0, ''),
        (None, 4.0, ''),
        (None, 4.0, ''),
        (None, 4.0, ''),
        (None, 4.0, ''),
        (None, 4.0, ''),
        (None, 4.0, ''),
        (None, 4.0, ''),
        (None, 4.0, ''),
        (None, 4.0, ''),
    ]
    for i, (pitch, ql, lyric) in enumerate(strophe2_ten):
        mm = 11 + i
        if mm > 40:
            break
        m = stream.Measure(number=mm)
        if mm == 11:
            m.insert(0, text_exp('Strophe 2 — T'))
        if pitch:
            m.append(add_lyric(n(pitch, ql, 'f' if mm == 11 else None), lyric))
            if ql < 4.0:
                m.append(r(4.0 - ql))
        else:
            m.append(r(4.0))
        custom[mm] = m

    for mm in range(41, 66):
        ml = measure_len(mm)
        m = stream.Measure(number=mm)
        m.append(n('F#4', ml, 'ff' if mm == 56 else None))
        custom[mm] = m

    coda = build_tenor_coda()
    custom.update(coda)
    return custom


def build_bass_v():
    custom = {}
    # mm.11-40: Strophe 2 (T/B)
    strophe2_bas = [
        ('D3', 1.0, 'Im'), ('E3', 1.0, 'Schwei-'), ('F#3', 1.0, '-gen'), ('G3', 1.0, 'hör-'),
        ('A3', 2.0, '-ten'), ('G3', 2.0, 'wir'),
        ('F#3', 2.0, 'die'), ('E3', 2.0, 'Welt,'),
        ('F#3', 1.0, 'im'), ('G3', 1.0, 'Sturm'), ('A3', 1.0, 'er-'), ('B3', 1.0, 'kann-'),
        ('C#4', 2.0, '-ten'), ('B3', 2.0, 'wir'),
        ('A3', 2.0, 'uns'), ('G3', 2.0, 'selbst.'),
        ('F#3', 4.0, ''),
        (None, 4.0, ''), (None, 4.0, ''), (None, 4.0, ''),
        (None, 4.0, ''), (None, 4.0, ''), (None, 4.0, ''),
        (None, 4.0, ''), (None, 4.0, ''), (None, 4.0, ''),
        (None, 4.0, ''), (None, 4.0, ''), (None, 4.0, ''),
        (None, 4.0, ''),
    ]
    for i, (pitch, ql, lyric) in enumerate(strophe2_bas):
        mm = 11 + i
        if mm > 40:
            break
        m = stream.Measure(number=mm)
        if mm == 11:
            m.insert(0, text_exp('Strophe 2 — B'))
        if pitch:
            m.append(add_lyric(n(pitch, ql, 'f' if mm == 11 else None), lyric))
            if ql < 4.0:
                m.append(r(4.0 - ql))
        else:
            m.append(r(4.0))
        custom[mm] = m

    for mm in range(41, 66):
        ml = measure_len(mm)
        m = stream.Measure(number=mm)
        m.append(n('D3', ml, 'ff' if mm == 56 else None))
        custom[mm] = m

    coda = build_bass_coda()
    custom.update(coda)
    return custom


# ============================================================
# パート設定テーブル
# ============================================================

PARTS_CONFIG = [
    ('Flute',          'Fl.',   instrument.Flute(),       'treble', build_flute_v),
    ('Oboe',           'Ob.',   instrument.Oboe(),         'treble', build_oboe_v),
    ('Clarinet in Bb', 'Cl.',   instrument.Clarinet(),     'treble', build_clarinet_v),
    ('Fagotto',        'Fg.',   instrument.Bassoon(),      'bass',   build_fagotto_v),
    ('Horn in F 1',    'Hr.1',  instrument.Horn(),         'treble', lambda: build_horn_v(1)),
    ('Horn in F 2',    'Hr.2',  instrument.Horn(),         'treble', lambda: build_horn_v(2)),
    ('Horn in F 3',    'Hr.3',  instrument.Horn(),         'treble', lambda: build_horn_v(3)),
    ('Horn in F 4',    'Hr.4',  instrument.Horn(),         'bass',   lambda: build_horn_v(4)),
    ('Trumpet in C 1', 'Tp.1',  instrument.Trumpet(),      'treble', lambda: build_trumpet_v(1)),
    ('Trumpet in C 2', 'Tp.2',  instrument.Trumpet(),      'treble', lambda: build_trumpet_v(2)),
    ('Trumpet in C 3', 'Tp.3',  instrument.Trumpet(),      'treble', lambda: build_trumpet_v(3)),
    ('Trombone 1',     'Tb.1',  instrument.Trombone(),     'bass',   lambda: build_trombone_v(1)),
    ('Trombone 2',     'Tb.2',  instrument.Trombone(),     'bass',   lambda: build_trombone_v(2)),
    ('Trombone 3',     'Tb.3',  instrument.Trombone(),     'bass',   lambda: build_trombone_v(3)),
    ('Tuba',           'Tuba',  instrument.Tuba(),         'bass',   build_tuba_v),
    ('Timpani',        'Timp.', instrument.Timpani(),      'bass',   build_timpani_v),
    ('Soprano',        'S.',    instrument.Soprano(),      'treble', build_soprano_v),
    ('Alto',           'A.',    instrument.Alto(),         'treble', build_alto_v),
    ('Tenor',          'T.',    instrument.Tenor(),        'treble', build_tenor_v),
    ('Bass',           'B.',    instrument.Bass(),         'bass',   build_bass_v),
    ('Violin I',       'Vn.I',  instrument.Violin(),       'treble', build_violin_i_v),
    ('Violin II',      'Vn.II', instrument.Violin(),       'treble', build_violin_ii_v),
    ('Viola',          'Va.',   instrument.Viola(),        'alto',   build_viola_v),
    ('Violoncello',    'Vc.',   instrument.Violoncello(),  'bass',   build_cello_v),
    ('Contrabass',     'Cb.',   instrument.Contrabass(),   'bass',   build_contrabass_v),
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

    prev_ts = None
    for mm in range(1, TOTAL_MEASURES + 1):
        ts = get_ts(mm)

        if mm in custom_measures_dict:
            m = custom_measures_dict[mm]
        else:
            m = rest_measure(mm)

        m.number = mm

        if mm == 1:
            m.insert(0, CLEF_MAP[clef_type]())
            m.insert(0, key.Key(KEY_STR))
            m.insert(0, meter.TimeSignature('4/4'))
            m.insert(0, tempo.MetronomeMark(text='Maestoso', number=96))

        if mm == CODA_START:
            has_tempo = any(isinstance(e, tempo.MetronomeMark) for e in m.elements)
            if not has_tempo:
                m.insert(0, tempo.MetronomeMark(
                    text='Maestoso – Presto', number=152))

        if ts != prev_ts and mm > 1:
            has_ts = any(isinstance(e, meter.TimeSignature) for e in m.elements)
            if not has_ts:
                m.insert(0, meter.TimeSignature(ts))

        prev_ts = ts
        part.append(m)

    return part


# ============================================================
# メイン
# ============================================================

def main():
    score = stream.Score()

    md = metadata.Metadata()
    md.title = 'Symphony No. XI "Grenze" — V. Neue Grenze'
    md.composer = 'Music TWIN Collective (Soul-Twin Society, 2026)'
    score.insert(0, md)

    print(f'Soprano high: {SOPRANO_HIGH}  Trumpet high: {TP_HIGH}')
    print(f'Coda: mm.{CODA_START}-{TOTAL_MEASURES}  (♩=152)')
    print()

    for name, abbrev, instr, clef_t, builder in PARTS_CONFIG:
        print(f'  Building part: {name}')
        custom = builder()
        part = build_part(name, abbrev, instr, clef_t, custom)
        score.insert(0, part)

    out_path = 'beethoven_xi_mov5.xml'
    score.write('musicxml', fp=out_path)
    print(f'\nMusicXML saved: {out_path}')


if __name__ == '__main__':
    main()
