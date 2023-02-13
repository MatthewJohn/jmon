# jmon

Simple JSON config-based website monitoring solution

## Getting started

```
docker-compose up -d

curl -XPOST localhost:5000/api/v1/check -H 'Content-Type: application/yml' -d '
name: Test1
steps:
  # Check homepage
  - goto: https://en.wikipedia.org/wiki/Main_Page
  - check:
      title: Wikipedia, the free encyclopedia
  # Perform search
  - find:
      id: searchform
      find:
        tag: input
        actions:
         - type: Pabalonium
         - press: enter
  - check:
      url: "https://en.wikipedia.org/w/index.php?search=Pabalonium&title=Special%3ASearch&ns0=1"
  - find:
      class: mw-search-nonefound
      check:
        - text: There were no results matching the query.

'
```