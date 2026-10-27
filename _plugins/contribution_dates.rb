# Gives each _contributions entry its conference's date, so jekyll-seo-tag and
# the feed don't fall back to the build time (Jekyll's default for collection
# documents without a date). Uses the conference's proceedings.published if
# known, otherwise its start_date. scripts/check_contributions.py makes sure
# one of them is set.
Jekyll::Hooks.register :site, :post_read do |site|
  conferences = site.collections["conferences"].docs
  site.collections["contributions"]&.docs&.each do |doc|
    next if doc.data.key?("date") && doc.data["date"] != site.time
    conf = conferences.find { |c| c.data["year"] == doc.data["year"] }
    next unless conf
    published = conf.data.dig("proceedings", "published") || conf.data["start_date"]
    doc.data["date"] = Jekyll::Utils.parse_date(published.to_s) if published
  end
end
