\version "2.18.2"
\language "english"

\pointAndClickOff

\header {
    title = "The Cat That Kittled in Jamie's Wig"
}

global = {
    \key g \major
    \time 4/4
}

cat_that_kittled = {
    \global
    \relative c' {
        \partial 4. {b'8\3 c8.\2 b16\3}
        a16 a,8. a8. b16 c8. d16 e8. fs16 |%1
        g8. g16 \grace {a8\3} g8. fs16 g8. c16\2 b8.\3 c16\2 |%2
        a16 a,8. a8. b16 c8. d16 \tuplet 3/2 {b'8\3 c\2 d} |%3
        \tuplet 3/2 {e8\2 fs\1 e\2} \tuplet 3/2 {d\1 c\2 b\3} a8. b16\3 c8.\2 b16\3 |%4
        a16 a,8. a8. b16 c8. d16 e8. fs16 |%5
        g8. d16 b8. d16 g8. b16\3 c8.\2 d16 |%6
        \tuplet 3/2 {e8\2 fs\1 e\2} \tuplet 3/2 {d c\2 b\3} c8. a16 b8. g16 |%7
        e16 a8. a8. g16 a8. b16 cs8. d16 \bar "||" |%8
        e16\3 a8. a8. gs16 e8.\3 fs16\2 g8.\2 d16 |%9
        e16\3 a8. a8. fs16\2 g8.\2 e16\3 fs8.\2 d16 |%10
        e16\3 a8. a8. gs16\2 e8.\3 fs16\2 g8.\2 fs16\2 |%11
        \tuplet 3/2 {e8\2 fs\1 e\2} \tuplet 3/2 {d c\2 b\3} c8. a16 b8.\3 g16 |%12
        e'16\3 a8. a8. gs16 e8.\3 fs16\2 g8.\2 d16 |%13
        e16\3 a8. a8. fs16\2 g8.\2 fs16\2 g8.\2 a16 |%14
        \tuplet 3/2 {b8 c b} \tuplet 3/2 {a\2 g\2 fs\2} g8.\2 e16\3 fs8.\2 d16 |%15
        \tuplet 3/2 {e8\2 fs\1 e\2} \tuplet 3/2 {d c\2 b\3} a2 \bar "|." |%16
    }
}

%ALSO YOU SHOULD DO LON DUBH... LIKE LAOISE KELLY / JEAN [GUITAR]

music = \cat_that_kittled

\score {
    <<
        \new Staff {
            \music
        }
        \new TabStaff \with {
            stringTunings = #guitar-dadgad-tuning
        }
         {
            \clef moderntab
            \transpose c' c {\music}
        }
    >>
}