import pandas as pd
from sklearn.preprocessing import LabelEncoder
import os

def preprocess_data(
    input_path: str,
    output_path: str
):
 
    df = pd.read_csv(input_path)
    # Mengatur missing values
    num_cols = df.select_dtypes(include=["int64", "float64"]).columns
    cat_cols = df.select_dtypes(include=["object", "bool"]).columns
    df[num_cols] = df[num_cols].fillna(df[num_cols].median())

    for col in cat_cols:
        df[col] = df[col].fillna(df[col].mode()[0])

    #  Menangani outlier sederhana
    if "Study Hours" in df.columns:
        df["Study Hours"] = df["Study Hours"].clip(lower=0, upper=10)

    if "Attendance (%)" in df.columns:
        df["Attendance (%)"] = df["Attendance (%)"].clip(lower=0, upper=100)

    encoder = LabelEncoder()

    for col in ["Gender", "ParentalSupport", "Online Classes Taken"]:
        if col in df.columns:
            df[col] = encoder.fit_transform(df[col])

    drop_cols = ["StudentID", "Name"]
    df = df.drop(columns=[c for c in drop_cols if c in df.columns])

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)

    print("seles!!!")


if __name__ == "__main__":
    INPUT_PATH = "student_raw/student_performance_updated_1000.csv"
    OUTPUT_PATH = "student_clean/student_performance_clean.csv"

    preprocess_data(INPUT_PATH, OUTPUT_PATH)