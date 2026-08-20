#!/usr/bin/env python3
"""
Symphony No. XI "Grenze"
I. Erwachen aus dem Schweigen  (Adagio sostenuto – Allegro furioso)

全25パート MusicXML 生成スクリプト（music21 使用）
MA楽曲構造分析書 + MC技法要求書 に基づく実装

実行: python gen_mov1.py
出力: beethoven_xi_mov1.xml  →  MuseScore4 で .mscz に変換
"""

from music21 import (
    stream, note, chord, metadata, key, meter, tempo,
    instrument, clef, dynamics, expressions, articulations, duration
)

# ============================================================
# グローバル設定
# ============================================================
TOTAL_MEASURES = 80     # 第Ⅰ楽章全体（冒頭80小節、残りはスタブ全休符）
ALLEGRO_START  = 8      # mm.8 から Allegro furioso ♩=152
KEY            = 'd'    # d-moll（1♭: Bb）
TIME_SIG       = '4/4'
TEMPO_ADAGIO   = 52
TEMPO_ALLEGRO  = 152


# ============================================================
# ユーティリティ
# ============================================================

def rest4():
    """4/4 拍子の全休符（4拍）"""
    return note.Rest(quarterLength=4)


def text_exp(txt, placement='above'):
    te = expressions.TextExpression(txt)
    te.placement = placement
    return te


def dyn(marking):
    """dynamics.Dynamic を返す"""
    return dynamics.Dynamic(marking)


def n(pitch, ql, dyn_str=None, artic=None):
    """
    音符を返す。
    pitch:   str ('D4', 'C#4', 'B-3' for Bb3)
    ql:      quarterLength
    dyn_str: 'pppp' など
    """
    nn = note.Note(pitch, quarterLength=ql)
    if dyn_str:
        nn.dynamic = dynamics.Dynamic(dyn_str)
    if artic:
        nn.articulations.append(artic)
    return nn


def measure_from_elements(mm_num, elements, extras=None):
    """
    elements: Note/Rest/Chord のリスト（合計拍数 = 4）
    extras:   (offset, elem) のリスト — 拍外に挿入する tempo/text 等
    """
    m = stream.Measure(number=mm_num)
    if extras:
        for offset, elem in extras:
            m.insert(offset, elem)
    for e in elements:
        m.append(e)
    return m


# ============================================================
# 各パートの小節データ定義
# ============================================================

# -------- Violin I --------
def build_violin_i():
    """
    MA文書 6.1 より:
    mm.1: D5 全音符 pppp, sul ponticello quasi niente
    mm.2: D4(q) C#4(q) C4(h) — 基底動機 上声
    mm.3: B3(q) Bb3(q) A3(h) — 基底動機 続き
    mm.4: D4(q) F4(q) A4(h) — d-moll主和音 初登場
    mm.5: 基底動機 反復（B-Bb-A-Ab: 下降継続）
    mm.6: 同（G-F#-F-E）
    mm.7: 全休符 "come No. X"
    mm.8: Allegro furioso ♩=152, 16分音符下降 + ffff
    mm.9-80: Allegro furioso 展開（スタブ）
    """
    custom = {}

    # mm.1: D5 全音符 pppp
    m1_extras = [(0, text_exp('sul ponticello, quasi niente'))]
    m1_notes  = [n('D5', 4.0, 'pppp')]
    custom[1] = measure_from_elements(1, m1_notes, m1_extras)

    # mm.2: D4(q) C#4(q) C4(h)
    custom[2] = measure_from_elements(2, [
        n('D4', 1.0, 'ppp'),
        n('C#4', 1.0),
        n('C4', 2.0, 'pp'),
    ])

    # mm.3: B3(q) Bb3(q) A3(h)
    custom[3] = measure_from_elements(3, [
        n('B3', 1.0, 'p'),
        n('B-3', 1.0),   # Bb3
        n('A3', 2.0),
    ])

    # mm.4: D4(q) F4(q) A4(h) — d-moll主和音
    custom[4] = measure_from_elements(4, [
        n('D4', 1.0, 'mf'),
        n('F4', 1.0),
        n('A4', 2.0),
    ])

    # mm.5: 下降継続 (G#3/Ab3 - G3 - F#3 - F3)
    custom[5] = measure_from_elements(5, [
        n('A-3', 1.0),   # Ab3
        n('G3', 1.0),
        n('F#3', 2.0),
    ])

    # mm.6: さらに下降 (F3 - E3 - Eb3 - D3)
    custom[6] = measure_from_elements(6, [
        n('F3', 1.0),
        n('E3', 1.0),
        n('E-3', 2.0),  # Eb3
    ])

    # mm.7: 全休符 "come No. X" オマージュ
    m7 = stream.Measure(number=7)
    m7.insert(0, text_exp('"come No. X"'))
    m7.append(note.Rest(quarterLength=4))
    custom[7] = m7

    # mm.8: Allegro furioso ♩=152
    # D4 C#4 C4 B3 Bb3 A3 Ab3 G3 (各16分音符×8=2拍) + D3 (2拍)
    m8 = stream.Measure(number=8)
    m8.insert(0, tempo.MetronomeMark(text='Allegro furioso', number=152))
    m8.insert(0, text_exp('fff, col legno + arco'))
    pitches_16th = ['D4', 'C#4', 'C4', 'B3', 'B-3', 'A3', 'A-3', 'G3']
    for p in pitches_16th:
        m8.append(n(p, 0.25, 'ff'))
    m8.append(n('D3', 2.0, 'fff'))
    custom[8] = m8

    # mm.9-24: Allegro furioso 第1主題反復（スタブ）
    for mm in range(9, 25):
        custom[mm] = measure_from_elements(mm, [
            n('D4', 0.25), n('C#4', 0.25), n('C4', 0.25), n('B3', 0.25),
            n('B-3', 0.25), n('A3', 0.25), n('A-3', 0.25), n('G3', 0.25),
            n('F#3', 0.25), n('F3', 0.25), n('E3', 0.25), n('E-3', 0.25),
            n('D3', 0.25), n('C#3', 0.25), n('C3', 0.25), n('B2', 0.25),
        ])

    return custom


