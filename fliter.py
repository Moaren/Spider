import json

fliter = Filiter()
file = "test_cases/1-253-802-0308.json"
fliter.dotask(file)

class Filiter:
	def __init__():
		pass

	def dotask(file):
		data = this.modify_info(file)
		this.store_in_new(data,file)

	def modify_info(self,file):
		with open(json_file,"r") as f:
                load_dict = json.load(f)
                load_dict.extend(data)
                # print(len(load_dict))
        with open(json_file, 'w') as f:
            f.write(json.dumps(load_dict))
        print(number + "'s info has been updated")

        with open(file,"r") as f:
        	load_lis = json.load(f)
        result = {"call_type":{},"caller":{}}
        for comment in loda_lis:
        	if(comment["call_type"]) not in result["call_type"]:
        		result["call_type"][comment["call_type"]] = 1
        	else:
        		result["caller"][comment["caller"]] += 1
        	if(comment["caller"]) not in result["caller"]:
        		result["caller"][comment["caller"]] = 1
        	else:
        		result["caller"][comment["caller"]] += 1
        return result

	def stroe_in_new(self,data,file):
		json_file = file.split(".json")[0] + "_filtered.json"
        with open(json_file, 'w') as f:
            f.write(json.dumps(data))
        print(number + "'s info has been flitered")




