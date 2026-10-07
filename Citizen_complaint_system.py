"""
Citizen Complaint System
========================
PROG211 - Object-Oriented Programming 1 | Limkokwing University, Sierra Leone

A small, open-source, privacy-respecting system that lets citizens report
public-service problems (water, roads, electricity, waste, health, education)
and lets officials track each complaint until it is resolved.

OOP concepts used (Lectures 1-3)
--------------------------------
* Classes, attributes, objects ........ Citizen, Complaint, ComplaintRegistry
* One data structure (dictionary) ..... complaints stored by complaint ID
* Instance methods .................... update_status(), display_info() ...
* Class methods (@classmethod) ........ total_complaints(), available_categories()
* Static methods (@staticmethod) ...... is_valid_description(), redact_sensitive()
* Tuple (optional bonus) .............. Complaint.STATUSES (immutable workflow)

Digital Public Goods (DPG) principles
-------------------------------------
* Open-source ......... plain Python, no third-party libraries, MIT licence
* Inclusive ........... simple text menu, plain-language messages, no login
* Privacy-respecting .. NO names, phone numbers or emails are stored; citizens
                        are identified only by an anonymous reference code and
                        a broad district; contact details typed into a
                        description are automatically redacted
* Modular & reusable .. each class has one job and can be reused/imported

Run:
    python complaint_system.py          -> interactive menu
    python complaint_system.py --demo   -> scripted demonstration
"""

import re
import sys
from datetime import date


# ---------------------------------------------------------------------------
# CLASS 1: Citizen  (anonymous - stores NO personal data)
# ---------------------------------------------------------------------------
class Citizen:
    """An anonymous citizen identified only by a reference code and district."""

    _citizen_count = 0  # class attribute shared by all Citizen objects

    def __init__(self, district):
        Citizen._citizen_count += 1
        self.citizen_ref = f"CIT-{Citizen._citizen_count:04d}"  # anonymous ID
        self.district = district.strip().title()
        self.complaints_filed = 0

    # ---- instance methods -------------------------------------------------
    def file_complaint(self, registry, category, description, priority="Normal"):
        """Create a Complaint for this citizen and store it in the registry.
        This is the interaction between Citizen, Complaint and Registry objects."""
        complaint = Complaint(self, category, description, priority)
        registry.add_complaint(complaint)
        self.complaints_filed += 1
        return complaint

    def display_info(self):
        print(f"  Citizen Ref : {self.citizen_ref}")
        print(f"  District    : {self.district}")
        print(f"  Filed       : {self.complaints_filed} complaint(s)")

    # ---- class method -----------------------------------------------------
    @classmethod
    def total_citizens(cls):
        """How many anonymous citizen profiles have been created."""
        return cls._citizen_count


