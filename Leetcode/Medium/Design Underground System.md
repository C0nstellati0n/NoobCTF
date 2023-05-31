# Design Underground System

[题目](https://leetcode.com/problems/design-underground-system/description/)

眼睛：hint说只用2个hash table就好了。大脑：我说3个就3个！冲锋！

```c#
public class UndergroundSystem {
    Dictionary<int,string> start;
    Dictionary<int,int> startTime;
    Dictionary<string,double[]> avg;
    public UndergroundSystem() {
        start=new();
        startTime=new();
        avg=new();
    }
    
    public void CheckIn(int id, string stationName, int t) {
        start[id]=stationName;
        startTime[id]=t;
    }
    
    public void CheckOut(int id, string stationName, int t) {
        string key=start[id]+"."+stationName; //中间加任意符号保证key唯一。a ab,aa b如果不加符号拼在一起就是一样的
        if(avg.ContainsKey(key)){
            avg[key][0]+=1;
        }
        else{
            avg[key]=new double[2];
            avg[key][0]=1;
        }
        avg[key][1]=t-startTime[id]+avg[key][1];
    }
    
    public double GetAverageTime(string startStation, string endStation) {
        return avg[startStation+"."+endStation][1]/avg[startStation+"."+endStation][0];
    }
}
```
```
Runtime
368 ms
Beats
52.78%
Memory
71.7 MB
Beats
86.11%
```
其实我思路都差不多了，把前两个hash table像第三个一样合在一起就好了。
```c#
//https://leetcode.com/problems/design-underground-system/solutions/554879/c-java-python-hashmap-pair-clean-concise-o-1/
public class UndergroundSystem {
    Dictionary<int, Tuple<string, int>> checkInDictionary = new();  // Uid - {StationName, Time}
    Dictionary<string, Tuple<double, int>> routeDictionary = new(); // RouteName - {TotalTime, Count}

    public UndergroundSystem() {}

    public void CheckIn(int id, string stationName, int t) {
        checkInDictionary[id]=new Tuple<string,int>(stationName, t);
    }

    public void CheckOut(int id, string stationName, int t) {
        Tuple<string, int> checkIn = checkInDictionary[id];
        checkInDictionary.Remove(id); // Remove after using it which will not make HashTable big

        string routeName = checkIn.Item1 + "_" + stationName;
        int totalTime = t - checkIn.Item2;

        Tuple<double, int> route = routeDictionary.GetValueOrDefault(routeName, new Tuple<double,int>(0.0, 0));
        routeDictionary[routeName]=new Tuple<double,int>(route.Item1 + totalTime, route.Item2 + 1);
    }

    public double GetAverageTime(string startStation, string endStation) {
        string routeName = startStation + "_" + endStation;
        Tuple<double, int> trip = routeDictionary[routeName];
        return trip.Item1 / trip.Item2;
    }
}
```
```
Runtime
342 ms
Beats
100%
Memory
80.2 MB
Beats
44.44%
```
或者使用oop，把答案写得更“实际”一点。
```c#
//https://leetcode.com/problems/design-underground-system/solutions/672744/java-solution-for-easy-understanding-using-oops/
class Passenger {
    public int checkinTime;
    public int checkoutTime;
    public string checkinLocation;
    public string checkoutLocation;

    public Passenger(string checkinLocation, int checkinTime) {
        this.checkinLocation = checkinLocation;
        this.checkinTime = checkinTime;
    }

    public void checkout(string checkoutLocation, int checkoutTime) {
        this.checkoutLocation = checkoutLocation;
        this.checkoutTime = checkoutTime;
    }

}

class Route {
    string startStation;
    string endStation;
    int totalNumberOfTrips;
    long totalTimeSpentInTrips;

    public Route(string startStation, string endStation) {
        this.startStation = startStation;
        this.endStation = endStation;
    }

    public double getAverageTime() {
        return (double) totalTimeSpentInTrips / totalNumberOfTrips;
    }

    public void addTrip(int startTime, int endTime) {
        totalTimeSpentInTrips += endTime - startTime;
        totalNumberOfTrips++;
    }
}

class UndergroundSystem {

    Dictionary<int, Passenger> currentPassengerDictionary;
    Dictionary<string, Route> routeDictionary;

    public UndergroundSystem() {
        currentPassengerDictionary = new();
        routeDictionary = new();
    }

    public void CheckIn(int id, string stationName, int t) {
        if (!currentPassengerDictionary.ContainsKey(id)) {
            Passenger passenger = new Passenger(stationName, t);
            currentPassengerDictionary[id]=passenger;
        }
    }

    public void CheckOut(int id, string stationName, int t) {
        if (currentPassengerDictionary.ContainsKey(id)) {
            Passenger passenger = currentPassengerDictionary[id];
            passenger.checkout(stationName, t);
            string routeKey = passenger.checkinLocation + "," + passenger.checkoutLocation;
            Route route = routeDictionary.GetValueOrDefault(routeKey, new Route(passenger.checkinLocation, passenger.checkoutLocation));
            route.addTrip(passenger.checkinTime, passenger.checkoutTime);
            routeDictionary[routeKey]=route;
            currentPassengerDictionary.Remove(id);
        }
    }

    public double GetAverageTime(string startStation, string endStation) {
        return routeDictionary[startStation + "," + endStation].getAverageTime();
    }
}
```
```
Runtime
346 ms
Beats
100%
Memory
81 MB
Beats
30.56%
```