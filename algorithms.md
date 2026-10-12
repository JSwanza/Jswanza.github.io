# Algorithms and Data Structures

**Artifact:** CartPole control (tabular Q-learning vs. enhanced)  
**Course of origin:** CS 370 Applied Artificial Intelligence  
**Enhancement category:** Algorithms and data structures  
**Author:** Jacob Hershberger

This page presents the original CS 370 CartPole Q-learning work and the capstone enhancement. The original uses a discretized state table and an unbounded history list. The enhancement replaces those with a circular replay buffer, continuous-state function approximation, and a lagged target network so the representation trade-off is explicit.

- [Code review (Milestone One)](https://youtu.be/F6IIgDRQelY)
- [Original artifact](#original)
- [Enhanced artifact](#enhanced)
- [Narrative](#narrative)
- [Course outcomes](#outcomes)

---

## Original

The original artifact is tabular Q-learning on CartPole from CS 370. Continuous cart position, cart velocity, pole angle, and pole angular velocity are cut into eight buckets per axis. The resulting tuple indexes a dictionary of action values. Experience is stored in an ordinary Python list that grows with every training step.

What it did well:
- Simple, inspectable Q-table
- Works on a coarse discrete grid

What it did not do well:
- Bin edges discard resolution
- The history list is unbounded (memory grows with episode count)
- No explicit complexity or capacity bound

**Original source:** [cartpole_tabular.py](q_learning_cartpole.py)

---

## Enhanced

The enhancement keeps the same simplified physics so the comparison is fair, then replaces the table and the list with three structures:

- **ReplayBuffer** — circular (ring) buffer. Push is O(1) and overwrites the oldest transition when full, so memory is bounded by capacity.
- **TinyQNet** — two-layer network that reads the raw continuous state (no binning).
- **Target network** — lagged copy of the policy network, updated on an interval so the TD target does not chase a moving value function.

Additional changes: minibatches, decaying epsilon, and inline complexity notes.

**Enhanced source:** [cartpole_enhanced.py](dqn_cartpole.py)

### Complexity comparison

| Structure              | Insert     | Sample / Lookup | Memory bound              |
|------------------------|------------|-----------------|---------------------------|
| Python list (original) | O(1) amort.| O(n)            | Unbounded                 |
| ReplayBuffer (ring)    | O(1)       | O(1)            | Fixed capacity            |
| Tabular Q dict         | O(1) avg   | O(1) avg        | Grows with visited bins   |
| TinyQNet               | —          | O(1) forward    | Fixed weights             |

Both scripts are stock Python 3 (no third-party packages). Run them with `python q_learning_cartpole.py` and `python dqn_cartpole.py`.

---

## Narrative

### What this artifact is

The artifact is a pair of CartPole control programs that began in CS 370 and were refined for this milestone. The original is tabular Q-learning on a discretized four-dimensional observation with an unbounded history list. The enhanced package keeps the same physics, then replaces the table and the list with a circular replay buffer, a small Q-network that reads raw observations, and a lagged target network.

### Why it is in this portfolio

CS 370 was the course where algorithms stopped being only sorting and trees and became a design choice with a memory cost. Tabular Q-learning is easy to defend on a small discrete grid. CartPole is not a small discrete grid. Bucketing throws away resolution at the bin edges, and an append-only list grows without a bound. Those are the trade-offs the outcome asks students to manage.

The ReplayBuffer makes the bound part of the type: push is O(1) and capacity is fixed. The Q-network removes the need to choose bin counts. The target network is the stability technique from Deep Q-learning (Mnih et al., 2015). Together they show function approximation, a concrete data structure, and an explicit representation trade-off.

### Reflection

A working demo is not the same thing as a portable argument. The original notebooks mixed environment, training loop, and commentary. Writing the ReplayBuffer class forced the split between “what the algorithm is” and “what the memory structure costs.” A Python list can store transitions; it cannot tell a reader that insert stays cheap only until memory runs out. A ring buffer makes the bound visible.

Function approximation is not automatically better. The network is intentionally tiny so the milestone stays on the data structure rather than on training speed. Both scripts are dependency-free so a reviewer can run them and inspect every line. Milestone Two feedback (clear rationale and explicit trade-offs) shaped the complexity table and the decision to stay dependency-free.

### Course outcomes addressed here

This enhancement primarily supports the outcome on designing and evaluating a computing solution with algorithmic principles while managing representation trade-offs. It also supports professional communication through the narrative, complexity table, and inline notes. Security and collaborative decision-making are only lightly touched and are carried by the other portfolio categories.

---

## Outcomes

| Outcome | How this enhancement supports it |
|---|---|
| Collaborative environments for decision making | Complexity table and comments are written for a reviewer who did not take CS 370. |
| Professional communication | This page, the side-by-side scripts, and the complexity table are the written record. |
| Design and evaluate a computing solution | Replaces an unbounded list and coarse bins with a bounded ring buffer and continuous-state approximation, and states the trade-off. |
| Techniques, skills, and tools | Stock Python, explicit ReplayBuffer, and a minimal Q-network used to implement the improved representation. |
| Security mindset | Not the focus of this category; input bounds and fixed capacity reduce one class of resource-growth risk. |

---

## References

Mnih, V., Kavukcuoglu, K., Silver, D., Rusu, A. A., Veness, J., Bellemare, M. G., Graves, A., Riedmiller, M., Fidjeland, A. K., Ostrovski, G., Petersen, S., Beattie, C., Sadik, A., Antonoglou, I., King, H., Kumaran, D., Wierstra, D., Legg, S., & Hassabis, D. (2015). Human-level control through deep reinforcement learning. *Nature, 518*(7540), 529–533. https://doi.org/10.1038/nature14236

Sutton, R. S., & Barto, A. G. (2018). *Reinforcement learning: An introduction* (2nd ed.). MIT Press.

AI assistance was used to draft and edit the wording of this page. The artifact, the enhancement decisions, and the code are my own. Tool use is disclosed in line with the course AI guidelines.
