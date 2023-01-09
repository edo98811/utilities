import data_manipulation as dm
import data_visualization as dv
import numpy as np

def main():
    data = dm.load_dict("media/neuropsycad/disk12t/EdoardoFilippiMasterThesis/metrics.json")
    avg_dices = np.zeros(len(data))

    for i,subj  in enumerate(data):
        avg_dices[i] = dv.avg_dice(subj)
    
    dv.plot_dice(data.keys(), avg_dices)

    
if __name__ == "__main__":
    main()