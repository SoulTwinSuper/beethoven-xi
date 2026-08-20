\version "2.24.0"

\header {
  title = "Symphony No. XI \"Grenze\""
  subtitle = "IV. Stille nach dem Sturm"
  subsubtitle = "嵐の後の静寂"
  composer = "Music TWIN Collective (Soul-Twin Society, 2026)"
  opus = "Op. posth. XI"
}

% ============================================================
% 楽章概要
% 拍子: 6/8
% 調性: F-dur
% テンポ: ♩.=54 (Andante tranquillo)
% 核心: 受容と変容
% 特徴: Hrコラール、Vc-Fg デュオ（バロック的）、Va-A ユニゾン
% ============================================================

globalIV = {
  \time 6/8
  \tempo "Andante tranquillo" 4. = 54
  \key f \major
}

% ============================================================
% ホルン×4本：コラール（mm.180-210）
% ベートーヴェン第9番第4楽章Hrコラールへのオマージュ
% ============================================================
hornI = \relative c'' {
  \globalIV
  \clef treble
  % 弱音器装着 ppp
  f4.\pp( e4 d8) |
  d2.~ |
  d4.( c4 b8) |
  a2. |
}

hornII = \relative c' {
  \globalIV
  \clef treble
  \transposition f
  % F-dur 正三和音 → C-dur → F-dur
  a4.\pp( g4 f8) |
  f2.~ |
  f4.( e4 d8) |
  c2. |
}

hornIII = \relative c' {
  \globalIV
  \clef treble
  \transposition f
  d4.\pp( c4 b8) |
  a2.~ |
  a4.( g4 f8) |
  e2. |
}

hornIV = \relative c {
  \globalIV
  \clef bass
  \transposition f
  f4.\pp( c4 e8) |
  f2.~ |
  f4.( c4 a8) |
  f2. |
}

% ============================================================
% チェロ+ファゴット：バロック様式バスデュオ（Vc-Fg）
% ============================================================
celloIV = \relative c, {
  \globalIV
  \clef bass
  \key f \major
  % バロック的二重奏（「限界を超えた古典への回帰」）
  f4.\mp( g4 a8) |
  a2.( |
  bes4. a4 g8) |
  f2. |
  c4.\mf( d4 e8) |
  f4.( g4 a8) |
  bes2.~ |
  bes4.( a4 g8) |
}

fagottoIV = \relative c {
  \globalIV
  \clef bass
  \key f \major
  % チェロと逆行する音型（対位法的）
  f4.\mp( e4 d8) |
  c2.( |
  bes,4. c4 d8) |
  f2. |
  a4.\mf( g4 f8) |
  e4.( f4 g8) |
  a2.~ |
  a4.( bes4 a8) |
}

% ============================================================
% ヴィオラ：Non vibrato 指定（透明な内声コラール）
% ============================================================
violaIV = \relative c' {
  \globalIV
  \clef alto
  \key f \major
  % non vibrato 指定
  c4.\p^\markup { \italic "non vib." }( d4 e8) |
  f2.~ |
  f4.( e4 d8) |
  c2. |
}

% ============================================================
% ソプラノ：子守唄的旋律（6/8、legato全音符連続）
% ============================================================
sopranoIV = \relative c'' {
  \globalIV
  \clef treble
  \key f \major
  % 子守唄的旋律
  f4.\p( g4 a8) |
  c2.~ |
  c4.( bes4 a8) |
  f2. |
  a4.( g4 f8) |
  e2.~ |
  e4.( f4 e8) |
  f2. |
}

% ============================================================
% スコア組み立て（第Ⅳ楽章 核心セクション）
% ============================================================
\score {
  <<
    \new StaffGroup \with {
      systemStartDelimiter = #'SystemStartBracket
    } <<
      \new Staff {
        \set Staff.instrumentName = "Hr. 1"
        \hornI
      }
      \new Staff {
        \set Staff.instrumentName = "Hr. 2"
        \hornII
      }
      \new Staff {
        \set Staff.instrumentName = "Hr. 3"
        \hornIII
      }
      \new Staff {
        \set Staff.instrumentName = "Hr. 4"
        \hornIV
      }
    >>
    \new StaffGroup \with {
      systemStartDelimiter = #'SystemStartBracket
    } <<
      \new Staff {
        \set Staff.instrumentName = "Vc."
        \celloIV
      }
      \new Staff {
        \set Staff.instrumentName = "Fg."
        \fagottoIV
      }
    >>
    \new StaffGroup \with {
      systemStartDelimiter = #'SystemStartBracket
    } <<
      \new Staff {
        \set Staff.instrumentName = "Va."
        \violaIV
      }
      \new Staff {
        \set Staff.instrumentName = "S."
        \sopranoIV
      }
    >>
  >>
  \layout {}
  \midi { \tempo 4. = 54 }
}

% ============================================================
% 楽章設計仕様（コメント）
%
% 第Ⅳ楽章の核心: 「受容と変容」
%
% 主要技法:
%   Hr×4: コラール（弱音器 ppp）、F-dur正三和音 → C-dur → F-dur
%          ベートーヴェン第9第4楽章Hrコラールへのオマージュ
%   Vc + Fg: バスドゥオ（バロック様式）、限界を超えた「古典への回帰」
%   Va: non vibrato 指定、透明な内声コラール
%   S: 子守唄的旋律（6/8、legato）
%   A + Va: 音色融合ユニゾン（弦と肉声）
%   Ob + Cl: 6度並行（牧歌的ハーモニー）
%
% 楽章境界:
%   Ⅲ→Ⅳ: 無調混沌後、長い fermata（指揮者裁量）→ Hr コラール ppp
%   Ⅳ→Ⅴ: ppp 消滅 → attacca（間を置かず）→ Timp ffff 宣言打
% ============================================================
