import os
import shutil
try:
    from oletools.oleobj import OleFileIO
except ImportError:
    OleFileIO = None

class OLEExtractor:
    def extract(self, file_path: str, output_dir: str) -> list:
        extracted = []
        if OleFileIO is None:
            return extracted
        try:
            ole = OleFileIO(file_path)
            for entry in ole.listdir():
                if entry[-1].lower().endswith('ole10native'):
                    data = ole.openstream(entry).read()
                    out_path = os.path.join(output_dir, '_'.join(entry))
                    with open(out_path, 'wb') as out:
                        out.write(data)
                    extracted.append(out_path)
            ole.close()
        except Exception:
            pass
        return extracted
