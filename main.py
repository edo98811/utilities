import FastsurferTesting as ft
import pandas as pd

ADNI_PATH = ""
OASIS_PATH = "/media/neuropsycad/disk12t/VascoDiogo/OASIS/FS7/"
BASE_PATH = "/media/neuropsycad/disk12t/EdoardoFilippiMasterThesis/"
DATA_FOLDER = "test_data/"



def main():
    table = ft.Table(pd.read_csv(BASE_PATH + "/text_and_csv_files/OASIS_table.csv"), OASIS_PATH, BASE_PATH + "/text_and_csv_files")

    aseg_free = pd.read_csv(BASE_PATH + "Stats_FreeSurfer/aseg.csv")
    aparcL_free = pd.read_csv(BASE_PATH + "Stats_FreeSurfer/aparcDKT_right.csv")
    aparcR_free = pd.read_csv(BASE_PATH + "Stats_FreeSurfer/aparcDKT_left.csv")

    stats_fast_healthy = ft.Stats(table, "healthy_FAST"," main_condition!='Cognitively normal'", d_folder=DATA_FOLDER, b_path=BASE_PATH)
    stats_fast_MC = ft.Stats(table, "MC_FAST", "main_condition!='Cognitively normal'", d_folder=DATA_FOLDER, b_path=BASE_PATH)

    stats_free_healthy = ft.Stats(table, "healthy_FREE", "main_condition!='Cognitively normal'" , BASE_PATH, DATA_FOLDER)
    stats_free_MC = ft.Stats(table, "MC_FREE", "main_condition!='Cognitively normal'", BASE_PATH, DATA_FOLDER, aseg=aseg_free,
                             aparcRight=aparcR_free, aparcLeft=aparcL_free)

    comp1 = ft.Comparisons(stats_free_MC, stats_fast_MC, "MC_oasis", 0.05, DATA_FOLDER, BASE_PATH)
    comp2 = ft.Comparisons(stats_free_healthy, stats_fast_healthy, "healthy_oasis", DATA_FOLDER, 0.05, BASE_PATH)
    comp1.bonferroni_correction()
    comp2.bonferroni_correction()

    comp1.violin()
    comp1.bland_altmann()

    comp2.violin()
    comp2.bland_altmann()


if __name__ == "__main__":
    main()
