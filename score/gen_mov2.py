#!/usr/bin/env python3
"""
Symphony No. XI "Grenze"
II. Kollision  (Allegro feroce — 7/8 + 5/8 交替変拍子)

全25パート MusicXML 生成スクリプト（music21 使用）
MC_オーケストラパート別技法要求書 + MA_楽曲構造分析書 に基づく実装

実行: python gen_mov2.py
出力: beethoven_xi_mov2.xml  →  MuseScore4 で .mscz に変換
"""

from music21 import (
    stream, note, chord, metadata, key, meter, tempo,
    instrument, clef, dynamics, expressions, articulations, duration
)

# ============================================================
# グローバル設定
# ============================================================
TOTAL_MEASURES = 80
KEY = 'b'   # b-moll (2♯: F#, C#)

# 変拍子パターン: 5/8 は mm.5-6 のみ (Bass Rezitativ 内省部)
# 以降は 7/8 継続（突発的5/8は mm.40-50 周辺に配置）
TIME_PATTERN = {}
for _mm in range(1, TOTAL_MEASURES + 1):
    if _mm in [5, 6, 40, 42, 44]:
        TIME_PATTERN[_mm] = '5/8'
    else:
        TIME_PATTERN[_mm] = '7/8'

MEASURE_LEN = {'7/8': 3.5, '5/8': 2.5}

TEMPO_MARK = 132


# ============================================================
# ユーティリティ
# ============================================================

def get_ts(mm):
    return TIME_PATTERN.get(mm, '7/8')


def measure_len(mm):
    return MEASURE_LEN[get_ts(mm)]


def rest_measure(mm):
    """拍子に合った全休符小節"""
    m = stream.Measure(number=mm)
    ts = get_ts(mm)
    if ts == '5/8':
        m.append(note.Rest(quarterLength=2.5))
    else:
        m.append(note.Rest(quarterLength=3.5))
    return m


def n(pitch, ql, dyn_str=None):
    nn = note.Note(pitch, quarterLength=ql)
    if dyn_str:
        nn.dynamic = dynamics.Dynamic(dyn_str)
    return nn


def r(ql):
    return note.Rest(quarterLength=ql)


def text_exp(txt, placement='above'):
    te = expressions.TextExpression(txt)
    te.placement = placement
    return te


def dyn(marking):
    return dynamics.Dynamic(marking)


def add_lyric(note_obj, text):
    note_obj.addLyric(text)
    return note_obj


# ============================================================
# 変拍子ヘッダー付き小節生成
# ============================================================

def make_measure(mm, elements, extras=None, prev_ts=None):
    """
    mm: 小節番号
    elements: Note/Rest のリスト（合計拍数は拍子に合わせること）
    extras: (offset, elem) のリスト
    prev_ts: 前小節の拍子文字列（同じなら TimeSignature を省略）
    """
    m = stream.Measure(number=mm)
    ts = get_ts(mm)
    if ts != prev_ts:
        m.insert(0, meter.TimeSignature(ts))
    if extras:
        for offset, elem in extras:
            m.insert(offset, elem)
    for e in elements:
        m.append(e)
    return m


# ============================================================
# Bass Rezitativ（mm.1-12）— 第Ⅱ楽章の核心
# ============================================================

