import pickle
import numpy as np
import sklearn
from sklearn import svm
from sklearn.datasets import samples_generator
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_regression
from sklearn.pipeline import Pipeline


class ClassifyException(Exception):
    """Exception for class Classify"""
    def __init__(self,message):
        Exception.__init__(self,message)

class Classify:
    def __init__(self,patient_data=[]):
        """Loads classifers from classify folder
        
        features = [b'sex_male_flag' b'age_years' b'weight_kg' b'breathlessness_flag'
                    b'cough_flag' b'chest_pain_flag' b'fever_flag' b'nasal_symptoms_flag'
                    b'MRC_grade' b'copd_family_history_flag' b'allergy_family_history_flag'
                    b'allergy_personal_history_flag' b'biomass_cooking_history_flag'
                    b'smoking_flag' b'chewing_flag' b'alcohol_flag' b'num_cigarettes'
                    b'max_pfm_reading' b'max_pfm_reading_over_reference']
    
        """
        with open('classifiers/copd_2','rb') as f:
            self.copd_classifier = pickle.load(f,encoding='bytes')
            self.copd_features = pickle.load(f)
        with open('classifiers/ar_2','rb') as f:
            self.ar_classifier = pickle.load(f,encoding='bytes')
            self.ar_features = pickle.load(f)
        with open('classifiers/asthma_2','rb') as f:
            self.asthma_classifier = pickle.load(f,encoding='bytes')
            self.asthma_features = pickle.load(f)
        with open('classifiers/other_2','rb') as f:
            self.other_classifier = pickle.load(f,encoding='bytes')
            self.other_features = pickle.load(f)
        self.classifer_names = {'copd': 'chronic obstructive pulmonary disease',
                                'ar': 'allergic rhinitis',
                                'asthma': 'asthma',
                                'other': 'other disease'
                                }
        self.patient_data = patient_data
        print('copd_classifier = ' + str(self.copd_classifier))
        print('copd_features = ' + str(self.copd_features))
        print('len(copd_features) =' + str(len(self.copd_features)))

    
    def getPatientData(self):
        """Returns the patient's data"""
        return self.patient_data
    
    def setPatientData(self,patient_data):
        """Receives the patients's data and store it"""
        self.patient_data = patient_data
    
    def testCopd(self):
        patient_data=[0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0]
        if len(patient_data) != len(self.copd_features):
            raise ClassifyException('len(patient_data) != len(self.copd_features), ' +
                                    str(len(patient_data)) +' != ' + str(len(self.copd_features)))                              
        
        patient_data=[0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0]
        patient_data = np.array(patient_data)
        p = self.copd_classifier.predict(patient_data) #BUG HERE
        print('COPD predition = ' + str(p))
        
    
        
    
    def predictCOPD(self):
        pass
        
    
    




def main():
    C = Classify()
    C.testCopd()





if __name__ == '__main__':
    main()
    
    
"""
BUG

Traceback (most recent call last):
  File "classifier_01.py", line 88, in <module>
    main()
  File "classifier_01.py", line 81, in main
    C.testCopd()
  File "classifier_01.py", line 64, in testCopd
    p = self.copd_classifier.predict(patient_data)
  File "/usr/local/lib/python3.5/dist-packages/sklearn/utils/metaestimators.py", line 115, in __get__
    attrgetter(self.delegate_names[-1])(obj)
  File "/usr/local/lib/python3.5/dist-packages/sklearn/pipeline.py", line 186, in _final_estimator
    return self.steps[-1][1]
AttributeError: 'Pipeline' object has no attribute 'steps'
"""
