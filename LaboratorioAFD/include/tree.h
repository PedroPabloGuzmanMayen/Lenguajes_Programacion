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
        bool calcNullable(Node* start);
};

#endif