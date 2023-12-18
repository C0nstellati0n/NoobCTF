# [Design a Food Rating System](https://leetcode.com/problems/design-a-food-rating-system)

但凡少那么一点执着这题就做出来了
```c++
class custom_comparator
{
public: 
    bool operator() (const pair<string, int>& a, const pair<string, int>& b) const //自定义set的比较器
    {
        return a.second == b.second ? a.first < b.first : a.second > b.second; //根据评分排序，越高的排在越前面；若一样就看名称的字母排序。c++里的大于号默认可以按照字母排序比较字符串
    }
};
class FoodRatings 
{
public:
    unordered_map<string, pair<string, int>> food_info; //将food名称map到其对应的cuisine和评分
    unordered_map<string, set<pair<string, int>, custom_comparator>> cuisine_info; //将cuisine名称map到set，set中存储的pair分别为food名称，food评分
    FoodRatings(vector<string>& foods, vector<string>& cuisines, vector<int>& ratings)
    {
        ios_base::sync_with_stdio(false);
        cin.tie(NULL);
        const int n = (int) foods.size(); 
        for(int i = 0; i < n; ++i)
        {
            food_info[foods[i]] = {cuisines[i], ratings[i]};
            cuisine_info[cuisines[i]].insert(make_pair(foods[i], ratings[i]));
        }
    }
    void changeRating(string food, int new_rating)
    {
        pair<string, int>& f = food_info[food];
        int old_rating = f.second;
        set<pair<string, int>, custom_comparator>& st = cuisine_info[f.first];
        st.erase({food, old_rating}); //set里的元素无法被修改，所以只能删除后加新的
        f.second = new_rating;
        st.insert(make_pair(food, new_rating));
        return;
    }
    string highestRated(string cuisine)
    {
        return cuisine_info[cuisine].begin()->first;
    }
};
```
以及不用自定义比较器的做法： https://leetcode.com/problems/design-a-food-rating-system/solutions/2324669/three-maps 。c++的set挺智能的，里面要是是pair，自动按照pair的第一个元素排序；若第一个元素一样，自动按照pair里的第二个元素排序

我写的时候执着于往set里面塞纯string而不是pair，然后自定义比较器里引用food_info里的rating。总之报错一堆，不要试