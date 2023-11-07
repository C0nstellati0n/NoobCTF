# [Seat Reservation Manager](https://leetcode.com/problems/seat-reservation-manager)

确实和[Smallest Number in Infinite Set](./Smallest%20Number%20in%20Infinite%20Set.md)一模一样
```c++
class SeatManager {
public:
    set<int> s;
    int cur;
    SeatManager(int n):cur(1) {}
    int reserve() {
        if(s.size()){
            int res=*s.begin();
            s.erase(res);
            return res;
        }
        cur++;
        return cur-1;
    }
    void unreserve(int seatNumber) {
        if(seatNumber<cur) s.insert(seatNumber);
    }
};
```