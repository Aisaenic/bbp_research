#!/usr/bin/env python3 

import argparse
import json 
import csv
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay
from sklearn.model_selection import RandomizedSearchCV, train_test_split, cross_val_score
from scipy.stats import randint
from sklearn.tree import export_graphviz
from sklearn.preprocessing import StandardScaler
from IPython.display import Image
import graphviz

#Parses command line args, one command line arg exists, csv file with cleaned and tagged data 
#Input: None 
#Output: csv file
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset")
    args = parser.parse_args()
    dataset = args.dataset
    return dataset

#Processes the csv file which contains the data 
#Input: csv file 
#Output: a list containing the features in a numpy array, the labels in a numpy array, and the names of the features in list form
def ingest_dataset(file):
    #put the featureset into pandas
    features = pd.read_csv(file)
    #one hot encoding to transform categorical data to numerical 
    features = pd.get_dummies(features) 
    #put the labels into array
    labels = np.array(features['tag'])
    #now that labels are in array, drop labels from features 
    features = features.drop('tag', axis=1)
    #save feature names 
    feature_names = list(features.columns)
    #convert features to array 
    features = np.array(features) 
    #return feature and label arrays, and list of feature names
    return [features, labels, feature_names]

#Creates and trains the classifier model and calculates scores
#Two basic models are in this function, random forest and k nearest neighbors
#Calculates accuracy, precision, and recall of the model
#Input: numpy array of features, numpy array of labels, list of feature names
#Output: N/A 
def train_model(features, labels, feature_names): 
    #split the data randomly into training and test sets, size of test set is 25% of data 
    train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size = 0.25, random_state = 42)
    #the two models, rf and knn, comment out the one you don't want to run 
    #model = RandomForestClassifier()
    model = KNeighborsClassifier(n_neighbors=51) 
    #train the model on the training dataset
    model.fit(train_features, train_labels)
    #use the trained model to predict the test features 
    predictions = model.predict(test_features)
    #calculate the accuracy
    accuracy = accuracy_score(test_labels, predictions)
    print("Accuracy: ", accuracy)
    #calculate the precision
    precision = precision_score(test_labels, predictions)
    print("Precision: ", precision)
    #calculate the recall 
    recall = recall_score(test_labels, predictions)
    print("Recall: ", recall) 
    
    #these next 3 lines are to improve the rf model (hyperparameter, feature importance) and knn model (best k)
    #uncomment them if you want to run them, your computer will be sad if you try to run more than one at a time
    #hyperparameter_model(train_features, test_features, train_labels, test_labels, feature_names, model)
    #feature_importance_model(train_features, test_features, train_labels, test_labels, feature_names, model) 
    #best_k_value(features, labels)

#Optimizes for finding the best value of k in knn model 
#Input: Numpy array of features, numpy array of labels 
#Output: N/A
def best_k_value(features, labels): 
    #number of neighbors to check out
    k_values = [i for i in range (1,50)]
    scores = []
    #standardizing the dataset. If you want to do it without standardization, can comment out the next two lines, but I tried both and the result didn't change
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)
    #create knn models with each number of neighbors and see how they do 
    for k in k_values:
        knn = KNeighborsClassifier(n_neighbors=k)
        score = cross_val_score(knn, features, labels, cv=5)
        print(score) 
        scores.append(np.mean(score))
    #show all scores for each number of neighbors to be able to tell which k was best 
    for val in scores: 
        print(scores.index(val), val) 

#Optimizes for finding the best hyperparameters for rf model 
#Inputs: numpy arrays of training features, testing features, training labels, testing labels; list of feature names, an rf model
#Outputs: N/A 
def hyperparameter_model(train_features, test_features, train_labels, test_labels, feature_names, model):
    #adjust number of trees 
    n_estimators = [int(x) for x in np.linspace(start = 200, stop = 2000, num = 10)]
    #adjust max depth
    max_depth = [int(x) for x in np.linspace(10, 110, num = 11)]
    max_depth.append(None)
    #adjust samples required to split a node 
    min_samples_split = [2, 5, 10]
    #adjust samples required at each leaf node 
    min_samples_leaf = [1, 2, 4] 
    #adjust bootstrapping for choosing samples 
    bootstrap = [True, False] 

    #create random grid that optimizer will circle through to try hyperparameters
    random_grid = {'n_estimators': n_estimators, 'max_depth': max_depth, 'min_samples_split': min_samples_split, 'min_samples_leaf': min_samples_leaf, 'bootstrap': bootstrap}
    #create a random search model to find hyperparamaters, using 5-fold CV and 100 iterations 
    model_random = RandomizedSearchCV(estimator = model, param_distributions = random_grid, n_iter = 100, cv = 5, verbose=2, random_state=42, n_jobs=-1)
    #train the hyperparameter search model
    model_random.fit(train_features, train_labels)
    #display what the best parameters are 
    print(model_random.best_params_)
    #make a prediction with these improved hyperparameters
    random_predictions = model_random.predict(test_features)
    #calculate new accuracy
    random_accuracy = accuracy_score(test_labels, random_predictions)
    print("new accuracy is ", random_accuracy)
    #calculate new precision
    random_precision = precision_score(test_labels, random_predictions)
    print("new precision is ", random_precision)
    #calculate new recall
    random_recall = recall_score(test_labels, random_predictions)
    print("new recall is ", random_recall)

#Optimizes for finding the best feature parameters for the model 
#Input: numpy arrays of training features, testing features, training labels, testing labels; list of feature names, an rf model
#Output: N/A 
def feature_importance_model(train_features, test_features, train_labels, test_labels, feature_names, model):
    #determine the importance features 
    importances = list(model.feature_importances_)
    feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(feature_names, importances)]
    feature_importances = sorted(feature_importances, key = lambda x:x[1], reverse = True)
    sorted_importances = [importance[1] for importance in feature_importances]
    sorted_features = [importance[0] for importance in feature_importances]
    cumulative_importances = np.cumsum(sorted_importances)
    #separate the non-important features out of training and testing sets 
    important_feature_names = [feature[0] for feature in feature_importances[0:5]]
    important_indices = [feature_names.index(feature) for feature in important_feature_names]
    important_train_features = train_features[:, important_indices]
    important_test_features = test_features[:, important_indices] 
    print(important_train_features)
    
    #train the model on only the important features
    model.fit(important_train_features, train_labels)
    #make prediction using important features 
    predictions_important = model.predict(important_test_features) 
    #calculate accuracy, precision, and recall using important features 
    accuracy_important = accuracy_score(test_labels, predictions_important)
    precision_important = precision_score(test_labels, predictions_important)
    recall_important = recall_score(test_labels, predictions_important)
    print("Accuracy with important features is ", accuracy_important) 
    print("new precision is ", precision_important)
    print("new recall is ", recall_important) 

def main():
    data_file = parse_args()
    ingest_result = ingest_dataset(data_file)
    feature_array = ingest_result[0]
    label_array = ingest_result[1]
    feature_names = ingest_result[2]
    train_model(feature_array, label_array, feature_names)

main()
