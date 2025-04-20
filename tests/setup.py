import os

temp_dir = os.path.join(os.getcwd(), 'tests/temp')
if not os.path.exists(temp_dir):
    os.mkdir(temp_dir)

mocks_dir = os.path.join(temp_dir, 'mocks')
if not os.path.exists(mocks_dir):
    os.mkdir(mocks_dir)

for item in os.listdir(mocks_dir):
    item_path = os.path.join(mocks_dir, item)

    if os.path.isfile(item_path):
        os.remove(item_path)