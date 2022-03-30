from sklearn.pipeline import Pipeline
import pickle 
from sklearn.neural_network import MLPClassifier
import pandas as pd
from sklearn.preprocessing import StandardScaler

#Ouvre le fichier csv
data = pd.read_csv("./Breast_cancer Dataset/breast_cancer.csv",";", index_col="ID_REF")

ToReplace = ['breast cancer','non cancer','benign breast disease', 'prostate disease'] 
Values = [1, 0, 0, 0]
data['ETAT'] = data['ETAT'].replace(to_replace=ToReplace, value=Values)

#x prends tout les columns en entrée, y tout les columns en sortie
x=data.drop(columns=["ETAT"])
y=data["ETAT"]



MLP = MLPClassifier(activation='tanh', solver='lbfgs', hidden_layer_sizes=[50,10])

P = Pipeline([('SS', StandardScaler()),
              ('classifieur',MLP)])
P.fit(x,y)  
pickle.dump(P, open('model_breast_cancer.pkl','wb'))