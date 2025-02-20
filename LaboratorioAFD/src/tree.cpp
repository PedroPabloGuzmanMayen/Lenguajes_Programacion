#include "tree.h"
#include "node.h"
#include "shunting_yard.h"
#include <stack>
#include <iostream>
#include <set>
#include <vector>
#include <algorithm>
#include <string>
#include <unordered_map>
#include "AFD.cpp"

std::set<int> setUnion(std::set<int >a,std::set<int >b){
    std::set<int>c;
    c.insert( a.begin() , a.end() );
    c.insert( b.begin() , b.end() );
    return c;
}

std::stack<int> Tree::findPositions(char letter){
    std::stack<int> out;
    for (const auto& pair : this->idValue){
        if(pair.second == letter){
            out.push(pair.first);
        }
    }
    return out;
}



Tree::Tree(std::string expression){
    this->treeExpr = expression;
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

void Tree::calcLastPos(Node* start){
    if (!start) return;

    if(start->getSon(0) != nullptr) calcLastPos(start->getSon(0));
    if(start->getSon(1) != nullptr) calcLastPos(start->getSon(1));

    if (start->getValue() == '.') {
        if (start->getSon(1)->getNullable()) {
            start->setLastPos(setUnion(start->getSon(0)->getLastPos(), start->getSon(1)->getLastPos()));
        } else {
            start->setLastPos(start->getSon(1)->getLastPos()); 
        }
    }
    else if (start->getValue() == '|') {
        start->setLastPos(setUnion(start->getSon(0)->getLastPos(), start->getSon(1)->getLastPos()));
    }
    else if (start->getValue() == '*') {
        start->setLastPos(start->getSon(0)->getLastPos()); 
    }
    else {
        start->setLastPos({start->getID()});
    }
}

void Tree::computeFollowPos(Node * start){
    if (!start) return;

    if(start->getSon(0) != nullptr) computeFollowPos(start->getSon(0));
    if(start->getSon(1) != nullptr) computeFollowPos(start->getSon(1));

    if (start->getValue() == '.'){
        for (int num : start->getSon(0)->getLastPos()) {
            for (int j: start->getSon(1)->getFirstPos()){
                followPosTable[num].insert(j);
            }
        }

    }
    else if (start->getValue() == '*'){
        for (int num : start->getLastPos()) {
            for (int j: start->getFirstPos()){
                followPosTable[num].insert(j);
            }
        }
    }


}

void Tree::displayFollowPos(){
    for (const auto& pair : followPosTable) {
        printf("Posición %d: ", pair.first );
        for (int value : pair.second){
            printf("%d ", value);
        }
        printf("\n");
    }
}

void Tree::getIdValues(Node* start){
    if (!start) return;
    if(start->getSon(0) != nullptr) getIdValues(start->getSon(0));
    if(start->getSon(1) != nullptr) getIdValues(start->getSon(1));
    //Verificar que no sea un operador
    if(start->getID() != 0 ){
        this->idValue[start->getID()] = start->getValue();
        if (start->getValue() == '#'){ //Indicar si es la posición de aceptación
            this->acceptedPos = start->getID();
        }
    }
}

void Tree::displayIDValues(){
    printf("ID values:\n ");
    for (const auto& pair : idValue) {
        printf("ID %d \n: ", pair.first );
        printf("Value %c \n", pair.second);
    }
}

void Tree::convertToAFD(){

    std::vector<std::set<int>> findedStates; //Aquí almacenamos los estados que vamos encontrando
    std::vector<std::set<int>> accepted_states; //Aquí almacenamos los valores de aceptación
    std::vector<std::set<int>> DSTATES; //Aquí almacenamos los estads sin marcar 
    std::map<std::set<int>, std::map<char, std::vector<std::set<int>>>> transitions; //Aquí guardamos las tranciones
    std::vector<std::string> alphabet = getAlphabet(this->treeExpr); //Obtenemos el alfabeto
    /*
    Las transiciones tienen el formato: 
    La primera llave es un conjunto
    El valor dela primera llave es otro Map!
    El Map que es la llave guarda un char, representando el símbolo y un vector de conjuntos
    Ejemplo:
    <1,2,3> : <"a": [<1,2>, <1,3,4>], "b":[<1,3,5>, <4,6,8>]>
    */
    findedStates.push_back(this->root->getFirstPos()); //Añadir firstpos de nodo raíz
    DSTATES.push_back(this->root->getFirstPos()); //Añadimos a la lista de estados sin marcar
    while (DSTATES.size() >0){
        std::set<int> current = DSTATES.back(); //Guardar el estado actual
        if (current.count(this->acceptedPos) >0){
            accepted_states.push_back(current); //Verificar si el estado actual es de aceptación
        }
        DSTATES.pop_back();
        for(const std::string& word : alphabet){
            std::stack<int> positions = findPositions(word[0]);
            std::set<int> newState;
            while (!positions.empty()) { 
                int pos = positions.top();
                positions.pop();
                newState = setUnion(newState, followPosTable[pos]); //Hacer la unión de follow pos
            }
            if (!newState.empty() && std::find(findedStates.begin(), findedStates.end(), newState) == findedStates.end()){ //Verificar si el nuevo estado existe
                findedStates.push_back(newState); //Si no existe, lo agregamos
                DSTATES.push_back(newState);
            }
            transitions[current][word[0]].push_back(newState); //Agregar la transición
        }
    }

    for (const auto& mySet : findedStates) {
        std::cout << "{ ";
        for (const int& val : mySet) {
            std::cout << val << " ";
        }
        std::cout << "} ";  
    }

    std::cout << std::endl;


}


    