# ---------------------------------------------------------------------------
# CLASS 2: Complaint
# ---------------------------------------------------------------------------
class Complaint:
    """A single public-service complaint and its progress."""

    # Tuple (optional bonus): the fixed, unchangeable workflow of a complaint.
    STATUSES = ("Received", "Under Review", "Resolved")

    # Dictionaries used as constant look-up tables.
    PRIORITIES = {"Low": 1, "Normal": 2, "Urgent": 3}
    CATEGORIES = {
        "water": "Ministry of Water Resources",
        "roads": "Sierra Leone Roads Authority",
        "electricity": "Electricity Distribution & Supply Authority",
        "waste": "City Council - Sanitation Unit",
        "health": "Ministry of Health",
        "education": "Ministry of Basic & Senior Secondary Education",
    }

    _complaint_count = 0

    def __init__(self, citizen, category, description, priority="Normal"):
        category = category.strip().lower()
        priority = priority.strip().title()

        if category not in Complaint.CATEGORIES:
            raise ValueError(f"Unknown category '{category}'. "
                             f"Choose from: {Complaint.available_categories()}")
        if priority not in Complaint.PRIORITIES:
            raise ValueError("Priority must be Low, Normal or Urgent.")
        if not Complaint.is_valid_description(description):
            raise ValueError("Description must be between 10 and 300 characters.")

        Complaint._complaint_count += 1
        self.complaint_id = f"CMP-{Complaint._complaint_count:04d}"
        self.citizen = citizen                     # object-to-object link
        self.category = category
        self.department = Complaint.CATEGORIES[category]
        self.description = Complaint.redact_sensitive(description.strip())
        self.priority = priority
        self.status = Complaint.STATUSES[0]        # "Received"
        self.date_filed = date.today().isoformat()

    # ---- instance methods -------------------------------------------------
    def update_status(self, new_status):
        """Move the complaint forward in its workflow (never backwards)."""
        new_status = new_status.strip().title()
        if new_status not in Complaint.STATUSES:
            raise ValueError(f"Status must be one of {Complaint.STATUSES}")
        if Complaint.STATUSES.index(new_status) <= Complaint.STATUSES.index(self.status):
            raise ValueError(f"Cannot move from '{self.status}' to '{new_status}'.")
        self.status = new_status

    def advance_status(self):
        """Move to the next stage automatically."""
        position = Complaint.STATUSES.index(self.status)
        if position == len(Complaint.STATUSES) - 1:
            raise ValueError("Complaint is already resolved.")
        self.status = Complaint.STATUSES[position + 1]

    def display_info(self):
        print(f"  [{self.complaint_id}] {self.category.title()} | "
              f"Priority: {self.priority} | Status: {self.status}")
        print(f"      Filed by   : {self.citizen.citizen_ref} "
              f"({self.citizen.district}) on {self.date_filed}")
        print(f"      Department : {self.department}")
        print(f"      Details    : {self.description}")

    # ---- class methods ----------------------------------------------------
    @classmethod
    def total_complaints(cls):
        """Total number of Complaint objects created so far."""
        return cls._complaint_count

    @classmethod
    def available_categories(cls):
        """Comma-separated list of valid categories (helps inclusive input)."""
        return ", ".join(cls.CATEGORIES)

    # ---- static methods ---------------------------------------------------
    @staticmethod
    def is_valid_description(text):
        """A description must be 10-300 characters long."""
        return 10 <= len(text.strip()) <= 300

    @staticmethod
    def redact_sensitive(text):
        """PRIVACY: remove emails and phone numbers typed into a description."""
        text = re.sub(r"[\w.+-]+@[\w-]+\.[\w.]+", "[email removed]", text)
        text = re.sub(r"\+?\d[\d\s-]{6,}\d", "[phone removed]", text)
        return text


# ---------------------------------------------------------------------------
# TASK 2 - Dictionary data structure + simple add / display functions
# ---------------------------------------------------------------------------
def add_record(store, complaint):
    """Add a complaint to the dictionary using its unique ID as the key."""
    store[complaint.complaint_id] = complaint


def display_records(store):
    """Loop through the dictionary and display every complaint."""
    if not store:
        print("  No complaints recorded yet.")
        return
    for complaint_id in store:
        store[complaint_id].display_info()
        print()


# ---------------------------------------------------------------------------
# CLASS 3: ComplaintRegistry  (wraps the dictionary)
# ---------------------------------------------------------------------------
class ComplaintRegistry:
    """Stores all complaints in ONE dictionary: {complaint_id: Complaint}."""

    def __init__(self):
        self.complaints = {}

    def add_complaint(self, complaint):
        add_record(self.complaints, complaint)

    def get_complaint(self, complaint_id):
        complaint_id = complaint_id.strip().upper()
        if complaint_id not in self.complaints:
            raise KeyError(f"No complaint with ID '{complaint_id}'.")
        return self.complaints[complaint_id]

    def display_all(self):
        display_records(self.complaints)

    def filter_by_status(self, status):
        """Return a new dictionary containing only complaints with that status."""
        return {cid: c for cid, c in self.complaints.items() if c.status == status}

    def summary(self):
        """Return a dictionary of counts per status, e.g. {'Received': 2, ...}."""
        counts = {status: 0 for status in Complaint.STATUSES}
        for complaint in self.complaints.values():
            counts[complaint.status] += 1
        return counts

    def display_summary(self):
        print(f"  Total complaints: {len(self.complaints)}")
        for status, count in self.summary().items():
            print(f"    {status:<13}: {count}")


