# [Binary Trees With Factors](https://leetcode.com/problems/binary-trees-with-factors)

也算是自己做出来了，字典怎么用，for循环怎么嵌套都是自己想的。然而dp equation还是偷懒去discussion区拿的，还因为几个细节导致解特别慢
```c#
//https://leetcode.com/problems/binary-trees-with-factors/solutions/125794/c-java-python-dp-solution
//注释为个人的写法
public class Solution {
    public int NumFactoredBinaryTrees(int[] arr) {
        Array.Sort(arr);
        Dictionary<int,long> dp=new(); //记得value和下面的ans都用long。我没用导致出过负数答案
        int mod=(int)(1e9+7);
        long ans=0;
        for(int i=0;i<arr.Length;i++){
            dp[arr[i]]=1;
            for(int j=0;j<i;j++){
                //if(arr[j]>arr[i]/2) break; //不要这句，会wrong answer
                //if(!dp.ContainsKey(arr[i])){
                    //dp[arr[i]]=1;
                //}
                //if(!dp.ContainsKey(arr[j])){
                    //dp[arr[j]]=1;
                //}
                if(arr[i]%arr[j]==0){
                    dp[arr[i]]=(dp[arr[i]]+(dp.ContainsKey(arr[i]/arr[j])?dp[arr[i]/arr[j]]:0)*dp[arr[j]])%mod; //dp equation，只在arr被排序后成立
                }
            }
            ans=(ans+dp[arr[i]])%mod;
        }
        //foreach(var item in dp.Values)
        //{
            //ans=(ans+item)%mod;
        //}
        return (int)ans;
    }
}
```