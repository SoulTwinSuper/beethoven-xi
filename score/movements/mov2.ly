\version "2.24.0"

\header {
  title = "Symphony No. XI \"Grenze\""
  subtitle = "II. Kollision"
  subsubtitle = "衝突"
  composer = "Music TWIN Collective (Soul-Twin Society, 2026)"
  opus = "Op. posth. XI"
}

% ============================================================
% 楽章概要
% 拍子: 7/8+5/8 交替
% 調性: b-moll
% テンポ: ♩=132 (Allegro feroce)
% 核心: 限界との正面衝突
% 合唱: バスレチタティーフ（楽章冒頭）
% ============================================================

% 第Ⅱ楽章グローバル（変拍子）
globalII = {
  \time 7/8
  \tempo "Allegro feroce" 4 = 132
  \key b \minor
}

% ============================================================
% バス独唱：第9番変容レチタティーフ（mm.1-12）
% "O Grenze, nicht dieses Ende! / Hier beginnt das wahre Lied!"
% ============================================================
bassVoice = \relative c {
  \globalII
  \clef bass
  % 楽章冒頭：伴奏なし
  \set midiInstrument = "voice oohs"
  % "O Grenze, nicht dieses Ende!"
  b4\f( c d) e4.~ |
  e4( fis) r4. |
  % "Hier beginnt"
  fis4\ff( g a b4.) |
  % "das wahre Lied!"
  fis2.( e4.) |
  % 内省：ppp
  \time 5/8
  d4\ppp( cis) b4. |
  r2. r4. |
  % 再び宣言：7/8 復帰
  \time 7/8
  b4\f( c d e4.) |
  fis4( g) a4.~ |
  a4( b) fis4.~ |
  % クライマックス ff
  fis2\ff e4. |
  % "Lied" ppp消滅
  b,2.\ppp ~ |
  b,4. r4. |
}

% ============================================================
% ティンパニ：pp tremolo（最小伴奏）
% ============================================================
timpII = \relative c, {
  \globalII
  \clef bass
  \repeat tremolo 7 { b,16\pp }
  \repeat tremolo 7 { b,16 }
  \repeat tremolo 7 { b,16 }
  \repeat tremolo 7 { b,16 }
  \time 5/8
  \repeat tremolo 5 { b,16 }
  \repeat tremolo 5 { b,16 }
  \time 7/8
  \repeat tremolo 7 { b,16 }
  \repeat tremolo 7 { b,16 }
  \repeat tremolo 7 { b,16 }
  b,4\ff r2.
  \repeat tremolo 7 { b,16\ppp }
  r4. r2
}

% ============================================================
% コントラバス：pizzicato（最小伴奏）
% ============================================================
contrabassII = \relative c, {
  \globalII
  \clef bass
  b,4\pp\pizz r4. r4 |
  r2. r4. |
  b,4\mf\pizz r r r4. |
  r2. r4. |
  \time 5/8
  r2. r4. |
  r2. r4. |
  \time 7/8
  b,4\f\pizz r r r4. |
  r2. r4. |
  b,4\ff\pizz r r r4. |
  b,4 r r4. |
  r2. r4. |
  r2. r4. |
}

% ============================================================
% スコア組み立て（バスレチタティーフ セクション mm.1-12）
% ============================================================
\score {
  <<
    \new Staff {
      \set Staff.instrumentName = "Bass Solo"
      \new Voice = "bass" { \bassVoice }
    }
    \new Lyrics \lyricsto "bass" {
      O Gren -- ze, nicht die -- ses En -- de!
      Hier be -- ginnt das wah -- re Lied!
    }
    \new Staff {
      \set Staff.instrumentName = "Timp."
      \timpII
    }
    \new Staff {
      \set Staff.instrumentName = "Cb."
      \contrabassII
    }
  >>
  \layout {}
  \midi { \tempo 4 = 132 }
}

% ============================================================
% 楽章設計仕様（コメント）
%
% 第Ⅱ楽章の中核技法:
%   B solo: "O Grenze, nicht dieses Ende! Hier beginnt das wahre Lied!"
%           第9番 "O Freunde" の変容（下降→上昇音形の逆転）
%   Tp: Ⅰ楽章全体で不在→m.72 の突然の fff 登場（衝撃効果）
%   Tb: グリッサンド（全音域）、衝突の「ぶつかり合い」
%   Hr: 4本ポリフォニー（4声フーガ様）
%   Timp: 4台ポリリズム（mm.80-120）
%         Timp.1: 3連符 / Timp.2: 4分音符 / Timp.3: 5連符 / Timp.4: 7連符
%
% 変拍子設計:
%   7/8 = 3+2+2 または 2+3+2（楽章内で変化）
%   5/8 = 3+2 または 2+3
%   交替によって「限界との衝突」の不規則性を表現
% ============================================================
