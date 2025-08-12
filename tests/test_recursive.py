from macroscope.analysis.office import OfficeAnalyzer
from macroscope.analysis.pdf import PDFAnalyzer
import tempfile
import os

def test_office_analyzer_interface():
    analyzer = OfficeAnalyzer()
    with tempfile.NamedTemporaryFile(suffix='.doc', delete=False) as f:
        f.write(b'Test')
        f.flush()
        result = analyzer.analyze(f.name)
        assert isinstance(result, dict)
    os.unlink(f.name)

def test_pdf_analyzer_interface():
    analyzer = PDFAnalyzer()
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
        f.write(b'Test')
        f.flush()
        result = analyzer.analyze(f.name)
        assert isinstance(result, dict)
    os.unlink(f.name)
