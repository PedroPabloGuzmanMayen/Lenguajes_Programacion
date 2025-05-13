#include "node.h"
#include <set>
#include <string>

Node::Node(char newValue){
    this->value = newValue;
    this->id = 0; //Se usará el 0 para identificar los nodos que no son nodo hoja
    this->leftSon = nullptr;
    this->rightSon = nullptr;
    this->nullable = false;
}

Node::Node(char newValue, int newID){
    this->value = newValue;
    this->id = newID;
    this->leftSon = nullptr;
    this->rightSon = nullptr;
    this->nullable = false;
}

void Node::setFirstPos(std::set<int> pos){ this->firstPos = pos; }

std::set<int> Node::getFirstPos(){ return this->firstPos; }

std::set<int> Node::getLastPos(){return this->lastPos; }

void Node::setLastPos(std::set<int> pos){ this->lastPos = pos; }

void Node::setSon(Node* son, int position){ position == 0 ? this->leftSon = son: this->rightSon = son; } //0 para hijo izquierdo, 1 para hijo derecho

Node* Node::getSon(int pos){ return pos == 0 ? this->leftSon: this->rightSon; }

void Node::display(){
    printf("Node value: %c\n", this->value);
    printf("Node id: %d\n", this->id);
    printf("Nullable: %d\n", this->nullable);
    printf("Elementos de first pos:\n");
    for (int num : this->firstPos) {
        printf("%d ", num); 
    }
    printf("\n");
    printf("Elementos de last pos:\n");
    for (int num : this->lastPos) {
        printf("%d ", num); 
    }
    printf("\n");
}

void Node::setNullable(bool newVal){ this->nullable = newVal;}

bool Node::getNullable(){ return this->nullable; }

char Node::getValue(){return this->value;}

int Node::getID(){return this->id; }

