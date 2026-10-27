---
title: "Creative Works at ACMC"
permalink: /proceedings/creative-works/
description: "Creative works selected for the Australasian Computer Music Conference: compositions, performances and installations, each with its own page and citation."
---

Creative works have been selected for ACMC concerts, listening rooms and
installations by peer review or by a jury. Each one below has its own page with
its program note, how it was presented and how to cite it. See also
[all proceedings]({{ '/proceedings/' | relative_url }}).

{% assign works = site.contributions | where: "type", "creative-work" | sort: "order" %}
{% assign by_year = works | group_by: "year" | sort: "name" | reverse %}
{%- for year in by_year %}
{%- assign conf = site.conferences | where: "year", year.items[0].year | first %}
<h2 id="acmc{{ year.name }}"><a href="{{ conf.url | relative_url }}">{{ conf.title }}</a></h2>
<ul class="contribution-list">
  {%- for item in year.items %}
  <li><a href="{{ item.url | relative_url }}">{{ item.title }}</a>{% if item.work.created %} [{{ item.work.created }}]{% endif %}
    <br><span class="meta">{{ item.authors | array_to_sentence_string: "and" }}{% if item.work.format %} · {{ item.work.format }}{% endif %}</span></li>
  {%- endfor %}
</ul>
{%- endfor %}
