import joblib
clf = joblib.load("model/clf.pkl")
print(clf.n_features_in_)  # Should print 384