# -------- Violin II --------
def build_violin_ii():
    custom = {}
    # mm.1-7: 全休符
    # mm.8: Allegro furioso 合流
    m8 = stream.Measure(number=8)
    m8.insert(0, tempo.MetronomeMark(text='Allegro furioso', number=152))
    pitches = ['A4', 'G4', 'F#4', 'F4', 'E4', 'E-4', 'D4', 'C#4']
    for p in pitches:
        m8.append(n(p, 0.25, 'f'))
    m8.append(n('A3', 2.0, 'ff'))
    custom[8] = m8
    # mm.9-24: 反復
    for mm in range(9, 25):
        custom[mm] = measure_from_elements(mm, [
            n('A4', 0.25), n('G4', 0.25), n('F#4', 0.25), n('F4', 0.25),
            n('E4', 0.25), n('E-4', 0.25), n('D4', 0.25), n('C#4', 0.25),
            n('C4', 0.25), n('B3', 0.25), n('B-3', 0.25), n('A3', 0.25),
            n('A-3', 0.25), n('G3', 0.25), n('F#3', 0.25), n('F3', 0.25),
        ])
    return custom


# -------- Viola --------
def build_viola():
    custom = {}
    # mm.8: 合流
    m8 = stream.Measure(number=8)
    m8.insert(0, tempo.MetronomeMark(text='Allegro furioso', number=152))
    m8.insert(0, text_exp('Bartók pizz.'))
    pitches = ['F4', 'E4', 'E-4', 'D4', 'C#4', 'C4', 'B3', 'B-3']
    for p in pitches:
        m8.append(n(p, 0.25, 'mf'))
    m8.append(n('F3', 2.0, 'f'))
    custom[8] = m8
    for mm in range(9, 25):
        custom[mm] = measure_from_elements(mm, [
            n('F4', 0.25), n('E4', 0.25), n('E-4', 0.25), n('D4', 0.25),
            n('C#4', 0.25), n('C4', 0.25), n('B3', 0.25), n('B-3', 0.25),
            n('A3', 0.25), n('A-3', 0.25), n('G3', 0.25), n('F#3', 0.25),
            n('F3', 0.25), n('E3', 0.25), n('E-3', 0.25), n('D3', 0.25),
        ])
    return custom


