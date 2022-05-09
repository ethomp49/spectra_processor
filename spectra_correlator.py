import csv
import math
import numpy


class Library:

    def __init__(self):
        self.spectra_files = {}

    # Callable function for adding files to the library
    def files_import(self, files):
        for file in files:
            self.spectra_files.setdefault(get_name(file), file)


class Matrix:

    # Basic constructor takes library files and calls the calculate method to get the correlation matrix
    def __init__(self, library):
        self.corr_matrix = calculate(library)


def calculate(library):
    combined_data = []
    for file in sorted(library.spectra_files.keys()):
        combined_data.append(read(library.spectra_files.get(file)))

    smoothed_data = []
    for spectrum in combined_data:
        smoothed_data.append(smooth(spectrum))

    corr_matrix = []
    for data_a in smoothed_data:
        row = []
        for data_b in smoothed_data:
            row.append(correlate(data_a, data_b))
        corr_matrix.append(row)
    return corr_matrix


def smooth(data):
    derivatives = []
    for i in range(1, len(data) - 1):
        derivatives.append((data[i + 1] - data[i - 1]) / 2)
    return derivatives

    # Reads and returns the absorbance values from spectra in .csv format as a list


def read(filename):
    with open(filename, newline='') as csvfile:
        data_reader = csv.reader(csvfile, dialect='excel')
        data = []
        for row in data_reader:
            data.append(float(row[1]))
        return data


# Returns the correlation value between two spectra
def correlate(spec_a, spec_b):
    return math.sqrt((numpy.dot(spec_a, spec_b) ** 2) / (numpy.dot(spec_a, spec_a) * numpy.dot(spec_b, spec_b)))


def get_name(file):
    return file.split('/')[-1].split('.')[0]