def bass_rezitativ():
    """
    MC文書 LilyPond Sample 2 より変換。
    旋律: B3→C4→D4→E4→F#4→G4→A4→B4（上昇型、第9番の逆）
    歌詞: "O Grenze, nicht dieses Ende! / Hier beginnt das wahre Lied!"
    拍子: 7/8 (mm.1-4) → 5/8 (mm.5-6) → 7/8 (mm.7-12)
    """
    measures = {}
    prev = None

    # mm.1 (7/8, 3.5拍): B3(q=1) C4(e=0.5) D4(e=0.5) E4(de=1.5)  f
    elems = [
        add_lyric(n('B3', 1.0, 'f'), 'O'),
        add_lyric(n('C4', 0.5), 'Gren-'),
        add_lyric(n('D4', 0.5), '-ze,'),
        add_lyric(n('E4', 1.5), 'nicht'),
    ]
    extras = [(0, text_exp('Bass Solo — "O Grenze, nicht dieses Ende!"'))]
    measures[1] = make_measure(1, elems, extras, prev); prev = '7/8'

    # mm.2 (7/8, 3.5拍): E4(q=1) F#4(q=1) rest(de=1.5)
    elems = [
        add_lyric(n('E4', 1.0), 'die-'),
        add_lyric(n('F#4', 1.0), '-ses'),
        add_lyric(r(1.5), ''),
    ]
    measures[2] = make_measure(2, elems, None, prev)

    # mm.3 (7/8, 3.5拍): F#4(q=1) G4(e=0.5) A4(e=0.5) B4(de=1.5)  ff
    elems = [
        add_lyric(n('F#4', 1.0, 'ff'), 'En-'),
        add_lyric(n('G4', 0.5), '-de!'),
        add_lyric(n('A4', 0.5), 'Hier'),
        add_lyric(n('B4', 1.5), 'be-'),
    ]
    measures[3] = make_measure(3, elems, None, prev)

    # mm.4 (7/8, 3.5拍): F#4(h=2) E4(de=1.5)
    elems = [
        add_lyric(n('F#4', 2.0), '-ginnt'),
        add_lyric(n('E4', 1.5), 'das'),
    ]
    measures[4] = make_measure(4, elems, None, prev)

    # mm.5 (5/8, 2.5拍): D4(e=0.5) C#4(q=1) B3(q=1)  ppp
    elems = [
        add_lyric(n('D4', 0.5, 'ppp'), 'wah-'),
        add_lyric(n('C#4', 1.0), '-re'),
        add_lyric(n('B3', 1.0), 'Lied!'),
    ]
    measures[5] = make_measure(5, elems, None, prev); prev = '5/8'

    # mm.6 (5/8, 2.5拍): 全休符（内省）
    measures[6] = make_measure(6, [r(2.5)], [(0, text_exp('(silenzio)'))] , prev)

    # mm.7 (7/8, 3.5拍): 再宣言  f
    elems = [
        add_lyric(n('B3', 1.0, 'f'), 'Neu-'),
        add_lyric(n('C4', 0.5), '-e'),
        add_lyric(n('D4', 0.5), 'Gren-'),
        add_lyric(n('E4', 1.5), '-ze,'),
    ]
    measures[7] = make_measure(7, elems, None, '5/8'); prev = '7/8'

    # mm.8 (7/8, 3.5拍): F#4(q=1) G4(q=1) A4(de=1.5)
    elems = [
        add_lyric(n('F#4', 1.0), 'neu-'),
        add_lyric(n('G4', 1.0), '-es'),
        add_lyric(n('A4', 1.5), 'Licht!'),
    ]
    measures[8] = make_measure(8, elems, None, prev)

    # mm.9 (7/8, 3.5拍): A4(q=1) B4(q=1) F#4(de=1.5)
    elems = [
        add_lyric(n('A4', 1.0), 'Hier'),
        add_lyric(n('B4', 1.0), 'be-'),
        add_lyric(n('F#4', 1.5), '-ginnt'),
    ]
    measures[9] = make_measure(9, elems, None, prev)

    # mm.10 (7/8, 3.5拍): F#4(h=2) E4(de=1.5)  ff
    elems = [
        add_lyric(n('F#4', 2.0, 'ff'), 'das'),
        add_lyric(n('E4', 1.5), 'wah-'),
    ]
    measures[10] = make_measure(10, elems, None, prev)

    # mm.11 (7/8, 3.5拍): B3(h=2) rest(de=1.5)  ppp
    elems = [
        add_lyric(n('B3', 2.0, 'ppp'), '-re'),
        r(1.5),
    ]
    measures[11] = make_measure(11, elems, None, prev)

    # mm.12 (7/8, 3.5拍): B3(de=1.5) rest(q=1) rest(q=1)
    elems = [
        add_lyric(n('B3', 1.5), 'Lied!'),
        r(2.0),
    ]
    measures[12] = make_measure(12, elems, None, prev)

    return measures