# -------- Violoncello --------
def build_cello():
    custom = {}
    # mm.1: D2 全音符 pppp, col legno tratto
    m1 = stream.Measure(number=1)
    m1.insert(0, text_exp('col legno tratto'))
    m1.append(n('D2', 4.0, 'pppp'))
    custom[1] = m1
    # mm.8: 合流
    m8 = stream.Measure(number=8)
    m8.insert(0, tempo.MetronomeMark(text='Allegro furioso', number=152))
    m8.append(n('D2', 1.0, 'fff'))
    m8.append(note.Rest(quarterLength=3))
    custom[8] = m8
    # mm.9-16: Vc solo 旋律（MC文書から）
    vc_solo = [
        # mm.9: D3 F3 A3
        [n('D3', 1.0, 'mp'), n('F3', 1.0), n('A3', 2.0)],
        # mm.10: D4(h.) C#4(q)
        [n('D4', 3.0), n('C#4', 1.0)],
        # mm.11: B3(h.)
        [n('B3', 4.0)],
        # mm.12: B3 A3 G3
        [n('B3', 1.0), n('A3', 1.0), n('G3', 2.0)],
        # mm.13: F3(h) E3(q) rest
        [n('F3', 2.0), n('E3', 1.0), note.Rest(quarterLength=1)],
        # mm.14: D3(h.)
        [n('D3', 4.0)],
        # mm.15: D3(q) rest rest
        [n('D3', 1.0), note.Rest(quarterLength=3)],
        # mm.16: rest
        [note.Rest(quarterLength=4)],
    ]
    for i, elems in enumerate(vc_solo):
        custom[9 + i] = measure_from_elements(9 + i, elems)
    return custom


# -------- Contrabass --------
def build_contrabass():
    custom = {}
    # mm.1-8: D1（または D2）ペダルポイント pppp
    for mm in range(1, 9):
        m = stream.Measure(number=mm)
        if mm == 1:
            m.insert(0, text_exp('ppp pedal point — sempre'))
        m.append(n('D2', 4.0, 'ppp' if mm == 1 else None))
        custom[mm] = m
    # mm.9-80: Allegro furioso ペダルD
    for mm in range(9, 25):
        custom[mm] = measure_from_elements(mm, [n('D2', 4.0)])
    return custom


# -------- Flute --------
def build_flute():
    custom = {}
    # mm.1-16: 全休符
    # mm.17-24: multiphonics（和音で近似）
    # MC文書 LilyPond サンプルより:
    # mm.17: C5+E5+G5 (付点2分音符) pp
    # mm.18: C5+E5+G5(q) → D5+F5+A5(h)
    # mm.19: A5(h.) mp
    for mm in range(17, 25):
        m = stream.Measure(number=mm)
        if mm == 17:
            m.insert(0, text_exp('multiphonics: C+E+G simultaneous'))
            # 和音（multiphonics 近似）
            ch = chord.Chord(['C5', 'E5', 'G5'], quarterLength=3)
            ch.dynamic = dynamics.Dynamic('pp')
            m.append(ch)
            m.append(note.Rest(quarterLength=1))
        elif mm == 18:
            ch = chord.Chord(['C5', 'E5', 'G5'], quarterLength=1)
            m.append(ch)
            ch2 = chord.Chord(['D5', 'F5', 'A5'], quarterLength=3)
            m.append(ch2)
        elif mm == 19:
            m.append(n('A5', 3.0, 'mp'))
            m.append(note.Rest(quarterLength=1))
        elif mm == 20:
            m.append(n('G5', 2.0))
            m.append(n('F5', 2.0))
        elif mm == 21:
            m.append(n('E5', 4.0))
        elif mm == 22:
            m.append(n('D5', 2.0))
            m.append(n('C#5', 2.0))
        else:
            m.append(n('C5', 1.0, 'p'))
            m.append(n('D5', 1.0))
            m.append(n('E5', 2.0))
        custom[mm] = m
    return custom


# -------- Oboe --------
def build_oboe():
    custom = {}
    # mm.1-24: 全休符（Adagio部）
    # mm.25: 長音クレッシェンド開始（MC文書: pp→f の12小節）
    m25 = stream.Measure(number=25)
    m25.insert(0, text_exp('pp→f, 12mm. cresc.'))
    m25.append(n('F4', 4.0, 'pp'))
    custom[25] = m25
    for mm in range(26, 37):
        custom[mm] = measure_from_elements(mm, [n('F4', 4.0)])
    m37 = stream.Measure(number=37)
    m37.append(n('F4', 4.0, 'f'))
    custom[37] = m37
    return custom


# -------- Clarinet in Bb --------
def build_clarinet():
    custom = {}
    # chalumeau (低音域) solo pppp（MA/MC文書）
    # mm.9から登場
    m9 = stream.Measure(number=9)
    m9.insert(0, text_exp('chalumeau (low register), pppp'))
    m9.append(n('E3', 4.0, 'pppp'))  # Cl in Bb → concert pitch -2半音
    custom[9] = m9
    for mm in range(10, 17):
        custom[mm] = measure_from_elements(mm, [n('E3', 4.0)])
    return custom


