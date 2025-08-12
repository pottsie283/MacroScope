from .office import DocumentAnalyzer

import re
import os
import requests
try:
    import yara
except ImportError:
    yara = None

YARA_RULES_PATH = os.path.join(os.path.dirname(__file__), "html_yara_rules.yar")

def fetch_live_cve_patterns():
    # CIRCL CVE Search API example (returns all CVEs, so we filter for web/HTML/JS)
    try:
        resp = requests.get("https://cve.circl.lu/api/search/javascript")
        if resp.status_code == 200:
            cves = resp.json()
            patterns = {}
            for cve in cves:
                cveid = cve.get("id")
                desc = cve.get("summary", "")
                # Heuristic: extract regex-like patterns from description (very basic)
                if "vbscript" in desc.lower():
                    patterns[cveid] = r"vbscript:.*?ExecuteGlobal"
                if "activexobject" in desc.lower():
                    patterns[cveid] = r"ActiveXObject"
                if "mshta" in desc.lower():
                    patterns[cveid] = r"mshta\\.exe"
                if "flash" in desc.lower():
                    patterns[cveid] = r"Adobe\s?Flash|flashplayer|SWFObject"
                # Add more heuristics as needed
            return patterns
    except Exception:
        pass
    # Fallback to static patterns if API fails
    return {
        "CVE-2018-8174": r"vbscript:.*?ExecuteGlobal",
        "CVE-2016-0189": r"mshta\\.exe|ActiveXObject\('Shell\\.Application'\)",
        "CVE-2015-5122": r"Adobe\s?Flash|flashplayer|SWFObject",
    }

class HTMLAnalyzer(DocumentAnalyzer):
    def analyze(self, file_path: str) -> dict:
        findings = {
            "suspicious_scripts": [],
            "suspicious_blobs": [],
            "suspicious_strings": [],
            "cve_hits": [],
            "yara_matches": [],
            "obfuscation": [],
            "exploit_kit": [],
            "errors": []
        }
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            # Suspicious script tags
            for match in re.finditer(r'<script.*?>(.*?)</script>', content, re.DOTALL|re.IGNORECASE):
                script = match.group(1)
                if "atob(" in script or "eval(" in script or "blob:" in script:
                    findings["suspicious_scripts"].append(script[:200])
            # Base64 blobs
            for match in re.finditer(r'data:[^;]+;base64,[A-Za-z0-9+/=]+', content):
                findings["suspicious_blobs"].append(match.group(0)[:200])
            # Suspicious keywords/APIs
            for keyword in ["download", "window.location", "iframe", "object", "msSaveOrOpenBlob", "ActiveXObject", "XMLHttpRequest", "document.write", "setTimeout", "setInterval"]:
                if keyword in content:
                    findings["suspicious_strings"].append(keyword)
            # Obfuscation heuristics
            if re.search(r'eval\s*\(', content) or re.search(r'unescape\s*\(', content):
                findings["obfuscation"].append("eval/unescape usage")
            if re.search(r'String\.fromCharCode', content):
                findings["obfuscation"].append("String.fromCharCode usage")
            # Exploit kit markers
            for kit in ["Neutrino", "Angler", "RIG"]:
                if kit.lower() in content.lower():
                    findings["exploit_kit"].append(kit)
            # CVE pattern matching (live feed)
            cve_patterns = fetch_live_cve_patterns()
            for cve, pattern in cve_patterns.items():
                if re.search(pattern, content, re.IGNORECASE):
                    findings["cve_hits"].append(cve)
            # YARA scanning
            if yara and os.path.exists(YARA_RULES_PATH):
                try:
                    rules = yara.compile(filepath=YARA_RULES_PATH)
                    matches = rules.match(data=content)
                    for match in matches:
                        findings["yara_matches"].append(match.rule)
                except Exception as e:
                    findings["errors"].append(f"YARA error: {e}")
        except Exception as e:
            findings["errors"].append(str(e))
        return findings
