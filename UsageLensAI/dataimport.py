from db import execute_non_query


def create_tables():
    execute_non_query(
        """
        CREATE TABLE IF NOT EXISTS groups (
            group_id INTEGER PRIMARY KEY,
            group_name TEXT NOT NULL
        )
        """
    )

    execute_non_query(
        """
        CREATE TABLE IF NOT EXISTS projects (
            project_id INTEGER PRIMARY KEY,
            project_name TEXT NOT NULL
        )
        """
    )

    execute_non_query(
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            user_name TEXT NOT NULL,
            group_id INTEGER,
            license_type TEXT,
            status TEXT,
            FOREIGN KEY(group_id) REFERENCES groups(group_id)
        )
        """
    )

    execute_non_query(
        """
        CREATE TABLE IF NOT EXISTS contents (
            content_id INTEGER PRIMARY KEY,
            created_by INTEGER,
            project_id INTEGER,
            created_date TEXT,
            last_modified_date TEXT,
            view_count INTEGER,
            FOREIGN KEY(created_by) REFERENCES users(user_id),
            FOREIGN KEY(project_id) REFERENCES projects(project_id)
        )
        """
    )


def insert_sample_data():
    execute_non_query("DELETE FROM contents")
    execute_non_query("DELETE FROM users")
    execute_non_query("DELETE FROM groups")
    execute_non_query("DELETE FROM projects")

    groups = [
        (1, "Operations"),
        (2, "HR"),
        (3, "Finance"),
    ]

    projects = [
        (1, "Project Alpha"),
        (2, "Project Beta"),
    ]

    users = [
        (1, "John", 1, "Author", "Active"),
        (2, "Mary", 2, "Author", "Active"),
        (3, "David", 1, "Consumer", "Active"),
        (4, "Ravi", 3, "Author", "Inactive"),
        (5, "Priya", 2, "Author", "Active"),
    ]

    contents = [
        (1, 1, 1, "2026-06-01", "2026-08-01", 850),
        (2, 1, 1, "2026-06-15", "2026-08-04", 420),
        (3, 2, 2, "2026-05-01", "2026-05-20", 12),
        (4, 5, 2, "2026-07-01", "2026-07-02", 0),
    ]

    for group in groups:
        execute_non_query(
            "INSERT INTO groups VALUES (?, ?)",
            group,
        )

    for project in projects:
        execute_non_query(
            "INSERT INTO projects VALUES (?, ?)",
            project,
        )

    for user in users:
        execute_non_query(
            "INSERT INTO users VALUES (?, ?, ?, ?, ?)",
            user,
        )

    for content in contents:
        execute_non_query(
            "INSERT INTO contents VALUES (?, ?, ?, ?, ?, ?)",
            content,
        )


def main():
    create_tables()
    insert_sample_data()
    print("UsageLensAI database created successfully.")


if __name__ == "__main__":
    main()