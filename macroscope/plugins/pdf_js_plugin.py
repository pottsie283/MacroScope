class PDFJSPlugin:
    def run(self, file_path: str) -> dict:
        # Example: flag if PDF has JavaScript
        try:
            from pdfminer.pdfparser import PDFParser
            from pdfminer.pdfdocument import PDFDocument
            from pdfminer.pdftypes import resolve1
            with open(file_path, "rb") as f:
                parser = PDFParser(f)
                doc = PDFDocument(parser)
                if hasattr(doc, 'catalog') and 'Names' in doc.catalog:
                    names = resolve1(doc.catalog['Names'])
                    if names and 'JavaScript' in names:
                        return {"js_found": True}
            return {"js_found": False}
        except Exception as e:
            return {"error": str(e)}
