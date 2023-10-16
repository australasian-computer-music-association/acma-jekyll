---
title: "Meeting Minutes"
feature_image: /assets/images/acmc2019-vr.jpg
permalink: /minutes/
layout: page
---

This page contains links to minutes of ACMA meetings including Annual General Meetings. In general, the association's AGM is scheduled during each year's ACMC conference and is open to ACMA members.

{% for min in site.minutes reversed %}
- [{{min.title}}]({{ min.url | relative_url }}) 
{% endfor %}

