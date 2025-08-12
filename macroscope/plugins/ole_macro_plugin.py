class OLEMacroPlugin:
    def run(self, file_path: str) -> dict:
        # Example: flag if file is OLE and has macros
        try:
            from oletools.olevba import VBA_Parser
            vba = VBA_Parser(file_path)
            has_macros = vba.detect_vba_macros()
            vba.close()
            return {"ole_macros": has_macros}
        except Exception as e:
            return {"error": str(e)}
