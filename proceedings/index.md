---
title: "ACMC Proceedings"
permalink: /proceedings/
description: "Proceedings of the Australasian Computer Music Conference since 1993: papers, abstracts and creative works, each with its own page."
---

The Australasian Computer Music Conference has published its proceedings since
the 1990s. Each paper, abstract and creative work listed here has its own page
with a citation, and a PDF where one was printed. We are still adding earlier
years one by one; where a year shows no entries yet, its conference page links
the complete volume.

- [All creative works]({{ '/proceedings/creative-works/' | relative_url }})
- [All conferences]({% link conferences.md %})

| Conference | Papers and abstracts | Creative works | Complete volume |
|---|---|---|---|
{%- assign confs = site.conferences | sort: "date" | reverse %}
{%- for conf in confs %}
{%- assign items = site.contributions | where: "year", conf.year %}
{%- assign works = items | where: "type", "creative-work" %}
| [{{ conf.title }}]({{ conf.url | relative_url }}) | {% if conf.year %}{{ items.size | minus: works.size }}{% endif %} | {% if conf.year %}{{ works.size }}{% endif %} | {% if conf.proceedings.full_volume %}[download]({{ conf.proceedings.full_volume | relative_url }}){% endif %} |
{%- endfor %}
