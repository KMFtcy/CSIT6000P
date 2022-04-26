import csv

dataset_path = '../data/dataset.csv'


def load():
    with open(dataset_path, encoding='utf-8-sig') as csvfile:
        poi_dataset = csvfile.readlines()
    return poi_dataset
