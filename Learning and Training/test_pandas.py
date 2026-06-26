import sys


def main() -> int:
    try:
        import pandas as pd
    except ImportError as exc:
        print("ERROR: pandas is not installed.")

        print(exc)
        return 1

    print("pandas version:", pd.__version__)
    df = pd.DataFrame(
        {
            "Name": ["Alice", "Bob", "Charlie"],
            "Age": [28, 34, 22],
            "Score": [85.5, 92.0, 78.0],
        }
    )

    print("\nDataFrame sample:")
    print(df)

    print("\nSummary statistics:")
    print(df.describe(include="all"))

    print("\nMean Score:", df["Score"].mean())
    print("Total Age:", df["Age"].sum())

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
