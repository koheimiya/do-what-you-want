### Requirements
It must be a tool that assists us to achieve our respective goals.
To do so, it offers the functionalities of
* Goal setting,
* Action planning,
* Progress monitoring.

### Details
* Goal setting and action planning are structured in hierarchical eight `timelines`,
namely, daily, weekly, monthly, quarterly, yearly, triennial, decennial and life-scale timelines.
Each time line is a line from past to present and then future with nodes on it.
`Nodes` represent goals, tasks, and actions to take.
The action nodes and task nodes have a parent on the parent timeline,
while the goal nodes and task nodes have partially ordered child nodes on the child timeline.
* Each timeline is segmented into past, present and future period.
At the moment of switching periods (e.g., at the end of days), we are prompted to reflect on the previous present period (i.e., summarize what we did and did not), revise the nodes on the upper timelines, and, based on the revision, arrange nodes on the next period and its lower timelines.
* Each node has a few attributes for monitoring the progress, namely, the state (closed/done/ongoing/open), the history of the children with accessible stats (e.g., the number of delays, the number of alternations), brief description, geographical info (action only), and dependency to other nodes.


### Objects
* Timeline
* Node


### Outer Functionalities
* (At switch) create/remove/write-description/set-geoinfo-of/set-dependency-of nodes
* Alter state
* See timeline/node/history-of-timeline


### Inner Functionalities
* Switch
* History management
