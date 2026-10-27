# Two small jobs for the _contributions collection (the per-item proceedings).
Jekyll::Hooks.register :site, :post_read do |site|
  conferences = site.collections["conferences"].docs
  entries = site.collections["contributions"]&.docs || []

  # 1. Give each entry its conference's date, so jekyll-seo-tag and the feed
  # don't fall back to the build time (Jekyll's default for collection
  # documents without a date). Uses the conference's proceedings.published if
  # known, otherwise its start_date; scripts/check_contributions.py makes sure
  # one of them is set.
  entries.each do |doc|
    next if doc.data.key?("date") && doc.data["date"] != site.time
    conf = conferences.find { |c| c.data["year"] == doc.data["year"] }
    next unless conf
    published = conf.data.dig("proceedings", "published") || conf.data["start_date"]
    doc.data["date"] = Jekyll::Utils.parse_date(published.to_s) if published
  end

  # 2. Keep whole volumes, zips and multi-item PDFs (front matter, abstracts,
  # program notes) out of the sitemap: any PDF or zip under /proceedings/ that
  # isn't an entry's own `pdf`. Google Scholar can't index several papers in
  # one PDF, so we only point it at per-item PDFs and their pages.
  own_pdfs = entries.map { |doc| doc.data["pdf"] }.compact
  site.static_files.each do |file|
    next unless file.url.start_with?("/proceedings/") && %w(.pdf .zip).include?(file.extname)
    file.data["sitemap"] = false unless own_pdfs.include?(file.url)
  end
end
