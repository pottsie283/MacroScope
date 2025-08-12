from .office import DocumentAnalyzer

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdftypes import resolve1
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
findings = {}
class PDFAnalyzer(DocumentAnalyzer):
    def analyze(self, file_path: str) -> dict:
        findings = {"objects": [], "js": [], "openaction": [], "embedded_files": [], "errors": []}
        try:
            with open(file_path, "rb") as f:
                parser = PDFParser(f)
                doc = PDFDocument(parser)
                # Look for OpenAction
                if hasattr(doc, 'catalog') and 'OpenAction' in doc.catalog:
                    findings["openaction"].append(str(doc.catalog['OpenAction']))
                # Look for embedded files
                if hasattr(doc, 'embedded_files'):
                    findings["embedded_files"].append(str(doc.embedded_files))
                # Look for JavaScript
                if hasattr(doc, 'catalog') and 'Names' in doc.catalog:
                    names = resolve1(doc.catalog['Names'])
                    if names and 'JavaScript' in names:
                        findings["js"].append(str(names['JavaScript']))
        except Exception as e:
            findings["errors"].append(str(e))
        return findings
