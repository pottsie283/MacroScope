from .office import DocumentAnalyzer

class OneNoteAnalyzer(DocumentAnalyzer):
    def analyze(self, file_path: str) -> dict:
        findings = {"objects": [], "errors": []}
        try:
            with open(file_path, "rb") as f:
                data = f.read(4096)
                if b"OneNote" in data:
                    findings["objects"].append("OneNote signature found")
                # Add more static checks as needed
        except Exception as e:
            findings["errors"].append(str(e))
        return findings
