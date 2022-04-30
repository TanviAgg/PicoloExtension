import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.model_selection import train_test_split

BETA_0_INTERCEPT = "beta_0_"
TARGET_FEATURE_NAME = "rent"
RANDOM_SEED = 42

def split_data(df, train_percentage):
    # Splitting dataset into train and test (Randomly select 80% for train)
    train, test = train_test_split(df, test_size=1-train_percentage/100, random_state=RANDOM_SEED)
    return train, test


def compute_beta_matrix(df, features):
    """
    BETA estimate = inv(X_t.X).X_t.Y
    :param df: train df
    :param features: input features
    :return: beta estimate values
    """
    k = len(features)
    X = df[features].values
    Y = df[[TARGET_FEATURE_NAME]].values

    XT = X.transpose()
    XT_X_inverse = np.linalg.inv(XT.dot(X))
    beta_estimate = XT_X_inverse.dot(XT).dot(Y)

    beta_values = pd.DataFrame(beta_estimate, columns=['Beta Values'], index=['beta_' + str(i) for i in range(k)])
    beta_values["feature"] = features
    return beta_estimate, beta_values


def predict_values_using_beta(beta_estimate, df, features):
    """
    compute the SSE between actual and predicted Y values
    :param beta_estimate: beta estimate computed above
    :param df: test df
    :param features: input features
    :return: SSE
    """
    X = df[features].values
    Y = df[[TARGET_FEATURE_NAME]].values

    Y_pred = X.dot(beta_estimate)
    residual = Y - Y_pred
    sse = np.sum(residual ** 2)

    return Y, Y_pred, sse


if __name__ == "__main__":
    rent_df = pd.read_csv('./datasets/q5.csv')
    print(rent_df["rent"].describe())

    # to account for beta_0 intercept we add a column with all values equal to 1
    rent_df.insert(2, BETA_0_INTERCEPT, 1.0)

    train_df, test_df = split_data(rent_df, train_percentage=80)

    print("---------------- part a -----------------")
    features_part_a = [BETA_0_INTERCEPT, "bedrooms", "bathrooms", "size_sqft"]
    beta_estimate_part_a, beta_values_part_a = compute_beta_matrix(train_df, features_part_a)
    _, _, sse_part_a = predict_values_using_beta(beta_estimate_part_a, test_df, features_part_a)
    print(beta_values_part_a)
    print("\nSSE using the first three features is {}\n".format(round(sse_part_a, 4)))

    print("---------------- part b -----------------")
    features_part_b = [BETA_0_INTERCEPT, "bedrooms", "bathrooms", "size_sqft", "floor"]
    beta_estimate_part_b, beta_values_part_b = compute_beta_matrix(train_df, features_part_b)
    _, _, sse_part_b = predict_values_using_beta(beta_estimate_part_b, test_df, features_part_b)
    print(beta_values_part_b)
    print("\nSSE using the first four features is {}\n".format(round(sse_part_b, 4)))

    print("---------------- part c -----------------")
    features_part_c = [BETA_0_INTERCEPT, "bedrooms", "bathrooms", "size_sqft", "floor",
                       "has_roofdeck", "has_washer_dryer", "has_doorman", "has_elevator",
                       "has_dishwasher", "has_patio", "has_gym"]
    beta_estimate_part_c, beta_values_part_c = compute_beta_matrix(train_df, features_part_c)
    _, _, sse_part_c = predict_values_using_beta(beta_estimate_part_c, test_df, features_part_c)
    print(beta_values_part_c)
    print("\nSSE using the first four features including amenities is {}\n".format(round(sse_part_c, 4)))

    print("---------------- part d -----------------")
    features_part_d = [BETA_0_INTERCEPT, "bedrooms", "bathrooms", "size_sqft", "floor",
                       "has_roofdeck", "has_washer_dryer", "has_doorman", "has_elevator",
                       "has_dishwasher", "has_patio", "has_gym", "building_age_yrs"]
    beta_estimate_part_d, beta_values_part_d = compute_beta_matrix(train_df, features_part_d)
    _, _, sse_part_d = predict_values_using_beta(beta_estimate_part_d, test_df, features_part_d)
    print(beta_values_part_d)
    print("\nSSE using the first four features including amenities and building_age_yrs is {}\n".format(round(sse_part_d, 4)))



