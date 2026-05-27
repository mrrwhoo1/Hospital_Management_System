"""
receipt_generator.py
====================
Generates a professional hospital payment receipt / bill as a PDF.
Uses only reportlab (no fpdf dependency needed).

Usage (standalone):
    from receipt_generator.py import generate_receipt
    path = generate_receipt(payment_data)   # returns path to saved PDF

payment_data dict keys:
    pay_id, patient_name, patient_id, age, contact, email, address,
    symptoms, amount, method, status, notes, date,
    hospital_name, doctor_name, department
All keys are optional except pay_id and patient_name — safe defaults are used.
"""

"""
receipt_generator.py  (v2 — improved spacing)
"""

import os
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)

# ── Brand colours ────────────────────────────────────────────────────────────
TEAL        = colors.HexColor("#1b6a60")
TEAL_LIGHT  = colors.HexColor("#e8f5f3")
TEAL_MID    = colors.HexColor("#c2deda")
DARK        = colors.HexColor("#2C3E50")
GREY        = colors.HexColor("#7f8c8d")
LIGHT_GREY  = colors.HexColor("#f7f9f9")
WHITE       = colors.white
RED         = colors.HexColor("#e74c3c")
GREEN       = colors.HexColor("#27ae60")
AMBER       = colors.HexColor("#f39c12")


def _status_colour(status: str):
    return {"Paid": GREEN, "Pending": AMBER, "Overdue": RED}.get(status, GREY)


