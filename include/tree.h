#ifndef TREE_H
#define TREE_H
#include "node.h"
#include <string>
#include <map>
#include <stack>
#include <set>
#include <vector>
#include <unordered_map>

class Tree{
    private:
        Node* root;
        std::map<int, std::set<int>> followPosTable;
        std::map<int, char> idValue;
        std::string treeExpr;
        int acceptedPos;


    public:
        Tree(std::string expression);
        void display(Node* node);
        Node* getRoot();
        void calcNullable(Node* start);
        void calclFirstPos(Node* start);
        void calcLastPos(Node* start);
        void computeFollowPos(Node* start);
        void displayFollowPos();

        std::tuple<
        std::vector<std::set<int>>, 
        std::vector<std::set<int>>, 
        std::vector<std::set<int>>, 
        std::vector<std::string>, 
        std::map<std::set<int>, std::map<char, std::set<int>>>>
        convertToAFD();
        void getIdValues(Node* start);
        void displayIDValues();
        std::stack<int> findPositions(char letter);
};

#endif