# ============================================================
# 各パートの custom 小節
# ============================================================

def build_bass_solo():
    """Bass独唱パート"""
    custom = bass_rezitativ()
    # mm.13-80: 全休符（合唱は mm.60 台で再登場予定・スタブ）
    # mm.60-70: 合唱クライマックス前の独唱
    m60 = stream.Measure(number=60)
    m60.insert(0, meter.TimeSignature('7/8'))
    m60.insert(0, text_exp('fff — Kulmination'))
    m60.append(add_lyric(n('B4', 1.0, 'fff'), 'O'))
    m60.append(add_lyric(n('C#5', 0.5), 'Gren-'))
    m60.append(add_lyric(n('D5', 0.5), '-ze!'))
    m60.append(add_lyric(n('E5', 1.5), ''))
    custom[60] = m60
    return custom


def build_timpani_ii():
    """
    Timpani 4台の pp tremolo（mm.1-12）→ ポリリズム（mm.80）
    music21では1パートとして実装（4台ユニゾン → 複数音符）
    """
    custom = {}
    # mm.1-12: pp tremolo (B2ペダル)
    for mm in range(1, 13):
        m = stream.Measure(number=mm)
        ts = get_ts(mm)
        if ts != (get_ts(mm - 1) if mm > 1 else None):
            m.insert(0, meter.TimeSignature(ts))
        if mm == 1:
            m.insert(0, text_exp('4 Timpani — pp tremolo sempre'))
        ml = measure_len(mm)
        num_e = int(ml / 0.5)  # 8分音符の個数
        for _ in range(num_e):
            m.append(n('B2', 0.5, 'pp' if mm == 1 else None))
        custom[mm] = m

    # mm.80: 4台ユニゾン → fff (C2)
    m80 = stream.Measure(number=80)
    m80.insert(0, meter.TimeSignature('7/8'))
    m80.insert(0, text_exp('ffff — tutti Timp convergence'))
    for _ in range(7):
        m80.append(n('B2', 0.5, 'ffff' if _ == 0 else None))
    custom[80] = m80
    return custom


def build_contrabass_ii():
    """pizzicato sfz — 各小節1打目 sfz"""
    custom = {}
    for mm in range(1, 41):
        m = stream.Measure(number=mm)
        ts = get_ts(mm)
        prev_ts = get_ts(mm - 1) if mm > 1 else None
        if ts != prev_ts:
            m.insert(0, meter.TimeSignature(ts))
        if mm == 1:
            m.insert(0, text_exp('pizzicato sfz on beat 1'))
        dyn_str = 'pp' if mm <= 12 else ('mf' if mm <= 30 else 'f')
        m.append(n('B2', 1.0, dyn_str))
        m.append(r(measure_len(mm) - 1.0))
        custom[mm] = m
    return custom


def build_violin_i_ii():
    """
    第Ⅱ楽章 Vn.I: spiccato + fff、半音クラスター
    mm.13 から参加
    """
    custom = {}
    for mm in range(13, 61):
        m = stream.Measure(number=mm)
        ts = get_ts(mm)
        prev_ts = get_ts(mm - 1) if mm > 1 else None
        if ts != prev_ts:
            m.insert(0, meter.TimeSignature(ts))
        if mm == 13:
            m.insert(0, text_exp('spiccato, fff — cluster: C#"-D"-D#"'))
        ml = measure_len(mm)
        num_e = int(ml / 0.5)
        # 半音クラスター（C5-C#5 往復）
        pitches = ['C5', 'C#5', 'D5', 'C#5', 'C5', 'C#5', 'D5', 'D#5']
        for i in range(num_e):
            p = pitches[i % len(pitches)]
            dyn_str = 'fff' if mm == 13 and i == 0 else None
            m.append(n(p, 0.5, dyn_str))
        custom[mm] = m
    return custom


