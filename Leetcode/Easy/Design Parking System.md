# Design Parking System

[题目](https://leetcode.com/problems/design-parking-system/description/)

写之前我应该看hint的，不然不会写出这么sb的答案。

```c#
public class ParkingSystem {
    int big;
    int medium;
    int small;
    int bCurr; //这几个curr根本就没必要，直接在big，small里减就好了
    int sCurr;
    int mCurr;
    public ParkingSystem(int big, int medium, int small) {
        this.big=big;
        this.medium=medium;
        this.small=small;
    }
    
    public bool AddCar(int carType) {
        switch(carType){
            case 1:
                bCurr++;
                if(bCurr>big){
                    return false;
                }
                break;
            case 2:
                mCurr++;
                if(mCurr>medium){
                    return false;
                }
                break;
            case 3:
                sCurr++;
                if(sCurr>small){
                    return false;
                }
                break;
        }
        return true;
    }
}
```
```
Runtime
170 ms
Beats
95.31%
Memory
59.3 MB
Beats
47.92%
```
当然就算我看了hint可能也写不出来下面的答案。
```c#
//https://leetcode.com/problems/design-parking-system/solutions/876953/java-c-python-3-lines/
public class ParkingSystem {
    int[] count;
    public ParkingSystem(int big, int medium, int small) {
        count = new int[]{big, medium, small};
    }

    public bool AddCar(int carType) {
        return count[carType - 1]-- > 0;
    }
}
```
```
Runtime
165 ms
Beats
100%
Memory
59.4 MB
Beats
22.92%
```