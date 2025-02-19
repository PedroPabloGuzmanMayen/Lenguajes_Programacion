#ifndef TREE_H
#define TREE_H
#include "node.h"
#include <string>

class Tree{
    private:
        Node* root;

    public:
        Tree(std::string expression);
        void display(Node* node);
        Node* getRoot();
        void calcNullable(Node* start);
        void calclFirstPos(Node* start);
        void calcLastPos(Node* start);
};

#endif