import os

from lib.writemdict import MDictWriter

def create_mdx(filepath: str, data: dict={}, remove_db=False):
    db_file_path = filepath + '.db'
    if remove_db and os.path.exists(db_file_path):
        os.remove(db_file_path)
    
    dictionary = {
        "doe": "a deer, a female deer.",
        "ray": "a drop of golden sun.",
        "me": "a name I call myself.",
        "far": "a long, long way to run.",
    }
    dictionary.update(data)

    writer = MDictWriter(
        dictionary, 
        title="Example Dictionary", 
        description="This is an example dictionary."
    )
    with open(filepath, 'wb') as f:
        writer.write(f)