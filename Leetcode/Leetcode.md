# Leetcode

最近打了个CTF，十几道题就做出来2道，还有一道是签到题……其中有部分算法题，看来是时候练Leetcode了。语言我用的是C#，不过各种语言差不多(现在看来并不是），选哪个不重要。现在记录说不定以后遇见类似的题可以直接抄。

## Easy

- [Two Sum](Easy/TwoSum.md)。Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.You may assume that each input would have exactly one solution, and you may not use the same element twice.You can return the answer in any order.给定nums数组和目标target，返回nums中相加得target的数字的索引。假设只有一对解，索引顺序不重要。使用字典，空间换取时间的方式缩短运行时间。
- [Palindrome Number](Easy/PalindromeNumber.md)。Given an integer x, return true if x is a palindrome,and false otherwise。判断给定数字x是否是回文数字。反转字符串和数字运算解法。
- [Roman to Integer](Easy/Roman%20to%20Integer.md)。将罗马数字表达转换为阿拉伯数字
- [Longest Common Prefix](Easy/Longest%20Common%20Prefix.md)。Write a function to find the longest common prefix string amongst an array of strings. If there is no common prefix, return an empty string "". 写一个返回众多字符串共同前缀的函数，如果没有就返回""。
- [Valid Parentheses](Easy/Valid%20Parentheses.md)。Given a string s containing just the characters '(', ')', '{', '}', '[' and ']',determine if the input string is valid.判断括号的闭合是否合法。
- [Merge Two Sorted Lists](Easy/Merge%20Two%20Sorted%20Lists.md)。Merge the two lists in a one sorted list. The list should be made by splicing together the nodes of the first two lists.Return the head of the merged linked list.合并两个已排序的单向链表。
- [Remove Duplicates from Sorted Array](Easy/Remove%20Duplicates%20from%20Sorted%20Array.md)。Given an integer array nums sorted in non-decreasing order, remove the duplicates in-place such that each unique element appears only once. The relative order of the elements should be kept the same. The result should be placed in the first part of the array nums. 去除数组重复的值，返回去重后数组的长度，同时修改参数nums传入的数组。
- [Remove Element](Easy/Remove%20Element.md).Given an integer array nums and an integer val, remove all occurrences of val in nums in-place. The relative order of the elements may be changed.给定一个数组nums和一个值val，移除数组中所有等同于val的元素。实现方法为，把val元素移到全部元素后面，再返回移除后的数组长度。
- [Search Insert Position](Easy/Search%20Insert%20Position.md).Given a sorted array of distinct integers and a target value, return the index if the target is found. If not, return the index where it would be if it were inserted in order.在升序数组nums中搜寻target，找得到就返回target的索引，找不到就返回应该被插入的索引。
- [Length of Last Word](Easy/Length%20of%20Last%20Word.md).Given a string s consisting of words and spaces, return the length of the last word in the string.给定一个包含单词和空格的字符串，返回最后一个单词的长度。
- [Plus One](Easy/Plus%20One.md).You are given a large integer represented as an integer array digits, where each digits[i] is the ith digit of the integer. The digits are ordered from most significant to least significant in left-to-right order.Increment the large integer by one and return the resulting array of digits.给定一个数组表示的数字，从左至右为高位到低位，返回加一后的数字的数组表达形式。
- [Add Binary](Easy/Add%20Binary.md).Given two binary strings a and b, return their sum as a binary string.给出两个数组表示的二进制字符串，返回两者相加的二进制结果的数组形式。
- [Sqrt(x)](Easy/Sqrt(x).md).Given a non-negative integer x, return the square root of x rounded down to the nearest integer. The returned integer should be non-negative as well. You must not use any built-in exponent function or operator.自己实现一个开方算法，不能使用语言自带的函数