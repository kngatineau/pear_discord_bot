import csv
import pandas as pd


#  exports the data to a CSV to be retrieved later by the !pair command
def export_data(message, answers):
    with open('root_message.csv', 'w', encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([str(message.id)] + answers)


#  parse the data from CSV to a list
def import_data():
    list_msg = pd.read_csv(r'root_message.csv')
    msg_list = list(list_msg)
    return msg_list
