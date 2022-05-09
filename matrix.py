import csv
import math


class Matrix:

    def __init__(self, library):
        self.files = library.spectra_files
        self.corr_matrix = self.calculate()

    def calculate(self):
        combined_data = []
        for file in self.files:
            combined_data.append(read(file))

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
    for i in range(2, len(data) - 1):
        derivatives = (data[i + 1] - data[i - 1]) / 2
        return derivatives


def read(filename):
    with open(filename, newline='') as csvfile:
        data_reader = csv.reader(csvfile, dialect='excel')
        data = []
        for row in data_reader:
            data.append(float(row[1]))
    return data


def correlate(spec_a, spec_b):
    return math.sqrt((spec_a @ spec_b) ** 2) / ((spec_a @ spec_a) * (spec_b @ spec_b))
