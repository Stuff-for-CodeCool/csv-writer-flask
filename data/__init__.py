import csv

FIELDNAMES = ["id", "title", "message", "view_count"]


def read_all_entries():
    output = []
    with open("data/database.csv", mode="r") as file:
        reader = csv.DictReader(file, fieldnames=FIELDNAMES)
        for row in reader:
            output.append(row)
    return output[1:]


def read_entry(id):
    entries = read_all_entries()
    output = []
    for entry in entries:
        if int(entry["id"]) == id:
            entry["view_count"] = int(entry["view_count"]) + 1
            output = entry

    with open("data/database.csv", mode="w", newline="\n") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()

        for index, entry in enumerate(entries):
            writer.writerow(
                {
                    "id": index,
                    "title": entry["title"],
                    "message": entry["message"],
                    "view_count": entry["view_count"],
                }
            )

    return output


def insert_entry(title, message):

    try:
        count = len(read_all_entries())

        with open("data/database.csv", mode="a", newline="\n") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)

            writer.writerow(
                {
                    "id": count,
                    "title": title,
                    "message": message,
                    "view_count": 1,
                }
            )
        return True

    except:
        return False
