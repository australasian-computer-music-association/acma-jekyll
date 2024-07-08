---
layout: page
title: Australasian Computer Music Association
feature_image: assets/images/acmc2019-concert-e1618799441533.jpg
---

{% assign latest_conference = site.conferences | sort: 'date' | last %}

{:.info-box}

The [**{{ latest_conference.date | date: "%Y" }}** Australasian Computer Music Conference (ACMC)]({{ latest_conference.url }}), {{ latest_conference.theme }}, will take place on {{ latest_conference.dates }} at {{ latest_conference.location }}. See [this link]({{ latest_conference.url }}) for submission and attendance information.

## About ACMA

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
