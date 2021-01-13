import json
from watson_developer_cloud import VisualRecognitionV3

visual_recognition = VisualRecognitionV3(
        '2018-03-19',
        iam_apikey='w6FTQKH4TkK_2C8x9JS_RJ3tHKqzQh_lq-Y2lOA98b_2')

# Create the classifiers
def create():
    with open('./Images/masks_on.zip', 'rb') as masks_on, \
        open('./Images/masks_off.zip', 'rb') as masks_off:
        
        response = visual_recognition.create_classifier(
            'people',
            masks_on_positive_examples = masks_on,
            masks_off_positive_examples = masks_off
            ).get_result()
        print(json.dumps(response, indent=2))

def get():
    response = visual_recognition.get_classifier('people_1591545932').get_result()
    print (json.dumps(response, indent=1))

def list():
    classifiers = visual_recognition.list_classifiers(verbose=False).get_result()
    print(json.dumps(classifiers, indent=2))

# Classify test data
def classify(path):
    #with open('./Images/test/test_on.jpeg', 'rb') as test_zip:
    with open(path, 'rb') as test_zip:
        response = visual_recognition.classify(
            test_zip,
            threshold='0.5',
            classifier_ids='people_1591545932').get_result()
            
        #print(json.dumps(response, indent=2))
    
        class_and_score = response['images'][0]['classifiers'][0]['classes']
        
        return class_and_score


#create()

#get()

#list()

# --- To test out classification without going through the GUI ---
# --- uncomment the code below, remove "path" parameter from the ---
# --- function  decleration, and replace the "with open(.." with the static path ---
# --- Then, run this file. ---

#classify()





        
    
