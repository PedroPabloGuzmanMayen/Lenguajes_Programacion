#include "node.h"
#include <string>

Node::Node(char newValue){
    this->value = newValue;
    this->id = 0; //Se usará el 0 para identificar los nodos que no son nodo hoja
    this->leftSon = nullptr;
    this->rightSon = nullptr;
    this->firstPos = -1;
    this->lastPos = -1;
}

Node::Node(char newValue, int newID){
    this->value = newValue;
    this->id = newID;
    this->leftSon = nullptr;
    this->rightSon = nullptr;
    this->firstPos = -1;
    this->lastPos = -1;
}

void Node::setFirstPos(int pos){ this->firstPos = pos; }

int Node::getFirstPos(){ return this->firstPos; }

void Node::setLastPos(int pos){ this->lastPos = pos; }

void Node::setSon(Node* son, int position){ position == 0 ? this->leftSon = son: this->rightSon = son; } //0 para hijo izquierdo, 1 para hijo derecho

Node* Node::getSon(int pos){ return pos == 0 ? this->leftSon: this->rightSon; }

void Node::display(){
    printf("Node value: %c\n", this->value);
    printf("Node id: %d\n", this->id);
}

