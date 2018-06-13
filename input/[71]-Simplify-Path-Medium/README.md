[71] Simplify Path  

https://leetcode.com/problems/simplify-path/description/

* algorithms
* Medium (26.52%)
* Total Accepted:    115.9K
* Total Submissions: 436.9K
* Testcase Example:  '"/home/"'

Given an absolute path for a file (Unix-style), simplify it.

For example,
path = "/home/", => "/home"
path = "/a/./b/../../c/", => "/c"

Corner Cases:


	Did you consider the case where path = "/../"?
	In this case, you should return "/".
	Another corner case is the path might contain multiple slashes '/' together, such as "/home//foo/".
	In this case, you should ignore redundant slashes and return "/home/foo".


