import requests

questions = [
    "How many patients do we have?",
    "List all doctors and their specializations",
    "Show appointments for last month",
    "Which doctor has the most appointments?",
    "What is the total revenue?",
    "Show revenue by doctor",
    "How many cancelled appointments last quarter?",
    "Top 5 patients by spending",
    "Average treatment cost by specialization",
    "Show monthly appointment count for the past 6 months",
    "Which city has the most patients?",
    "List patients who visited more than 3 times",
    "Show unpaid invoices",
    "What percentage of appointments are no-shows?",
    "Show the busiest day of the week",
    "Revenue trend by month",
    "Average appointment duration by doctor",
    "List patients with overdue invoices",
    "Compare revenue between departments",
    "Show patient registration trend by month"
]

for q in questions:
    response = requests.post(
        "http://127.0.0.1:8000/chat",
        json={"question": q}
    )
    
    print("\nQUESTION:", q)
    print("RESPONSE:", response.json())