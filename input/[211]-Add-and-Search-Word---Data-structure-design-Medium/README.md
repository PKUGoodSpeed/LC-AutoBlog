[211] Add and Search Word - Data structure design  

https://leetcode.com/problems/add-and-search-word-data-structure-design/description/

* algorithms
* Medium (25.84%)
* Total Accepted:    78.5K
* Total Submissions: 303.6K
* Testcase Example:  '["WordDictionary","addWord","addWord","addWord","search","search","search","search"]\n[[],["bad"],["dad"],["mad"],["pad"],["bad"],[".ad"],["b.."]]'

Design a data structure that supports the following two operations:


void addWord(word)
bool search(word)


search(word) can search a literal word or a regular expression string containing only letters a-z or .. A . means it can represent any one letter.

Example:


addWord("bad")
addWord("dad")
addWord("mad")
search("pad") -> false
search("bad") -> true
search(".ad") -> true
search("b..") -> true


Note:
You may assume that all words are consist of lowercase letters a-z.

