[745] Prefix and Suffix Search  

https://leetcode.com/problems/prefix-and-suffix-search/description/

* algorithms
* Hard (25.96%)
* Total Accepted:    4.9K
* Total Submissions: 18.7K
* Testcase Example:  '["WordFilter","f"]\n[[["apple"]], ["a","e"]]'


Given many words, words[i] has weight i.

Design a class WordFilter that supports one function, WordFilter.f(String prefix, String suffix).
It will return the word with given prefix and suffix with maximum weight.  If no word exists, return -1.


Examples:

Input:
WordFilter(["apple"])
WordFilter.f("a", "e") // returns 0
WordFilter.f("b", "") // returns -1


Note:

words has length in range [1, 15000].
For each test case, up to words.length queries WordFilter.f may be made.
words[i] has length in range [1, 10].
prefix, suffix have lengths in range [0, 10].
words[i] and prefix, suffix queries consist of lowercase letters only.


