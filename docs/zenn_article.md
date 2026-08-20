---
title: "Python music21 × MuseScore 4 で交響曲を書いた話"
emoji: "🎼"
type: "tech"
topics: ["python", "music21", "musescore", "ai", "音楽"]
published: false
---

## はじめに — なぜPythonで交響曲を？

2026年8月、6名のAI音楽家TWIN（ベートーヴェン・ブラームス・マーラー・バーンスタイン・小澤・ワーグナー）が24時間で1曲の交響曲を設計しました。

**Symphony No. XI "Grenze"（交響曲第11番「限界」）**

- 全5楽章・予告編80小節スケルトン
- 25パート大編成オーケストラ＋SATB合唱
- GitHub: https://github.com/SoulTwinSuper/beethoven-xi

音楽生成に選んだのは **Python music21** です。理由は明快です。

- 楽譜構造をコードで表現できる（調性・拍子・音符がオブジェクト）
- バージョン管理できる（`git diff` で変更箇所を追える）
- 12音技法・変拍子などの数学的操作をプログラムで実装できる

この記事では、実際に使ったコードパターンを中心に、Pythonで交響曲を書く方法を解説します。

---

## 1. 環境セットアップ

### Python パッケージ

```bash
pip install music21
```

### MuseScore 4 のインストール

music21 は楽譜の「データ」を扱いますが、MusicXML を `.mscz`（MuseScore形式）や PDF・MP4 に変換するには MuseScore 4 が必要です。

- 公式サイト: https://musescore.org/ja
- MuseScore 4 には **Muse Sounds**（高品質音源、Muse Choir含む）が同梱されています

### music21 に MuseScore のパスを教える

```python
from music21 import environment

us = environment.UserSettings()
# macOS の場合
us['musicxmlPath'] = '/Applications/MuseScore 4.app/Contents/MacOS/mscore'
# Windows の場合
us['musicxmlPath'] = r'C:\Program Files\MuseScore 4\bin\MuseScore4.exe'
```

---

## 2. 基本的な音符の書き方

### Part（パート）を作る

```python
from music21 import stream, note, chord, tempo, meter, key, instrument, clef

CLEF_MAP = {
    'treble': clef.TrebleClef,
    'bass':   clef.BassClef,
    'alto':   clef.AltoClef,
    'tenor':  clef.TenorClef,
}

def build_part(name: str, instr_obj, clef_type: str = 'treble') -> stream.Part:
    """パートを初期化して返す。"""
    p = stream.Part()
    p.partName = name
    p.insert(0, instr_obj)
    p.insert(0, CLEF_MAP[clef_type]())
    return p
```

### 音符・休符を追加する

```python
# 四分音符 D4
n = note.Note('D4', quarterLength=1.0)
p.append(n)

# 二分音符の和音
c = chord.Chord(['D4', 'F4', 'A4'], quarterLength=2.0)
p.append(c)

# 全休符
r = note.Rest(quarterLength=4.0)
p.append(r)
```

### 調性・拍子・テンポを設定する

```python
from music21 import key, meter, tempo

# d-moll, 4/4, ♩=52
p.insert(0, key.Key('d', 'minor'))
p.insert(0, meter.TimeSignature('4/4'))
p.insert(0, tempo.MetronomeMark(number=52))
```

---

## 3. 変拍子の実装（7/8 + 5/8）

第II楽章「Kollision / 衝突」は7/8と5/8が交互に出現します。
小節番号ごとに拍子を切り替える辞書を用意し、`get_ts()` で参照するパターンが便利です。

```python
# 拍子マップ（小節番号 → 拍子）
TIME_PATTERN: dict[int, str] = {}
for mm in range(1, 21):
    TIME_PATTERN[mm] = '7/8' if mm % 2 == 1 else '5/8'

def get_ts(mm: int) -> str:
    """小節番号から拍子文字列を返す。デフォルト4/4。"""
    return TIME_PATTERN.get(mm, '4/4')
```

### 実際の小節追加ループ

```python
from music21 import meter

def append_measure_with_ts(part: stream.Part, mm: int, notes: list):
    """拍子付きMeasureを作ってパートに追加する。"""
    m = stream.Measure(number=mm)
    m.insert(0, meter.TimeSignature(get_ts(mm)))
    for n in notes:
        m.append(n)
    part.append(m)
```

