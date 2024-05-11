#DEVARSH VORA
#1002159763

import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings("ignore")

# Get the current working directory
current_dir = os.getcwd()

# Construct the relative path to the CSV file
file_path = os.path.join(current_dir, 'nba_stats.csv')

# Load the dataset
df = pd.read_csv(file_path)

# Encode the 'Pos' column into numerical values
label_encoder = LabelEncoder()
df['Pos_encoded'] = label_encoder.fit_transform(df['Pos'])

# Select numeric columns only
numeric_columns = df.select_dtypes(include=['int64', 'float64'])

# Calculate correlation of each numeric column with 'Pos'
correlation_with_pos = {}
for column in numeric_columns.columns:
    correlation_with_pos[column] = df[column].corr(df['Pos_encoded'])

# Convert dictionary to DataFrame
correlation_df = pd.DataFrame.from_dict(correlation_with_pos, orient='index', columns=['Correlation_with_Pos'])

# Sort correlation values in ascending order
correlation_df_sorted = correlation_df.sort_values(by='Correlation_with_Pos')

# Plot the correlation values
plt.figure(figsize=(10, 6))
correlation_df_sorted.plot(kind='bar', color='skyblue')
plt.title('Correlation with "Pos"', fontsize=16)
plt.xlabel('Numeric Columns')
plt.ylabel('Correlation with "Pos"')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Selecting feature column based on above correlation chart
class_column = 'Pos'
feature_columns = ['FG%', '3P%',  '2P%', 'FT%', 'eFG%' , 'ORB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
df_feature = df[feature_columns]
df_class = df[class_column]

# Standardize features
df_feature = pd.DataFrame(StandardScaler().fit_transform(df_feature))

# Split data into training and testing sets with random_state
train_feature, test_feature, train_class, test_class = train_test_split(df_feature, df_class, stratify=df_class, train_size=0.80, test_size=0.20, random_state=0)

# Create and train a Multi-Layer Perceptron classifier
model = MLPClassifier(hidden_layer_sizes=(30,), max_iter=500, alpha=0.001,
                      solver='adam', verbose=0,  random_state=1,
                      learning_rate_init=0.001)

model.fit(train_feature, train_class)
predict = model.predict(test_feature)

train_predict = model.predict(train_feature)
train_accuracy = accuracy_score(train_class, train_predict)
print("\nTraining set accuracy:", train_accuracy)
print("\nValidation set accuracy: {:.2f}\n\n".format(model.score(test_feature, test_class)))

# Print confusion matrix for training set
print("Confusion Matrix for Training Set")
print("{}".format(train_class.unique()))
print(confusion_matrix(train_class, train_predict, labels=train_class.unique()))

# Print confusion matrix for validation set
print("\nConfusion Matrix for Validation Set")
print("{}".format(test_class.unique()))
print(confusion_matrix(test_class, predict, labels=test_class.unique()))
print("-" * 80)

# Stratified Cross-validation
skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=0)
scores = []
for train_index, test_index in skf.split(df_feature, df_class):
    X_train, X_test = df_feature.iloc[train_index], df_feature.iloc[test_index]
    y_train, y_test = df_class.iloc[train_index], df_class.iloc[test_index]
    model.fit(X_train, y_train)
    scores.append(model.score(X_test, y_test))

print("\n\nAccuracy in each Fold:\n{}".format(scores))  
print("\nAvg cross val score: {:.2f}\n\n".format(sum(scores)/10))
print("-" * 80)

# FOR DUMMY_TEST.csv

def test_model_with_new_data(test_def):
    # Get the current working directory
    current_dir = os.getcwd()

    file_path = os.path.join(current_dir, 'dummy_test.csv')

    # Load the dataset
    test_df = pd.read_csv(file_path)
    # Preprocess the test data
    test_df_feature = test_df[feature_columns]
    test_df_feature = pd.DataFrame(StandardScaler().fit_transform(test_df_feature))
    test_df_class = test_df[class_column]
    
    # Evaluate the model on the new test data
    test_accuracy = model.score(test_df_feature, test_df_class)
    predict = model.predict(test_df_feature)
    conf_matrix = confusion_matrix(test_df_class, list(predict), labels=test_df_class.unique())
    
    print("\nTest set accuracy (Dummy_test): {:.2f}\n\n".format(test_accuracy))
    print("\nConfusion Matrix")
    print("{}".format(test_df_class.unique()))
    print(conf_matrix)
    
test_model_with_new_data('test_df')