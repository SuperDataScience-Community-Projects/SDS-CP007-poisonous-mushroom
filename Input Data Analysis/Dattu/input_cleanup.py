import pandas
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

class MushroomClassificationProject(object):

    def __init__(self):
        self.datasets = {
            'primary': '/Users/dots/Documents/Data Science Projects/Poisonous Mushroom Classification/Data Sets/MushroomDataset/primary_data2.csv',
            'secondary': '/Users/dots/Documents/Data Science Projects/Poisonous Mushroom Classification/Data Sets/MushroomDataset/secondary_data2.csv',
        }

        self.output = {
            'primary': '/Users/dots/Documents/Data Science Projects/Poisonous Mushroom Classification/Data Sets/MushroomDataset/primary_data_op.xlsx',
            'secondary': '/Users/dots/Documents/Data Science Projects/Poisonous Mushroom Classification/Data Sets/MushroomDataset/secondary_data_op.xlsx',
            'sec_plot': '/Users/dots/Documents/Data Science Projects/Poisonous Mushroom Classification/Data Sets/MushroomDataset/secondary_hist.pdf',
        }
        self.primary_exploratory_dfs = {
            "NULL": "default",
            "VALUE_COUNTS": "default",
            "CARDINALITY": "default",
        }

        self.secondary_exploratory_dfs = {
            "NULL": "default",
            "VALUE_COUNTS": "default",
            "CARDINALITY": "default",
        }

        self.secondary_numeric_cols = ['cap-diameter', 'stem-height', 'stem-width']

    def create_report(self):
        df_primary = self.read_data(self.datasets['primary'])
        self.primary_exploratory_dfs['NULL'] = self.get_null_info(df_primary)
        self.primary_exploratory_dfs['VALUE_COUNTS'] = self.get_value_measures(df_primary)
        self.primary_exploratory_dfs['CARDINALITY'] = self.get_cardinality(df_primary)

        self.write_excel(self.primary_exploratory_dfs, self.output['primary'])

        df_secondary = self.read_data(self.datasets['secondary'])
        self.secondary_exploratory_dfs['NULL'] = self.get_null_info(df_secondary)
        self.secondary_exploratory_dfs['VALUE_COUNTS'] = self.get_value_measures(df_secondary)
        self.secondary_exploratory_dfs['CARDINALITY'] = self.get_cardinality(df_secondary)

        self.write_excel(self.secondary_exploratory_dfs, self.output['secondary'])
        self.generate_histogram_numeric_cols(df_secondary, self.secondary_numeric_cols, self.output['sec_plot'])

    def generate_histogram_numeric_cols(self, df_hist, numeric_cols, pdf_path):
        with PdfPages(pdf_path) as pdf:
            for col in numeric_cols:
                # Create a new figure for each histogram
                fig, ax = plt.subplots()

                # Plot the histogram
                df_hist[col].hist(ax=ax)
                ax.set_title(col)

                # Save the figure to the PDF
                pdf.savefig(fig)
                plt.close(fig)

    def write_excel(self, df_dict, path):
        with pandas.ExcelWriter(path, engine='xlsxwriter') as writer:
            for key in df_dict:
                df_dict[key].to_excel(writer, sheet_name=key, index=False)

    def read_data(self, path):
        df = pandas.read_csv(path, on_bad_lines='skip')
        return df

    def get_value_measures(self, df_data):
        cat_cols = df_data.select_dtypes(include=object).columns.tolist()
        df = pandas.DataFrame(
            df_data[cat_cols].melt(var_name='column', value_name='value').value_counts()).sort_values(
            by=['column', 'count']).reset_index()

        new_column = df.groupby(['column'])['count'].apply(lambda x: x / x.sum())
        df['count_%age'] = new_column.reset_index(level=0, drop=True)

        return df

    def get_value_measures1(self, df_data):
        cat_cols = df_data.select_dtypes(include=object).columns.tolist()
        df = pandas.DataFrame(
            df_data[cat_cols].melt(var_name='column', value_name='value').value_counts()).sort_values(
            by=['column', 'count']).reset_index()

        new_column = df.groupby(['column'])['count'].apply(lambda x: 100 * x / x.sum())
        df['count_%age'] = new_column.reset_index(level=0, drop=True)

        return df

    def get_cardinality(self, df_data):
        df = df_data.nunique().to_frame("Cardinality").reset_index().rename(
            columns={'index': 'colnames'})

        return df

    def get_null_info(self, df_data):
        df = df_data.isnull().sum().to_frame('nullcount').reset_index().rename(
            columns={'index': 'colnames'})

        return df


if __name__ == '__main__':
    report = MushroomClassificationProject()
    report.create_report()
