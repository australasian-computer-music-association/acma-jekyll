---
layout: page
title: Australasian Computer Music Association
feature_image: assets/images/acmc2019-concert-e1618799441533.jpg
---

{:.info-box}
The **2023** Australasian Computer Music Conference (ACMC) will take place from **October 9-11, 2023** hosted by [UNE Sydney](https://www.une.edu.au/campus-life/une-sydney). 
- The Call for Submissions is here: <https://www.une.edu.au/acmc2023>
- Link to the event on facebook: <https://fb.me/e/5XkIHhLcu>
- Link to submission portal: <https://cmt3.research.microsoft.com/ACMC2023>


{% comment %}
The 2022 Australasian Computer Music Conference (ACMC) took place in Te
Whanganui-a-Tara, Aotearoa | Wellington, New Zealand from August 31 -
September 1. See the conference website at [acmc2022.com](https://www.acmc2022.com)
{% endcomment %}

The [Australasian Computer Music
Association]({% link about.md %}) is a forum for Australian and
New Zealand composers and researchers with an interest in music technology and
computer music. The association was founded in 1989.

The [Australasian Computer Music Conference
(ACMC)]({% link conferences.md %}) is an annual gathering
hosted in various cities in the region since 1993. The [proceedings of previous
conferences]({% link conferences.md %}) are available online.

_[Chroma](https://journal.computermusic.org.au/chroma)_ is our peer-reviewed
Journal, and was relaunched in 2021. [Submissions are now
open](https://journal.computermusic.org.au/chroma).

[Membership]({% link membership.md %}}) of the Australasian
Computer Music Association is available for individuals and organisations, and
is included in conference registration. Membership fees assist with our
publishing costs and pay for conference scholarships and awards.

The [committee]({% link committee.md %}) is responsible for the
association's governance, and planning our activities and publications. It is
elected from the association's members. The association is not run for profit
and all committee members are volunteers.

## Latest News

{% for post in site.posts limit:3 %}
### [{{post.title}}]({{ post.url | relative_url }})

<h6 class="font-italic">{{ post.date | date_to_string }}</h6>

{{ post.excerpt }}
{% endfor %}

[More news...]({% link news/index.html %})

