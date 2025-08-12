import os
import shutil
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdftypes import resolve1

class PDFEmbeddedExtractor:
    def extract(self, file_path: str, output_dir: str) -> list:
        extracted = []
        try:
            with open(file_path, "rb") as f:
                parser = PDFParser(f)
                doc = PDFDocument(parser)
                if hasattr(doc, 'embedded_files'):
                    ef = doc.embedded_files
                    for name, stream in ef.items():
                        out_path = os.path.join(output_dir, name)
                        with open(out_path, 'wb') as out:
                            out.write(stream.get_data())
                        extracted.append(out_path)
        except Exception:
            pass
        return extracted