# -------- Fagotto --------
def build_fagotto():
    custom = {}
    # mm.9-: 最低音域、Cb倍加
    m9 = stream.Measure(number=9)
    m9.insert(0, text_exp('contrafagotto range'))
    m9.append(n('D2', 4.0, 'pp'))
    custom[9] = m9
    for mm in range(10, 17):
        custom[mm] = measure_from_elements(mm, [n('D2', 4.0)])
    return custom


# -------- Horn 1-4 --------
def build_horn(num):
    """
    第2主題: F4-A4-C5-E5 (Gestopft, mm.25-32)
    Hr.1 が主旋律, Hr.2-4 が和声充填
    """
    custom = {}
    # mm.25-32: 第2主題
    hr_pitches = {
        1: ['F4', 'A4', 'C5', 'E5', 'F5', 'E5', 'D5', 'C5'],
        2: ['A3', 'C4', 'E4', 'G4', 'A4', 'G4', 'F4', 'E4'],
        3: ['C3', 'E3', 'G3', 'C4', 'C4', 'C4', 'B-3', 'A3'],
        4: ['F2', 'F2', 'F2', 'C3', 'F3', 'C3', 'F2', 'F2'],
    }
    pitches = hr_pitches[num]
    for i, pitch in enumerate(pitches):
        mm = 25 + i
        m = stream.Measure(number=mm)
        if i == 0:
            ql_list = [1.5, 0.5, 1.0]  # 付点四分 + 八分 + 四分 の繰り返し
            m.insert(0, text_exp('con sordino (Gestopft)'))
        else:
            ql_list = [1.5, 0.5, 1.0]
        # シンプルに: 付点四分 + 八分 + 四分
        dyn_str = 'mf' if i == 0 else None
        m.append(n(pitch, 1.5, dyn_str))
        m.append(n(pitch, 0.5))
        m.append(n(pitch, 2.0))
        custom[mm] = m
    return custom


# -------- Trumpet 1-3 --------
def build_trumpet(num):
    """mm.1-72 全休符。mm.72 で突然 fff 登場（MC文書）"""
    custom = {}
    if num == 1 and TOTAL_MEASURES >= 72:
        m72 = stream.Measure(number=72)
        m72.insert(0, text_exp('突然 fff (subito fff)'))
        m72.append(n('D5', 1.0, 'fff'))
        m72.append(n('C#5', 1.0))
        m72.append(n('C5', 2.0))
        custom[72] = m72
    return custom


# -------- Trombone 1-3 --------
def build_trombone(num):
    """第Ⅰ楽章: 完全沈黙（MC文書）"""
    return {}


# -------- Tuba --------
def build_tuba():
    """第Ⅰ楽章: 完全沈黙"""
    return {}


# -------- Timpani --------
def build_timpani():
    """
    MC文書: mm.1-3 全休符 → mm.4: D pppp → tremolo
    """
    custom = {}
    # mm.1-3: 全休符
    # mm.4: D2 単打 pppp
    m4 = stream.Measure(number=4)
    m4.insert(0, text_exp('D — tuned, pppp single stroke'))
    m4.append(n('D2', 1.0, 'pppp'))
    m4.append(note.Rest(quarterLength=3))
    custom[4] = m4
    # mm.5-8: 徐々に増加
    for mm, dyn_str in [(5, 'ppp'), (6, 'pp'), (7, 'p')]:
        custom[mm] = measure_from_elements(mm, [n('D2', 1.0, dyn_str), note.Rest(quarterLength=3)])
    # mm.8-16: tremolo（8分音符繰り返しで近似）
    for mm in range(8, 17):
        m = stream.Measure(number=mm)
        if mm == 8:
            m.insert(0, text_exp('tremolo — sempre'))
        for _ in range(8):
            m.append(n('D2', 0.5))
        custom[mm] = m
    return custom


# -------- Soprano --------
def build_soprano():
    """第Ⅰ楽章末部: Sprechstimme solo（MC文書）"""
    custom = {}
    if TOTAL_MEASURES >= 70:
        m70 = stream.Measure(number=70)
        m70.insert(0, text_exp('Sprechstimme — senza testo'))
        # Sprechstimme: × 音符頭（music21 では NoteHead style で近似）
        sp = note.Note('A4', quarterLength=4)
        sp.notehead = 'x'
        sp.dynamic = dynamics.Dynamic('ppp')
        m70.append(sp)
        custom[70] = m70
        for mm in range(71, 76):
            m = stream.Measure(number=mm)
            sp2 = note.Note('G4', quarterLength=4)
            sp2.notehead = 'x'
            m.append(sp2)
            custom[mm] = m
    return custom


# -------- Alto / Tenor / Bass --------
def build_empty():
    """第Ⅰ楽章では不在"""
    return {}


