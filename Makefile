# Copyright (c) 2013, Matt Layman

# Build the docs and hack the URLs so that they will refer to /MarkWiki path
# expected by pythonhosted.org.
docs:
	markwiki -f build/docs
	find build/docs -type f -exec sed -i "s|='/|='/MarkWiki/|g" {} \;
	find build/docs -type f -exec sed -i 's|="/|="/MarkWiki/|g' {} \;
