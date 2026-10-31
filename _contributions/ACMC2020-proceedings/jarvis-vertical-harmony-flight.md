---
title: 'Vertical Harmony: Flight-Path as Musical Form'
authors:
- Robert Jarvis
year: 2020
type: abstract
section: DAWs, Liveness, and Algorithms
order: 10
media:
- kind: video
  url: https://youtu.be/Ct-Sb-zGlG0
  label: Video
- kind: video
  url: https://youtu.be/Df2m_d7aEgY
  label: Recording of DAWs, Liveness, and Algorithms
- kind: website
  url: https://australasian-computer-music-association.github.io/acmc2020/poster_64.html
  label: Page on the ACMC 2020 conference site
bio: Robert Jarvis is an accomplished audio-visual artist based in Melbourne, Australia. He works across live video performance, music, animation and software development, with a focus on the development of tools for live audio-visual performance. He is currently a PhD candidate at RMIT University where he is exploring the intersection of gliding flight and musical performance.
---
We present output of research into the integration of human flight and musical performance via telemetry driven, spatial meta-compositions. The work explores the use of a sailplane flight path as a structure around which musical form can emerge. It serves as a point of reflection on the composition of such spatial meta-compositions and their potential for enhancing personal experiences and enabling new modes of artistic performance in mixed realities.

The system has three primary components - a body-worn sensing unit responsible for logging and broadcasting positional data, a log playback system, and a suite of composition modules built in Max for Live.

The positional sensing unit consists of an Ardupilot-based flight controller and Raspberry Pi computer. The Raspberry Pi communicates with the Ardupilot board via the Mavlink protocol allowing for logging and broadcasting of captured sense data as Open Sound Control (OSC). The system has been designed such that it can be used for logging data as well as communicating in real-time with the composition modules either locally over Wi-Fi or remotely via 433Mhz radio link. The telemetry playback module was built in Max allowing for the replaying of logged telemetry alongside synchronised video recordings. This enables the composer to create a spatial meta-composition "offline" for later use in a real-time performance context.

The piece Aileron One is the output of an iterative, creative process consisting of cycles of music composition and interactive system development. The work uses only a subset of the data points captured during the flight; altitude (position above the ground in metres), total velocity (in metres per second), and heading (orientation around the up vector in degrees).

Altitude serves as the foundational element on which the piece is built. The piece can be considered as a vertical structure rising to approximately 950 metres above the ground. A circular chord progression (Fmaj9 Fmaj9/E Am9 G) repeats along the up vector with instrumentation becoming denser in six, discrete, evenly spaced layers. To add variation and movement, a set of instruments are panned to four evenly spaced compass headings. Total velocity is then used to control the speed of melodic and percussive elements throughout the piece.

The spatial approach leads to interesting temporal-harmonic consequences: as the glider ascends, the repeating chord progression is played in one direction, as the glider descends the progression is played in the other direction. The rate at which the progression moves is dictated by the vertical velocity of the glider. The harmonic progression ascends at a steady rate as the glider is towed into the air, leading to a point of contrast when the tow is released and the glider transitions to a slow, steady descent. The musical effect of these moments is an aesthetic mirroring of the dynamics of the aircraft.

It can also be seen that during periods of rapid ascent and descent such as during aerobatic manoeuvres, the musical result is less coherent as chords pass to quickly to establish effective tension and release. This highlights a challenge of composing spatial meta-compositions, that is how to spatially scale musical properties such that passing through them at a range of velocities produces satisfying musical results.

The work as it is presented is part of an active research effort and as such will continue to be refined. We foresee potential to create far richer work by creating coherent mappings between musical elements and data components resulting in complex, emergent musical results.

We are actively investigating gliding flight alongside other forms of physical activities such as kayaking and rock climbing to determine both the performative potential of these activities as well as the musical considerations when composing spatial meta-compositions of contrasting scales and physical contexts.
