[596] Classes More Than 5 Students  

https://leetcode.com/problems/classes-more-than-5-students/description/

* database
* Easy (31.48%)
* Total Accepted:    18.8K
* Total Submissions: 59.7K
* Testcase Example:  '{"headers": {"courses": ["student", "class"]}, "rows": {"courses": [["A", "Math"], ["B", "English"], ["C", "Math"], ["D", "Biology"], ["E", "Math"], ["F", "Computer"], ["G", "Math"], ["H", "Math"], ["I", "Math"]]}}'


There is a table courses with columns: student and class

Please list out all classes which have more than or equal to 5 students.


For example, the table:


+---------+------------+
| student | class      |
+---------+------------+
| A       | Math       |
| B       | English    |
| C       | Math       |
| D       | Biology    |
| E       | Math       |
| F       | Computer   |
| G       | Math       |
| H       | Math       |
| I       | Math       |
+---------+------------+


Should output:

+---------+
| class   |
+---------+
| Math    |
+---------+



Note:
The students should not be counted duplicate in each course.

