from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

# Assuming features and labels are already prepared
X_train, X_val, y_train, y_val = train_test_split(features, labels, test_size=0.2, random_state=42)

model = MLPClassifier(hidden_layer_sizes=(512, 256), max_iter=1000)
model.fit(X_train, y_train)

# Evaluate model
accuracy = model.score(X_val, y_val)
print(f"Validation Accuracy: {accuracy}")
