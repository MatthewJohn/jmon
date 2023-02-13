# jmon

Simple JSON config-based website monitoring solution

## Getting started

```
docker-compose up -d

curl -XPOST localhost:5000/api/v1/check -H 'Content-Type: application/yml' -d '
name: Test1
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
      id: search2
      actions:
        - type: Pabalonium
        - press: enter
  - check:
      url: "https://www.w3schools.com/python/default.asp"

'
```