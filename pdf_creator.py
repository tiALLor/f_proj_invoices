from fpdf import FPDF
from fpdf.enums import CellBordersLayout
import os


black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
light_gray = (239, 241, 244)


class PDF(FPDF):
    def header(self):
        # Setting font: helvetica bold 15
        self.set_font("helvetica", style="B", size=24)
        # Printing title:
        self.cell(40, 30, "Invoice", align="C")
        # Performing a line break:
        self.ln(30)

    def footer(self):
        # Position cursor at 1.5 cm from bottom:
        self.set_y(-15)
        # Setting font: helvetica italic 8
        self.set_font("helvetica", style="I", size=8)
        # Printing page number:
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def adress(self, text1, data, x, y) -> None:
        self.set_xy(x=15, y=y)
        self.cell(x)
        self.set_font("helvetica", size=8, style="U")
        self.cell(0, 0, text1, align="L")
        self.ln(6)
        self.set_font("helvetica", size=11, style="B")
        for item in data:
            self.cell(x)
            self.cell(0, 0, item, align="L")
            self.set_font("DejaVu", size=7)
            self.ln(3.5)


def create_pdf(data, file_name):
    file_name = f"{file_name}.pdf"
    print(file_name)
    pdf = PDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    pdf.add_font("DejaVu", "", r"Fonts\DejaVuSansCondensed.ttf", uni=True)
    pdf.set_margins(left=15, top=20, right=15)
    pdf.set_auto_page_break(True, margin=10)
    pdf.set_font("helvetica", size=12)

    pdf.cell(10)
    pdf.set_font("helvetica", size=12, style="BU")
    pdf.cell(0, 0, f"Invoice number: {data["invoice_id"]:06d}", align="L")
    pdf.ln(7)

    pdf.cell(10)
    pdf.set_font("helvetica", size=10, style="B")
    pdf.cell(0, 0, f"Date of issue: {data["invoice_date"]}", align="L")
    pdf.ln(5)

    pdf.cell(10)
    pdf.set_font("helvetica", size=10, style="BU")
    pdf.cell(0, 0, f"Date due: {data["due_date"]}", align="L")
    pdf.ln(5)

    # seller
    pdf.adress("Seller: ", data["seller_addr"], 10, 60)

    # Buyer
    pdf.adress("Buyer: ", data["customer_addr"], 120, 60)

    # Ivoice base on
    pdf.set_xy(x=20, y=105)
    pdf.set_font("helvetica", size=10, style="U")
    pdf.cell(0, 0, "Subject:", align="L")
    pdf.ln(6)
    pdf.set_font("helvetica", size=8, style="")
    pdf.cell(
        10,
        0,
        f"The Invoice is created base on Purchase order no. {data["po_id"]:06d}",
        align="L",
    )
    pdf.ln(5)

    table_data = data["po_item_data"]

    pdf.set_font("helvetica", size=6)
    with pdf.table(
        text_align="CENTER", cell_fill_color=light_gray, cell_fill_mode="ROWS"
    ) as table:
        for data_row in table_data:
            row = table.row()
            for datum in data_row:
                row.cell(datum, border="BOTTOM")

    # Summary values of the invoice
    pdf.set_xy(x=100, y=200)
    summary_values = data["invoice_price"]
    header = [("Total", "Amount:")]
    total_netto = [("Total Netto value: ", f"{summary_values["total_netto"]} EUR")]
    total_vat = [("Total VAT value: ", f"{summary_values["total_vat"]} EUR")]
    total_brutto = [("Total Brutto value: ", f"{summary_values["total_brutto"]} EUR")]
    table_data = header + total_netto + total_vat + total_brutto
    # print(table_data)         # debug

    pdf.set_font("helvetica", size=10)
    table_width = 80
    with pdf.table(
        width=table_width,
        cell_fill_color=light_gray,
        cell_fill_mode="ROWS",
        borders_layout="SINGLE_TOP_LINE",
        align="R",
    ) as table:
        for data_row in table_data:
            row = table.row()
            for datum in data_row:
                row.cell(datum)

    pdf.set_x(150)
    pdf.set_y(250)
    pdf.set_font("helvetica", size=14, style="BU")
    pdf.cell(
        0,
        0,
        f"Total {summary_values["total_brutto"]} EUR due to {data["due_date"]}",
        align="R",
    )

    # Specify the folder where you want to save the PDF
    output_folder = "PDF_invoice"
    os.makedirs(output_folder, exist_ok=True)

    # Specify the full path for the PDF file
    output_path = os.path.join(output_folder, file_name)
    pdf.output(output_path)


def main():
    create_pdf()


if __name__ == "__main__":
    main()
