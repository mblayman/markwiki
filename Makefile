# Copyright (c) 2016, Matt Layman

.PHONY: docs

# Build the docs and hack the URLs so that they will refer to /MarkWiki path
# expected by pythonhosted.org.

# Sometimes docs get built while some doc files are still open. Clean out the
# swp files.
docs:
	rm -rf build/docs*
	markwiki -f build/docs
	find build/docs -name "*.swp" -print0 | xargs -0 rm -rf
	find build/docs -type f -exec sed -i "s|='/|='/MarkWiki/|g" {} \;
	find build/docs -type f -exec sed -i 's|="/|="/MarkWiki/|g' {} \;
	cd build/docs && zip -r ../docs.zip ./* && cd ../..
