# jmon

Simple JSON config-based website monitoring solution

This project is currently in early development.

It can currently:
 * Register checks
 * Perform checks across agents
 * Checks can:
   * Goto URL
   * Check title/url/element text
   * Click on elements, send text and press enter
   * Find elements by ID/class/tag/placeholder/text

For a list of upcoming features and issues being worked on, please see https://gitlab.dockstudios.co.uk/mjc/jmon/-/issues

## Getting started

```
# Startup
docker-compose up -d

# Create s3 bucket in minio
docker-compose exec minio mc mb jmon-results

# Add check for W3Schools
curl -XPOST localhost:5000/api/v1/checks -H 'Content-Type: application/yml' -d '
name: Check_W3Schools
steps:
  # Goto Homepage
  - goto: https://www.w3schools.com/default.asp
  - check:
      title: W3Schools Online Web Tutorials
  # Accept cookies
  - find:
      id: accept-choices
      actions:
       - click

  # Use search to find python
  - find:
      placeholder: "Search our tutorials, e.g. HTML"
      actions:
        - type: Python
        - press: enter
  - check:
      url: "https://www.w3schools.com/python/default.asp"
'

# Add check for Wikipedia
curl -XPOST localhost:5000/api/v1/checks -H 'Content-Type: application/yml' -d '
name: Check_Wikipedia
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
      url: "https://en.wikipedia.org/w/index.php?fulltext=Search&search=Pabalonium&title=Special%3ASearch&ns0=1"
  - find:
      class: mw-search-nonefound
      check:
        text: There were no results matching the query.
  - actions:
    - screenshot: Homepage
'
```

Goto http://localhost:5555 to view the celary tasks.


