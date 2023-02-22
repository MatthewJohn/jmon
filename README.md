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

# Disable screenshots on error
screenshot_on_error: false


# Specify browser
# Options are:
#  * BROWSER_CHROME
#  * BROWSER_FIREFOX
#  * REQUESTS - for performing only json and response code checks
client: BROWSER_CHROME

# Check every 5 minutes
interval: 300

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

After submitting new checks, new checks are scheduled every 2 minutes.

Goto http://localhost:5000 to view dashboard

Goto http://localhost:5555 to view the celary tasks.

Goto http://localhost:9001 to view minio for s3 bucket, logging in with AWS credentials from .env


## Creating Notifications

Create a new python module in `jmon/plugins/notifications` with a class inheriting from `NotificationPlugin`, implementing one or more of the following methods:
 * `on_complete`
 * `on_first_success`
 * `on_every_success`
 * `on_first_failure`
 * `on_every_failure`

For an example, see the `jmon/plugins/notifications/example_notification.py` plugin and the `jmon/plugins/notifications/slack_example.py` plugins

