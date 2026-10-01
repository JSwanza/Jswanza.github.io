[event-tracker-software-engineering.md](https://github.com/user-attachments/files/32913576/event-tracker-software-engineering.md)
# Software Design and Engineering

**Artifact:** Android Event Tracker  
**Course of origin:** CS 360, Mobile Architecture and Programming  
**Enhancement category:** Software design and engineering  
**Author:** Jacob Hershberger

This page presents the original CS 360 Event Tracker and the capstone enhancement. The original shows a working mobile prototype. The enhancement shows the same product rebuilt around clearer structure, safer data handling, and a design that another developer can extend.

Use the links below to move between the review, the original work, the enhanced work, and this narrative. Downloadable source is linked from each section so nothing on this page has to be opened as a raw file list.

- [Code review (Milestone One)](../code-review/)
- [Original artifact](#original)
- [Enhanced artifact](#enhanced)
- [Narrative](#narrative)
- [Course outcomes](#outcomes)

---

## Original

The original artifact is the Project Three Event Tracking application from CS 360. It was built in Android Studio for Android. A signed-in user can create an account, add events, edit or delete them, and receive a reminder when an event is due.

The original already did the job it was assigned to do:

- Account create and sign-in, stored locally
- Event list rendered in a RecyclerView
- Add, update, and delete for events
- Date and time selection for a reminder
- AlarmManager notification when an event fires
- SQLite storage for users and events

What it did not do well was separate those jobs. Activity classes owned layout, validation, database calls, and notification scheduling at the same time. Comments explained what a line did more often than why a choice was made. Input checks were thin. Tests were manual.

**Original source:** [link to original project or release tag]  
**Original screens:** place two or three screenshots here (sign-in, event list, add event).

---

## Enhanced

The enhancement keeps the same user-facing behavior and rebuilds the path underneath it. The goal was not a new app. The goal was a design another person could review, test, and change without first reverse-engineering the Activities.

What changed:

- **Structure.** UI, validation, persistence, and notification scheduling are split. Activities and the list adapter bind data and forward actions. A small event service owns create, update, and delete. A database helper owns SQL. A scheduler owns AlarmManager.
- **Data rules.** Event title, date, and time are checked before a row is written. Empty titles and past reminder times are rejected with a message on the form, not a crash later.
- **Security.** Passwords are no longer stored in plain text. New accounts store a salted hash. The database is not exposed to other apps. Notification text uses the event title only and does not log credentials.
- **Documentation.** Class-level comments state responsibility. Public methods state inputs, failure cases, and side effects. A short README maps packages to features.
- **Testing.** Validation and the event service are covered by local unit tests for empty input, duplicate handling, and a successful create. UI flows remain manual, and that limit is stated in the README.

The screens look familiar on purpose. The design change is in the boundaries between components.

**Enhanced source:** [link to enhanced project or release tag]  
**Enhanced screens:** place the matching screenshots beside the original set.  
**Tests:** link the unit-test class or a short test report.

---

## Narrative

### What this artifact is

This artifact is the Android Event Tracker from CS 360, created as the Project Three mobile prototype, then enhanced in CS 499 for software design and engineering. The original stores accounts and events on the device, lists events, and fires a reminder. The enhanced version keeps that behavior and reorganizes the code so each part has one job.

### Why it is in this portfolio

I selected this project because it is the clearest mobile product in my coursework, and because the original was a good prototype with a weak design. Shipping the feature set was the CS 360 goal. Making the design reviewable is the capstone goal.

The original showcases applied mobile work: activities, RecyclerView, SQLite, and AlarmManager. The enhancement showcases the engineering layer around that work. A reviewer can open the event service without reading layout code, can see where a bad date is rejected, and can run the unit tests without a device. Those are the components that demonstrate software development skill beyond completing an assignment.

The enhancement improved the artifact in four ways. Responsibilities are separated, so a change to notification timing does not require editing the list screen. Validation fails closed. Credentials are hashed. The README and comments record the design instead of leaving it implied.

Skills demonstrated in the enhancement:

- Decomposition of a working Android app into UI, domain, and data layers
- Input validation at the boundary before persistence
- Local credential storage with a salted hash rather than plaintext
- Unit tests on the logic that does not need the Android UI framework
- Written design notes a teammate or reviewer can follow

### Reflection

The hard part was not adding a feature. The hard part was moving logic out of the Activities without breaking the reminder path. AlarmManager and the activity result flow were the two places I broke first. I fixed them by keeping scheduling behind one class and treating the activity as a caller, not as the owner of the alarm.

Milestone One feedback called out structure, thin documentation, and missing checks around user input and stored credentials. Those notes set the enhancement scope. I did not add a new screen. I split the existing flow, documented each new class, hashed passwords, and added tests on the validation and service layer. That is the feedback incorporated here.

I learned that a prototype can be correct and still be hard to trust. The original passed a manual walkthrough. The enhanced version can explain itself. I also learned the limit of this pass: UI tests are still manual, and the database is still a local SQLite file rather than a shared backend. Those gaps belong to later categories in this portfolio, not to a claim that this enhancement finished every outcome.

### Course outcomes addressed here

This enhancement fully supports communication and software design, and it supports security and tool use in part. Algorithmic efficiency and collaborative decision-making are only touched. They are carried more directly by the other portfolio categories and by the self-assessment.

---

## Outcomes

| Outcome | How this enhancement supports it |
|---|---|
| Collaborative environments for decision making | The README and class comments are written for a reviewer or teammate, not only for the author. The code review video is the spoken version of the same design discussion. |
| Professional communication | This page, the before-and-after screenshots, and the linked source are the written and visual record. The code review is the oral record. |
| Design and evaluate a computing solution | The enhancement evaluates the original Activities-do-everything design and replaces it with explicit boundaries, validation, and tests, with the trade-off that UI tests remain manual. |
| Techniques, skills, and tools | Android Studio, SQLite, AlarmManager, and local unit tests are used to implement a design that keeps the original product behavior. |
| Security mindset | Plaintext passwords, weak input checks, and logging risk were the flaws called out in review. Hashing, validation before write, and a private database are the mitigations in this pass. |

---

## Files on this page

- Original project archive or tag
- Enhanced project archive or tag
- Screenshot set: sign-in, list, add event, for both versions
- Unit test class or test output
- Link to the Milestone One code review video

AI assistance was used to draft and edit the wording of this page. The artifact, the enhancement decisions, and the code are my own. Tool use is disclosed in line with the course AI guidelines.
