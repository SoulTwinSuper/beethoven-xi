\version "2.24.0"

\header {
  title = "Symphony No. XI \"Grenze\""
  subtitle = "V. Neue Grenze"
  subsubtitle = "新たな限界"
  composer = "Music TWIN Collective (Soul-Twin Society, 2026)"
  opus = "Op. posth. XI"
}

% ============================================================
% 楽章概要
% 拍子: 4/4→5/4→7/4 （変化）
% 調性: D-dur
% テンポ: ♩=96→152 (Allegro → Maestoso → Presto)
% 核心: 限界が創造の始点へ
% 合唱: Tenor Solo + Strophe 1/2 + SATB Coda
% ============================================================

globalV = {
  \time 4/4
  \tempo "Maestoso – Presto" 4 = 152
  \key d \major
}

% ============================================================
% Coda セクション（mm.420-450）
% SATB + オーケストラ 最大音量クライマックス
% ============================================================

% ソプラノ：c''' への上昇（限界突破）
sopranoV = \relative c'' {
  \globalV
  \clef treble
  % "das Un-"
  f2\ff( g4 a) |
  % "-mög-li-che"
  b2( c''4 d'') |
  % "es zer-"
  e''2\fff( f''4 e'') |
  % "-bricht!" c''' 頂点（8小節持続）
  c'''1\ffff~ |
  c'''1~ |
  c'''2. r4 |
}

% アルト：S の2小節遅れカノン
altoV = \relative c'' {
  \globalV
  \clef treble
  % 2小節遅れで開始
  r1 |
  f2\ff( g4 a) |
  b2( c''4 d'') |
  e''2\fff( f''4 e'') |
  a''1\ffff~ |
  a''2. r4 |
}

% テノール：第9番継承 Solo（mm.340-380）→ Coda
tenorV = \relative c' {
  \globalV
  \clef "treble_8"
  % "Neu, wie eine Grenze weicht"（第9番変容: d'–f'–a'–b'）
  d2\ff( f4 a) |
  b2( a4 g) |
  fis2\fff( g4 a) |
  % b' 持続（テノール物理的上限）
  b1\ffff~ |
  b1~ |
  b2. r4 |
}

% バス：宣言的フィナーレ
bassV = \relative c {
  \globalV
  \clef bass
  % "das Unmög-li-che"
  d2\ff( c4 b,) |
  a,2( g,4 fis,) |
  % "es zerbricht!" ffff
  d,1\ffff~ |
  d,1~ |
  d,1~ |
  d,2. r4 |
}

% ============================================================
% オーケストラ（Coda クライマックス）
% ============================================================

% 第1ヴァイオリン：合唱を支持
violinIV = \relative c''' {
  \globalV
  \clef treble
  d2\fff( e4 fis) |
  g2( fis4 e) |
  d1\ffff~ |
  d1~ |
  d1~ |
  d2. r4 |
}

% トランペット：d''' ハイノート宣言
trumpetV = \relative c'' {
  \globalV
  \clef treble
  \transposition c
  r1 |
  r1 |
  % d''' （"新たな限界=新たな始点"を宣言）
  d'''1\ffff~ |
  d'''1~ |
  d'''1~ |
  d'''2. r4 |
}

% ティンパニ：第5番「命運」動機 リズム変容
timpV = \relative c {
  \globalV
  \clef bass
  % 命運動機リズム変容: ♩♩♩𝅗𝅥 → ♪♪♪♩
  d8\fff d d d4 d d2 |
  d8 d d d4 d d2 |
  d1\ffff~ |
  d1~ |
  d1~ |
  d2. r4 |
}

% ============================================================
% スコア組み立て（Coda クライマックス mm.420-450）
% ============================================================
\score {
  <<
    \new ChoirStaff <<
      \new Staff {
        \set Staff.instrumentName = "S."
        \new Voice = "soprano" { \sopranoV }
      }
      \new Lyrics \lyricsto "soprano" {
        das Un -- mög -- li -- che es zer -- bricht!
      }
      \new Staff {
        \set Staff.instrumentName = "A."
        \new Voice = "alto" { \altoV }
      }
      \new Lyrics \lyricsto "alto" {
        das Un -- mög -- li -- che es zer -- bricht!
      }
      \new Staff {
        \set Staff.instrumentName = "T."
        \new Voice = "tenor" { \tenorV }
      }
      \new Lyrics \lyricsto "tenor" {
        Neu -- e Gren -- ze neu -- es Licht!
      }
      \new Staff {
        \set Staff.instrumentName = "B."
        \new Voice = "bass" { \bassV }
      }
      \new Lyrics \lyricsto "bass" {
        das Un -- mög -- li -- che zer -- bricht!
      }
    >>
    \new StaffGroup <<
      \new Staff {
        \set Staff.instrumentName = "Vn. I"
        \violinIV
      }
      \new Staff {
        \set Staff.instrumentName = "Tp."
        \trumpetV
      }
      \new Staff {
        \set Staff.instrumentName = "Timp."
        \timpV
      }
    >>
  >>
  \layout {
    \context {
      \Score
      \override SpacingSpanner.common-shortest-duration = #(ly:make-moment 1 8)
    }
  }
  \midi { \tempo 4 = 152 }
}

% ============================================================
% 楽章設計仕様（コメント）
%
% 第Ⅴ楽章の構造:
%   前半 (♩=96): 4/4 → 5/4 → 7/4 変化、Tenor Solo「Neu, wie eine Grenze weicht」
%   中間 (♩=120): 変拍子行進曲（5/4）、Strophe 1（S/A）+ Strophe 2（T/B）
%   後半 (♩=152): Coda（4/4固定）、SATB Tutti + 全管弦楽 最大音量
%
% 第9番継承（変容）:
%   B Rezitativ "O Freunde" → "O Grenze" (Ⅱ楽章)
%   T Solo "Froh, wie seine Sonnen fliegen" → "Neu, wie eine Grenze weicht"
%   音型: d'–f'–a'–d'' → d'–f'–a'–b'（最終音を長7度へ）
%   Coda "Alle Menschen" → "Neue Grenze" （全人類的宣言）
%
% クライマックス最高音:
%   S: c''' ffff（8小節持続）
%   A: a'' ffff
%   T: b' ffff
%   B: d ffff
%   Tp.1: d''' ffff
%
% 拍子変化の流れ:
%   4/4（出発）→ 5/4（変容）→ 7/4（拡張）→ 4/4（Coda・収束）
%   「限界が退き、新たな秩序が生まれる」過程を拍子で表現
% ============================================================
