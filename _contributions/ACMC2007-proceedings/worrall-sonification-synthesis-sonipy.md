---
title: Sonification, Synthesis and SoniPy
# Printed as "Artist Talk: Sonification, Synthesis and SoniPy".
authors:
- David Worrall
year: 2007
type: artist-talk
section: Artist Talks
order: 26
pages: '125'
pdf: /proceedings/ACMC2007-proceedings/worrall-sonification-synthesis-sonipy.pdf
---
**1. Data sonification**

One way of classifying data sonifications is according to where they are placed on a continuum with free data transformation on one end to perceptually linear mapping on the other.

Closer to the ‘free data’ end of the continuum would be the use digital documents as control data for some sound synthesis routines as arbitrarily determined by the sonifier. It is likely that the (possibly imagined) content of the documents would play a role in culturally contexturalising the resulting soundscape.

My current work sits closer to the other end of the continuum. I’m sonifying high-frequency intraday stockmarket data as delivered by a securities exchange trading-engine. Whilst there are utilitarian uses for such sonifications to assist decision-making participants and regulators, my primary concern is a cultural one: to provide a better ‘feel’ for market exchanges, which have increasingly infiltrated our lives at the same time as their operation has become more virtualised.

This work is undertaken as a PhD in data sonification at The University of Canberra, funded by them and the Capital Markets Cooperative Research Centre in Sydney.

**2. The SoniPy Project**

As data sonification is an interdisciplinary activity, it is not surprising that a diverse range of research and production tools is required. My forays into the sonification of High Frequency Data (HFD) made it clear to me that, in general, music composition software was inadequate for the task of data sonification once handling the data itself became critical, as it does in the timely handling of multi-dimensional or multiplexed streams.

I’ll further expand on the reasons for the these limitations and the criteria I established for finding, testing and integrating software components that can work together is a time-consuming and somewhat frustrating task.

The Sonipy Project aims to collect a set of tools by collating public-domain Python modules that are suitable for the purpose and integrating them using a modular framework. In doing so, the Project aims to provide a community resource for individual sonifiers who don't have the time, skill or inclination to independently go through the process of putting together such a coherently-functioning toolset.

A full discussion of the motivations and concepts involved is discussed in the ICAD 2007 paper which is available for download from the SoniPy website: <http://sonipy.sourceforge.net/>. SoniPy is established as an open-source community-based project. It is just beginning and contributions are welcome.
