#include "node.h"
#include <string>

Node::Node(std::string newValue, int newID){
    value = newValue;
    id = newID;
    leftSon = nullptr;
    rightSon = nullptr;
    firstPos = -1;
    lastPos = -1;
}

void Node::setFirstPos(int pos){ firstPos = pos; }

int Node::getFirstPos(){ return firstPos; }

void Node::setLastPos(int pos){ lastPos = pos; }

void Node::setSon(Node* son, int position){ position == 0 ? leftSon = son: rightSon = son; } //0 para hijo izquierdo, 1 para hijo derecho

Node* Node::getSon(int pos){pos == 0 ? leftSon: rightSon; }