# ============================================================
# パート生成メイン
# ============================================================

PARTS_CONFIG = [
    # (name, abbrev, instrument, clef_type, key, custom_builder)
    ('Flute',           'Fl.',    instrument.Flute(),            'treble',   'd', build_flute),
    ('Oboe',            'Ob.',    instrument.Oboe(),             'treble',   'd', build_oboe),
    ('Clarinet in Bb',  'Cl.',    instrument.Clarinet(),         'treble',   'd', build_clarinet),
    ('Fagotto',         'Fg.',    instrument.Bassoon(),          'bass',     'd', build_fagotto),
    ('Horn in F 1',     'Hr.1',   instrument.Horn(),             'treble',   'd', lambda: build_horn(1)),
    ('Horn in F 2',     'Hr.2',   instrument.Horn(),             'treble',   'd', lambda: build_horn(2)),
    ('Horn in F 3',     'Hr.3',   instrument.Horn(),             'treble',   'd', lambda: build_horn(3)),
    ('Horn in F 4',     'Hr.4',   instrument.Horn(),             'bass',     'd', lambda: build_horn(4)),
    ('Trumpet in C 1',  'Tp.1',   instrument.Trumpet(),          'treble',   'd', lambda: build_trumpet(1)),
    ('Trumpet in C 2',  'Tp.2',   instrument.Trumpet(),          'treble',   'd', lambda: build_trumpet(2)),
    ('Trumpet in C 3',  'Tp.3',   instrument.Trumpet(),          'treble',   'd', lambda: build_trumpet(3)),
    ('Trombone 1',      'Tb.1',   instrument.Trombone(),         'bass',     'd', lambda: build_trombone(1)),
    ('Trombone 2',      'Tb.2',   instrument.Trombone(),         'bass',     'd', lambda: build_trombone(2)),
    ('Trombone 3',      'Tb.3',   instrument.Trombone(),    'bass',     'd', lambda: build_trombone(3)),
    ('Tuba',            'Tuba',   instrument.Tuba(),             'bass',     'd', build_tuba),
    ('Timpani',         'Timp.',  instrument.Timpani(),          'bass',     'd', build_timpani),
    ('Soprano',         'S.',     instrument.Soprano(),          'treble',   'd', build_soprano),
    ('Alto',            'A.',     instrument.Alto(),             'treble',   'd', build_empty),
    ('Tenor',           'T.',     instrument.Tenor(),            'treble',   'd', build_empty),
    ('Bass',            'B.',     instrument.Bass(),        'bass',     'd', build_empty),
    ('Violin I',        'Vn.I',   instrument.Violin(),           'treble',   'd', build_violin_i),
    ('Violin II',       'Vn.II',  instrument.Violin(),           'treble',   'd', build_violin_ii),
    ('Viola',           'Va.',    instrument.Viola(),            'alto',     'd', build_viola),
    ('Violoncello',     'Vc.',    instrument.Violoncello(),      'bass',     'd', build_cello),
    ('Contrabass',      'Cb.',    instrument.Contrabass(),       'bass',     'd', build_contrabass),
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

    for mm in range(1, TOTAL_MEASURES + 1):
        if mm in custom_measures_dict:
            m = custom_measures_dict[mm]
        else:
            m = stream.Measure(number=mm)
            m.append(note.Rest(quarterLength=4))

        m.number = mm

        # mm.1 共通ヘッダー
        if mm == 1:
            m.insert(0, CLEF_MAP[clef_type]())
            m.insert(0, key.Key(key_str))
            m.insert(0, meter.TimeSignature(TIME_SIG))
            m.insert(0, tempo.MetronomeMark(
                text='Adagio sostenuto', number=TEMPO_ADAGIO))

        part.append(m)

    return part


# ============================================================
# メイン
# ============================================================

def main():
    score = stream.Score()

    md = metadata.Metadata()
    md.title = 'Symphony No. XI "Grenze"'
    md.composer = 'Music TWIN Collective (Soul-Twin Society, 2026)'
    score.insert(0, md)

    for name, abbrev, instr, clef_t, key_s, builder in PARTS_CONFIG:
        print(f'  Building part: {name}')
        custom = builder()
        part = build_part(name, abbrev, instr, clef_t, key_s, custom)
        score.insert(0, part)

    out_path = 'beethoven_xi_mov1.xml'
    score.write('musicxml', fp=out_path)
    print(f'\nMusicXML saved: {out_path}')
    print('Next: Open with MuseScore 4 → Save as .mscz')


if __name__ == '__main__':
    main()
