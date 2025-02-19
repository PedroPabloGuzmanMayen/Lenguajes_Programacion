#include "tree.h"
#include "node.h"
#include <stack>
#include <set>
#include <algorithm>
#include <string>

std::set<int> setUnion(std::set<int >a,std::set<int >b){
    std::set<int>c;
    c.insert( a.begin() , a.end() );
    c.insert( b.begin() , b.end() );
    return c;
}

Tree::Tree(std::string expression){

    int counter = 1; //Nos ayudará a asignarle una posición/id a cada nodo
    std::stack<Node*> nodeStack; //Stack de nodos: nos ayudará a tener registro de los nodos que se van creando

    for (int i = 0; i<expression.length(); i++){
        if ((expression[i] == '|' || expression[i] == '.') && !nodeStack.empty()){
            //Los 2 últimos en el elementos en el stack de nodos serán los hijos del nuevo nodo
            Node* newNode = new Node(expression[i]);
            newNode->setSon(nodeStack.top(), 1); 
            nodeStack.pop();
            newNode->setSon(nodeStack.top(), 0);
            nodeStack.pop();
            nodeStack.push(newNode);
        }
        else if (expression[i] == '*' && !nodeStack.empty()){
            //El último elemento en el stack de nodos será el hijo izquierdo del nuevo nodo
            Node* newNode = new Node(expression[i]);
            newNode->setSon(nodeStack.top(), 0);
            nodeStack.pop();
            nodeStack.push(newNode);
        }
        else {
            //Si no es un operador, simplemente lo agregamos al stack de nodos, este nodo si tendrá un id asociado. 
            nodeStack.push(new Node(expression[i], counter));
            counter +=1;
        }

    }
    //El último nodo en el stack será el nodo raíz
    if(!nodeStack.empty()){
        this->root = nodeStack.top();
        nodeStack.pop();
    }
}

void Tree::display(Node* node){
    if (!node) return; //Si es null, retornamos
    node->display(); //Imprimimos la información del nodo
    display(node->getSon(0)); //Vamos al hijo izquierdo
    display(node->getSon(1)); //Vamos al hijo derecho;
}

Node* Tree::getRoot(){
    return this->root;
}

void Tree::calcNullable(Node* start){
    //printf("Computing nullable: ");
    if(!start) return;

    calcNullable(start->getSon(0));
    calcNullable(start->getSon(1));

    if (start->getValue() == '.'){
        start->setNullable(start->getSon(0)->getNullable() && start->getSon(1)->getNullable() );
    }
    else if (start->getValue() == '|'){
        start->setNullable(start->getSon(0)->getNullable() || start->getSon(1)->getNullable() );
    }
    else if (start->getValue() == '*'){
        start->setNullable(true);
    }
    else {
        start->setNullable(false);
    }
}

void Tree::calclFirstPos(Node* start){
    if (!start) return;

    if(start->getSon(0) != nullptr) calclFirstPos(start->getSon(0));
    if(start->getSon(1) != nullptr) calclFirstPos(start->getSon(1));

    if (start->getValue() == '.') {
        if (start->getSon(0)->getNullable()) {
            start->setFirstPos(setUnion(start->getSon(0)->getFirstPos(), start->getSon(1)->getFirstPos()));
        } else {
            start->setFirstPos(start->getSon(0)->getFirstPos()); 
        }
    }
    else if (start->getValue() == '|') {
        start->setFirstPos(setUnion(start->getSon(0)->getFirstPos(), start->getSon(1)->getFirstPos()));
    }
    else if (start->getValue() == '*') {
        start->setFirstPos(start->getSon(0)->getFirstPos()); 
    }
    else {
        start->setFirstPos({start->getID()});
    }
}

#include "tree.h"
#include "node.h"
#include <stack>
#include <set>
#include <algorithm>
#include <string>

std::set<int> setUnion(std::set<int >a,std::set<int >b){
    std::set<int>c;
    c.insert( a.begin() , a.end() );
    c.insert( b.begin() , b.end() );
    return c;
}

Tree::Tree(std::string expression){

    int counter = 1; //Nos ayudará a asignarle una posición/id a cada nodo
    std::stack<Node*> nodeStack; //Stack de nodos: nos ayudará a tener registro de los nodos que se van creando

    for (int i = 0; i<expression.length(); i++){
        if ((expression[i] == '|' || expression[i] == '.') && !nodeStack.empty()){
            //Los 2 últimos en el elementos en el stack de nodos serán los hijos del nuevo nodo
            Node* newNode = new Node(expression[i]);
            newNode->setSon(nodeStack.top(), 1); 
            nodeStack.pop();
            newNode->setSon(nodeStack.top(), 0);
            nodeStack.pop();
            nodeStack.push(newNode);
        }
        else if (expression[i] == '*' && !nodeStack.empty()){
            //El último elemento en el stack de nodos será el hijo izquierdo del nuevo nodo
            Node* newNode = new Node(expression[i]);
            newNode->setSon(nodeStack.top(), 0);
            nodeStack.pop();
            nodeStack.push(newNode);
        }
        else {
            //Si no es un operador, simplemente lo agregamos al stack de nodos, este nodo si tendrá un id asociado. 
            nodeStack.push(new Node(expression[i], counter));
            counter +=1;
        }

    }
    //El último nodo en el stack será el nodo raíz
    if(!nodeStack.empty()){
        this->root = nodeStack.top();
        nodeStack.pop();
    }
}

void Tree::display(Node* node){
    if (!node) return; //Si es null, retornamos
    node->display(); //Imprimimos la información del nodo
    display(node->getSon(0)); //Vamos al hijo izquierdo
    display(node->getSon(1)); //Vamos al hijo derecho;
}

Node* Tree::getRoot(){
    return this->root;
}

void Tree::calcNullable(Node* start){
    //printf("Computing nullable: ");
    if(!start) return;

    calcNullable(start->getSon(0));
    calcNullable(start->getSon(1));

    if (start->getValue() == '.'){
        start->setNullable(start->getSon(0)->getNullable() && start->getSon(1)->getNullable() );
    }
    else if (start->getValue() == '|'){
        start->setNullable(start->getSon(0)->getNullable() || start->getSon(1)->getNullable() );
    }
    else if (start->getValue() == '*'){
        start->setNullable(true);
    }
    else {
        start->setNullable(false);
    }
}