def build_violin_ii_ii():
    """Vn.II: 複付点リズム刻み（逆アクセント）、mm.13 から"""
    custom = {}
    for mm in range(13, 61):
        m = stream.Measure(number=mm)
        ts = get_ts(mm)
        prev_ts = get_ts(mm - 1) if mm > 1 else None
        if ts != prev_ts:
            m.insert(0, meter.TimeSignature(ts))
        if mm == 13:
            m.insert(0, text_exp('double stop 4th — ff'))
        ml = measure_len(mm)
        # 付点四分 + 8分 の繰り返し
        remaining = ml
        idx = 0
        pattern = [1.5, 0.5, 1.5, 0.5]  # 付点q + e 繰り返し
        while remaining > 0.05:
            ql = min(pattern[idx % len(pattern)], remaining)
            p = 'D5' if (idx % 2 == 0) else 'A4'
            dyn_str = 'ff' if mm == 13 and idx == 0 else None
            m.append(n(p, ql, dyn_str))
            remaining -= ql
            idx += 1
        custom[mm] = m
    return custom


def build_viola_ii():
    """Bartók pizzicato、mm.13 から"""
    custom = {}
    for mm in range(13, 61):
        m = stream.Measure(number=mm)
        ts = get_ts(mm)
        prev_ts = get_ts(mm - 1) if mm > 1 else None
        if ts != prev_ts:
            m.insert(0, meter.TimeSignature(ts))
        if mm == 13:
            m.insert(0, text_exp('Bartók pizzicato — fff'))
        ml = measure_len(mm)
        # C-G-D-A 各8分音符
        pitches = ['C4', 'G4', 'D4', 'A4']
        num_e = int(ml / 0.5)
        for i in range(num_e):
            p = pitches[i % 4]
            dyn_str = 'fff' if mm == 13 and i == 0 else None
            m.append(n(p, 0.5, dyn_str))
        custom[mm] = m
    return custom


def build_cello_ii():
    """弓圧変化（同音 pppp → ffff）、mm.13 から"""
    custom = {}
    for mm in range(13, 41):
        m = stream.Measure(number=mm)
        ts = get_ts(mm)
        prev_ts = get_ts(mm - 1) if mm > 1 else None
        if ts != prev_ts:
            m.insert(0, meter.TimeSignature(ts))
        ml = measure_len(mm)
        dyn_labels = {13: 'pppp', 20: 'pp', 27: 'mf', 35: 'f', 40: 'ffff'}
        dyn_str = dyn_labels.get(mm)
        if mm == 13:
            m.insert(0, text_exp('bow pressure crescendo: pppp → ffff (28mm.)'))
        m.append(n('B2', ml, dyn_str))
        custom[mm] = m
    return custom


def build_contrabass_ii_part():
    return build_contrabass_ii()


def build_flute_ii():
    """超高速スケール（3オクターブ）、mm.17 から"""
    custom = {}
    for mm in range(17, 61):
        m = stream.Measure(number=mm)
        ts = get_ts(mm)
        prev_ts = get_ts(mm - 1) if mm > 1 else None
        if ts != prev_ts:
            m.insert(0, meter.TimeSignature(ts))
        if mm == 17:
            m.insert(0, text_exp('3-octave scale at ♩=132 — fff'))
        ml = measure_len(mm)
        # B4→B5→B6→B5→B4 を往復（近似）
        num_e = int(ml / 0.5)
        pitches_cycle = ['B4', 'C#5', 'D5', 'E5', 'F#5', 'G5', 'A5', 'B5']
        for i in range(num_e):
            p = pitches_cycle[i % len(pitches_cycle)]
            dyn_str = 'fff' if mm == 17 and i == 0 else None
            m.append(n(p, 0.5, dyn_str))
        custom[mm] = m
    return custom


