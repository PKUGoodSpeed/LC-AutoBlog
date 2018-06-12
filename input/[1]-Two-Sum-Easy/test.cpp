class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target){
        unordered_map<int, int> pos;
        for(int i=0; i<(int)nums.size(); ++i){
            if(pos.count(target-nums[i])){
                return vector<int> {pos[target-nums[i]], i};
            }
            pos[nums[i]] = i;
        }
        return vector<int>{-1, -1};
    }
};