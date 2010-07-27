mdpp=$(wildcard *.mdpp)
mkdn=$(patsubst %.mdpp,%.md,$(mdpp))
html=$(patsubst %.md,%.html,$(mkdn))

.PHONY: all
all: $(html)

.PHONY: clean
clean:
	-rm -f $(html) $(mkdn)

%.mkdn: %.mdpp
	markdown-pp $< > $@

%.html: %.mkdn
	markdown $< > $@

