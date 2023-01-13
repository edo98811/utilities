import data_manipulation as dm
import data_visualization as dv
import numpy as np

def main():
    data = dm.load_dict("/media/neuropsycad/disk12t/EdoardoFilippiMasterThesis/utilities/metrics.json")

    avg_dices = []

    count = 0
    for i,subj in enumerate(data.keys()):
        count = count +1
        # print(data[subj]["dice_x"][0])

        dices = np.zeros(len(data[subj]["dice_x"][0]))
        avg_dice_class_n = []

        # calculate the dice values per class and not per slice
        for class_n in range(len(dices)):
            dice_values_class_n = [data[subj]["dice_x"][i][class_n] for i in range(len(data[subj]["dice_x"][i]))]
            # print(dice_values_class_n)
            avg_dice_class_n.append(dv.avg_dice(dice_values_class_n))

        avg_dices.append(avg_dice_class_n)

        # plot
        class_n_list = []
        for j in range(len(avg_dice_class_n)):
            class_n_list.append(j)
            class_n_list.append(j)

        dv.plot_dice_labels(class_n_list, avg_dice_class_n)

        # n of subjects
        if count > 10:
            break

if __name__ == "__main__":
    main()