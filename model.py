
def transform(data)
    return something

if __name__ == '__main__':
    data = processing()
    X, y = transform(data)
    model = LogisticWhatever()
    model.fit(X, y)
    y_pred = model.predict(data)
    print f1_score(y_actual, y_pred)