def build_oboe_ii():
    """staccatissimo 連打（等間隔）、mm.17 から"""
    custom = {}
    for mm in range(17, 61):
        m = stream.Measure(number=mm)
        ts = get_ts(mm)
        prev_ts = get_ts(mm - 1) if mm > 1 else None
        if ts != prev_ts:
            m.insert(0, meter.TimeSignature(ts))
        if mm == 17:
            m.insert(0, text_exp('staccatissimo — ff'))
        ml = measure_len(mm)
        num_e = int(ml / 0.5)
        for i in range(num_e):
            nn = n('B4', 0.5, 'ff' if mm == 17 and i == 0 else None)
            nn.articulations.append(articulations.Staccatissimo())
            m.append(nn)
        custom[mm] = m
    return custom


def build_clarinet_ii():
    """overblow + 3オクターブ跳躍、mm.17 から"""
    custom = {}
    for mm in range(17, 61):
        m = stream.Measure(number=mm)
        ts = get_ts(mm)
        prev_ts = get_ts(mm - 1) if mm > 1 else None
        if ts != prev_ts:
            m.insert(0, meter.TimeSignature(ts))
        if mm == 17:
            m.insert(0, text_exp('overblow / 3-oct jump'))
        ml = measure_len(mm)
        # chalumeau → altissimo 跳躍
        pitches = ['B3', 'B4', 'B5', 'B4']
        num_e = int(ml / 0.5)
        for i in range(num_e):
            p = pitches[i % len(pitches)]
            dyn_str = 'ff' if mm == 17 and i == 0 else None
            m.append(n(p, 0.5, dyn_str))
        custom[mm] = m
    return custom


def build_fagotto_ii():
    """staccato 8分音符連打（バスライン）、mm.1 から"""
    custom = {}
    for mm in range(1, 41):
        m = stream.Measure(number=mm)
        ts = get_ts(mm)
        prev_ts = get_ts(mm - 1) if mm > 1 else None
        if ts != prev_ts:
            m.insert(0, meter.TimeSignature(ts))
        if mm == 1:
            m.insert(0, text_exp('staccato bass line'))
        ml = measure_len(mm)
        num_e = int(ml / 0.5)
        # B2 → F#2 → B2
        pitches = ['B2', 'F#2', 'B2', 'F#2', 'E2', 'F#2', 'G2', 'A2']
        for i in range(num_e):
            p = pitches[i % len(pitches)]
            dyn_str = 'mf' if mm == 1 and i == 0 else None
            nn = n(p, 0.5, dyn_str)
            if mm >= 1:
                nn.articulations.append(articulations.Staccato())
            m.append(nn)
        custom[mm] = m
    return custom


def build_horn_ii(num):
    """4本フーガ様独立旋律、mm.25 から"""
    custom = {}
    # 各Hrが異なる旋律で開始（半音ずつずれて fugue 風）
    start_pitch = {1: 'F#5', 2: 'E5', 3: 'D5', 4: 'C#5'}
    for mm in range(25, 61):
        m = stream.Measure(number=mm)
        ts = get_ts(mm)
        prev_ts = get_ts(mm - 1) if mm > 1 else None
        if ts != prev_ts:
            m.insert(0, meter.TimeSignature(ts))
        if mm == 25:
            m.insert(0, text_exp(f'Hr.{num} — shake fff (Fugue entry {num})'))
        ml = measure_len(mm)
        sp = start_pitch[num]
        # 開始音から上昇・下降を繰り返す
        root_note = note.Note(sp)
        pitch_name = root_note.nameWithOctave
        num_e = int(ml / 0.5)
        pitches_map = {1: ['F#5', 'G5', 'A5', 'B5', 'A5', 'G5', 'F#5', 'E5'],
                       2: ['E5', 'F#5', 'G5', 'A5', 'G5', 'F#5', 'E5', 'D5'],
                       3: ['D5', 'E5', 'F#5', 'G5', 'F#5', 'E5', 'D5', 'C#5'],
                       4: ['C#5', 'D5', 'E5', 'F#5', 'E5', 'D5', 'C#5', 'B4']}
        pc = pitches_map[num]
        for i in range(num_e):
            dyn_str = 'fff' if mm == 25 and i == 0 else None
            m.append(n(pc[i % len(pc)], 0.5, dyn_str))
        custom[mm] = m
    return custom


