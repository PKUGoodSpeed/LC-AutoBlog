[318] Maximum Product of Word Lengths  

https://leetcode.com/problems/maximum-product-of-word-lengths/description/

* algorithms
* Medium (46.02%)
* Total Accepted:    64.4K
* Total Submissions: 139.9K
* Testcase Example:  '["abcw","baz","foo","bar","xtfn","abcdef"]'

Given a string array words, find the maximum value of length(word[i]) * length(word[j]) where the two words do not share common letters. You may assume that each word will contain only lower case letters. If no such two words exist, return 0.

Example 1:


Input: ["abcw","baz","foo","bar","xtfn","abcdef"]
Output: 16 
Explanation: The two words can be "abcw", "xtfn".

Example 2:


Input: ["a","ab","abc","d","cd","bcd","abcd"]
Output: 4 
Explanation: The two words can be "ab", "cd".

Example 3:


Input: ["a","aa","aaa","aaaa"]
Output: 0 
Explanation: No such pair of words.


