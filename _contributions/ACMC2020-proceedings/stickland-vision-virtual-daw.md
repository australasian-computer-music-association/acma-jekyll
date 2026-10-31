---
title: Towards a Vision for a Virtual DAW Collaboration Studio for Professional Post-Production Music Projects
authors:
- Scott Stickland
- Nathan Scott
- Rukshan Athauda
year: 2020
type: abstract
section: DAWs, Liveness, and Algorithms
order: 11
media:
- kind: video
  url: https://youtu.be/Df2m_d7aEgY
  label: Recording of DAWs, Liveness, and Algorithms
- kind: website
  url: https://australasian-computer-music-association.github.io/acmc2020/poster_77.html
  label: Page on the ACMC 2020 conference site
bio: |-
  **Scott Stickland** is a third-year PhD (Music) candidate in the School of Creative Industries at The University of Newcastle (UoN), Australia. He has previously completed a Master of Music Technology (UoN) and a Bachelor of Education (Sec) – Music (Melbourne), and taught and coordinated music programs in Victorian secondary schools for 16 years. Scott has presented papers at ACMC2018 and WAC 2019 since commencing his PhD. He currently teaches audio and music production through his business, Monty Sound Production, and plays keyboards in the national touring band, Cool Change – The Ultimate Tribute.

  **Nathan Scott** is a lecturer in the School of Creative Industries at the University of Newcastle, Australia. He has interdisciplinary research interests spanning creative arts, technology, science, health and education. Nathan has presented and performed internationally, and has published in the areas of music, technology, education, gaming and the human voice. He has presented workshops in regional NSW (2003) and developed an online international postgraduate program supporting the use of technology in music contexts. He participated in the CHASS Expanding Horizons forum in Canberra (2006) and undertook a sub-project as part of an ALTC National Teaching Fellowship (2010).

  **Dr Rukshan Athauda** is a Senior Lecturer at the School of Electrical Engineering and Computing at The University of Newcastle (UoN), Australia. Dr Athauda’s research interests span Database Systems, Technology-enhanced Learning, Cloud Computing and IT Security. Dr Athauda has published over 60 peer-reviewed research articles internationally. He has supervised 4 PhD completions at UoN and also undertaken a number of admin roles including Head of Discipline and Program Convenor. Prior to joining UoN, Dr Athauda has worked at Microsoft Corporation, USA, High-Performance Database Research Centre at Florida International University, USA and Sri Lanka Institute of Information Technology, Sri Lanka.
---
The global coronavirus (COVID-19) pandemic has brought into sharp relief not only the need for effective and inclusive online collaboration platforms but those that provide naturalistic and contextual extensions to the day-to-day “offline” milieu [1-3]. In this presentation, we explore “What would an ‘ideal’ online collaboration platform provide for professional post-production in music?”

We interviewed a group of music/sound practitioners who regularly work with complex multitrack digital audio projects and, in many cases, have limited or no facility for remote real-time collaboration directly through their music software. We collated the data produced from professionals working in Australian recording and post-production contexts through a series of user-focused interviews. This process ascertains their existing methods of collaboration/production and garners their perspectives of an “ideal” environment for collaborative remote music post-production. In this talk, we present an analysis of their information and the subsequent outcomes.
Overwhelmingly, the collaborative post-production practices described by the interviewees are asynchronous. That is, real-time collaboration does not occur even though it is highly desirable. Although some music production platforms now feature integrated collaboration methods, such as Avid’s Cloud Collaboration [4] and Steinberg’s VST Transit [5], audio and session/project file sharing via third-party cloud storage remains a popular means for studio engineers to disseminate work to their clients for feedback and approval. Using services such as Dropbox [6] and Google Drive [7], studio mixers/producers upload stems and a software-specific project file, or just an audio mix, for the client to download and audition. Any changes require further communication between the client and mixer/producer before any alterations can proceed. Upon completion, the uploading/downloading, auditioning, and feedback process begins again, until eventually reaching a mutually-satisfactory result, or, in some instances, the client depletes the budget. When integrating video into a project, and depending on a music production software’s import/export capabilities, some practitioners prefer to share advanced authoring format (AAF) [8] or open media framework (OMF) [9] files instead, primarily to ensure video-audio synchronisation, but also to include basic automation, such as volume and panning changes. The interviewees also articulated a “wish-list” of features and capabilities given the opportunity to collaborate remotely with clients, producers, or other studios in real-time, highlighting the expected outcomes of such an environment.

