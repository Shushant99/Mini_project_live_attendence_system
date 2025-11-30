import csv
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from attendance.models import AttendanceRecord

def export_csv(session):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="attendance_{session.id}.csv"'

    writer = csv.writer(response)
    writer.writerow(["Name", "Roll", "Time", "Confidence"])

    records = AttendanceRecord.objects.filter(session=session)

    for r in records:
        writer.writerow([r.student.name, r.student.roll_number, r.timestamp, r.confidence])
    return response


def export_pdf(session):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="attendance_{session.id}.pdf"'

    c = canvas.Canvas(response)
    c.drawString(100, 800, f"Attendance Report - {session.subject}")

    y = 750
    for r in AttendanceRecord.objects.filter(session=session):
        c.drawString(80, y, f"{r.student.name} - {r.timestamp}")
        y -= 20

    c.save()
    return response