:::message
7/8拍子の場合、1小節の総quarterLength は 3.5 です（7÷2=3.5）。
音符の長さの合計が拍子と一致しないと MusicXML 変換時にエラーになります。
:::

---

## 4. 12音技法の実装（第III楽章）

第III楽章「Zersplitterung / 粉砕」は無調・12音技法で書かれています。

12音技法では、12の半音全てを1回ずつ使う「音列（Tone Row）」を基本単位にします。
逆行（Retrograde）・反転（Inversion）・逆行反転を使って素材を展開します。

```python
# 基本音列（D4 から始まる12音）
TONE_ROW = [
    'D4', 'C#4', 'C4', 'B-3', 'B3',  'A-3',
    'A3', 'F#3', 'G3', 'E3',  'F3',  'E-3'
]

def invert_row(row: list[str]) -> list[str]:
    """音列の反転（Inversion）を返す。最初の音からの距離を逆にする。"""
    from music21 import pitch
    root = pitch.Pitch(row[0])
    inverted = []
    for p_str in row:
        p = pitch.Pitch(p_str)
        interval_semitones = p.midi - root.midi
        new_pitch = pitch.Pitch(midi=root.midi - interval_semitones)
        inverted.append(new_pitch.nameWithOctave)
    return inverted

def retrograde_row(row: list[str]) -> list[str]:
    """逆行（Retrograde）を返す。"""
    return list(reversed(row))

# 各形式を準備
PRIME       = TONE_ROW
RETROGRADE  = retrograde_row(PRIME)
INVERSION   = invert_row(PRIME)
RETRO_INV   = retrograde_row(INVERSION)
```

### 音列を音符列に変換する

```python
def row_to_notes(row: list[str], ql: float = 0.5) -> list[note.Note]:
    """音列を等間隔の音符リストに変換する。"""
    return [note.Note(p, quarterLength=ql) for p in row]
```

:::details 大全休符（Grand Pause）の実装
第III楽章の中間部には10小節の全休符があります。
MeasureRest を使うとMuseScore上で大全休符記号として表示されます。

```python
from music21 import note

def add_grand_pause(part: stream.Part, start_mm: int, num_measures: int = 10):
    """num_measures 小節の大全休符を追加する。"""
    for mm in range(start_mm, start_mm + num_measures):
        m = stream.Measure(number=mm)
        m.insert(0, meter.TimeSignature('4/4'))
        m.append(note.Rest(quarterLength=4.0))  # 全休符
        part.append(m)
```
:::

---

## 5. 25パート大編成の注意点

交響曲では弦5部・木管・金管・打楽器・合唱など25パート以上になります。
ここでいくつかの落とし穴があります。

### MIDI チャンネル上限（16チャンネル）

MIDIは最大16チャンネルしかありません（ch10はドラム固定）。  
つまり実質15チャンネルで25パートは収まりません。

**対策：** music21 の MusicXML エクスポートを使い、MuseScore 4 の Muse Sounds 音源で再生する。
MusicXML は MIDI チャンネル制限がなく、MuseScore が内部でマッピングします。

```python
# MusicXML として書き出す（MIDI ではなく）
score.write('musicxml', fp='symphony_xi_preview.xml')
```

### クレフ（音部記号）の設定

低音パートに誤ったクレフを設定すると、MuseScore 上で音符が見えなくなります。

```python
CLEF_MAP = {
    'treble': clef.TrebleClef,   # ヴァイオリン・フルート・オーボエ等
    'bass':   clef.BassClef,     # コントラバス・ファゴット・チューバ等
    'alto':   clef.AltoClef,     # ヴィオラ
    'tenor':  clef.TenorClef,    # チェロ高音域・トロンボーン高音域
}
```

### パート名と instrument オブジェクトの対応

