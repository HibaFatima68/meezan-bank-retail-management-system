from app import app
from flask import render_template, send_file
from datetime import datetime
import os, tempfile
try:
    import pdfkit
    PDFKIT_AVAILABLE = True
except ImportError:
    PDFKIT_AVAILABLE = False


@app.route('/download_reciept/<filename>')
def download_reciept(filename):
    return send_file(filename, as_attachment=True)


@app.route('/success/<filename>')
def payment(filename):
    return render_template('user/payment.html', filename=filename)

@app.route('/success/<filename>/download')
def downlaod_success_reciept(filename):
    return send_file(filename, as_attachment=True)


def generate_receipt(reciept_data):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    
    if PDFKIT_AVAILABLE:
        try:
            html_template_path = "app/templates/user/receipt_template.html"

            with open(html_template_path, "r") as file:
                receipt_content = file.read()

            receipt_content = receipt_content.format(**reciept_data)

            filename = f'reciept_{timestamp}.pdf'

            temp_dir = tempfile.mkdtemp()

            temp_html_path = os.path.join(temp_dir, "temp_receipt.html")
            with open(temp_html_path, "w", encoding='utf-8') as temp_file:
                temp_file.write(receipt_content)

            pdf_path = os.path.join(temp_dir, filename)
            pdfkit.from_file(temp_html_path, pdf_path)

            # clean the temp html file
            os.remove(temp_html_path)

            return pdf_path
        except Exception as e:
            # If PDF generation fails, return None and handle gracefully
            print(f"PDF generation failed: {e}")
            return None
    else:
        # PDF generation not available, return None
        return None