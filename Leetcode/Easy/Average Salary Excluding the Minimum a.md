# Average Salary Excluding the Minimum and Maximum Salary

[题目](https://leetcode.com/problems/average-salary-excluding-the-minimum-and-maximum-salary/description/)

直接简单粗暴一行完事。

```c#
public class Solution {
    public double Average(int[] salary) {
        return (double)(salary.Sum()-salary.Min()-salary.Max())/(salary.Length-2); //注意要强转double，否则会给出错误答案
    }
}
```

```
Runtime
77 ms
Beats
91.28%
Memory
38.3 MB
Beats
37.83%
```

或者先把salary排序。

```c#
//https://leetcode.com/problems/average-salary-excluding-the-minimum-and-maximum-salary/solutions/3472407/easy-solutions-in-java-python-and-c-look-at-once-with-exaplanation/
class Solution {
    public double Average(int[] salary) {
        Array.Sort(salary);
        double sum = 0;
        for(int i = 1; i < salary.Length-1; i++) {
            sum = sum + salary[i];
        }
        return sum / (salary.Length - 2);
    }
}
```

```
Runtime
81 ms
Beats
80.10%
Memory
38.7 MB
Beats
11.2%
```

又或者不排序，在手动累加时记录最大值和最小值。

```c#
//https://leetcode.com/problems/average-salary-excluding-the-minimum-and-maximum-salary/solutions/3471419/easy-solution-of-java-c-100-faster-code-easy-to-understand-beginner-friendly/
class Solution {
    public double Average(int[] s) {
        int max =0;
        int min = 100000000;
        double avg=0;
		// getting max and min salary
        for(int i=0;i<s.Length;i++)
        {
            if(s[i]>max)
                max=s[i];
            if(s[i]<min)
                min =s[i];
        }
         
		 // adding all the salaries
		 
        for(int i=0;i<s.Length;i++)
        {
            avg+=s[i];
        }
        avg = (avg-min-max)/(s.Length-2); // finding mean and excluding min and max values. 
        return avg;
        
    }
}
```

```
Runtime
80 ms
Beats
83.88%
Memory
38 MB
Beats
80.26%
```