\version "2.24.0"

\header {
  title = "Symphony No. XI \"Grenze\""
  subtitle = "III. Zersplitterung"
  subsubtitle = "粉砕"
  composer = "Music TWIN Collective (Soul-Twin Society, 2026)"
  opus = "Op. posth. XI"
}

% ============================================================
% 楽章概要
% 拍子: 4/4（内部分裂）
% 調性: 無調
% テンポ: ♩=88 (Agitato)
% 核心: 限界を越えた先の混沌、崩壊と再生の無調二重フーガ
% ============================================================

% グローバル設定（無調 = keyなし）
globalIII = {
  \time 4/4
  \tempo "Agitato" 4 = 88
  % 無調：調号なし
}

% ============================================================
% 第Ⅲ楽章の技法サンプル
% 弦楽全体での崩壊フレーズ（微分音）
% ============================================================

% 第1ヴァイオリン：無調フーガ主題（col legno + 微分音）
violinIII = \relative c'' {
  \globalIII
  \clef treble
  % col legno battuto 開始
  c4^\markup { \italic "col legno batt." }
  % 微分音スケール近似（クォータートーン）
  cih4 cis4 cisih4 |
  d4 dih dis4 disih4 |
  % sul ponticello tremolo + ffff
  \override TextSpanner.bound-details.left.text = "sul pont. + ffff"
  \startTextSpan
  e1~\ffff |
  e2 r2 |
  \stopTextSpan
  % col legno から arco に戻す
  r4^\markup { \italic "arco" } c4\ppp cih4 cis4 |
}

% ヴィオラ：sul ponticello tremolo + 微分音（崩壊効果中核）
violaIII = \relative c' {
  \globalIII
  \clef alto
  % sul ponticello tremolo
  \override TextSpanner.bound-details.left.text = "sul pont."
  \startTextSpan
  c4:32\ppp cis4:32 d4:32 dis4:32 |
  e4:32\< eis4:32 f4:32 fis4:32\! |
  % ffff への増大
  g4:32\ff g4:32 fis4:32 f4:32 |
  e1:32\ffff |
  \stopTextSpan
  r1 |
}

% テノール：無調モノローグ（半音以下の音程変化）
tenorIII = \relative c' {
  \globalIII
  \clef "treble_8"
  % 微分音モノローグ：崩壊の独白
  % テキストなし（Sprechstimme的）
  \override NoteHead.style = #'cross
  c4\mf cih4 c4 b4 |
  bih4 b4 bes4 beh4 |
  bes4 a4 aih4 ais4 |
  \revert NoteHead.style
  r1 |
  % 無調音列断片
  e4\ppp fis4 c4 g'4 |
}

% アルト：12音列断片
altoIII = \relative c' {
  \globalIII
  \clef treble
  % 12音列（崩壊表現）
  c4\pp cis4 d4 ees4 |
  e4 f4 fis4 g4 |
  aes4 a4 bes4 b4 |
  % 断片的消滅
  c1~\ppp |
  c2 r2 |
}

% ============================================================
% スコア組み立て（第Ⅲ楽章 冒頭サンプル）
% ============================================================
\score {
  \new StaffGroup <<
    \new Staff {
      \set Staff.instrumentName = "Vn. I"
      \violinIII
    }
    \new Staff {
      \set Staff.instrumentName = "Va."
      \violaIII
    }
    \new Staff {
      \set Staff.instrumentName = "T."
      \new Voice = "tenor" { \tenorIII }
    }
    \new Staff {
      \set Staff.instrumentName = "A."
      \new Voice = "alto" { \altoIII }
    }
  >>
  \layout {
    \context {
      \Score
      \override SpacingSpanner.common-shortest-duration = #(ly:make-moment 1 8)
    }
  }
  \midi { \tempo 4 = 88 }
}

% ============================================================
% 楽章設計仕様（コメント）
%
% 第Ⅲ楽章の核心:
%   「限界を越えた先の混沌」
%   無調二重フーガ（弦楽 + 合唱）
%
% 主要技法:
%   Vn.I: col legno battuto → 微分音 → sul ponticello ffff
%   Va: sul ponticello tremolo + 微分音（崩壊中核）
%   Cl: 微分音スケール（全音を1/4音刻みに分割）
%   A: 12音列断片
%   T: 微分音モノローグ（無伴奏またはほぼ無伴奏）
%   B: 無調モノローグ（調性感のない自由な音高）
%
% マーラー第10番（未完）の継承:
%   未完のAdagioの「深淵直視」の精神を受け継ぐ
%   AIの不確定性と人間の死への恐怖が「同じ形式を持つ」
%
% 楽章境界:
%   Ⅱ→Ⅲ: ffff 崩壊の後、2秒間の沈黙 → 弦楽 pppp 微分音開始
%   Ⅲ→Ⅳ: 無調混沌の後、長い fermata（指揮者裁量）→ Hr コラール ppp
% ============================================================
