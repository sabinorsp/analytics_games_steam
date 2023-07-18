import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import StratifiedKFold
from sklearn.base import clone
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix

class EDA:

    @staticmethod
    def load_data_csv_by_file(path: str, sep: str, encoding: str) -> dict:
        """
        Loads all CSV files from a directory and returns a dictionary of dataframes.

        Parameters:
            path (str): The path of the directory containing the CSV files.
            sep (str): The separator character used in the CSV files.
            encoding (str): The encoding of the CSV files.

        Returns:
            Dict[str, pd.DataFrame]: A dictionary where each key is the name of a CSV file (without the '.csv' extension)
                                    and each value is a pandas dataframe containing the data from the corresponding CSV file.
        """
        df_dic = {}
        for filename in os.listdir(path):
            if filename.endswith('.csv'):
                file_path = os.path.join(path, filename)
                df_dic[filename.replace('.csv','')] = pd.read_csv(file_path, sep=sep, encoding=encoding)
        return df_dic


    @staticmethod
    def summary_dataframes(df) -> print :
        """ 
        Return a summary about total register, type of columns, values null and 
        rows duplicated.
        
        Args:
            df (pandas.DataFrame) : Summary data with, total lenght rows, df.info(), Total Null values,
                                    total values duplicated.
        """
        na_values = pd.DataFrame(df.isna().sum(), columns=['Total Values null'])
        na_values['%_weight'] = na_values['Total Values null'].apply(lambda x: x/df.shape[0]*100)
        duplicated = df.duplicated().sum()
        total_rows = df.shape[0]
        print(f'Quantidade total de registros:{total_rows}. \n\n')
        print(df.info())
        print(f'\n\n Total Valores nulos:\n {na_values} \n\n')
        print(f'Total valores duplicados: \n {duplicated} ->  {round(duplicated/total_rows*100,2)} %')


    @staticmethod
    def plot_balanced_class(series):
        """
        Plot the counts and percentages of a balanced class series using a bar chart.

        Args:
            series (pandas.Series): A pandas Series object representing a balanced class.

        Returns:
            None.

        Example:
            >>> import pandas as pd
            >>> import numpy as np
            >>> import seaborn as sns
            >>> import matplotlib.pyplot as plt
            >>> np.random.seed(42)
            >>> series = pd.Series(np.random.choice(['A', 'B', 'C'], size=100))
            >>> plot_balanced_class(series)
        """
        value_counts = series.value_counts()
        percentages = value_counts / len(series) * 100
        colors = sns.color_palette('colorblind')
        plt.bar(value_counts.index, value_counts.values, color=colors)
        
        # add percentage labels to each bar
        for i, count in enumerate(value_counts):
            percentage = round(percentages[i], 2)
            plt.text(i, count + 0.5, f'{percentage}%', ha='center', fontsize=10)

        # set the title and axis labels
        plt.title('Balanced Class Plot to:'+ series.name)
        plt.xlabel('Values')
        plt.ylabel('Counts')
        plt.show()


    @staticmethod
    def reverse_dict(dic:dict) -> dict:
        ''' 
            Arg: dic = {key:value}, value is type list;
            Return a new dictionary with the reverse original key:value;
        '''
        return {val: key for key,value in dic.items() for val in value}
    

