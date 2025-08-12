import argparse
import os
import sys
import hashlib
import tempfile
import shutil
from macroscope.analysis.office import OfficeAnalyzer
from macroscope.analysis.pdf import PDFAnalyzer
from macroscope.report import Report

# Terminal color codes
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
BOLD = '\033[1m'
RESET = '\033[0m'

def color_status(ok):
    return f"{GREEN}[OK]{RESET}" if ok else f"{RED}[FAIL]{RESET}"


def get_sha256(file_path):
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

def analyze_file(file_path, doc_type=None, output_format="json", extract_dir=None, plugins=None, recursive=False, analyzed_files=None):
    import atexit
    if analyzed_files is None:
        analyzed_files = set()
    if file_path in analyzed_files:
        return  # Prevent infinite recursion
    analyzed_files.add(file_path)
    if not doc_type:
        doc_type = "pdf" if file_path.lower().endswith(".pdf") else "office"
    analyzer = PDFAnalyzer() if doc_type == "pdf" else OfficeAnalyzer()
    findings = analyzer.analyze(file_path)
    # Plugin support
    plugin_results = {}
    if plugins:
        for plugin_name in plugins:
            try:
                mod = __import__(f"macroscope.plugins.{plugin_name}", fromlist=[plugin_name])
                plugin_class = getattr(mod, [c for c in dir(mod) if c.endswith("Plugin")][0])
                plugin = plugin_class()
                plugin_results[plugin_name] = plugin.run(file_path)
            except Exception as e:
                plugin_results[plugin_name] = {"error": str(e)}
    findings["plugins"] = plugin_results
    # Extraction logic
    extracted_files = []
    if doc_type == "office":
        try:
            from macroscope.extractors.ole import OLEExtractor
            ole_extractor = OLEExtractor()
            extracted_files.extend(ole_extractor.extract(file_path, extract_dir))
        except Exception:
            pass
    elif doc_type == "pdf":
        try:
            from macroscope.extractors.pdf_embedded import PDFEmbeddedExtractor
            pdf_extractor = PDFEmbeddedExtractor()
            extracted_files.extend(pdf_extractor.extract(file_path, extract_dir))
        except Exception:
            pass
    findings["extracted_files"] = extracted_files
    report = Report(findings)
    print(report.to_output())
    print(f"{BOLD}SHA256{RESET}: {get_sha256(file_path)}")
    if extract_dir:
        print(f"{YELLOW}[INFO]{RESET} Artifacts would be extracted to: {extract_dir}")
        # Securely delete temp extraction dir on exit if it was auto-created
        def _cleanup():
            if os.path.exists(extract_dir) and extract_dir.startswith("/var/folders/"):
                shutil.rmtree(extract_dir, ignore_errors=True)
        atexit.register(_cleanup)
    # Recursively analyze extracted files
    if recursive:
        for ef in extracted_files:
            analyze_file(ef, None, output_format, extract_dir, plugins, recursive, analyzed_files)

def main():
    parser = argparse.ArgumentParser(description="MacroScope Document Malware Triage Toolkit")
    subparsers = parser.add_subparsers(dest="command", required=False)

    analyze_parser = subparsers.add_parser("analyze", help="Analyze a document")
    analyze_parser.add_argument("file", help="Path to the document to analyze")
    analyze_parser.add_argument("--type", choices=["office", "pdf"], help="Type of document (auto-detect if omitted)")
    analyze_parser.add_argument("--format", choices=["json", "text"], default="json", help="Output format")
    analyze_parser.add_argument("--extract", help="Directory to extract embedded artifacts (secure temp dir if omitted)")
    analyze_parser.add_argument("--recursive", action="store_true", help="Recursively analyze extracted artifacts")
    analyze_parser.add_argument("--plugin", action="append", help="Plugin(s) to run (by module name in macroscope.plugins)")

    # Future: add more subcommands (e.g., hash, batch, plugin)

    args = parser.parse_args()

    if args.command == "analyze" or not args.command:
        extract_dir = args.extract or tempfile.mkdtemp(prefix="macroscope_")
        try:
            analyze_file(args.file, args.type, args.format, extract_dir, args.plugin, args.recursive)
        finally:
            if not args.extract:
                shutil.rmtree(extract_dir)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