A conclusion to be drawn from the interviews is that, outside of remote one-to-one recording of an instrumentalist or vocalist, studio engineers do not engage in real-time remote collaboration simply because synchronous post-production collaboration methods do not currently exist. That is not to say that studio professionals have not contemplated what would constitute a practical remote post-production real-time collaborative environment. All the interviewees were forthcoming when asked to provide a wish-list of capabilities and features they would consider essential when working with a synchronous platform. Some common themes emerged from the various responses, particularly:

- The ability to see and speak with the client during the session;
- The ability to edit, mix and produce, and operate the music production software in-studio;
- The ability to audition remote changes on-the-spot; and
- The integrity and high fidelity of the project’s audio files are maintained and protected.

One interviewee stated his expectation quite succinctly, saying he wanted the experience “to be like I was sitting there in the studio” with his project collaborators in a “virtual studio”. One could well adopt this sentiment as an overarching vision for developing any remote collaboration platform, particularly one that operates in a real-time environment.

Our research work has the potential to make this vision a reality. In 2018, we proposed a framework that had the potential to realise real-time collaboration on music production projects over the Internet [10]. Further refinement to the framework, mainly focusing on online group establishment and the creation of bilateral control data channels, led to our prototype implementation paper, presented at the 2019 Web Audio Conference [11]. Presently, we are working on a fully-functional online collaboration platform for professional post-production in music. In future, we expect to evaluate this platform in real-world “virtual studio” environments with industry professionals/sound engineers and clients.

Supporting Material

1. Organisation for Economic Co-operation and Development. 2020. Education responses to COVID-19: Embracing digital learning and online collaboration. (23 March 2020) Retrieved 5 May 2020 from https://www.oecd.org/coronavirus/policy-responses/education-responses-to-covid-19-embracing-digital-learning-and-online-collaboration-/
2. Burris, P. 2020. COVID-19 Era Will Tell Us Much About Future of Collaboration Tools. eWeek. Retrieved 5 May 2020 from https://www.eweek.com/enterprise-apps/covid-19-era-will-tell-us-much-about-future-of-collaboration-tools
3. Wong, K. (2020, June). COVID-19 Pushes PLM/PDM to the Cloud: From bill of materials and file sharing to collaboration, many functions move to the cloud during lockdown. Digital Engineering 247, 26, 5, 23-25. Retrieved 15 June 2020, from http://search.ebscohost.com/login.aspx?direct=true&db=aps&AN=143695425&site=eds-live.
4. Avid Technology Inc. 2020. Producing Software for Music - Cloud Collaboration - Pro Tools. Retrieved 7 March 2020 from https://www.avid.com/pro-tools/cloud-collaboration
5. Steinberg Media Technologies GmbH. 2020. VST Transit | Steinberg. Retrieved 7 March 2020 from https://www.steinberg.net/en/products/vst/vst_transit.html?et_cid=15&et_lid=22&et_sub=VST%20Transit
6. Dropbox Inc. n.d. Dropbox Professional. Retrieved 7 March 2020 from https://www.dropbox.com/pro
7. Google LLC. 2020. Google Drive: Free Cloud Storage for Personal Use. Retrieved 7 March 2020 from https://www.google.com/drive/
8. McLeish, D. and Tudor, P. 2004. The Advanced Authoring Format and its Relevance to the Exchange of Audio Editing Decisions. In Proceedings of the 25th International Conference of the Audio Engineering Society (London, United Kingdom, 17-19 June 2004). Audio Engineering Society Inc., New York, United States. Retrieved 9 January 2019 from http://www.aes.org/tmpFiles/elib/20190108/12824.pdf
9. Lamaa, F. 1993. Open Media Framework Interchange. In Proceedings of the 8th Audio Engineering Society Conference UK (London, United Kingdom, 18-19 May 1993). Audio Engineering Society Inc., London, United Kingdom. Retrieved 9 January 2019 from http://www.aes.org/tmpFiles/elib/20190108/6134.pdf
10. Stickland, S., Scott, N. and Athauda, R. 2018. A Framework for Real-Time Online Collaboration in Music Production. In Proceedings of the ACMC2018: Conference of the Australasian Computer Music Association (Perth, Australia, 6-9). Retrieved 20 March 2019 from https://computermusic.org.au/conferences/acmc-2018/
11. Stickland, S., Athauda, R. and Scott, N. 2019. Design of a real-time multiparty DAW Collaboration Application using Web MIDI and WebRTC APIs. In Proceedings of the Web Audio Conference (WAC 2019) Diversity in Web Audio (NTNU, Trondheim, Norway, 4-6). Trondheim, Norway. Retrieved 1 May 2020 from https://www.ntnu.edu/documents/1282113268/1292502725/WAC_2019_proceedings.pdf
