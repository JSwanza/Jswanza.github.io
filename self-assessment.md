# Professional Self-Assessment

**Jacob Hershberger**  
Southern New Hampshire University  
CS 499 Computer Science Capstone

This self-assessment introduces the work that follows and reflects on how the Computer Science program and the process of building this ePortfolio have shaped my skills, goals, and readiness for professional work.

## Strengths, Goals, and Preparation

Completing the Computer Science program while working full-time and raising a family has made the practical value of the coursework clear. The ePortfolio process sharpened that further. Selecting artifacts, reviewing them, and rewriting them forced me to decide which skills I can actually demonstrate rather than which courses I completed. Three areas stand out.

**Collaborating in a team environment.** Most of my program work was individual, but several courses required me to treat the code as something another person would have to read. In CS 320 the testing assignments pushed me to write checks that another developer could run without knowing my mental model. In CS 360 the Event Tracker began as a set of Activities that owned everything; the enhancement for this portfolio split that work so a teammate could change notification timing without touching the list screen. The code review video was the spoken version of the same idea: explain the design so someone else can follow it. I still prefer clear ownership and written notes over long meetings, but I now treat documentation and testable boundaries as part of the deliverable, not as an afterthought.

**Communicating with stakeholders.** The Grazioso Salvare dashboard in CS 340 was the clearest example. The client needed staff to filter dogs by rescue type without learning a query language. The radio buttons, table, chart, and map were the interface; the MongoDB queries were the implementation. Writing the README and later the database narrative forced me to explain which fields the filters depend on and why the indexes exist. In CS 330 the OpenGL work required me to show a scene rather than only describe it. Both experiences reinforced that a technical solution is only useful if the person who needs it can see what it does and trust the result.

**Data structures and algorithms.** CS 260 and CS 370 moved this from theory to a design choice with a cost. The CartPole work in this portfolio is the concrete case. The original tabular Q-learning used an unbounded Python list and coarse bins. The enhancement replaced the list with a circular replay buffer of fixed capacity and replaced the table with a small network that reads the raw continuous state. The complexity table on that page exists because the trade-off is the point: a list is simple until memory grows without a bound; a ring buffer makes the bound visible. The same habit appears in smaller places—choosing a dictionary versus a list, or deciding whether a query should run in the database or after the data has already been loaded.

**Software engineering and databases.** The Event Tracker enhancement and the Grazioso Salvare enhancement cover the two sides of this. On the software side I separated UI, validation, persistence, and scheduling, added input checks before a write, and hashed passwords instead of storing them in plain text. On the database side I added indexes on the filter fields, moved the rescue-type criteria into aggregation pipelines, and removed hardcoded credentials from the default path. Both changes keep the original user-facing behavior while making the internal structure reviewable. My earlier Oracle and SQL coursework still shapes how I think about data access; the MongoDB work added document modeling and aggregation to that foundation.

**Security.** None of the three artifacts is a security project, but each one contains a concrete mitigation that came from reviewing the original. The Event Tracker stopped storing plaintext passwords and stopped logging credentials in notification text. The Grazioso Salvare module no longer falls back to a hardcoded username and password, and it raises connection failures instead of returning an empty list. The CartPole buffer has a fixed capacity so an unbounded history list cannot grow without limit. These are small changes, but they are the difference between a working prototype and a design that anticipates misuse or failure. CS 405 and the secure-coding material in the program supplied the vocabulary; the enhancements made me apply it to code I had already written.

Outside the three artifacts, CS 330 gave me direct experience with transformations, lighting, and a camera in OpenGL—the area I want to keep developing for games and simulations. CS 370 added reinforcement-learning practice beyond the CartPole example used here. The testing work in CS 320 made me treat unit tests as part of the design rather than a final check. Together these courses, plus the daily use of dashboards and SQL in my current role, form the practical base the ePortfolio is meant to show.

My professional goal is to move from automotive technical work into a role that uses the graphics, software-engineering, and data skills I have built—game development, interactive simulation, or a software-engineering position that values clear design and measurable results. The ePortfolio is the first public record of that direction. It shows specific improvements I made to my own earlier work, the reasons for those improvements, and the limits I still acknowledge.

## How the Artifacts Fit Together

The three artifacts that follow are drawn from different courses and demonstrate different categories, but they share the same pattern: take a working project, identify a structural weakness, and replace it with a design that can be reviewed and extended.

- The **Software Design and Engineering** artifact is the CS 360 Android Event Tracker. The original stored accounts and events and fired reminders, but Activities owned layout, validation, database calls, and scheduling at the same time. The enhancement splits those responsibilities, adds validation before a write, hashes passwords, and covers the service layer with unit tests. It shows that a mobile prototype can be reorganized into something another developer can change without reverse-engineering the UI.

- The **Algorithms and Data Structures** artifact is the CS 370 CartPole controller. The original used tabular Q-learning on a discretized state and an unbounded history list. The enhancement replaces the list with a circular replay buffer of fixed capacity and replaces the table with a small network that reads continuous observations, plus a lagged target network. It shows a representation trade-off made explicit: memory is bounded, bin edges are removed, and the cost of each choice is stated.

- The **Databases** artifact is the CS 340 Grazioso Salvare dashboard. The original connected a Dash interface to a MongoDB collection and filtered dogs by rescue type. The enhancement adds indexes on the filter fields, moves the criteria into aggregation pipelines so the database returns only the needed fields, and removes hardcoded credentials. It shows that a working query path can still hide a collection scan, and that the fix is both an index and a clearer boundary between the database and the application.

Taken together, the three enhancements cover structure, representation cost, and data access. The code review video that opens the technical section explains the original weaknesses and the planned changes in spoken form. The narratives that accompany each artifact explain the same changes in writing and map them to the course outcomes. The self-assessment you are reading is the frame: it states the skills the artifacts are meant to evidence and the direction I intend to take them.

The pages that follow contain the original and enhanced work, the narratives, and the outcome tables. They are organized so a reviewer can move from this introduction to any single artifact, or from the code review to the specific change it described.

---

AI assistance was used to draft and edit the wording of this page. The reflection, the examples, and the claims about my work are my own. Tool use is disclosed in line with the course AI guidelines.