def generate_receipt(data: dict, output_dir: str = ".") -> str:
    os.makedirs(output_dir, exist_ok=True)

    pay_id       = data.get("pay_id", "N/A")
    patient_name = data.get("patient_name", "Unknown Patient")
    patient_id   = data.get("patient_id", "—")
    age          = data.get("age", "—")
    contact      = data.get("contact", "—")
    email        = data.get("email", "—")
    address      = data.get("address", "—")
    symptoms     = data.get("symptoms", "—")
    amount       = data.get("amount", 0.0)
    method       = data.get("method", "—")
    status       = data.get("status", "—")
    notes        = data.get("notes", "") or "—"
    date_raw     = data.get("date", datetime.now())
    doctor_name  = data.get("doctor_name", "—")
    department   = data.get("department", "—")
    hospital     = data.get("hospital_name", "SmartHealth Medical Centre")

    if isinstance(date_raw, datetime):
        date_str = date_raw.strftime("%d %B %Y, %H:%M")
    else:
        date_str = str(date_raw)

    safe_name = patient_name.replace(" ", "_")
    filename  = f"Receipt_PAY{pay_id}_{safe_name}.pdf"
    filepath  = os.path.join(output_dir, filename)

    # ── Page: wider margins so content has more room ─────────────────────────
    doc = SimpleDocTemplate(
        filepath,
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=12 * mm,
        bottomMargin=12 * mm,
    )
    PAGE_W = A4[0] - 36 * mm   # usable width ≈ 174 mm

    styles = getSampleStyleSheet()

    def S(name, **kw):
        return ParagraphStyle(name, parent=styles["Normal"], **kw)

    # ── Text styles ───────────────────────────────────────────────────────────
    hosp_s      = S("Hosp",    fontSize=24, textColor=WHITE,      alignment=TA_CENTER,
                               fontName="Helvetica-Bold", leading=30)
    sub_s       = S("Sub",     fontSize=10, textColor=TEAL_LIGHT, alignment=TA_CENTER, leading=16)
    title_s     = S("Title",   fontSize=30, textColor=TEAL,       alignment=TA_CENTER,
                               fontName="Helvetica-Bold", leading=38, spaceAfter=3)
    ref_s       = S("Ref",     fontSize=10, textColor=GREY,       alignment=TA_CENTER, leading=16)
    sec_s       = S("Sec",     fontSize=10, textColor=WHITE,       fontName="Helvetica-Bold", leading=14)
    lbl_s       = S("Lbl",     fontSize=9,  textColor=GREY,       leading=14)
    val_s       = S("Val",     fontSize=10, textColor=DARK,       fontName="Helvetica-Bold", leading=14)
    amt_lbl_s   = S("AmtLbl",  fontSize=10, textColor=TEAL_LIGHT, alignment=TA_CENTER, leading=16)
    amt_s       = S("Amt",     fontSize=26, textColor=WHITE,      fontName="Helvetica-Bold",
                               alignment=TA_CENTER, leading=34)
    stat_s      = S("Stat",    fontSize=13, textColor=_status_colour(status),
                               fontName="Helvetica-Bold", alignment=TA_CENTER, leading=20)
    tbl_hdr_s   = S("TblHdr",  fontSize=9,  textColor=WHITE,      fontName="Helvetica-Bold", leading=13)
    tbl_cell_s  = S("TblCell", fontSize=9,  textColor=DARK,       leading=13)
    tbl_bold_s  = S("TblBold", fontSize=9,  textColor=DARK,       fontName="Helvetica-Bold", leading=13)
    tbl_tot_s   = S("TblTot",  fontSize=10, textColor=WHITE,      fontName="Helvetica-Bold",
                               alignment=TA_RIGHT, leading=14)
    footer_s    = S("Footer",  fontSize=8,  textColor=GREY,       alignment=TA_CENTER, leading=13)

    story = []

    # ════════════════════════════════════════════════════════════════════════════
    # 1. HEADER BANNER
    # ════════════════════════════════════════════════════════════════════════════
    banner = Table(
        [[Paragraph(f"<b>{hospital}</b>", hosp_s)],
         [Paragraph("Hospital Management System  •  Billing Department", sub_s)]],
        colWidths=[PAGE_W]
    )
    banner.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), TEAL),
        ("TOPPADDING",    (0, 0), (-1, 0),  16),
        ("BOTTOMPADDING", (0, 0), (-1, 0),  4),
        ("TOPPADDING",    (0, 1), (-1, 1),  2),
        ("BOTTOMPADDING", (0, 1), (-1, 1),  14),
        ("LEFTPADDING",   (0, 0), (-1, -1), 0),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
    ]))
    story.append(banner)
    story.append(Spacer(1, 10 * mm))

    # ════════════════════════════════════════════════════════════════════════════
    # 2. TITLE + REFERENCE
    # ════════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("PAYMENT RECEIPT", title_s))
    story.append(Paragraph(f"Reference: PAY-{pay_id:04}  |  Date: {date_str}", ref_s))
    story.append(Spacer(1, 7 * mm))
    story.append(HRFlowable(width="100%", thickness=2, color=TEAL,
                             spaceBefore=0, spaceAfter=8 * mm))

    # ════════════════════════════════════════════════════════════════════════════
    # 3. INFO SECTIONS — two full-width tables side by side
    #    Each section header spans both columns; rows are label | value
    # ════════════════════════════════════════════════════════════════════════════
    def section_hdr_row(title, ncols=2):
        """A header row that spans all columns."""
        cell = Paragraph(f"  {title}", sec_s)
        row  = [cell] + [""] * (ncols - 1)
        return row

    def irow(label, value):
        return [Paragraph(label, lbl_s), Paragraph(str(value), val_s)]

    # ── Left panel: Patient information ─────────────────────────────────────
    pt_data = [
        section_hdr_row("Patient Information"),
        irow("Full Name",  patient_name),
        irow("Patient ID", f"PT-{patient_id}"),
        irow("Age",        str(age)),
        irow("Contact",    contact),
        irow("Email",      email),
        irow("Address",    address),
        irow("Symptoms",   symptoms),
    ]
    lbl_w = 32 * mm
    val_w = 52 * mm
    pt_tbl = Table(pt_data, colWidths=[lbl_w, val_w])
    pt_tbl.setStyle(TableStyle([
        # Header row
        ("SPAN",          (0, 0), (1, 0)),
        ("BACKGROUND",    (0, 0), (1, 0),  TEAL),
        ("TOPPADDING",    (0, 0), (1, 0),  7),
        ("BOTTOMPADDING", (0, 0), (1, 0),  7),
        # Data rows
        ("BACKGROUND",    (0, 1), (-1, 1), WHITE),
        ("BACKGROUND",    (0, 2), (-1, 2), LIGHT_GREY),
        ("BACKGROUND",    (0, 3), (-1, 3), WHITE),
        ("BACKGROUND",    (0, 4), (-1, 4), LIGHT_GREY),
        ("BACKGROUND",    (0, 5), (-1, 5), WHITE),
        ("BACKGROUND",    (0, 6), (-1, 6), LIGHT_GREY),
        ("BACKGROUND",    (0, 7), (-1, 7), WHITE),
        ("TOPPADDING",    (0, 1), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 7),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("GRID",          (0, 1), (-1, -1), 0.4, TEAL_MID),
        ("BOX",           (0, 0), (-1, -1), 1,   TEAL),
    ]))

    # ── Right panel: Visit & Billing details ─────────────────────────────────
    vt_data = [
        section_hdr_row("Visit & Billing Details"),
        irow("Doctor",     doctor_name),
        irow("Department", department),
        irow("Method",     method),
        irow("Status",     status),
        irow("Notes",      notes),
    ]
    vt_tbl = Table(vt_data, colWidths=[lbl_w, val_w])
    vt_tbl.setStyle(TableStyle([
        ("SPAN",          (0, 0), (1, 0)),
        ("BACKGROUND",    (0, 0), (1, 0),  TEAL),
        ("TOPPADDING",    (0, 0), (1, 0),  7),
        ("BOTTOMPADDING", (0, 0), (1, 0),  7),
        ("BACKGROUND",    (0, 1), (-1, 1), WHITE),
        ("BACKGROUND",    (0, 2), (-1, 2), LIGHT_GREY),
        ("BACKGROUND",    (0, 3), (-1, 3), WHITE),
        ("BACKGROUND",    (0, 4), (-1, 4), LIGHT_GREY),
        ("BACKGROUND",    (0, 5), (-1, 5), WHITE),
        ("TOPPADDING",    (0, 1), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 7),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("GRID",          (0, 1), (-1, -1), 0.4, TEAL_MID),
        ("BOX",           (0, 0), (-1, -1), 1,   TEAL),
    ]))

    # Place the two panels side by side with a gap column
    GAP = 6 * mm
    panel_w = lbl_w + val_w   # 84 mm each
    side_by_side = Table(
        [[pt_tbl, "", vt_tbl]],
        colWidths=[panel_w, GAP, panel_w],
    )
    side_by_side.setStyle(TableStyle([
        ("VALIGN",       (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING",  (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING",   (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 0),
    ]))
    story.append(KeepTogether(side_by_side))
    story.append(Spacer(1, 9 * mm))

    # ════════════════════════════════════════════════════════════════════════════
    # 4. AMOUNT BOX
    # ════════════════════════════════════════════════════════════════════════════
    sub_total = float(amount)
    tax_amt   = round(sub_total * 0.16, 2)
    grand     = sub_total + tax_amt

    amount_box = Table(
        [[Paragraph("TOTAL AMOUNT DUE", amt_lbl_s)],
         [Paragraph(f"K {grand:,.2f}", amt_s)],
         [Paragraph(status.upper(), stat_s)]],
        colWidths=[PAGE_W],
    )
    amount_box.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 1), TEAL),
        ("BACKGROUND",    (0, 2), (-1, 2), TEAL_LIGHT),
        ("TOPPADDING",    (0, 0), (-1, 0), 12),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 4),
        ("TOPPADDING",    (0, 1), (-1, 1), 4),
        ("BOTTOMPADDING", (0, 1), (-1, 1), 12),
        ("TOPPADDING",    (0, 2), (-1, 2), 10),
        ("BOTTOMPADDING", (0, 2), (-1, 2), 10),
        ("BOX",           (0, 0), (-1, -1), 1.5, TEAL),
    ]))
    story.append(amount_box)
    story.append(Spacer(1, 9 * mm))

    # ════════════════════════════════════════════════════════════════════════════
    # 5. BILLING BREAKDOWN TABLE
    # ════════════════════════════════════════════════════════════════════════════
    sec_hdr_tbl = Table(
        [[Paragraph("  Billing Breakdown", sec_s)]],
        colWidths=[PAGE_W]
    )
    sec_hdr_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), TEAL),
        ("TOPPADDING",    (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
    ]))
    story.append(sec_hdr_tbl)
    story.append(Spacer(1, 1 * mm))

    # Column widths: #, Description, Qty, Unit Price, Total
    cw = [12*mm, 74*mm, 16*mm, 36*mm, 36*mm]

    def hdr(t): return Paragraph(t, tbl_hdr_s)
    def cel(t): return Paragraph(t, tbl_cell_s)
    def bol(t): return Paragraph(t, tbl_bold_s)
    def tot(t): return Paragraph(t, tbl_tot_s)

    bd_data = [
        [hdr("#"), hdr("Description"), hdr("Qty"), hdr("Unit Price (K)"), hdr("Total (K)")],
        [cel("1"), cel(f"Medical Consultation – {department}"), cel("1"),
         cel(f"{sub_total:,.2f}"), cel(f"{sub_total:,.2f}")],
        ["", "", "", bol("Sub-total"),   tot(f"K {sub_total:,.2f}")],
        ["", "", "", bol("VAT (16%)"),   tot(f"K {tax_amt:,.2f}")],
        ["", "", "", bol("GRAND TOTAL"), tot(f"K {grand:,.2f}")],
    ]

    bd_tbl = Table(bd_data, colWidths=cw, repeatRows=1)
    bd_tbl.setStyle(TableStyle([
        # Header
        ("BACKGROUND",    (0, 0), (-1, 0), TEAL),
        ("TEXTCOLOR",     (0, 0), (-1, 0), WHITE),
        ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
        # Alignment
        ("ALIGN",         (0, 0), (-1, -1), "LEFT"),
        ("ALIGN",         (2, 0), (-1, -1), "RIGHT"),
        # Alternating data rows
        ("BACKGROUND",    (0, 1), (-1, 1), LIGHT_GREY),
        # Summary rows background
        ("BACKGROUND",    (0, 2), (-1, 3), WHITE),
        ("BACKGROUND",    (0, 4), (-1, 4), TEAL),
        # Padding — generous
        ("TOPPADDING",    (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        # Grid for data rows only
        ("GRID",          (0, 0), (-1, 1), 0.5, TEAL_MID),
        ("LINEABOVE",     (0, 2), (-1, 2), 1,   TEAL),
        ("LINEBELOW",     (0, 3), (-1, 3), 1,   TEAL),
        ("BOX",           (0, 0), (-1, -1), 1,  TEAL),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(bd_tbl)
    story.append(Spacer(1, 10 * mm))

    # ════════════════════════════════════════════════════════════════════════════
    # 6. FOOTER
    # ════════════════════════════════════════════════════════════════════════════
    story.append(HRFlowable(width="100%", thickness=1, color=TEAL_MID,
                             spaceBefore=0, spaceAfter=5 * mm))
    story.append(Paragraph(
        "Thank you for choosing SmartHealth Medical Centre. "
        "This is a computer-generated receipt and is valid without a signature.",
        footer_s
    ))
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph(
        f"Generated on {datetime.now().strftime('%d %B %Y at %H:%M')}  "
        f"|  SmartHealth HMS  |  support@smarthealth.zm",
        footer_s
    ))

    doc.build(story)
    return filepath


if __name__ == "__main__":
    from datetime import datetime
    sample = {
        "pay_id":        1,
        "patient_name":  "Brian Taylor",
        "patient_id":    45,
        "age":           32,
        "contact":       "+260760932789",
        "email":         "briantaylor@gmail.com",
        "address":       "184 Kabwe Road, Lusaka",
        "symptoms":      "Flu",
        "amount":        500.00,
        "method":        "Mobile Money",
        "status":        "Paid",
        "notes":         "Paid via Airtel Money",
        "date":          datetime(2026, 4, 9, 18, 50),
        "doctor_name":   "Dr. Nkandu Mwale",
        "department":    "General Medicine",
        "hospital_name": "SmartHealth Medical Centre",
    }
    out = generate_receipt(sample, output_dir="/home/claude")
    print(f"Saved: {out}")