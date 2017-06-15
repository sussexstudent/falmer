# Falmer
*Experimental Django-powered API for services & content*

Currently the union is not in control of backend, leading some areas of poor UX, reliance of the CMS provider adding features 'one-day' or at cost. We've been able to improve services via 'serverless' helpers via AWS Lambda, but lack of persistent is limiting.

Falmer houses experimental service API's to explore what can be achieved with more control.

An main rule of the services that Falmer provides while still existing as an experiment is the idea that if required services can be wound down with minimal refactoring.


## Ideas & Areas for exploration

- **Storing structured data to be used on specific website pages** where the current solution is a pain point; *think staff contact page*
- **Management of feature flags, time sensitive changes, global changes without bundle changes**; *think homepage hero management, enabling/disabling site wide modals*
- **Forms and process** for students accessing services; *think creating a society*
- **Housing auxiliary information** where current systems are inflexible; *think committee members tagging their own societies*
- **Image management**; *think tagging, collections, usage information, image server integration*
- **Search API migration**; *currently the search API is a lambda handler parsing the CMS results - this would allow result curation such as pinning and filtering*
- **Slack automation**; *auth via, report issues, log usage*
