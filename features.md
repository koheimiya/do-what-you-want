### Requirements
It must be a tool that assists us to achieve our respective goals.
To do so, it offers the functionalities of
* Goal setting,
* Action planning,
* Progress monitoring.

### Details -- Project framework
* Five different project scope: self, family, friend, community, society.
* Macro planning: scope switching.
    * Timezone method: wake -> {self, society} -> comminuty -> {self, friend, family} -> sleep
* Micro planning: project switching within respective scopes.

### Details -- Timeline framework
* Goals
    * Goals are structured in hierarchical eight `Timelines`,
    namely, daily, weekly, monthly, quarterly, yearly, triennial, decennial and life-scale timelines.
    Each time line consists of goal nodes and the action plan.
    The action plan is a array of subtimelines with the children nodes of the goal nodes assigned to them.
    * `Nodes` represent (sub)goals one wish to achieve.
    The nodes may or may not have a parent on the upper timelines, but should have children on the lower timelines unless it is .
    * Each node has a few attributes for monitoring the progress, namely, the status (closed/done/ongoing/open), the children nodes, and a brief description.


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
