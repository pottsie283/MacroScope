from abc import ABC, abstractmethod

class DocumentAnalyzer(ABC):
    @abstractmethod
    def analyze(self, file_path: str) -> dict:
        pass

import os
findings = {}
try:
    from oletools.olevba import VBA_Parser
except ImportError:
    VBA_Parser = None

class OfficeAnalyzer(DocumentAnalyzer):
    def analyze(self, file_path: str) -> dict:
        findings = {"macros": [], "autoexec": [], "suspicious": [], "errors": []}
        if VBA_Parser is None:
            findings["errors"].append("oletools not installed")
            return findings
        try:
            vba = VBA_Parser(file_path)
            if vba.detect_vba_macros():
                for (filename, stream_path, vba_filename, vba_code) in vba.extract_macros():
                    findings["macros"].append({"filename": vba_filename, "code": vba_code[:200]})
                    # Look for autoexec keywords
                    if any(k in vba_code.lower() for k in ["autoopen", "document_open", "workbook_open", "auto_close"]):
                        findings["autoexec"].append(vba_filename)
                    # Look for suspicious patterns
                    if any(k in vba_code.lower() for k in ["shell.application", "wscript.shell", "powershell", "cmd.exe", "base64decode"]):
                        findings["suspicious"].append(vba_filename)
            vba.close()
        except Exception as e:
            findings["errors"].append(str(e))
        return findings
