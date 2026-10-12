# Databases

**Artifact:** Grazioso Salvare Rescue Dashboard  
**Course of origin:** CS 340 Client/Server Development  
**Enhancement category:** Databases  
**Author:** Jacob Hershberger

This page presents the original CS 340 Grazioso Salvare dashboard and the capstone enhancement. The original connects a Dash interface to a MongoDB collection of Austin Animal Center outcomes through a PyMongo CRUD module. The enhancement keeps the same user-facing filters, table, chart, and map, then moves the filter work into indexed aggregation pipelines and tightens credential and error handling in the data layer.

---

## Original

The original artifact is the Project Two dashboard from CS 340. Staff select a rescue type (Water Rescue, Mountain/Wilderness Rescue, Disaster/Individual Tracking, or Reset). The application queries the `aac.animals` collection, shows matching dogs in a searchable table, draws a breed pie chart, and places a marker on a map.

What it did well:

- Clear CRUD module (`animal_shelter.py`) with create, read, update, and delete
- Rescue-type filters that match the client’s breed, sex, and age criteria
- Interactive table, pie chart, and geolocation map driven by Dash callbacks
- Working end-to-end path from radio button to MongoDB query to visualization

What it did not do well:

- Filter queries used `find()` with no supporting indexes, so every filter scanned the collection
- All matching documents were pulled into Pandas before the table and chart were built
- Database credentials were hardcoded in the notebook and the CRUD module
- Error paths printed messages but did not distinguish connection failures from query failures
- No explicit data-model notes or index plan for a reviewer

**Original source:** [ProjectTwoDashboard.ipynb](ProjectTwoDashboard.ipynb)  
**CRUD module:** [animal_shelter.py](animal_shelter.py)

---

## Enhanced

The enhancement keeps the same four rescue-type filters and the same visual layout. The change is in how the database is used.

What changed:

- **Indexes.** Compound indexes were added on the fields the filters actually use (`animal_type`, `breed`, `sex_upon_outcome`, `age_upon_outcome_in_weeks`). The Water, Wilderness, and Disaster queries can now use an index instead of a collection scan.
- **Aggregation pipelines.** The filter logic moved from a `find()` followed by a full Pandas conversion into a MongoDB aggregation pipeline. The pipeline matches the rescue criteria, projects only the columns the table and chart need, and returns a smaller result set. Pandas is used only for the final chart and table binding.
- **Credential and error handling.** The CRUD module no longer falls back to hardcoded credentials when none are supplied. Connection and operation failures raise a clear exception the dashboard can catch, instead of only printing a message and returning an empty list.
- **Documentation.** A short data-model note lists the fields required by each rescue type and the indexes that support them.

The screens look the same on purpose. The database path underneath them is now explicit and bounded.

**Enhanced source:** [enhanced dashboard or CRUD module]  
**Indexes and pipeline notes:** [link or inline section]

### Query comparison

| Approach | Filter execution | Data moved to Python | Index use |
|----------|------------------|----------------------|-----------|
| Original `find()` | Collection scan | Full matching documents | None |
| Enhanced aggregation + indexes | Index-supported match | Projected fields only | Compound index on filter fields |

---

## Narrative

### What this artifact is

This artifact is the Grazioso Salvare Rescue Dashboard from CS 340. It was built so staff could filter Austin Animal Center outcome records by rescue type and see the results in a table, a breed chart, and a map. The original used a PyMongo CRUD module and Dash. The enhanced version keeps that interface and replaces the unindexed `find()` calls with aggregation pipelines backed by indexes, and removes the hardcoded credentials.

### Why it is in this portfolio

I selected this project because it is the clearest database product in my coursework. The original already demonstrated a working client-server path: a user action becomes a query, the query returns documents, and the documents drive a visualization. The limitation was that the database did most of the work only by accident. Every filter scanned the collection, every matching document traveled to Python, and the credentials lived in source files.

The enhancement makes the database choices visible. The indexes exist because the filter fields are known. The aggregation pipeline exists because the table and chart do not need every field. The credential change exists because a reviewer should not find a password in the notebook. Those are the components that show database skill beyond connecting a driver and calling `find()`.

### Reflection

The hard part was not writing the pipeline. The hard part was deciding what belonged in MongoDB and what still belonged in Pandas. Moving the match and the projection into the pipeline cut the data that crossed the network, but the pie chart and the map still needed a small in-memory table. I kept that boundary explicit so a reviewer can see the trade-off instead of guessing.

Milestone feedback on the earlier categories asked for clear rationale and explicit trade-offs. That shaped the query comparison table and the decision to keep the visual layout unchanged. I also learned that a working dashboard can still hide a collection scan. Adding the indexes and rewriting the filters as pipelines made the cost of each rescue type measurable.

### Course outcomes addressed here

This enhancement primarily supports the outcomes on designing and evaluating a computing solution and on using tools and techniques in computing practice. It also supports a security mindset through credential handling and professional communication through the data-model notes and query comparison. Collaborative decision-making is carried by the self-assessment and by the way the indexes and pipelines are documented for a reviewer.

---

## Outcomes

| Outcome | How this enhancement supports it |
| --- | --- |
| Collaborative environments for decision making | Index plan and pipeline notes are written so a teammate or reviewer can see which fields the filters depend on and why the indexes exist. |
| Professional communication | This page, the query comparison table, and the data-model notes are the written record of the database design. |
| Design and evaluate a computing solution | Replaces an unindexed collection scan with an index-supported aggregation pipeline and states the trade-off of moving only the needed fields to Python. |
| Techniques, skills, and tools | MongoDB indexes, aggregation pipelines, PyMongo, and Dash are used to keep the original product behavior while changing the data path. |
| Security mindset | Hardcoded credentials are removed from the default path. Connection and operation failures are raised instead of swallowed, so a bad credential or a downed server is visible. |

---

AI assistance was used to draft and edit the wording of this page. The artifact, the enhancement decisions, and the code are my own. Tool use is disclosed in line with the course AI guidelines.
