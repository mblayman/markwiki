# Copyright (c) 2013, Matt Layman

# Build the docs and hack the URLs so that they will refer to /MarkWiki path
# expected by pythonhosted.org.

# Sometimes docs get built while some doc files are still open. Clean out the
# swp files.
docs:
	markwiki -f build/docs
	find build/docs -name "*.swp" -print0 | xargs -0 rm -rf
	find build/docs -type f -exec sed -i "s|='/|='/MarkWiki/|g" {} \;
	find build/docs -type f -exec sed -i 's|="/|="/MarkWiki/|g' {} \;
