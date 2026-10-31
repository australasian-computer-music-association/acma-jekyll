---
title: 'Creating a Platform for Embedded Intelligent Instruments: Maybe I Like the Misery'
authors:
# Printed "Charles Patrick Martin"; spelt as in his other entries.
- Charles Martin
year: 2024
type: abstract
section: Papers Presentation — Instruments, Education and AI
order: 58
pages: 45-46
section_pdf: /proceedings/ACMC2024-proceedings.pdf
---
This talk discusses recent progress with IMPSY, a Python platform for embedding generative AI into new digital musical instruments. Our research aims to empower researchers and musicians with tools for creating intelligent instruments that learn from small datasets. IMPSY employs a mixture density RNN to generate musical data in realtime, interfacing with other musical systems via MIDI, OSC, WebSockets, or serial. We've tested IMPSY on various Raspberry Pi models, including the cost-effective Zero 2 W, achieving acceptable performance. Our experiments showcase collaborative performances and concerts using these embedded intelligent instruments. Benchmark findings reveal that TensorFlow Lite offers optimal performance and that predictions under 5ms are possible on a Zero 2 W and under 0.5ms on a Raspberry Pi 5. To mitigate the misery of complex Python dependencies and multi-device management, we use Poetry for package management and Ansible to help develop a pre-installed Raspberry Pi OS image. These strategies have significantly accelerated our research and its practical applications. Our IMPSYpi image operates without an internet connection and can be configured by musicians via ethernet-over-USB and using a webrather than command-line-interface. IMPSY enables electronic musicians to incorporate generative AI in hardware setups without relying on internet connectivity, using the musician's own data for predictions. This research demonstrates that IMPSY can operate effectively on even the cheapest Linux-based Raspberry Pi (29AUD). This work represents a significant step towards accessible, embedded AI for musical performance and composition.