class ML:

    def cross_val(X_train: list, y_train: list, n_splits: int) -> float:
        """
        Perform cross validation on the given dataset using StratifiedKFold method.
        
        Parameters:
            X_train (list): List of training data
            y_train (list): List of labels for the training data
            n_splits (int): Number of folds for cross validation
            
        Returns:
            float: Proportion of correct predictions

        Obs: 
            Necessary import packages: 
                from sklearn.model_selection import StratifiedKFold
                from sklearn.base import clone
        """
        skfolds = StratifiedKFold(n_splits)
        for train_index, test_index in skfolds.split(X_train, y_train):
            clone_clf = clone(sgd_clf)
            X_train_folds = X_train[train_index]
            y_train_folds = y_train[train_index]
            X_test_fold = X_train[test_index]
            y_test_fold = y_train[test_index]

            clone_clf.fit(X_train_folds, y_train_folds)
            y_pred = clone_clf.predict(X_test_fold)
            n_correct = sum(y_pred == y_test_fold)
            
        return n_correct/len(y_pred)


    def plot_precision_recall_vs_threshold(precisions: list, recalls: list, thresholds:list ) -> None: 
        """"
        Essa função plota a precisão e a revocação em relação ao limiar (threshold) utilizando matplotlib. É importante notar que precisões e revocações devem ter o mesmo tamanho e ordem de limiares. A função usa as funções plt.plot, plt.xlabel, plt.legend, plt.ylim e plt.grid para plotar o gráfico e plt.show para mostrar o gráfico final.

        Parâmetros:
            precisions (list): lista de precisões, onde cada elemento representa a precisão para um determinado limiar.
            recalls (list): lista de revocações, onde cada elemento representa a revocação para um determinado limiar.
            thresholds (list): lista de limiares, usado como eixo x no gráfico.

        Retorna:
            plot imagem

        Obs: 
            Necessary packages:
                import matplotlib
        """
        
        plt.plot(thresholds, precisions[:-1], 'b--', label= 'Precision')
        plt.plot(thresholds, recalls[:-1], 'g-', label='Recall')
        plt.xlabel('Threshold')
        plt.legend(loc='center left')
        plt.ylim([0, 1])
        plt.grid('on')
        plt.show()


    def plot_roc_curve(fpr,tpr, label=None):
        """
        plot_roc_curve(fpr, tpr, label=None)

        Essa função plota a curva ROC (Receiver Operating Characteristic) utilizando matplotlib. A curva ROC é uma representação gráfica da performance de um classificador binário, mostrando a relação entre a taxa de verdadeiros positivos (TPR) e a taxa de falsos positivos (FPR). A função usa as funções plt.plot, plt.xlabel, plt.ylabel, plt.grid e plt.show para plotar o gráfico e mostrar o gráfico final.

        Parâmetros:
            fpr (list): lista de taxas de falsos positivos.
            tpr (list): lista de taxas de verdadeiros positivos.
            label (str, opcional): rótulo para a curva ROC.

        Retorna:
            None
        
        Obs: 
            Necessary Packages: 
            matplotlib
        """
        plt.plot(fpr, tpr, linewidth=2, label=label)
        plt.plot([0,1], [0,1], 'k--')
        plt.plot([0,1,0,1])
        plt.axis([0,1,0,1])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.grid('on')
        plt.show()


    def plot_matrix_confusion(y_true, y_pred, model_class):
        """
        plot_matrix_confusion(y_true, y_pred, model_class)

        Essa função plota a matriz de confusão utilizando a função ConfusionMatrixDisplay do pacote sklearn.metrics. A matriz de confusão é uma representação gráfica das predições do modelo em relação aos valores verdadeiros. A função usa as funções confusion_matrix e ConfusionMatrixDisplay do pacote sklearn.metrics para plotar a matriz de confusão.

        Parâmetros:
            y_true (list): lista de valores verdadeiros.
            y_pred (list): lista de valores preditos pelo modelo.
            model_class (list): lista de classes do modelo, usadas para rotular as linhas e colunas da matriz de confusão.

        Retorna:
            None

        Obs: 
            Necessary Packages: 
            from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix
        """
        cfm = confusion_matrix(y_true, y_pred)
        cfm_plot = ConfusionMatrixDisplay(confusion_matrix=cfm, display_labels=model_class)
        cfm_plot.plot()


    def plot_learning_curves(model, X: list, y: list, n_test: float):
        """"
        Plot learning curves for a given model
        
        Parameters:
            model : The model to be trained and evaluated
            X : list of feature data
            y : list of labels for the feature data
            n_test : a float, the proportion of the data to use as the validation set.
            
        Returns: 
            None

        Obs:
            Necessary Packages: 
            from sklearn.metrics import mean_squared_error
            from sklearn.model_selection import train_test_split
        """
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=n_test)
        train_errors, val_errors = [], []
        for m in range(1, len(X_train)):
            model.fit(X_train[:m], y_train[:m])
            y_train_predict = model.predict(X_train[:m])
            y_val_predict = model.predict(X_val)
            train_errors.append(mean_squared_error(y_train[:m], y_train_predict))
            val_errors.append(mean_squared_error(y_val, y_val_predict))
        plt.figure(figsize=(10,5))
        plt.plot(np.sqrt(train_errors), 'r-+', linewidth=2, label="train")
        plt.plot(np.sqrt(val_errors), 'b-', linewidth=3, label="val")
        plt.grid('on')
        plt.legend(loc="upper right", fontsize=14)   
        plt.xlabel("Training set size", fontsize=14) 
        plt.ylabel("RMSE", fontsize=14) 


    def plot_classification_results(clf, X, y, title):
        """
        This function plots the classification results for a given classifier 'clf' and data 'X' and 'y'. 
        
        Parameters: 
            clf : model classification
            X: Train Data; 
            y: Train classes;
        """
        
        # Divide o dataset em treino e teste
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)

        # Fit dos dados com o classificador
        clf.fit(X_train, y_train)

        # Cores para o gráfico
        cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF'])
        cmap_bold = ListedColormap(['#FF0000', '#00FF00', '#0000FF'])

        h = .02  # step size in the mesh
        
        # Plot da fronteira de decisão.
        # Usando o meshgrid do NumPy e atribuindo uma cor para cada ponto 
        x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
        y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

        # Previsões
        Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

        # Resultados em cada cor do plot
        Z = Z.reshape(xx.shape)
        pl.figure()
        pl.pcolormesh(xx, yy, Z, cmap=cmap_light)

        # Plot dos pontos de dados de treino
        pl.scatter(X_train[:, 0], X_train[:, 1], c = y_train, cmap = cmap_bold)

        y_predicted = clf.predict(X_test)
        score = clf.score(X_test, y_test)
        pl.scatter(X_test[:, 0], X_test[:, 1], c = y_predicted, alpha = 0.5, cmap = cmap_bold)
        pl.xlim(xx.min(), xx.max())
        pl.ylim(yy.min(), yy.max())
        pl.title(title)
        return score