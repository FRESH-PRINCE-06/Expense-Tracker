import csv
import os
from datetime import datetime

# ---------- Settings (constants) ----------
FILE_NAME = "expenses.csv"
FIELDS = ["id", "date", "category", "amount", "note"]


# ---------- Storage: load and save ----------
def load_expenses():
    """Read expenses.csv into a list of dictionaries."""
    expenses = []
    if not os.path.exists(FILE_NAME):   # first run: no file yet
        return expenses
    with open(FILE_NAME, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])          # CSV gives text, convert to numbers
            row["amount"] = float(row["amount"])
            expenses.append(row)
    return expenses


def save_expenses(expenses):
    """Write the whole list back to expenses.csv."""
    with open(FILE_NAME, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(expenses)


# ---------- Feature 1: add ----------
def add_expense(expenses):
    category = input("Category (Food, Transport, Bills...): ").strip().title()
    if category == "":
        print("Category cannot be empty.")
        return
    note = input("Note (optional): ").strip()

    try:
        amount = float(input("Amount: "))
    except ValueError:                  # user typed letters
        print("Please enter a valid number.")
        return
    if amount <= 0:                     # negative or zero
        print("Amount must be greater than zero.")
        return

    # new id = biggest existing id + 1 (default=0 handles an empty list)
    new_id = max([e["id"] for e in expenses], default=0) + 1

    expense = {
        "id": new_id,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "category": category,
        "amount": amount,
        "note": note,
    }
    expenses.append(expense)
    save_expenses(expenses)
    print("Expense added!")


# ---------- Feature 2: view ----------
def view_expenses(expenses):
    if not expenses:
        print("No expenses yet.")
        return
    print(f"\n{'ID':<5}{'Date':<12}{'Category':<14}{'Amount':<10}Note")
    print("-" * 55)
    for e in expenses:
        print(f"{e['id']:<5}{e['date']:<12}{e['category']:<14}{e['amount']:<10.2f}{e['note']}")


# ---------- Feature 3: delete ----------
def delete_expense(expenses):
    if not expenses:
        print("Nothing to delete.")
        return
    view_expenses(expenses)
    try:
        target = int(input("\nEnter ID to delete: "))
    except ValueError:
        print("Invalid ID. Enter a whole number.")
        return

    for e in expenses:
        if e["id"] == target:
            expenses.remove(e)
            save_expenses(expenses)
            print("Deleted.")
            return
    print("ID not found.")


# ---------- Feature 4: monthly summary ----------
def monthly_summary(expenses):
    month = input("Month (YYYY-MM, e.g. 2026-11): ").strip()
    total = 0
    by_category = {}

    for e in expenses:
        if e["date"].startswith(month):
            total += e["amount"]
            cat = e["category"]
            by_category[cat] = by_category.get(cat, 0) + e["amount"]

    if total == 0:
        print("No expenses for that month.")
        return

    print(f"\nSummary for {month}")
    print("-" * 35)
    for cat, amt in by_category.items():
        print(f"{cat:<15}{amt:>10.2f}  ({amt / total * 100:.1f}%)")
    print("-" * 35)
    print(f"{'TOTAL':<15}{total:>10.2f}")


# ---------- Menu ----------
def main():
    expenses = load_expenses()
    while True:
        print("\n=== EXPENSE TRACKER ===")
        print("1. Add expense")
        print("2. View expenses")
        print("3. Delete expense")
        print("4. Monthly summary")
        print("5. Quit")
        choice = input("Choose (1-5): ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            delete_expense(expenses)
        elif choice == "4":
            monthly_summary(expenses)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()