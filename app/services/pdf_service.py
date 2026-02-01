from pypdf import PdfReader
import io

class PDFService:
    @staticmethod
    async def extract_text(file_content: bytes) -> str:
        "Extract text from pdf"
        pdf_file = io.BytesIO(file_content)
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        return text

pdf_service = PDFService()