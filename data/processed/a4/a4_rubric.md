# A4 rating rubric: environmental structure of a work task

You are scoring WORK ENVIRONMENTS, not difficulty, skill, pay, or how impressive the job is.

For each item you are given an occupation title and one task that occupation performs.
Score the environment in which THAT TASK is carried out on four dimensions, each 1 to 5.

1. ENVIRONMENT PREDICTABILITY
   5 = the physical setting is fixed and known in advance and barely changes between
       repetitions (a fixed workstation, a production line, a controlled indoor room)
   1 = the setting changes every time and cannot be known in advance (a different customer
       home each visit, open terrain, a disaster site, a moving crowd)

2. OBJECT VARIABILITY
   5 = the task acts on identical, standardised objects presented the same way each time
   1 = the objects vary in shape, size, weight, position or condition every time, or are
       living, deformable, or unique

3. WORKSPACE ACCESS
   5 = the work area is open, uncluttered and easy for a machine on a fixed base or simple
       wheeled platform to reach
   1 = the work area is confined, cluttered, elevated, underground, requires climbing,
       crawling, or moving through human-scale spaces built only for people

4. NEED FOR IMPROVISATION
   5 = the task follows a fixed procedure with no judgement about how to proceed physically
   1 = the worker constantly improvises the physical approach in response to what is found

Score honestly and independently per dimension. Do NOT try to produce an overall
automation score, and do NOT let the prestige or wage of the occupation influence you. A
highly paid surgeon and a low paid home health aide can both sit in unpredictable settings;
a machine operator and a data entry clerk can both sit in predictable ones.

Output STRICT JSON, a single array, one object per item, nothing else:

[{"item_id":"T001","predictability":3,"object_variability":2,"workspace_access":4,"improvisation":2}]

Every item in the input must appear exactly once in your output.
