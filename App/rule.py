import json

class Rule:
################################################################################
# setting the membervars of the newly initialised class
# 
# @param name header aka name of the rule
# @param id specified number of the rule (not truly unique)
# @param text the details of the rule (including advanced formatting)
################################################################################
    def __init__(self, name, id, text):
        self.id = id
        self.name = name
        self.text = text

################################################################################
# getting the name of the rule
################################################################################
    def getName(self):
        return self.name

################################################################################
# getting the id of the rule
################################################################################
    def getId(self):
        return self.id

################################################################################
# getting the text of the rule
################################################################################
    def getText(self):
        return self.text

################################################################################
# setting the text of the rule
################################################################################
    def setText(self, text):
        self.text = text

################################################################################
# setting the name of the rule
################################################################################
    def setName(self, name):
        self.name = name


################################################################################
# scanning the given file for rules and returning an array of rules
# returns empty array if there are none or there is an error
################################################################################
def scanRules(path):
    rules = []
    try:
        with open(path, 'r') as file:
            data = file.read()

        rules_dict = json.loads(data)

        for rule in rules_dict:
            tmp_rule = Rule(rule['name'], rule['id'], rule['text'])
            rules.append(tmp_rule)

    except:
        print('No rules')
    
    return rules

        
