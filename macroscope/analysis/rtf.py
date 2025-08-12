from .office import DocumentAnalyzer

import re
class RTFAnalyzer(DocumentAnalyzer):
    def analyze(self, file_path: str) -> dict:
        findings = {"exploits": [], "errors": []}
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            # Look for known exploit signatures (e.g., CVE-2017-11882)
            if "objupdate" in content.lower() and "eqnedt32" in content.lower():
                findings["exploits"].append("CVE-2017-11882 signature detected")
            # Look for suspicious OLE objects
            if "\objdata" in content:
                findings["exploits"].append("Embedded OLE object detected")
        except Exception as e:
            findings["errors"].append(str(e))
        return findings
