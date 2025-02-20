#ifndef TREE_H
#define TREE_H
#include "node.h"
#include <string>
#include <map>
#include <stack>
#include <set>

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
        void convertToAFD();
        void getIdValues(Node* start);
        void displayIDValues();
        std::stack<int> findPositions(char letter);
};

#endif