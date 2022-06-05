import os
import pickle
import datetime
import numpy as np
from utils.tikzutils import TikzDocument

SAMPLE_DATA = [
    {
        'id': '6DF37H',
        'full_name': 'Alice Amber',
        'gender': 'FEMALE',
        'date_of_birth':'1990-10-01',
        'height': 160,
        'weight': 45,
    },
    {
        'id': '4EZ19L',
        'full_name': 'Bob Brian',
        'gender': 'MALE',
        'date_of_birth':'1989-08-24',
        'height': 170,
        'weight': 85,
    },
    {
        'id': '7GN61P',
        'full_name': 'Charlie Craig',
        'gender': 'MALE',
        'date_of_birth':'1996-02-11',
        'height': 190,
        'weight': 68,
    },
    {
        'id': '2TS85A',
        'full_name': 'Diana Dakota',
        'gender': 'FEMALE',
        'date_of_birth':'1992-05-13',
        'height': 152,
        'weight': 64,
    },

]

def make_binning(attr, attrbin):
    attr_binned = np.digitize(attr, attrbin, right=False) # range: attrbin[i-1] <= x < attrbin[i]
    uniques, counts = np.unique(attr_binned, return_counts=True)
    binnames = np.asarray([r'$<'+f'{attrbin[0]}$']+[f'${attrbin[i]}-{attrbin[i+1]-1}$' for i in range(len(attrbin)-1)]+[r'$\geq'+f'{attrbin[-1]}$'])
    bins = binnames[uniques]
    return bins, counts

if __name__ == "__main__":

    filename = os.path.join('data', 'demographics_data.pkl')
    #filename = 'na.pkl'
    final_attributes = ['gender', 'age', 'height', 'bmi'] # final attributes to be released

    base_attributes = ['gender', 'date_of_birth', 'height', 'weight'] # attributes that are already contained in the dictionary
    derivate_attributes = ['age', 'bmi'] # attributes that are derived from the base attributes
    start_date = '2022-05-25'


    attributes_bins = {
                        'gender': None, # if None, attributes are not binned and are aggregated as they are
                        'age': [25, 30, 35, 40, 45],
                        'height': list(range(160, 200, 10)), # bins will be <160, 160-170, ..., 180-190, >190
                        'bmi': list(range(20, 45, 5)),
    } # bins for the attributes
    attribute_names = {
                        'gender': 'Gender',
                        'age': 'Age',
                        'height': 'Height',
                        'bmi': 'BMI',
    } # names for the attributes

    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            user_data = pickle.load(f)
    else:
        user_data = SAMPLE_DATA

    # convert list of dictionaries to dictionary of lists
    # {'gender': ['FEMALE', 'MALE', ...], 'date_of_birth': ['1990-10-01', '1989-08-24',...], ...}
    attr_data = {attr: [user[attr] for user in user_data] for attr in base_attributes}

    # compute age
    if 'age' in derivate_attributes:
        start_datetime = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        attr_data['age'] = [(start_datetime-datetime.datetime.strptime(dob, '%Y-%m-%d')).days//365
                                for dob in attr_data['date_of_birth']
        ]

    # compute bmi
    if 'bmi' in derivate_attributes:
        attr_data['bmi'] = [w/(h/100)**2 for w, h in zip(attr_data['weight'], attr_data['height'])]

    for attr in final_attributes:
        if attributes_bins[attr] is not None:
            bins, counts = make_binning(attr_data[attr], attributes_bins[attr])
        else:
            bins, counts = np.unique(attr_data[attr], return_counts=True)

        hist_dict = {bin: count for bin, count in zip(bins, counts)}

        doc = TikzDocument(attr.capitalize(), None)

        doc.add_histogram(hist_dict, title=attr.capitalize(), wbar=0.2 if attr=='gender' else 0.4, floating=None)
        doc.save_document(f'out/{attr}.tex')
    exit(0)