# ---------------------------------------------------------------------------
# DEMO MODE (shows object creation and interaction between objects)
# ---------------------------------------------------------------------------
def run_demo():
    registry = ComplaintRegistry()

    print("=" * 62)
    print(" CITIZEN COMPLAINT SYSTEM - DEMONSTRATION")
    print("=" * 62)

    print("\n1) Creating anonymous citizens (no names or phone numbers)...")
    amara = Citizen("Western Area Urban")
    kadiatu = Citizen("Bo")
    amara.display_info()
    print()
    kadiatu.display_info()

    print("\n2) Citizens file complaints (Citizen -> Complaint -> Registry)...")
    amara.file_complaint(registry, "water",
                         "No running water in our street for two weeks.", "Urgent")
    amara.file_complaint(registry, "roads",
                         "Large pothole near the junction. Call me on 076 123 456.")
    kadiatu.file_complaint(registry, "education",
                           "School has no teachers for Mathematics.", "Low")
    print("  3 complaints filed successfully.")

    print("\n3) Displaying all complaints stored in the dictionary:\n")
    registry.display_all()

    print("4) Officials update complaint progress (instance methods)...")
    registry.get_complaint("CMP-0001").advance_status()
    registry.get_complaint("CMP-0002").update_status("Resolved")
    registry.get_complaint("CMP-0001").display_info()
    print()
    registry.get_complaint("CMP-0002").display_info()

    print("\n5) Error handling - trying to move a complaint backwards:")
    try:
        registry.get_complaint("CMP-0002").update_status("Received")
    except ValueError as error:
        print(f"  Error caught: {error}")

    print("\n6) Class methods and static methods:")
    print(f"  Complaint.total_complaints()      -> {Complaint.total_complaints()}")
    print(f"  Citizen.total_citizens()          -> {Citizen.total_citizens()}")
    print(f"  Complaint.available_categories()  -> {Complaint.available_categories()}")
    print(f"  Complaint.is_valid_description('Too short') -> "
          f"{Complaint.is_valid_description('Too short')}")

    print("\n7) Summary report:")
    registry.display_summary()
    print("\n" + "=" * 62)


# ---------------------------------------------------------------------------
# INTERACTIVE MENU
# ---------------------------------------------------------------------------
def run_menu():
    registry = ComplaintRegistry()
    menu = (
        "\n===== CITIZEN COMPLAINT SYSTEM =====\n"
        " 1. File a new complaint\n"
        " 2. View all complaints\n"
        " 3. Track a complaint by ID\n"
        " 4. Advance a complaint's status (official)\n"
        " 5. Summary report\n"
        " 0. Exit\n"
    )
    while True:
        print(menu)
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                district = input("Your district (no personal details): ")
                print(f"Categories: {Complaint.available_categories()}")
                category = input("Category: ")
                description = input("Describe the problem (10-300 characters): ")
                priority = input("Priority (Low/Normal/Urgent) [Normal]: ") or "Normal"
                citizen = Citizen(district)
                complaint = citizen.file_complaint(registry, category, description, priority)
                print(f"\nThank you. Your anonymous reference: {citizen.citizen_ref}")
                print(f"Keep your complaint ID to track progress: {complaint.complaint_id}")
            elif choice == "2":
                print()
                registry.display_all()
            elif choice == "3":
                registry.get_complaint(input("Complaint ID (e.g. CMP-0001): ")).display_info()
            elif choice == "4":
                complaint = registry.get_complaint(input("Complaint ID: "))
                complaint.advance_status()
                print(f"Status updated to: {complaint.status}")
            elif choice == "5":
                registry.display_summary()
            elif choice == "0":
                print("Goodbye.")
                break
            else:
                print("Please choose a number from the menu.")
        except (ValueError, KeyError) as error:
            print(f"Sorry: {error}")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        run_demo()
    else:
        run_menu()