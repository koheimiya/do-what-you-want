# About This Repo
You may have many things you want to do, but unfortunately, too many that you easily lose the track.
Now, a simple framework will help you do what you want.

### Requirements
* It assists you to keep tracking your countless and interdependent goals/tasks.
* It does NOT deal with action planning, monitoring or anythings to do with actual ways of achieving goals. Leave it to any PDCA tools out there. 

### The Key Feature
* Structure your goals/tasks into a dependency graph

### Effect
* Stay focused on short-term goals while not losing track on long-term ones
* Easy to prioritize them
* Make them ready to assign your resources

### Subfeatures
* Saving/loading a directed acyclic graph (DAG) over goals/tasks
* Each node (goal/task) is allowed to have a label and a priority
* Easy to browse and edit

### Possible Implementation: Tagged Tree
* Media: text file with each line of `- [PRIORITY] LABEL #TAG1 #TAG2 ..`
    * PRIORITY is marked by numbers. Least priority is `[]`. If it is done, marked as `[X]`.
* Viewer:
    * Up/Down/Left/Right: Select a node.
    * Fold and unfold the sub tree.
    * Show and hide DONEs.
    * Edit the properties, including the label, priority, and tags.
