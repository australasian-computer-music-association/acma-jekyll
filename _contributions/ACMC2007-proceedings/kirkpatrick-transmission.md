---
title: Transmission
authors:
- David Kirkpatrick
- Paul Kopetko
year: 2007
type: artist-talk
section: Artist Talks
order: 23
pages: '122'
pdf: /proceedings/ACMC2007-proceedings/kirkpatrick-transmission.pdf
---
Transmission is a collaborative computer music piece which attempts to cross the boundaries between the rigid, static nature of pre-recorded electronic music and the improvisation of live, in-the-moment performance. This is achieved through the design of a new computer-based musical instrument which was premiered at a University of Wollongong concert on the 1st of June 2007.

In Transmission, a computer tracks the movements of two performers on stage, whose physical location and bodily gestures are used to capture sounds being broadcast over the FM radio spectrum. These captured radio sounds are mixed with an array of pre-recorded sounds also triggered by gestures. The appropriation of FM radio sound during the performance is key to the improvisational aspect of the work, as the sonic ‘found objects’ which are captured will not only be different in every performance, but also virtually impossible to predict beforehand. It is thus up to the performers’ musical intuition to capture and treat suitable ranges of live radio to combine with improvised selections from a bank of gesturally-selected pre-recorded music. In using the body to control a mergence of pre-composition and improvisation, a piece of computer music is created that bridges the gap between composer, performer and machine, begging the question of where one entity ends and the other begins.

The technical setup for the piece is as follows: two performers are monitored from above by a black and white CCTV camera. The output from the CCTV camera is connected to our computer system through a Falcon Frame Grabber PCI card, which then sends the video footage in real-time to Frieder Weiss’ EyeCon software (recently used in a Sydney Opera House performance entitled Glow by the dance company Chunky Move). Our self-designed EyeCon patch detects the two performers and tracks their positions and movements, forwarding this data to Pure Data via OSC. The position information of the first performer is used by Pure Data to control the frequency scanner of a Radio Xtreme USB FM radio tuner, so that as the performer moves left and right along the stage, the tuner moves left and right along the FM frequency spectrum. More in-depth position and gestural information sent to Pure Data is converted into MIDI signals and routed to Abelton Live, which applies digital filtering effects to the radio signal in real-time. The second performer’s movement and gesture cues are similarly sent through Pure Data to Abelton Live in order to trigger and process a bank of pre-recorded clips.

In our presentation at the conference we will discuss the artistic principles behind Transmission, as well as the technical process used to develop the computer-based instrument. We shall display documentation of our performance and propose ways in which a similar process could be used in future to create a virtually unlimited array of works encompassing sound, light and projection.
