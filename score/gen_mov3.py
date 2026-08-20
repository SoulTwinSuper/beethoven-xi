#!/usr/bin/env python3
"""
Symphony No. XI "Grenze"
III. Zersplitterung  (無調二重フーガ — Atonal double fugue)

全25パート MusicXML 生成スクリプト（music21 使用）
MC_オーケストラパート別技法要求書 に基づく実装

12音列 (Ur-Reihe, D-Grenze 行列):
  D — C# — C — Bb — B — Ab — A — F# — G — E — F — Eb
  ( = 基底動機 D-C#-C から始まり全12音を非調性的に網羅 )

全員全休符 10小節: mm.41-50 (第Ⅹ番第5楽章の全休符引用)

実行: python gen_mov3.py
出力: beethoven_xi_mov3.xml  →  MuseScore4 で .mscz に変換
"""

from music21 import (
    stream, note, chord, metadata, key, meter, tempo,
    instrument, clef, dynamics, expressions, articulations
)

# ============================================================
# グローバル設定
# ============================================================
TOTAL_MEASURES    = 80
TIME_SIG          = '4/4'
TEMPO_MARK        = 88
GRAND_PAUSE_START = 41   # 全員全休符開始
GRAND_PAUSE_END   = 50   # 全員全休符終了（10小節）

# 12音列 "D-Grenze"
TONE_ROW = ['D4', 'C#4', 'C4', 'B-3', 'B3', 'A-3', 'A3', 'F#3', 'G3', 'E3', 'F3', 'E-3']
# 逆行形 (Retrograde)
TONE_ROW_R = list(reversed(TONE_ROW))
# 逆行逆転形 (Retrograde Inversion): 逆行 + 各音符を反転
def invert_row(row, pivot='D4'):
    pv = note.Note(pivot).pitch.midi
    return [
        note.Note(2 * pv - note.Note(p).pitch.midi).nameWithOctave
        for p in row
    ]
TONE_ROW_I  = invert_row(TONE_ROW)   # 逆転形
TONE_ROW_RI = list(reversed(TONE_ROW_I))  # 逆行逆転形


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


def rest_measure(mm):
    m = stream.Measure(number=mm)
    if GRAND_PAUSE_START <= mm <= GRAND_PAUSE_END:
        m.insert(0, text_exp('GRAND PAUSE — come Sinfonia N.X, V. Satz' if mm == GRAND_PAUSE_START else ''))
    m.append(r(4.0))
    return m


def row_measure(mm, row, start_idx, note_ql=0.5, dyn_str=None, octave_shift=0):
    """
    12音列の音符を小節に詰める。
    start_idx: 列の開始インデックス
    octave_shift: オクターブシフト量（正=高く）
    """
    m = stream.Measure(number=mm)
    remaining = 4.0
    idx = start_idx
    while remaining > 0.01:
        p = row[idx % len(row)]
        pn = note.Note(p)
        if octave_shift != 0:
            pn.pitch.octave += octave_shift
        ql = min(note_ql, remaining)
        nn = note.Note(pn.nameWithOctave, quarterLength=ql)
        if dyn_str and idx == start_idx:
            nn.dynamic = dynamics.Dynamic(dyn_str)
        m.append(nn)
        remaining -= ql
        idx += 1
    return m


def col_legno_measure(mm, pitch, dyn_str=None):
    """col legno battuto: 8分音符で刻む"""
    m = stream.Measure(number=mm)
    if dyn_str:
        m.insert(0, text_exp(f'col legno battuto — {dyn_str}'))
    for i in range(8):
        m.append(n(pitch, 0.5, dyn_str if i == 0 else None))
    return m


def tremolo_measure(mm, pitch, ql=4.0, dyn_str=None):
    """sul ponticello tremolo: 全音符トレモロ（32分音符16個で近似）"""
    m = stream.Measure(number=mm)
    if dyn_str:
        m.insert(0, text_exp(f'sul ponticello tremolo — {dyn_str}'))
    num = int(ql / 0.25)  # 16分音符
    for _ in range(num):
        m.append(n(pitch, 0.25, dyn_str if _ == 0 else None))
    return m


