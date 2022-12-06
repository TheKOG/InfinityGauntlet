from record import Record
from snap import is_Snap,Load
if __name__=='__main__':
    Load('pth/best_pth')
    print("counting")
    while True:
        Record("tmp/tmp.wav",debug=False)
        val=is_Snap("tmp/tmp.wav")
        if(val>0.9):
            # print(val)
            print("Snap!")
            # exit()