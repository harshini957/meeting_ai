import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import pandas as pd


def generate_pdf(action_data: dict, meeting_id: str) -> str:
    os.makedirs("data/reports/pdf", exist_ok=True)
    path = f"data/reports/pdf/meeting_{meeting_id}.pdf"

    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4

    y = height - 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Meeting Action Items")
    y -= 30

    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Meeting ID: {meeting_id}")
    y -= 30

    for idx, item in enumerate(action_data.get("action_items", []), start=1):
        if y < 100:
            c.showPage()
            c.setFont("Helvetica", 10)
            y = height - 50

        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, f"{idx}. Task:")
        c.setFont("Helvetica", 10)
        c.drawString(100, y, item.get("task", ""))
        y -= 15

        c.drawString(70, y, f"Owner: {item.get('owner', '')}")
        y -= 15

        c.drawString(70, y, f"Assigned By: {item.get('assigned_by', '')}")
        y -= 15

        c.drawString(70, y, f"Due Date: {item.get('due_date', '')}")
        y -= 15

        c.drawString(70, y, f"Source: {item.get('source_sentence', '')}")
        y -= 30

    c.save()
    return path


def generate_excel(action_data: dict, meeting_id: str) -> str:
    os.makedirs("data/reports/excel", exist_ok=True)
    path = f"data/reports/excel/meeting_{meeting_id}.xlsx"

    df = pd.DataFrame(action_data.get("action_items", []))
    df.to_excel(path, index=False)

    return path
