# Citizen Complaint System

## The Problem
Citizens often struggle to report broken public services (no water, damaged roads, power cuts,
uncollected waste, school and clinic problems) and then never learn what happened to their report.
This program lets a citizen file a complaint **anonymously**, get a complaint ID, and lets officials
move the complaint through a clear workflow: **Received → Under Review → Resolved**.

## Requirements
* Python 3.8 or newer
* No third-party libraries (standard library only: `re`, `sys`, `datetime`)

## How to Run
```bash
git clone https://github.com/<your-username>/citizen-complaint-system.git
cd citizen-complaint-system
python complaint_system.py --demo     # scripted demonstration
python complaint_system.py            # interactive menu
```

## Project Structure
| File | Purpose |
|------|---------|
| `complaint_system.py` | Python source code (all classes, functions, demo, menu) |
| `sample_output.txt` | Output of `python complaint_system.py --demo` |
| `README.md` | Documentation and DPG alignment |
| `LICENSE` | MIT open-source licence |

## OOP Design

### Task 1 – Classes, attributes and objects
| Class | Attributes | Key methods |
|-------|-----------|-------------|
| `Citizen` | `citizen_ref`, `district`, `complaints_filed` | `file_complaint()`, `display_info()` |
| `Complaint` | `complaint_id`, `citizen`, `category`, `department`, `description`, `priority`, `status`, `date_filed` | `update_status()`, `advance_status()`, `display_info()` |
| `ComplaintRegistry` | `complaints` (dictionary) | `add_complaint()`, `get_complaint()`, `display_all()`, `filter_by_status()`, `summary()` |

**Interaction between objects:** a `Citizen` object calls `file_complaint()`, which creates a
`Complaint` object (linked back to the citizen) and stores it in the `ComplaintRegistry`.

### Task 2 – Data structure (one data structure: dictionary)
All complaints are stored in a **dictionary** with the unique complaint ID as the key:
`{"CMP-0001": <Complaint>, "CMP-0002": <Complaint>, ...}`.
The functions `add_record(store, complaint)` and `display_records(store)` add records to and display
records from the dictionary.
*Bonus:* an immutable **tuple** `Complaint.STATUSES = ("Received", "Under Review", "Resolved")`
defines the fixed complaint workflow.

### Task 3 – Methods
| Type | Methods |
|------|---------|
| Instance methods | `Citizen.file_complaint()`, `Citizen.display_info()`, `Complaint.update_status()`, `Complaint.advance_status()`, `Complaint.display_info()` |
| Class methods (`@classmethod`) | `Citizen.total_citizens()`, `Complaint.total_complaints()`, `Complaint.available_categories()` |
| Static methods (`@staticmethod`) | `Complaint.is_valid_description()`, `Complaint.redact_sensitive()` |

## Digital Public Goods (DPG) Alignment
| DPG principle | How this solution meets it |
|---------------|----------------------------|
| **Open-source** | Published on GitHub under the MIT licence; uses only the Python standard library so anyone can run, study, copy and improve it at no cost. |
| **Inclusive and accessible design** | Simple numbered text menu; plain-language messages and error messages; no login, account or internet needed; the list of valid categories is shown to the user; the system works on low-spec computers. |
| **Privacy-respecting** | No name, phone number, email, address or national ID is ever stored. Citizens get only an anonymous reference (`CIT-0001`) and a broad district. Emails and phone numbers typed into a description are automatically removed by `redact_sensitive()`. |
| **Modular and reusable** | Each class has one responsibility (`Citizen`, `Complaint`, `ComplaintRegistry`). The classes can be imported into other programs (e.g. a web or mobile front end) without changing them. Categories and departments are kept in one dictionary that is easy to adapt to other countries. |

## Example Usage

### Sample input (interactive menu)
```
Choose an option: 1
Your district (no personal details): Freetown
Categories: water, roads, electricity, waste, health, education
Category: water
Describe the problem (10-300 characters): Tap is dry since Monday, email me a@b.com
Priority (Low/Normal/Urgent) [Normal]: Urgent
```

### Sample output
```
Thank you. Your anonymous reference: CIT-0001
Keep your complaint ID to track progress: CMP-0001
```
Tracking it later (option 3, `CMP-0001`):
```
  [CMP-0001] Water | Priority: Urgent | Status: Received
      Filed by   : CIT-0001 (Freetown) on 2026-10-03
      Department : Ministry of Water Resources
      Details    : Tap is dry since Monday, email me [email removed]
```
The full scripted run is in [`sample_output.txt`](sample_output.txt).

## Possible Future Improvements
Save complaints to a JSON file, add a web interface, add an official login for status updates,
and translate the menu into Krio, Mende and Temne.

## Licence
MIT – see `LICENSE`.