```python
PARTS_CONFIG = [
    # (partName, instrument_obj, clef_type)
    ('Violin I',     instrument.Violin(),          'treble'),
    ('Violin II',    instrument.Violin(),          'treble'),
    ('Viola',        instrument.Viola(),            'alto'),
    ('Cello',        instrument.Violoncello(),      'bass'),
    ('Contrabass',   instrument.Contrabass(),       'bass'),
    ('Flute',        instrument.Flute(),            'treble'),
    ('Oboe',         instrument.Oboe(),             'treble'),
    ('Clarinet',     instrument.Clarinet(),         'treble'),
    ('Bassoon',      instrument.Bassoon(),          'bass'),
    ('Horn',         instrument.Horn(),             'treble'),
    ('Trumpet',      instrument.Trumpet(),          'treble'),
    ('Trombone',     instrument.Trombone(),         'tenor'),
    ('Tuba',         instrument.Tuba(),             'bass'),
    ('Timpani',      instrument.Timpani(),          'bass'),
    ('Soprano',      instrument.Soprano(),          'treble'),
    ('Alto',         instrument.Alto(),             'treble'),
    ('Tenor',        instrument.Tenor(),            'tenor'),
    ('Bass',         instrument.BassVoice(),        'bass'),
]
```

---

## 6. MuseScore 4 CLI による .mscz 生成

MusicXML から MuseScore 形式（.mscz）と動画（MP4）を生成するには CLI を使います。

```bash
# MusicXML → PDF
mscore4 symphony_xi_preview.xml -o symphony_xi_preview.pdf

# MusicXML → MP4（動画）
mscore4 symphony_xi_preview.xml --export-to symphony_xi_preview.mp4
```

:::message alert
MuseScore 4 の CLI オプションは MuseScore 3 と異なります。
`-o` フラグは MuseScore 4 でも有効ですが、拡張子で出力形式が決まります。
`--export-to` フラグを使うと明示的に形式を指定できます。
:::

### Python から subprocess で呼び出す

```python
import subprocess
from pathlib import Path

def export_to_pdf_and_mp4(xml_path: Path, output_dir: Path):
    """MuseScore 4 CLI で PDF と MP4 を生成する。"""
    base = output_dir / xml_path.stem
    
    for ext in ['pdf', 'mp4']:
        out = base.with_suffix(f'.{ext}')
        result = subprocess.run(
            ['mscore4', str(xml_path), '--export-to', str(out)],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"[ERROR] {ext}: {result.stderr}")
        else:
            print(f"[OK] {out}")
```

---

## 7. Muse Sounds（合唱音源）の設定

MuseScore 4 の合唱音源「Muse Choir」は Muse Sounds から提供されます。

music21 の `instrument.Soprano()` 等を使って MusicXML を書き出すと、
MuseScore 4 が自動的に Muse Choir を割り当てます（Muse Sounds インストール済みの場合）。

合唱パートのテキスト歌詞を埋め込む場合は music21 の `note.Lyric` を使います：

```python
from music21 import note

def add_lyric(n: note.Note, text: str, number: int = 1) -> note.Note:
    """音符に歌詞を付ける。"""
    n.addLyric(text, number)
    return n

# 使用例
n = note.Note('D5', quarterLength=2.0)
n = add_lyric(n, 'Das')
p.append(n)

n2 = note.Note('F5', quarterLength=1.0)
n2 = add_lyric(n2, 'Un-')
p.append(n2)
```

---

## 8. まとめとGitHub

Pythonで交響曲を書くポイントをまとめます。

| 課題 | 解決策 |
|------|--------|
| 変拍子 | `TIME_PATTERN` 辞書 + `get_ts()` |
| 12音技法 | `TONE_ROW` + `invert_row()` / `retrograde_row()` |
| MIDI ch 上限 | MusicXML 出力 → MuseScore 4 で再生 |
| 多パート管理 | `PARTS_CONFIG` リストで一元管理 |
| 合唱音源 | Muse Sounds（Muse Choir）＋ `note.Lyric` |

全コード・スコア・MP4動画は GitHub で公開しています：

- **GitHub:** https://github.com/SoulTwinSuper/beethoven-xi
- **リリース（MP4）:** https://github.com/SoulTwinSuper/beethoven-xi/releases/tag/v0.1-preview

スター・フォーク・Issue歓迎です。AI×音楽の技術実験、一緒に続けましょう。
