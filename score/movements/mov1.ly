\version "2.24.0"

\header {
  title = "Symphony No. XI \"Grenze\""
  subtitle = "I. Erwachen aus dem Schweigen"
  subsubtitle = "沈黙からの覚醒"
  composer = "Music TWIN Collective (Soul-Twin Society, 2026)"
  opus = "Op. posth. XI"
}

% ============================================================
% 楽章概要
% 拍子: 3/4
% 調性: d-moll
% テンポ: ♩=42→72 (Adagio misterioso → Andante)
% 核心: No.X 全休符の「次の一音」
% ============================================================

% グローバル設定
global = {
  \time 3/4
  \tempo "Adagio misterioso" 4 = 42
  \key d \minor
}

% ============================================================
% 第1ヴァイオリン：ハーモニクスによる最初の音（mm.1-16）
% ============================================================
violinI = \relative c'' {
  \global
  \clef treble
  % mm.1-4: 完全休符（No.X全休符の継続）
  R2.*4
  % mm.5: ナチュラルハーモニクス a''' pppp（最初の音）
  <\parenthesize a''>4\4\flageolet\pppp ~
  <\parenthesize a''>2\flageolet
  % mm.6-7: 消えゆく余韻
  <\parenthesize a''>2.\flageolet\ppppp
  r2.
  % mm.8-12: sul ponticello tremolo 開始
  \override TextSpanner.bound-details.left.text = "sul pont."
  \startTextSpan
  a''4\pppp\trill( g'' fis'')
  e''2.~
  e''4( d'' cis'')
  d''2. ~
  d''4 r2
  \stopTextSpan
}

% ============================================================
% チェロ：最初の旋律提示（mm.9-16）
% ============================================================
cello = \relative c {
  \global
  \clef bass
  % mm.1-8: 完全休符
  R2.*8
  % mm.9-16: チェロ solo 旋律（主題A）
  \set midiInstrument = "cello"
  d4\mp( f a)
  d'2( cis4)
  b2.~
  b4( a g)
  f2( e4)
  d2.~
  d4 r2
  r2.
}

% ============================================================
% フルート：multiphonics（mm.17-24）
% ============================================================
flute = \relative c'' {
  \global
  \clef treble
  % mm.1-16: 完全休符
  R2.*16
  % mm.17: multiphonics c''+e''+g''
  \override NoteHead.style = #'harmonic
  <c'' e'' g''>2.\pp
  <c'' e'' g''>4( <d'' f'' a''>2)
  % mm.19: 単音へ収束
  \revert NoteHead.style
  a''2.\mp(
  g''2 f''4)
  e''2.~
  e''4( d''2)
  % mm.23: 第1Vn との合流
  cis''4\p( d'' e'')
  f''2.~
}

% ============================================================
% ティンパニ：沈黙を破る最初の一打（mm.4-16）
% ============================================================
timpani = \relative c {
  \global
  \clef bass
  % mm.1-3: 完全休符
  R2.*3
  % mm.4: 沈黙を破る最初の一打（pppp）
  d,4\pppp r2
  % mm.5-8: 徐々に増加
  r4 d,4\ppp r
  r2 d,4\pp
  d,2.\p ~
  d,4 r2
  % mm.9-16: tremolo 開始
  \repeat tremolo 6 { d,8 }
  \repeat tremolo 6 { d,8 }
  \repeat tremolo 6 { d,8 }
  \repeat tremolo 6 { d,8 }
  \repeat tremolo 6 { d,8 }
  \repeat tremolo 6 { d,8 }
  \repeat tremolo 6 { d,8 }
  \repeat tremolo 6 { d,8 }
}

% ============================================================
% スコア組み立て（冒頭セクション mm.1-24）
% ============================================================
\score {
  \new StaffGroup <<
    \new Staff {
      \set Staff.instrumentName = "Vn. I"
      \violinI
    }
    \new Staff {
      \set Staff.instrumentName = "Vc."
      \cello
    }
    \new Staff {
      \set Staff.instrumentName = "Fl."
      \flute
    }
    \new Staff {
      \set Staff.instrumentName = "Timp."
      \timpani
    }
  >>
  \layout {
    \context {
      \Score
      \omit BarNumber
    }
  }
  \midi {
    \tempo 4 = 42
  }
}

% ============================================================
% 楽章設計仕様（コメント）
%
% 22パート構成（全楽章）:
%   弦楽 5: Vn.I, Vn.II, Va, Vc, Cb
%   木管 4: Fl（Picc兼任）, Ob, Cl, Fg（Cfg兼任）
%   金管 9: Hr×4, Tp×3, Tb×3（+Tuba = 10）
%   打楽器: Timp×4台
%   合唱 4: S, A, T, B
%
% 本ファイルは第Ⅰ楽章の核心部分（冒頭）サンプル
% MuseScore変換: LilyPond → MusicXML → .mscz
% ============================================================