def build_trumpet_ii(num):
    """ハーフバルブ + sfz 連続、mm.30 から"""
    custom = {}
    for mm in range(30, 61):
        m = stream.Measure(number=mm)
        ts = get_ts(mm)
        prev_ts = get_ts(mm - 1) if mm > 1 else None
        if ts != prev_ts:
            m.insert(0, meter.TimeSignature(ts))
        if mm == 30:
            m.insert(0, text_exp(f'Tp.{num} — half-valve sfz on beat 1'))
        ml = measure_len(mm)
        p = ['D5', 'C#5', 'D5'][num - 1]
        m.append(n(p, 1.0, 'sfz'))
        m.append(r(measure_len(mm) - 1.0))
        custom[mm] = m
    return custom


def build_trombone_ii(num):
    """グリッサンド ffff、mm.35 から"""
    custom = {}
    for mm in range(35, 61):
        m = stream.Measure(number=mm)
        ts = get_ts(mm)
        prev_ts = get_ts(mm - 1) if mm > 1 else None
        if ts != prev_ts:
            m.insert(0, meter.TimeSignature(ts))
        if mm == 35:
            m.insert(0, text_exp(f'Tb.{num} — glissando ffff'))
        ml = measure_len(mm)
        p = ['B2', 'A2', 'G2'][num - 1]
        m.append(n(p, ml, 'ffff' if mm == 35 else None))
        custom[mm] = m
    return custom


def build_tuba_ii():
    """第Ⅱ楽章: mm.35 から低音主柱"""
    custom = {}
    for mm in range(35, 61):
        m = stream.Measure(number=mm)
        ts = get_ts(mm)
        prev_ts = get_ts(mm - 1) if mm > 1 else None
        if ts != prev_ts:
            m.insert(0, meter.TimeSignature(ts))
        if mm == 35:
            m.insert(0, text_exp('Tuba — fff bass pillar'))
        ml = measure_len(mm)
        m.append(n('B1', ml, 'fff' if mm == 35 else None))
        custom[mm] = m
    return custom


def build_soprano_ii():
    return {}  # 第Ⅱ楽章は soprano 休み


def build_alto_ii():
    """第Ⅱ楽章合唱: mm.50 から全体参加"""
    custom = {}
    for mm in range(50, 61):
        m = stream.Measure(number=mm)
        ts = get_ts(mm)
        prev_ts = get_ts(mm - 1) if mm > 1 else None
        if ts != prev_ts:
            m.insert(0, meter.TimeSignature(ts))
        if mm == 50:
            m.insert(0, text_exp('Alto — ff (chorus entry)'))
        ml = measure_len(mm)
        m.append(add_lyric(n('D5', ml, 'ff' if mm == 50 else None), 'Lied!' if mm == 50 else ''))
        custom[mm] = m
    return custom


def build_tenor_ii():
    """Rezitativ様式、mm.50 から"""
    custom = {}
    for mm in range(50, 61):
        m = stream.Measure(number=mm)
        ts = get_ts(mm)
        prev_ts = get_ts(mm - 1) if mm > 1 else None
        if ts != prev_ts:
            m.insert(0, meter.TimeSignature(ts))
        if mm == 50:
            m.insert(0, text_exp('Tenor — Rezitativ'))
        ml = measure_len(mm)
        m.append(add_lyric(n('F#4', ml, 'ff' if mm == 50 else None), 'Lied!' if mm == 50 else ''))
        custom[mm] = m
    return custom


# ============================================================
# パート設定テーブル
# ============================================================

