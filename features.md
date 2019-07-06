### Requirements
It must be a tool that assists us to achieve our respective goals.
To do so, it offers the functionalities of
* Goal setting,
* Action planning,
* Progress monitoring.

### Details
* Goals
    * Goals are structured in hierarchical eight `Timelines`,
    namely, daily, weekly, monthly, quarterly, yearly, triennial, decennial and life-scale timelines.
    Each time line is a line from past to present and then future with nodes on it.
    * `Nodes` represent goals one wish to achieve.
    The nodes may or may not have a parent on the upper timeline and children on the lower timeline.
    * Each timeline is segmented into past, present and future period.
    At the moment of switching periods (e.g., at the end of days), we are prompted to reflect on the previous period (i.e., summarize what we did and did not) and arrange nodes on the next period.
    * Each node has a few attributes for monitoring the progress, namely, the status (closed/done/ongoing/open), the children nodes, a brief description and the timestamp.
* Actions

### Future work
* Geographical concerns
* Dependency among goals


### Objects
* Node
    * `name`
    * `status`
    * `children`: List of children global ids.
    * `description`
    * `timestamp`
    * `make_new_goals()`
* Timeline:
    * `nodelist`: List of nodes. Indices are local ids.
    * `periodlist`: Dictionary of list of node local ids.
* GoalBoard: List of timelines.

### Outer Functionalities
* Create/remove node
* Set name/child/description
* Alter status
* Browse timeline/node/history
* Import calendars

### Inner Functionalities
* Switch
* 
