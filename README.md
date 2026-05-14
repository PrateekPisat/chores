# Chores Application

Yes, this is a glorified to-do list. My roommates and I had a piece of paper stuck to the fridge, with the chores each of us had to perform each week. One day, we ran out of room and all of us were too lazy to replace it with another piece. So, I spent months building an app instead of replacing that piece of paper, which would have taken minutes.

<div style="text-align: center;">
  <img src="https://imgs.xkcd.com/comics/automation.png" alt="Centered image" style="display: block; margin: 0 auto;">
</div>

The gist is that you (and your roommates) are assigned tasks each week, and you can mark those tasks as completed(ideally when you actually do the work).

---

## Model Hierarchy (Backend SQLAlchemy Models)

- **House**: Represents a household. Each house can have multiple users as members (via the `HouseMember` association table) and can have multiple chores assigned to it.
- **User**: Represents a person using the app. Users can belong to multiple houses (again via `HouseMember`) and can be assigned chores through chore distributions.
- **HouseMember**: Association table that links users and houses, enabling a many-to-many relationship between them. Each entry represents a user being a member of a specific house.
- **Chore**: Represents a chore or task that belongs to a house. Each chore can be distributed to users for completion, and is associated with a single house.
- **ChoreDistribution**: Represents the assignment of a specific chore to a user, enabling tracking of which user is responsible for which chore instance.
