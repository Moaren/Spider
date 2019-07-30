import json
import glob, os


class Filiter:
    summary_file = "summary.json"

    def __init__(self, parent_dir):
        self.parent_dir = parent_dir


    def dotask(self,file):
        data = self.modify_info(file)
        self.store_in_new(data,file)
        print(file + " has been flitered. ")

    def modify_info(self,file):
        file = parent_dir + file
        print(file)
        with open(file,"r") as f:
            load_lis = json.load(f)
        result = {}
        for comment in load_lis:
            if(comment["call_type"] == ""):
                continue
            if (comment["call_type"]) not in result.keys():
                result[comment["call_type"]] = []
            else:
                result[comment["call_type"]].append(comment["content"])
        return result

    def store_in_new(self,data,file):
        store_file = parent_dir+ 'result\\' + file
        json_file = store_file.split(".json")[0] + "_filtered.json"
        with open(json_file, 'w') as f:
            f.write(json.dumps(data))
        self.add_to_summary(data,file)

    def add_to_summary(self, data, file):
        summary_file = parent_dir + 'result\\' + Filiter.summary_file

        with open(summary_file,"r") as f:
            result = json.load(f)

        # result = {"number_info":{number:{"call_type":no,...},...},"summary":{"call_type":no,...}}
        number = file.split(".json")[0]

        if "number_info" not in result.keys():
            result["number_info"] = {}
        if number not in result["number_info"].keys():
            result["number_info"][number] = {}
        if "summary" not in result.keys():
            result["summary"] = {}

        for key,value in data.items():
            result["number_info"][number][key] = len(value)
            if(key in result["summary"].keys()):
                result["summary"][key] += len(value)
            else:
                result["summary"][key] = 0

        with open(summary_file, 'w') as f:
            f.write(json.dumps(result))




parent_dir = 'C:\\Users\\wang_cheng\\git_stuff\\crawler\\800notes\\original\\Spider\\800notes\\'
# parent_dir.replace("\\","/")
# parent_dir += "/"
# print(parent_dir)
fliter = Filiter(parent_dir)


for file in glob.glob(os.path.join(parent_dir, '*.json')):
    st = file[len(parent_dir)-1]
    fliter.dotask(file.split(st)[-1])
    # n

