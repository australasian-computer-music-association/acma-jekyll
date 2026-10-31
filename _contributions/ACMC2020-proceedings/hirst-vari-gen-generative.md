---
title: 'Vari-Gen: A Generative System for Creating Musical Variations Using Max, Bach, and Cage in Real-Time'
authors:
- David Hirst
year: 2020
type: abstract
section: Synthesis, Interaction, and Notation
order: 66
media:
- kind: video
  url: https://youtu.be/wYl8gwqq_Co
  label: Recording of Synthesis, Interaction, and Notation
- kind: website
  url: https://australasian-computer-music-association.github.io/acmc2020/poster_9.html
  label: Page on the ACMC 2020 conference site
bio: David Hirst’s electroacoustic music compositions have been performed in the United States, Canada, the UK, the Netherlands, New Zealand, South Korea and nationally across Australia. He studied computer music at La Trobe University, composition with Jonty Harrison at the University of Birmingham, and completed a PhD in electroacoustic music composition and analysis at the University of Melbourne. Hirst has worked as an academic at the Tasmanian Conservatorium of Music, La Trobe University, and at the University of Melbourne. He is currently Honorary Principal Fellow at the Melbourne Conservatorium of Music, University of Melbourne. His most recent album, “The Shape of Water” is available on iTunes and Spotify.
---
This talk will demonstrate a new system for generating variations on segments of music that have been previously recorded or composed and saved as MIDI files.

The system builds on work presented at the ACMC 2018 Perth conference which was documented in the paper Hacking Music Notation with Bach and Cage (Hirst, 2018). That paper documented the “Composer’s Little Helper” (CLH) which is a Max patcher that makes use of the “Bach” and “Cage” libraries to manipulate and mix musical notation that has been saved in a “shelf” as separate segments. CLH implements musical operations such as transposition, inversion, retrograde, plus a number of other “treatments” that use the high-level “Cage” library for real-time computer-aided composition.

The Composer’s Little Helper was a non-realtime system to assist in the compositional process. In contrast, Vari-Gen is like the next generation development where a generative system is used to produce note information in realtime. Reading from a MIDI file, variations in pitch, onset time, durations and note velocity are produced and can be varied in realtime using a Markov methodology for each parameter independently.

Using the “bach.roll” representation of the original MIDI file, which is a musical staff with note-heads notated in proportional notation, the composer/performer can select a specific number of notes for treatment, vary the transposition, durations, onset times, velocities, and the order of the Markov chain for each parameter of the variation generator.

Realtime output triggers sound using a VST instrument plugin, which can be varied to suit the musical style. The note output is recorded in another bach.roll object, which can be saved as a MIDI file at any time.

In essence, the system functions as an exotic sequencer/variation generator, and because it all happens in realtime, it could also function as a performance instrument.

The two part work Pierre and Frank was created using a combination of the Vari-Gen software and non-realtime editing (to be screened at ACMC 2020).
