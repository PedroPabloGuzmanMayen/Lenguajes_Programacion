#ifndef TREE_H
#define TREE_H
#include "node.h"
#include <string>
#include <map>
#include <set>

class Tree{
    private:
        Node* root;
        std::map<int, std::set<int>> followPosTable;
        std::map<int, char> idValue;


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
};

#endif