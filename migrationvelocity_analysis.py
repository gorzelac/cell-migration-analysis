import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv


def filter_csv_by_value(file_path, target_value):
    df = pd.read_csv(str(file_path)+".dat", sep=',', header=3)
    df = df.sort_values(by=[df.columns[8], df.columns[2]])
    filtered_df = df[df.iloc[:, 2] == target_value]

    return filtered_df

def lastline(file_path):
    df = pd.read_csv(str(file_path)+".dat", sep=',', header=3)
    lasttrack = df.iloc[-1, 2]
    
    return lasttrack

def xposition(result):
    dfx0=result.iloc[0,4]

    return dfx0

def yposition(result):
    dfy0=result.iloc[0,5]
    
    return dfy0

def tracks(result, x0, y0, trackdel):

   
    result = result[result.iloc[:, 8] > trackdel]

   
    if len(result) < 3:
        return None

   
    x = result.iloc[:, 4].to_numpy() - x0
    y = result.iloc[:, 5].to_numpy() - y0

   
    dx = np.diff(x)
    dy = np.diff(y)
    steps = np.sqrt(dx**2 + dy**2)

    
    if len(steps) == 0:
        return None

    mean_dis = np.mean(steps) * 1.22
    sd = np.std(steps)

    return x, y, mean_dis, steps, sd



if __name__ == "__main__":
    
    file_path = 'tracklist.csv F11'  # Insert the TrackMate _spot .csv file
    i=1
    meandistlst=[]
    while i<=lastline(file_path):      

        
        result = filter_csv_by_value(file_path, i)
        
        trackdel=5
        result = result[result.iloc[:, 8] > trackdel]   
        if result.empty:
         print(f"Track {i} does not exit – omitted.")
         i += 1
         continue
        
        
        x0=xposition(result)
        y0=yposition(result)
        xymod=tracks(result,x0,y0,trackdel)
        
        if xymod is None:
            i += 1
            continue

        sd = xymod[4]

        if not np.isfinite(sd):
            i += 1
            continue

         
        
        if int(np.array(xymod[4]))<4 and (len(xymod[0])>5): #filter of tracks meandisplacement  and frame numbers with continous tracking default:  xymod[4]))>3 and (len(xymod[0])>5
              plt.plot(xymod[0]*1.22, xymod[1]*1.22, marker='o', markersize=0, linewidth=1)
              meandistlst.append(xymod[3])

        plt.title(str('meandisplacement:')+str(xymod[2]))
        plt.xlabel('x-displacement [µm]')
        plt.ylabel('y-displacement [µm]')
        i+=1

        # use meanlst.csv to generate bar diagrams
        with open(str(file_path) + 'meanlst.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            for arr in meandistlst:
                for value in arr:
                    writer.writerow([value])



    plt.axis([-100, 100, -100, 100])
    plt.gca().set_aspect('equal')

    plt.savefig(str(file_path)+".svg")
    plt.show()
