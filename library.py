class Library:
    spectra_files = set()

    def __init__(self):
        pass

    # Add files selected in GUI
    def files_import(self, files):
        for file in files:
            self.spectra_files.add(file)

    # Remove file from the set
    def files_remove(self, file):
        self.spectra_files.remove(file)
