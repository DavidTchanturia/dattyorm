from data_operators.csv_data_operator import CSVDataOperator

csv_data = CSVDataOperator("test_files/t3es*t_file.csv")
csv_data.get_data()

print(csv_data.df)
print(csv_data.file_metadata)
print("============================================================")
csv_data.delete_data(0)
print(csv_data.df)
print("============================================================")

csv_data.update_data(2, name="giorgi")
print(csv_data.df)
print("============================================================")

csv_data.insert_data({"name": "kolia", "age": 23, "sex": "k"})
print(csv_data.df)
print("============================================================")

csv_data.commit_to_file()