import csv
from os.path import dirname, join

FIELDNAMES = ["id", "title", "message", "view_count"]


def count_all_entries():
    with open(
        join(dirname(__file__), "database.csv"),
        mode="r",
        newline="\n",
    ) as file:
        reader = csv.DictReader(file, fieldnames=FIELDNAMES)
        return len(list(reader))


def get_paged_entries(page=1, limit=4):
    start_at = (page - 1) * limit
    end_at = start_at + limit
    output = []

    with open(
        join(dirname(__file__), "database.csv"),
        mode="r",
        newline="\n",
    ) as file:
        reader = csv.DictReader(file, fieldnames=FIELDNAMES)
        for row in list(reader)[1:]:
            output.append(row)

    return output[start_at:end_at]


def get_entry(id):
    with open(
        join(dirname(__file__), "database.csv"),
        mode="r+",
        newline="\n",
    ) as file:
        reader = csv.DictReader(file, fieldnames=FIELDNAMES)
        entries = list(reader)[1:]

        for row in entries:
            if int(row.get("id")) == int(id):
                update_entry(id=int(id), entries=entries)
                return row


def update_entry(id, entries):
    with open(
        join(dirname(__file__), "database.csv"),
        mode="w+",
        newline="\n",
    ) as file:
        output = []

        for entry in entries:

            if int(entry.get("id", 0)) == id:
                entry["view_count"] = int(entry.get("view_count", 0)) + 1

            output.append(entry)

        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()

        for entry in output:
            writer.writerow(entry)


def add_entry(title, message):
    with open(
        join(dirname(__file__), "database.csv"),
        mode="a+",
        newline="\n",
    ) as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        # writer.writeheader()

        writer.writerow(
            {
                "id": count_all_entries(),
                "title": title,
                "message": message,
                "view_count": 0,
            }
        )

        return count_all_entries()