PARTS_CONFIG = [
    ('Flute',          'Fl.',   instrument.Flute(),       'treble', 'b', build_flute_ii),
    ('Oboe',           'Ob.',   instrument.Oboe(),         'treble', 'b', build_oboe_ii),
    ('Clarinet in Bb', 'Cl.',   instrument.Clarinet(),     'treble', 'b', build_clarinet_ii),
    ('Fagotto',        'Fg.',   instrument.Bassoon(),      'bass',   'b', build_fagotto_ii),
    ('Horn in F 1',    'Hr.1',  instrument.Horn(),         'treble', 'b', lambda: build_horn_ii(1)),
    ('Horn in F 2',    'Hr.2',  instrument.Horn(),         'treble', 'b', lambda: build_horn_ii(2)),
    ('Horn in F 3',    'Hr.3',  instrument.Horn(),         'treble', 'b', lambda: build_horn_ii(3)),
    ('Horn in F 4',    'Hr.4',  instrument.Horn(),         'bass',   'b', lambda: build_horn_ii(4)),
    ('Trumpet in C 1', 'Tp.1',  instrument.Trumpet(),      'treble', 'b', lambda: build_trumpet_ii(1)),
    ('Trumpet in C 2', 'Tp.2',  instrument.Trumpet(),      'treble', 'b', lambda: build_trumpet_ii(2)),
    ('Trumpet in C 3', 'Tp.3',  instrument.Trumpet(),      'treble', 'b', lambda: build_trumpet_ii(3)),
    ('Trombone 1',     'Tb.1',  instrument.Trombone(),     'bass',   'b', lambda: build_trombone_ii(1)),
    ('Trombone 2',     'Tb.2',  instrument.Trombone(),     'bass',   'b', lambda: build_trombone_ii(2)),
    ('Trombone 3',     'Tb.3',  instrument.Trombone(),     'bass',   'b', lambda: build_trombone_ii(3)),
    ('Tuba',           'Tuba',  instrument.Tuba(),         'bass',   'b', build_tuba_ii),
    ('Timpani',        'Timp.', instrument.Timpani(),      'bass',   'b', build_timpani_ii),
    ('Soprano',        'S.',    instrument.Soprano(),      'treble', 'b', build_soprano_ii),
    ('Alto',           'A.',    instrument.Alto(),         'treble', 'b', build_alto_ii),
    ('Tenor',          'T.',    instrument.Tenor(),        'treble', 'b', build_tenor_ii),
    ('Bass',           'B.',    instrument.Bass(),         'bass',   'b', build_bass_solo),
    ('Violin I',       'Vn.I',  instrument.Violin(),       'treble', 'b', build_violin_i_ii),
    ('Violin II',      'Vn.II', instrument.Violin(),       'treble', 'b', build_violin_ii_ii),
    ('Viola',          'Va.',   instrument.Viola(),        'alto',   'b', build_viola_ii),
    ('Violoncello',    'Vc.',   instrument.Violoncello(),  'bass',   'b', build_cello_ii),
    ('Contrabass',     'Cb.',   instrument.Contrabass(),   'bass',   'b', build_contrabass_ii_part),
]


CLEF_MAP = {
    'treble': clef.TrebleClef,
    'bass':   clef.BassClef,
    'alto':   clef.AltoClef,
    'tenor':  clef.TenorClef,
}


def build_part(name, abbrev, instr, clef_type, key_str, custom_measures_dict):
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
            m.insert(0, key.Key(key_str))
            m.insert(0, meter.TimeSignature('7/8'))
            m.insert(0, tempo.MetronomeMark(
                text='Allegro feroce', number=TEMPO_MARK))
        elif ts != prev_ts:
            # 拍子変更が小節の custom_measures に既に含まれていない場合に追加
            has_ts = any(isinstance(e, meter.TimeSignature)
                         for e in m.elements)
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
    md.title = 'Symphony No. XI "Grenze" — II. Kollision'
    md.composer = 'Music TWIN Collective (Soul-Twin Society, 2026)'
    score.insert(0, md)

    for name, abbrev, instr, clef_t, key_s, builder in PARTS_CONFIG:
        print(f'  Building part: {name}')
        custom = builder()
        part = build_part(name, abbrev, instr, clef_t, key_s, custom)
        score.insert(0, part)

    out_path = 'beethoven_xi_mov2.xml'
    score.write('musicxml', fp=out_path)
    print(f'\nMusicXML saved: {out_path}')
    print('Next: MuseScore4 -o movements/mov2.mscz beethoven_xi_mov2.xml')


if __name__ == '__main__':
    main()
