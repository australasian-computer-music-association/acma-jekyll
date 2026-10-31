---
title: Interfacing Real-Time Audio and File I/O
authors:
- Ross Bencina
year: 2014
type: paper
section: Refereed Papers
order: 3
pages: 21-28
pdf: /proceedings/ACMC2014-proceedings/bencina-interfacing-real-time.pdf
---
Programming a computer to record or play a sound file in real-time is not as easy as it may seem. The naive approach is to call file I/O APIs from within the routine that handles real-time audio I/O. This leads to audible glitches whenever the time taken to access a file exceeds the time available to deliver a buffer of real-time audio.

This paper describes an approach to streaming file playback and recording that operates correctly under these conditions. It performs file I/O in a separate thread, buffers audio data to mask file I/O delays, and uses asynchronous message passing and lock-free queues for inter-thread communication.
