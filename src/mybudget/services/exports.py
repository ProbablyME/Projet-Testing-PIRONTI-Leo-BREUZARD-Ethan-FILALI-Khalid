import csv


def export_csv(transactions, file_path):
    with open(file_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "amount", "description", "date", "type", "category"])
        for t in transactions:
            writer.writerow([t.id, t.amount, t.description, t.date, t.type, t.category])
