import os
import pandas as pd
# Each website is a separate project (folder)
def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating directory ' + directory)
        os.makedirs(directory)


# Create queue and crawled files (if not created)
def create_data_files(project_name, base_url): #√
    queue = os.path.join(project_name , 'queue.csv')
    crawled = os.path.join(project_name,"crawled.csv")
    if not os.path.isfile(queue):
        write_file(queue, base_url)
    if not os.path.isfile(crawled):
        # write_file(crawled, None)
        with open(crawled, "w") as my_empty_csv:
            pass

# Create a new file
def write_file(path, data): #√
    if type(data) != type([]): #Convert the data type to list
        data = [data]
    df = pd.DataFrame(data)
    df.to_csv(path, index=False, header=None)


# Add data onto an existing file
def append_to_file(path, data): #√
    if type(data) != type([]): #Convert the data type to list
        data = [data]
    df = pd.DataFrame(data)
    df.to_csv(path, index=False, mode = "a", header=False)

# # Delete the contents of a file
# def delete_file_contents(path):
#     open(path, 'w').close()


# Read a file and convert each line to set items
def file_to_set(file_name):
    # results = set()
    # with open(file_name, 'rt') as f:
    #     for line in f:
    #         results.add(line.replace('\n', ''))
    # return results
    try:
        df = pd.read_csv(file_name, header=None)
    except Exception:
        return set()
    results = set(_[0] for _ in df.values)
    return results


# Iterate through a set, each item will be a line in a file
def set_to_file(links, file_name):
    # print(links)
    df = pd.DataFrame(sorted(links))
    df.to_csv(file_name, index=False, header=False)
    # with open(file_name,"w") as f:
    #     for l in sorted(links):
    #         try:
    #             f.write(l+"\n")
    #         except Exception:
    #             pass


# project = "800notes"
# # base_url = "https://800notes.com/Phone.aspx/1-240-273-1357"
# # create_data_files(project,base_url)