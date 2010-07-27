mdpp=$(wildcard *.mdpp)
mkdn=$(patsubst %.mdpp,%.mkdn,$(mdpp))
html=$(patsubst %.mkdn,%.html,$(mkdn))

.PHONY: markdown
markdown: $(mkdn)

.PHONY: html
html: $(html)

.PHONY: clean
clean:
	-rm -f $(html) $(mkdn)

%.mkdn: %.mdpp
	markdown-pp $< > $@

%.html: %.mkdn
	markdown $< > $@

