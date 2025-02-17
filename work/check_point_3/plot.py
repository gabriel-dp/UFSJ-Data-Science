import matplotlib.pyplot as plt
import seaborn as sns

def generate_plot(df, x, y, x_label, y_label):
    df = df.sort_values(y, ascending=True)

    plt.figure(figsize=(12, 6))
    sns.barplot(x=x, y=y, data=df, palette='YlOrRd')

    plt.xlabel(x_label, fontsize=14)
    plt.ylabel(y_label, fontsize=14)

    return plt