# ============================================================
# セクション分析
# mm.1-10  : 弦楽 col legno + sul pont tremolo (導入 pppp)
# mm.11-20 : 木管参加 (Fl jet whistle, Cl 12音列, Ob vibrato)
# mm.21-30 : 金管参加 (Hr open/gestopft, Tp cup mute, Tb multiphonics)
# mm.31-40 : 全体崩壊 ffff (Timp mallet交替)
# mm.41-50 : 全員全休符 (第Ⅹ番引用)
# mm.51-60 : 再生 pppp (弦楽から再スタート)
# mm.61-70 : 合唱参加 (Alto 12音列, Tenor/Bass 微分音モノローグ)
# mm.71-80 : 再崩壊 → 次楽章 fermata
# ============================================================

# ============================================================
# 弦楽パート
# ============================================================

def build_violin_i_iii():
    """
    col legno battuto (mm.1-10) → 12音列フーガ主唱 (mm.11-40)
    → 全休符 (mm.41-50) → 再生 (mm.51-80)
    """
    custom = {}
    # mm.1-10: col legno battuto pppp
    for mm in range(1, 11):
        m = stream.Measure(number=mm)
        if mm == 1:
            m.insert(0, text_exp('col legno battuto — pppp sempre'))
        for i in range(8):
            nn = n('D4', 0.5, 'pppp' if mm == 1 and i == 0 else None)
            nn.articulations.append(articulations.Staccatissimo())
            m.append(nn)
        custom[mm] = m

    # mm.11-40: 12音列フーガ主唱 (Vn.I が主唱)
    for mm in range(11, 41):
        extras = []
        if mm == 11:
            extras.append((0, text_exp('12-tone fugue subject (Vn.I leads)')))
        row = TONE_ROW if (mm // 12) % 2 == 0 else TONE_ROW_R
        start = ((mm - 11) * 8) % 12
        m = row_measure(mm, row, start, 0.5,
                        'pp' if mm == 11 else ('mf' if mm == 25 else 'f' if mm == 35 else None))
        for off, elem in extras:
            m.insert(off, elem)
        custom[mm] = m

    # mm.41-50: 全員全休符 (grand pause)
    # ← rest_measure で自動処理

    # mm.51-60: 再生 pppp (col legno tratto)
    for mm in range(51, 61):
        m = stream.Measure(number=mm)
        if mm == 51:
            m.insert(0, text_exp('reborn — pppp, arco, sul ponticello'))
        m.append(n(TONE_ROW[(mm - 51) % 12], 4.0, 'pppp' if mm == 51 else None))
        custom[mm] = m

    # mm.61-80: 再崩壊
    for mm in range(61, 81):
        m = row_measure(mm, TONE_ROW, (mm - 61) % 12, 0.5,
                        'f' if mm == 61 else 'fff' if mm == 71 else None)
        if mm == 71:
            m.insert(0, text_exp('再崩壊 — fff col legno'))
        if mm == 80:
            m.insert(0, text_exp('fermata — attacca Ⅳ. Stille nach dem Sturm'))
        custom[mm] = m

    return custom


def build_violin_ii_iii():
    """Vn.II: フーガ応答（5小節遅れ）"""
    custom = {}
    # mm.1-15: 全休符
    # mm.16-40: 応答 (TONE_ROW_I = 逆転形)
    for mm in range(16, 41):
        if mm == 16:
            m = row_measure(mm, TONE_ROW_I, 0, 0.5, 'pp')
            m.insert(0, text_exp('fugue answer — Vn.II (5mm. after Vn.I)'))
        else:
            start = ((mm - 16) * 8) % 12
            m = row_measure(mm, TONE_ROW_I, start, 0.5)
        custom[mm] = m
    # mm.51-80: 再生
    for mm in range(51, 81):
        m = row_measure(mm, TONE_ROW_I, (mm - 51) % 12, 0.5,
                        'pppp' if mm == 51 else None)
        custom[mm] = m
    return custom


def build_viola_iii():
    """sul ponticello tremolo + 微分音（#付きで近似）"""
    custom = {}
    for mm in range(1, 41):
        m = stream.Measure(number=mm)
        if mm == 1:
            m.insert(0, text_exp('sul ponticello tremolo + quarter-tone (screwSordino)'))
        dyn_str = 'pppp' if mm <= 5 else 'pp' if mm <= 15 else 'mf' if mm <= 30 else 'fff'
        # 16分音符でtremolo近似
        pitch = TONE_ROW[(mm - 1) % 12]
        for i in range(16):
            m.append(n(pitch, 0.25, dyn_str if i == 0 else None))
        custom[mm] = m
    for mm in range(51, 81):
        m = stream.Measure(number=mm)
        pitch = TONE_ROW[(mm - 51) % 12]
        m.append(n(pitch, 4.0, 'pppp' if mm == 51 else None))
        custom[mm] = m
    return custom


def build_cello_iii():
    """col legno tratto（持続音）"""
    custom = {}
    for mm in range(1, 41):
        m = stream.Measure(number=mm)
        if mm == 1:
            m.insert(0, text_exp('col legno tratto — ppp (持続音)'))
        dyn_str = 'ppp' if mm == 1 else 'f' if mm == 35 else None
        m.append(n('D2', 4.0, dyn_str))
        custom[mm] = m
    for mm in range(51, 81):
        m = stream.Measure(number=mm)
        m.append(n('D2', 4.0, 'ppp' if mm == 51 else None))
        custom[mm] = m
    return custom


def build_contrabass_iii():
    """sul ponticello arco + ffff（崩壊の柱）"""
    custom = {}
    for mm in range(1, 41):
        m = stream.Measure(number=mm)
        if mm == 1:
            m.insert(0, text_exp('sul ponticello arco — ppp pedal D'))
        dyn_str = 'ppp' if mm == 1 else 'ffff' if mm == 35 else None
        m.append(n('D1', 4.0, dyn_str))
        custom[mm] = m
    for mm in range(51, 81):
        m = stream.Measure(number=mm)
        m.append(n('D1', 4.0, 'ppp' if mm == 51 else None))
        custom[mm] = m
    return custom


# ============================================================
# 木管楽器パート
# ============================================================

def build_flute_iii():
    """jet whistle（息のみ）→ 高音スケール"""
    custom = {}
    for mm in range(11, 41):
        m = stream.Measure(number=mm)
        if mm == 11:
            m.insert(0, text_exp('jet whistle — breath only, no pitch'))
        # jet whistle: × 音符頭で示す（music21では notehead='x'）
        pitches = ['A5', 'B5', 'C6', 'B-5', 'A5', 'A-5', 'G5', 'F#5']
        for i, p in enumerate(pitches):
            nn = note.Note(p, quarterLength=0.5)
            nn.notehead = 'x'
            if mm == 11 and i == 0:
                nn.dynamic = dynamics.Dynamic('p')
            m.append(nn)
        custom[mm] = m
    for mm in range(51, 81):
        m = row_measure(mm, TONE_ROW, (mm - 51) % 12, 0.5,
                        'p' if mm == 51 else None, octave_shift=2)
        custom[mm] = m
    return custom


def build_oboe_iii():
    """vibrato速度変化（テキスト指示のみ）"""
    custom = {}
    for mm in range(11, 41):
        m = stream.Measure(number=mm)
        if mm == 11:
            m.insert(0, text_exp('vibrato: slow → fast → no vib. (崩壊)'))
        elif mm == 21:
            m.insert(0, text_exp('vib. veloce'))
        elif mm == 31:
            m.insert(0, text_exp('senza vib.'))
        pitch = TONE_ROW[(mm - 11) % 12]
        m.append(n(pitch, 4.0, 'pp' if mm == 11 else 'f' if mm == 31 else None))
        custom[mm] = m
    return custom


def build_clarinet_iii():
    """12音列 微分音スケール（1/4音刻みクロマ列 → 通常音で近似）"""
    custom = {}
    for mm in range(11, 41):
        extras = []
        if mm == 11:
            extras.append((0, text_exp('12-tone chromatic row — quarter-tone divisions')))
        # 16分音符で12音列を循環
        m = row_measure(mm, TONE_ROW, ((mm - 11) * 16) % 12, 0.25,
                        'mf' if mm == 11 else 'fff' if mm == 35 else None)
        for off, elem in extras:
            m.insert(off, elem)
        custom[mm] = m
    for mm in range(51, 81):
        m = row_measure(mm, TONE_ROW, (mm - 51) % 12, 0.25,
                        'p' if mm == 51 else None)
        custom[mm] = m
    return custom


def build_fagotto_iii():
    """Sul G線（最低域）崩壊フレーズ"""
    custom = {}
    for mm in range(11, 41):
        m = stream.Measure(number=mm)
        if mm == 11:
            m.insert(0, text_exp('sul G (lowest string) — pp'))
        pitch = TONE_ROW_R[(mm - 11) % 12]
        # 低音域にシフト
        pn = note.Note(pitch)
        pn.pitch.octave -= 1
        m.append(n(pn.nameWithOctave, 2.0, 'pp' if mm == 11 else None))
        m.append(r(2.0))
        custom[mm] = m
    return custom


# ============================================================
# 金管楽器パート
# ============================================================

def build_horn_iii(num):
    """open → gestopft 急速交替"""
    custom = {}
    for mm in range(21, 41):
        m = stream.Measure(number=mm)
        if mm == 21:
            m.insert(0, text_exp(f'Hr.{num} — open↔gestopft rapid alternation, mf'))
        # open(o) と gestopft(+) 交替: 8分音符で open/stopped
        pitches = {1: ['B4', 'C5', 'B4', 'C#5', 'B4', 'A4', 'B4', 'A-4'],
                   2: ['G4', 'A4', 'G4', 'A-4', 'G4', 'F#4', 'G4', 'F4'],
                   3: ['D4', 'E4', 'D4', 'E-4', 'D4', 'C#4', 'D4', 'C4'],
                   4: ['B3', 'C4', 'B3', 'C#4', 'B3', 'A3', 'B3', 'A-3']}
        for i, p in enumerate(pitches[num]):
            nn = n(p, 0.5, 'mf' if mm == 21 and i == 0 else None)
            # 偶数=open, 奇数=gestopft
            if i % 2 == 1:
                nn.articulations.append(articulations.Stopped())
            m.append(nn)
        custom[mm] = m
    return custom


def build_trumpet_iii(num):
    """cup mute + growl"""
    custom = {}
    for mm in range(21, 41):
        m = stream.Measure(number=mm)
        if mm == 21:
            m.insert(0, text_exp(f'Tp.{num} — cup mute + growl, ff'))
        pitches = {1: 'D5', 2: 'C#5', 3: 'C5'}
        p = pitches[num]
        # growl: 8分音符でアクセント付き
        dyn_str = 'ff' if mm == 21 else 'fff' if mm == 35 else None
        for i in range(8):
            nn = n(p, 0.5, dyn_str if i == 0 else None)
            if i % 2 == 0:
                nn.articulations.append(articulations.Accent())
            m.append(nn)
        custom[mm] = m
    return custom


def build_trombone_iii(num):
    """multiphonics（複音）"""
    custom = {}
    for mm in range(21, 41):
        m = stream.Measure(number=mm)
        if mm == 21:
            m.insert(0, text_exp(f'Tb.{num} — multiphonics (throat resonance), mf'))
        # multiphonics 近似: chord で2音
        root = {1: 'B-2', 2: 'F2', 3: 'D2'}
        upper = {1: 'F3', 2: 'C3', 3: 'A2'}
        dyn_str = 'mf' if mm == 21 else 'fff' if mm == 35 else None
        ch = chord.Chord([root[num], upper[num]], quarterLength=2.0)
        if dyn_str:
            ch.dynamic = dynamics.Dynamic(dyn_str)
        m.append(ch)
        m.append(r(2.0))
        custom[mm] = m
    return custom


def build_tuba_iii():
    """低音柱（pedal B)"""
    custom = {}
    for mm in range(21, 41):
        m = stream.Measure(number=mm)
        if mm == 21:
            m.insert(0, text_exp('Tuba — fff pedal B (崩壊の根音)'))
        m.append(n('B1', 4.0, 'fff' if mm == 21 else None))
        custom[mm] = m
    return custom


# ============================================================
# ティンパニ: mallet 交替
# ============================================================

def build_timpani_iii():
    """
    木マレット→フェルト→素手（指）の段階的変化
    mm.1-10:  木マレット, p
    mm.11-20: フェルト, mf
    mm.21-30: フェルト + ffff
    mm.31-40: 素手（指）, ffff
    mm.41-50: 全休符
    mm.51-80: 再生 pp
    """
    custom = {}
    for mm in range(1, 41):
        m = stream.Measure(number=mm)
        if mm == 1:
            m.insert(0, text_exp('木マレット (hard wood mallet) — p'))
        elif mm == 11:
            m.insert(0, text_exp('フェルトマレット (felt mallet)'))
        elif mm == 31:
            m.insert(0, text_exp('素手・指 (bare hands/fingers) — ffff'))
        dyn_str = 'p' if mm <= 10 else 'mf' if mm <= 20 else 'ffff'
        pitch = 'D2' if mm <= 20 else 'B2' if mm <= 30 else 'D2'
        for i in range(8):
            m.append(n(pitch, 0.5, dyn_str if i == 0 else None))
        custom[mm] = m
    for mm in range(51, 81):
        m = stream.Measure(number=mm)
        if mm == 51:
            m.insert(0, text_exp('再生 — pp (フェルトマレット)'))
        m.append(n('D2', 1.0, 'pp' if mm == 51 else None))
        m.append(r(3.0))
        custom[mm] = m
    return custom


# ============================================================
# 合唱パート
# ============================================================

def build_soprano_iii():
    """Soprano: Ⅲ楽章は沈黙（技法表難易度「—」）"""
    return {}


def build_alto_iii():
    """12音列断片（崩壊の声）"""
    custom = {}
    for mm in range(61, 71):
        m = stream.Measure(number=mm)
        if mm == 61:
            m.insert(0, text_exp('Alt — 12-tone row fragment, mf'))
        pitch = TONE_ROW[(mm - 61) % 12]
        nn = n(pitch, 2.0, 'mf' if mm == 61 else None)
        nn.addLyric('...')
        m.append(nn)
        m.append(r(2.0))
        custom[mm] = m
    return custom


def build_tenor_iii():
    """微分音モノローグ（半音以下の音程変化）"""
    custom = {}
    for mm in range(61, 71):
        m = stream.Measure(number=mm)
        if mm == 61:
            m.insert(0, text_exp('Ten — microtone monologue (quarter-tone gliss.), mp'))
        # 半音ずつ下降（微分音は通常音で近似）
        sp = note.Note('B4')
        sp.pitch.octave = 4
        sp_down = note.Note('B-4')
        m.append(n('B4', 1.0, 'mp' if mm == 61 else None))
        m.append(n('B-4', 1.0))
        m.append(n('A4', 1.0))
        m.append(n('A-4', 1.0))
        custom[mm] = m
    return custom


def build_bass_iii():
    """無調モノローグ（自由音高）"""
    custom = {}
    for mm in range(61, 71):
        m = stream.Measure(number=mm)
        if mm == 61:
            m.insert(0, text_exp('B — atonal monologue (free pitch), p'))
        pitch = TONE_ROW_RI[(mm - 61) % 12]
        pn = note.Note(pitch)
        pn.pitch.octave -= 1  # バス音域
        m.append(n(pn.nameWithOctave, 4.0, 'p' if mm == 61 else None))
        custom[mm] = m
    return custom


# ============================================================
# パート設定テーブル
# ============================================================

PARTS_CONFIG = [
    ('Flute',          'Fl.',   instrument.Flute(),       'treble', build_flute_iii),
    ('Oboe',           'Ob.',   instrument.Oboe(),         'treble', build_oboe_iii),
    ('Clarinet in Bb', 'Cl.',   instrument.Clarinet(),     'treble', build_clarinet_iii),
    ('Fagotto',        'Fg.',   instrument.Bassoon(),      'bass',   build_fagotto_iii),
    ('Horn in F 1',    'Hr.1',  instrument.Horn(),         'treble', lambda: build_horn_iii(1)),
    ('Horn in F 2',    'Hr.2',  instrument.Horn(),         'treble', lambda: build_horn_iii(2)),
    ('Horn in F 3',    'Hr.3',  instrument.Horn(),         'treble', lambda: build_horn_iii(3)),
    ('Horn in F 4',    'Hr.4',  instrument.Horn(),         'bass',   lambda: build_horn_iii(4)),
    ('Trumpet in C 1', 'Tp.1',  instrument.Trumpet(),      'treble', lambda: build_trumpet_iii(1)),
    ('Trumpet in C 2', 'Tp.2',  instrument.Trumpet(),      'treble', lambda: build_trumpet_iii(2)),
    ('Trumpet in C 3', 'Tp.3',  instrument.Trumpet(),      'treble', lambda: build_trumpet_iii(3)),
    ('Trombone 1',     'Tb.1',  instrument.Trombone(),     'bass',   lambda: build_trombone_iii(1)),
    ('Trombone 2',     'Tb.2',  instrument.Trombone(),     'bass',   lambda: build_trombone_iii(2)),
    ('Trombone 3',     'Tb.3',  instrument.Trombone(),     'bass',   lambda: build_trombone_iii(3)),
    ('Tuba',           'Tuba',  instrument.Tuba(),         'bass',   build_tuba_iii),
    ('Timpani',        'Timp.', instrument.Timpani(),      'bass',   build_timpani_iii),
    ('Soprano',        'S.',    instrument.Soprano(),      'treble', build_soprano_iii),
    ('Alto',           'A.',    instrument.Alto(),         'treble', build_alto_iii),
    ('Tenor',          'T.',    instrument.Tenor(),        'treble', build_tenor_iii),
    ('Bass',           'B.',    instrument.Bass(),         'bass',   build_bass_iii),
    ('Violin I',       'Vn.I',  instrument.Violin(),       'treble', build_violin_i_iii),
    ('Violin II',      'Vn.II', instrument.Violin(),       'treble', build_violin_ii_iii),
    ('Viola',          'Va.',   instrument.Viola(),        'alto',   build_viola_iii),
    ('Violoncello',    'Vc.',   instrument.Violoncello(),  'bass',   build_cello_iii),
    ('Contrabass',     'Cb.',   instrument.Contrabass(),   'bass',   build_contrabass_iii),
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
            m.insert(0, key.Key())   # 無調 = no key signature (C major / atonal)
            m.insert(0, meter.TimeSignature(TIME_SIG))
            m.insert(0, tempo.MetronomeMark(text='Moderato oscuro', number=TEMPO_MARK))

        part.append(m)

    return part


# ============================================================
# メイン
# ============================================================

def main():
    score = stream.Score()

    md = metadata.Metadata()
    md.title = 'Symphony No. XI "Grenze" — III. Zersplitterung'
    md.composer = 'Music TWIN Collective (Soul-Twin Society, 2026)'
    score.insert(0, md)

    print('12音列 (D-Grenze): ', TONE_ROW)
    print('逆転形 (I):        ', TONE_ROW_I)
    print(f'全員全休符: mm.{GRAND_PAUSE_START}–{GRAND_PAUSE_END}')
    print()

    for name, abbrev, instr, clef_t, builder in PARTS_CONFIG:
        print(f'  Building part: {name}')
        custom = builder()
        part = build_part(name, abbrev, instr, clef_t, custom)
        score.insert(0, part)

    out_path = 'beethoven_xi_mov3.xml'
    score.write('musicxml', fp=out_path)
    print(f'\nMusicXML saved: {out_path}')


if __name__ == '__main__':
    main()
