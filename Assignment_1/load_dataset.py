import csv

dataset_path = '/home/tangchaoyang/develop/CSIT6000P/Assignment_1/dataset.csv'


def load():
    with open(dataset_path, encoding='utf-8-sig') as csvfile:
        poi_dataset = csvfile.readlines()
    return poi_dataset
