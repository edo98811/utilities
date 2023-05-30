import sklearn
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
import sklearn.metrics as metrics
import sklearn.feature_selection as feature_selection
import pandas as pd
import os
import data_manipulation as dm
import imblearn as im
import comparisons_updated as cu
import FastsurferTesting_pc as ft
import numpy as np
import missingno as msno
import matplotlib.pyplot as plt

"""
idee 
    togliere referenze a self 
    fare in modo che i model sano ritornati e che quindi sia tutto modulare per poterne usare molti 
    salvare risultati in excel

"""


class Models_Binary:
    def __init__(self, data, base_path, data_path="\\machine_learning"):

        self.X_normalized = None
        self.X_feature_selected = None
        if len(data) == 2:
            self.data = data
        else:
            raise Exception("wrong number of class inputs (only binary classification)")
        self.base_path = base_path

        self.data_path = base_path + data_path
        if not os.path.exists(data_path):
            os.makedirs(data_path)

        self.X, self.Y = self._dataset_preparation()
        ft.LogWriter.log("dataset object created")

    @staticmethod
    def _select_dataset(d, stats_object):

        if d == "aseg":
            dataframe_selected = stats_object.df_stats_aseg
            subj_lists = stats_object.df_stats_aseg["ID"].tolist()
            columns = set(stats_object.df_stats_aseg.columns.tolist())
        elif d == "aparcR":
            dataframe_selected = stats_object.df_stats_aparcL
            subj_lists = stats_object.df_stats_aparcL["ID"].tolist()
            columns = set(stats_object.df_stats_aparcL.columns.tolist())
        elif d == "aparcL":
            dataframe_selected = stats_object.df_stats_aparcL
            subj_lists = stats_object.df_stats_aparcL["ID"].tolist()
            columns = set(stats_object.df_stats_aparcL.columns.tolist())
        elif d == "aseg_normalized":
            dataframe_selected = stats_object.aseg_normalized
            subj_lists = stats_object.aseg_normalized.index.values.tolist()
            columns = set(stats_object.aseg_normalized.columns.tolist())
        elif d == "aseg_normalized_mmse":
            dataframe_selected = stats_object.aseg_normalized_mmse
            subj_lists = stats_object.aseg_normalized_mmse.index.values.tolist()
            columns = set(stats_object.aseg_normalized_mmse.columns.tolist())
        elif d == "aparcL_cleaned":
            dataframe_selected = stats_object.aparcL_cleaned
            subj_lists = stats_object.aparcL_cleaned.index.values.tolist()
            columns = set(stats_object.aparcL_cleaned.columns.tolist())
        elif d == "aparcR_cleaned":
            dataframe_selected = stats_object.aparcR_cleaned
            subj_lists = stats_object.aparcR_cleaned.index.values.tolist()
            columns = set(stats_object.aparcR_cleaned.columns.tolist())
        else:
            return None, None, None

        columns_set = set(columns)

        return dataframe_selected, subj_lists, columns_set

    @staticmethod
    def load_features(file, queries=("",), sheet=1):
        """select the data that needs to be used based on filters given as input"""

        data = pd.read_excel(file)
        # iterate through sheets

        for query in queries:
            # loads the data and applies the filter
            filtered_data = data

            columns = filtered_data.columns.tolist()
            continue

        return

    @staticmethod
    def _drop_nan(X):
        cols_to_drop = []
        for name in X.columns.tolist():
            if X.loc[:, name].isnull().values.any():
                # X.loc[:, column] = X.loc[:, column].fillna(0)
                cols_to_drop.append(name)
                # drop column
        X.drop(columns=cols_to_drop, inplace=True)
        return X

    def save_dataset(self, X, y=None, filename="dataset.xlsx"):

        ft.LogWriter.log("dataset saved")
        if y is None:
            df = X
        else:
            df = pd.concat([y, X], axis=1)

        df.to_excel(f"{self.data_path}{filename}")
        dm.write_txt(df.columns.tolist(), f"{self.data_path}features.txt")

    def _dataset_preparation(self, data=("aparcL_cleaned", "aparcR_cleaned", "aseg_normalized"),
                             columns_to_exclude=("mmse")):

        df = pd.DataFrame()
        for i, stats_object in enumerate(self.data):
            df_class = pd.DataFrame()
            subjects_ID = set()
            columns_all = set()

            for d in data:
                dataframe_selected, subj_lists, columns_set = self._select_dataset(d, stats_object)
                # devo essere sicuro che gli indici coincidano tra tutti i dataframe

                df_class = pd.concat([df_class, dataframe_selected], axis=1)
                subjects_ID = subjects_ID.union(subj_lists)
                columns_all = columns_all.union(columns_set)

                for column in columns_all:
                    if column in columns_to_exclude:
                        df_class.drop(column, inplace=True)

                df_class["class"] = i

            if 'df_class' in locals():
                df = pd.concat([df, df_class], axis=0)
            else:
                raise Exception("dataset could not be created")

        df = df.sample(frac=1)

        # df.to_excel(f"{self.base_path}dataset.xlsx")

        Y = df.loc[:, "class"].copy(deep=True)
        X = df.drop(columns=["class"]).copy(deep=True)

        return X, Y
        """
        :param decode:
        :param dataframe_selected:
        :return:
        """
        """
        idee
            un altra idea è unsare una lista di due da unire per creare il dataset, la lista contiene in una quelly sani 
            e in una quelli dell'altro dataset
            - potrei usare due queries per selezionare i soggetti che sono da considerare healthy e quelli che non lo sono 
        dafare 
            - filtrare i soggetti usando la query, devo aggiungere 0 e 1 alla fine del dataset per ogni soggetto 
            - eliminare le colonne inutili 
            - unificare tutte le features
            - dividere il dataframe
            - salvare dataset x
            - salvare dataset y 
        """

    @staticmethod
    def feature_selection(X, y, features=None, method=0):
        X_feature_selected = None
        Models_Binary._drop_nan(X)
        if features is None:
            if method == 0:
                X_feature_selected = X
            if method == 1:
                X_feature_selected = feature_selection.SelectKBest(score_func=feature_selection.f_classif,
                                                                   k=10).fit_transform(
                    X, y)
        else:
            X_feature_selected = X[X.columns.intersection(features)]

        return X_feature_selected

    @staticmethod
    def _set_splitting(X, y, test=0.2, method="under"):
        """
        :param X:
        :param y:
        :param test:
        :param method: "under", "over", "balance_same_seed"
        :return:
        """

        if method == "under":
            under_sampler = im.under_sampling.RandomUnderSampler(random_state=42)
            X_balanced, y_balanced = under_sampler.fit_resample(X, y)
            Models_Binary.check_balance(y_balanced)

            X_train, X_test, y_train, y_test = train_test_split(X_balanced, y_balanced, test_size=test, random_state=0)

        elif method == "over":
            under_sampler = im.over_sampling.RandomOverSampler(random_state=42)
            X_balanced, y_balanced = under_sampler.fit_resample(X, y)
            Models_Binary.check_balance(y_balanced)

            X_train, X_test, y_train, y_test = train_test_split(X_balanced, y_balanced, test_size=test, random_state=0)

        elif method == "no":
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test, random_state=0)
        elif method == "balance_same_seed":
            np.random.seed(42)

            data = np.hstack((X, np.expand_dims(y.to_numpy(), axis=1)))
            class1 = data[data[:, -1] == 1, :]
            class2 = data[data[:, -1] == 0, :]
            n = int(np.ceil((1 - test) * min(len(class1), len(class2))))

            train1 = np.random.permutation(range(len(class1)))[:n]
            train2 = np.random.permutation(range(len(class1)))[:n]

            test1 = np.random.permutation(range(len(class1)))[n + 1:]
            test2 = np.random.permutation(range(len(class1)))[n + 1:]

            train = np.concatenate(([class1[train1, :], class2[train2, :]]), axis=0)
            test = np.concatenate(([class1[test1, :], class2[test2, :]]), axis=0)
            np.random.shuffle(train)
            np.random.shuffle(test)

            Models_Binary.check_balance(train)
            Models_Binary.check_balance(test)
            y_train = train[:, -1]
            X_train = train[:, :-2]
            y_test = test[:, -1]
            X_test = test[:, :-2]
        else:
            return None

        return X_train, X_test, y_train, y_test

    @staticmethod
    def check_balance(y):
        # byclass = self.X.groupby(by="class").count()
        # ft.LogWriter.log(f"{byclass}")
        if isinstance(y, pd.DataFrame):
            ft.LogWriter.log(f"{len(y['class' == 1])}")
            ft.LogWriter.log(f"{len(y['class' == 0])}")
        elif type(y) is np.ndarray:
            print("to_implement")
            pass

    @staticmethod
    def normalize_features(X, method="minmax"):
        if method == "standard":
            X_normalized = sklearn.preprocessing.StandardScaler().fit_transform(X)
        elif method == "minmax":
            X_normalized = sklearn.preprocessing.MinMaxScaler().fit_transform(X)
        elif method == "other":
            X_normalized = sklearn.preprocessing.MinMaxScaler().fit_transform(X)
        else:
            return None

        return X_normalized

    @staticmethod
    def train_model(X_train, y_train, model_type):
        if model_type == "logistic":
            model = LogisticRegression().fit(X_train, y_train)
        elif model_type == "svm":
            model = SVC().fit(X_train, y_train)
        else:
            raise Exception("invalid model type")

        return model

    @staticmethod
    def test_model(X_test, model):
        if model is None:
            return
        return model.predict(X_test)

    @staticmethod
    def metrics(y_test, y_pred, index, features, text):

        results_dict = dict()

        results_dict["accuracy"] = metrics.accuracy_score(y_test, y_pred)
        results_dict["precision"] = metrics.precision_score(y_test, y_pred)
        results_dict["recall"] = metrics.recall_score(y_test, y_pred)
        results_dict["balanced_accuracy"] = metrics.balanced_accuracy_score(y_test, y_pred)
        results_dict["confusion_matrix"] = str(metrics.confusion_matrix(y_test, y_pred))
        results_dict["text"] = text
        results_dict["features_used"] = ';'.join(features)

        results_series = pd.DataFrame(results_dict, index=(index,))
        # results_series.name = index

        return results_series

    def get_model(self, index, sb_, n_):
        match index:
            case 1:
                return LogisticRegression(), f"model: logistic regression \n feature selection: " \
                                             f"{sb_} sampling \n normalization method: {n_} \n" \
                                             f" additional parameters: "
            case 2:
                return LogisticRegression(penalty="l2"), f"model: logistic regression \n feature selection: " \
                                                         f"{sb_} sampling \n normalization method: {n_} \n" \
                                                         f" additional parameters: penalty=l2"
            case 3:
                return SVC(), f"model: SVM \n feature selection: " \
                              f"{sb_} sampling \n normalization method: {n_} \n" \
                              f" additional parameters: "
            case 4:
                return SVC(kernel="linear"), f"model: SVM \n feature selection: " \
                                             f"{sb_} sampling \n normalization method: {n_} \n" \
                                             f" additional parameters: kernel=linear"
            case 5:
                return SVC(kernel="poly", degree=5), f"model: SVM \n feature selection: " \
                                                     f"{sb_} sampling \n normalization method: {n_} \n" \
                                                     f" additional parameters: kernel=poly, degree=5"
            case 5:
                return SVC(kernel="poly"), f"model: SVM \n feature selection: " \
                                           f"{sb_} sampling \n normalization method: {n_}" \
                                           f" \n additional parameters: kernel=poly"
            case 6:
                return SVC(kernel="sigmoid"), f"model: SVM \n feature selection: " \
                                              f"{sb_} sampling \n normalization method: {n_} \n" \
                                              f" additional parameters: kernel=sigmoid "
            case 7:
                return RandomForestClassifier(n_estimators=100, max_depth=6,
                                              max_features=3), f"model: Random Forest: \n feature selection: " \
                                                               f"{sb_} sampling \n normalization method: {n_} \n" \
                                                               f" additional parameters: "
            case _:
                return None, None

    def classify(self, name, features=None, feature_selection_method=None, normalization=("minmax",),
                 model_type=("logistic", "svm"), setbalance=("over",), n_iter=1):
        """

        :param features:
        :param feature_selection_method:
        :param normalization:
        :param model_type:
        :param setbalance:
        :param n_iter:
        :return:
        """

        res = pd.DataFrame()
        X_selected = self.feature_selection(self.X, self.Y, features=features, method=feature_selection_method)
        for n_ in normalization:
            X_normalized = self.normalize_features(X_selected, method=n_)
            for sb_ in setbalance:
                X_train, X_test, y_train, y_test = self._set_splitting(X_normalized, self.Y, method=sb_)

                for i in range(n_iter):
                    index_list = range(8)
                    for index in index_list:
                        model, text = self.get_model(index, n_, sb_)
                        if model is None or text is None:
                            continue
                        model.fit(X_train, y_train)
                        y_pred = Models_Binary.test_model(X_test, model)
                        res = pd.concat([res, Models_Binary.metrics(y_test, y_pred, index, features, text)], axis=0)

                    # # logistic regression 1
                    # index = f"logistc_{sb_}_{i}_try1"
                    #
                    # # scores = sklearn.model_selection.cross_validate(LogisticRegression(), X_train, y_train, scoring='balanced_accuracy', return_estimator=True)
                    # # model = scores['estimator']
                    #
                    # model = LogisticRegression().fit(X_train, y_train)
                    # y_pred = Models_Binary.test_model(X_test, model)
                    # text = f"model: logistic regression \n feature selection: {sb_} sampling \n normalization method: {n_} \n additional parameters: "
                    # res = pd.concat([res, Models_Binary.metrics(y_test, y_pred, index, features, text)], axis=0)
                    # # logistic regression 1
                    # # index = f"logistc_{sb_}_{i}_try4"
                    # #
                    # # model = LogisticRegression(penalty='elasticnet').fit(X_train, y_train)
                    # # y_pred = Models_Binary.test_model(X_test, model)
                    # # res = pd.concat([res, Models_Binary.metrics(y_test, y_pred, index)], axis=1)
                    # # logistic regression 1
                    # # index = f"logistc_{sb_}_{i}_try2"
                    # #
                    # # model = LogisticRegression(penalty='l1').fit(X_train, y_train)
                    # # y_pred = Models_Binary.test_model(X_test, model)
                    # # res = pd.concat([res, Models_Binary.metrics(y_test, y_pred, index)], axis=1)
                    # # logistic regression 1
                    # index = f"logistc_{sb_}_{i}_try3"
                    #
                    # model = LogisticRegression(penalty='l2').fit(X_train, y_train)
                    # y_pred = Models_Binary.test_model(X_test, model)
                    # text = f"model: logistic regression \n feature selection: {sb_} sampling \n normalization method: {n_} \n additional parameters: penalty: l2"
                    # res = pd.concat([res, Models_Binary.metrics(y_test, y_pred, index, features, text)], axis=0)
                    #
                    # # svm 1
                    # index = f"svm_{sb_}_{i}_try1"
                    #
                    # model = SVC().fit(X_train, y_train)
                    # y_pred = Models_Binary.test_model(X_test, model)
                    # text = f"model: SVM \n feature selection: {sb_} sampling \n normalization method: {n_} \n additional parameters: "
                    # res = pd.concat([res, Models_Binary.metrics(y_test, y_pred, index, features, text)], axis=0)
                    # # svm 2
                    # index = f"svm_{sb_}_{i}_try2"
                    #
                    # model = SVC(kernel='linear').fit(X_train, y_train)
                    # y_pred = Models_Binary.test_model(X_test, model)
                    # text = f"model: SVM \n feature selection: {sb_} sampling \n normalization method: {n_} \n additional parameters: kernel='linear'"
                    # res = pd.concat([res, Models_Binary.metrics(y_test, y_pred, index, features, text)], axis=0)
                    # # svm 3
                    # index = f"svm_{sb_}_{i}_try3"
                    #
                    # model = SVC(kernel='sigmoid').fit(X_train, y_train)
                    # y_pred = Models_Binary.test_model(X_test, model)
                    # text = f"model: SVM \n feature selection: {sb_} sampling \n normalization method: {n_} \n additional parameters: kernel='sigmoid'"
                    # res = pd.concat([res, Models_Binary.metrics(y_test, y_pred, index, features, text)], axis=0)
                    # # svm 4
                    # index = f"svm_{sb_}_{i}_try4"
                    #
                    # model = SVC(kernel='poly').fit(X_train, y_train)
                    # y_pred = Models_Binary.test_model(X_test, model)
                    # text = f"model: SVM \n feature selection: {sb_} sampling \n normalization method: {n_} \n additional parameters: kernel='poly' degree=3"
                    # res = pd.concat([res, Models_Binary.metrics(y_test, y_pred, index, features, text)], axis=0)
                    # # svm 5
                    # index = f"svm_{sb_}_{i}_try5"
                    #
                    # model = SVC(kernel='poly', degree=5).fit(X_train, y_train)
                    # y_pred = Models_Binary.test_model(X_test, model)
                    # text = f"model: SVM \n feature selection: {sb_} sampling \n normalization method: {n_} \n additional parameters: kernel='poly', degree=5"
                    # res = pd.concat([res, Models_Binary.metrics(y_test, y_pred, index, features, text)], axis=0)
                    #
                    # index = f"random_forest_{sb_}_{i}_try5"
                    #
                    # model = RandomForestClassifier(n_estimators=100, max_depth=6, max_features=3).fit(X_train, y_train)
                    # y_pred = Models_Binary.test_model(X_test, model)
                    # text = f"model: RandomForest \n feature selection: {sb_} sampling \n normalization method: {n_} \n additional parameters: n_estimators=100, max_depth=6, max_features=3"
                    # res = pd.concat([res, Models_Binary.metrics(y_test, y_pred, index, features, text)], axis=0)

        # res.to_excel(self.data_path + filename)
        return res

    def plot_scores(self, results, n_subplots=8, n_rows=2, img_name="boxplots"):
        if not os.path.exists(self.data_path + "boxplots\\"):
            os.makedirs(self.data_path + "boxplots\\")
        img_name = self.data_path + "boxplots\\" + img_name
        c_to_exclude = ("class",)
        plots_n = 0
        fig = None

        for column in results:
            if column not in c_to_exclude:
                values = results.loc[:, ["class", column]]

                if not plots_n % n_subplots:
                    # plots when
                    if plots_n > 1:
                        if fig is not None:
                            fig.savefig(f"{img_name}"
                                        f"_{str(plots_n - n_subplots)}-{str(plots_n)}.png")  # save the figure to file

                    fig, axs = self.create_plot(n_subplots, n_rows)

                plot_ = values.boxplot(by="class", ax=axs[plots_n % n_subplots])
                plot_.plot()
                plots_n += 1

        if plots_n % n_subplots != 0:
            if fig is not None:
                fig.savefig(f"{img_name}"
                            f"_{str(plots_n - (plots_n % n_subplots))}-{str(plots_n)}.png")  # save the figure to file
                del axs, fig

    @staticmethod
    def create_plot(n_subplots, n_rows):

        fig, axs = plt.subplots(n_rows, int(n_subplots / n_rows), figsize=(40, 20))
        axs = axs.ravel()
        plt.subplots_adjust(hspace=0.5)
        plt.subplots_adjust(wspace=0.2)

        return fig, axs

    def scores(self, filename, indexes, features=None, setbalance=("over",)):
        X_selected = self.feature_selection(self.X, self.Y, features=features)
        subjects = X_selected.index.tolist()
        # X_train, X_test, y_train, y_test = self._set_splitting(X_selected, self.Y)

        results = pd.DataFrame()
        results["class"] = self.Y
        results.index = subjects

        for index_name in indexes.keys():
            results[index_name] = np.nan

            for index, element in X_selected.iterrows():
                results.loc[index, index_name] = self.compute_index(element, indexes[index_name])
                # score.add(self.compute_index(element, indexes[index_name]), index=index)

        results.to_excel(self.data_path + filename)
        self.plot_scores(results)
        plot_ = results.boxplot(by="class")
        for plotn in plot_:
            plotn.plot()
        plt.show()

    """
    index = dictionary 
    name: [(coeff, var), ]
    """

    @staticmethod
    def _plot_scores(results):
        pass

    def compute_index(self, dataset, index_formula):
        score = 0
        # index formula, list of tuples (coeff, variable name)
        for coeff, variable in index_formula:
            score += coeff * dataset.loc[variable]

        return score

    def cross_validation(self):
        pass

    """
        res = pd.DataFrame()
        if features is None:
            X_selected = self.feature_selection(self.X, self.Y, features=features, method=feature_selection_method)
        else:
            for n_f, features_ in enumerate(features):
                X_selected = self.feature_selection(self.X, self.Y, features=features_, method=feature_selection_method)
                for n_ in normalization:
                    X_normalized = self.normalize_features(X_selected, method=n_)
                    for sb_ in setbalance:
                        X_train, X_test, y_train, y_test = self._set_splitting(X_normalized, self.Y, method=sb_)
        
                        for m_ in model_type:
                            for i in range(n_iter):
                                index = f"features_set_n{n_f}_{m_}_{sb_}_{n_}_{i}"
        
                                model = Models_Binary.train_model(X_train, y_train, m_)
                                y_pred = Models_Binary.test_model(X_test, model)
                                res = pd.concat([res, Models_Binary.metrics(y_test, y_pred, index)], axis=1)

        res.to_excel(self.data_path + filename)
        """
    # res = pd.DataFrame()
    # X_selected = self.feature_selection(self.X, self.Y, features=features, method=feature_selection_method)
    # for n_ in normalization:
    #     X_normalized = self.normalize_features(X_selected, method=n_)
    #     for sb_ in setbalance:
    #         X_train, X_test, y_train, y_test = self._set_splitting(X_normalized, self.Y, method=sb_)
    #
    #         for m_ in model_type:
    #             for i in range(n_iter):
    #                 index = f"{m_}_{sb_}_{n_}_{i}"
    #
    #                 model = Models_Binary.train_model(X_train, y_train, m_)
    #                 y_pred = Models_Binary.test_model(X_test, model)
    #                 res = pd.concat([res, Models_Binary.metrics(y_test, y_pred, index)], axis=1)
    #
    # res.to_excel(self.data_path + filename)
    # res = pd.DataFrame()

    # def medial_temporal_lobe_atrophy_score(self, features=None):
    #
    #     if features is None:
    #         features = []
    #
    #     a = features[0]
    #     b = features[1]
    #     c = features[3]
    #
    # def HAV_atrophy_score(self):
    #     model = 1
    #
    # def feature_tests(self):
    #     pass
    # def logistic_regression(self, features=None, normalization="minmax", model="logistc", setbalance="balance_same_seed"):
    #
    #     X_fs = self.feature_selection(self.X, self.Y, features=features)
    #     X_normalized = self.normalize_features(X_fs)
    #
    #     X_train, X_test, y_train, y_test = self._set_splitting(X_normalized, self.Y)
    #
    #     model_log = LogisticRegression().fit(X_train, y_train)
    #     y_pred_log = model_log.predict(X_test)
    #
    #     # %% md
    #     # 16. Compare the end results by their accuracy
    #     # %%
    #     acc_log = accuracy_score(y_test, y_pred_log)
    #     print(f"accuracy under sampling: {acc_log}")
    #     del X_train, X_test, y_train, y_test
    #
    #     X_train, X_test, y_train, y_test = self._set_splitting(self.X_normalized, self.Y, balance="over")
    #     model_log = LogisticRegression().fit(X_train, y_train)
    #     y_pred_log = model_log.predict(X_test)
    #
    #     # %% md
    #     # 16. Compare the end results by their accuracy
    #     # %%
    #     acc_log = accuracy_score(y_test, y_pred_log)
    #     print(f"accuracy over sampling: {acc_log}")