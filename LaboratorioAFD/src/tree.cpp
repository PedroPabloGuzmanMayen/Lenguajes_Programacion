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
#include "AFD.h"
#include <tuple>
#include "constantes.h"

std::set<int> setUnion(std::set<int >a,std::set<int >b){
    std::set<int>c;
    c.insert( a.begin() , a.end() );
    c.insert( b.begin() , b.end() );
    return c;
}

std::pair<bool, int> findCommonElement(const std::set<int>& current, const std::vector<int>& acceptedPos) {
    for (int c : current) {
        if (std::find(acceptedPos.begin(), acceptedPos.end(), c) != acceptedPos.end()) {
            return {true, c};  
        }
    }
    return {false, -1};  
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
        else  {
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
        if (start->getValue() == EPSILON){
            start->setNullable(true); 
        }
        else {
            start->setNullable(false);
        }
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
        if (start->getValue() == EPSILON){
            start->setFirstPos({});
        }
        else {
            start->setFirstPos({start->getID()}); 
        }
        
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
        if (start->getValue() == EPSILON){ //Verficar si es la cadena vacia
            start->setLastPos({});
        }
        else {
            start->setLastPos({start->getID()}); 
        }
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



void Tree::getIdValues(Node* start) {

    std::vector<std::string> alfabetoGriego = {
        "\x03", "\x04", "\x05", "\x06", "\x07", "\x08", "\x09",
        "\x13", "\x14", "\x15",
       "\x16", "\x17", "\x18", "\x19",
   };
   

    if (!start) return;
    if (start->getSon(0) != nullptr) getIdValues(start->getSon(0));
    if (start->getSon(1) != nullptr) getIdValues(start->getSon(1));

    // Verificar que no sea un operador
    if (start->getID() != 0) {
        this->idValue[start->getID()] = start->getValue();

        // Asegurarse de que getValue() sea un tipo compatible
        std::string value;
        if (sizeof(start->getValue()) == sizeof(char)) {
            value = std::string(1, start->getValue()); // Si es char, convertirlo a std::string
        } else {
            value = start->getValue(); // Si ya es un string o tipo adecuado, usarlo directamente
        }

        // Verificar si el valor está en el alfabeto griego
        if (std::find(alfabetoGriego.begin(), alfabetoGriego.end(), value) != alfabetoGriego.end()) {
            this->acceptedPos.push_back(start->getID());
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

void Tree::displayAcceptedPos(){
    for (int i = 0; i< this->acceptedPos.size(); i++){
        printf("Accepted Pos: %d\n", acceptedPos[i]);
    }
}

std::tuple<
        std::vector<std::set<int>>, 
        std::vector<std::set<int>>, 
        std::vector<std::set<int>>, 
        std::vector<std::string>, 
        std::map<std::set<int>, std::map<char, std::set<int>>> ,
        std::map<std::set<int>,char> >
Tree::convertToAFD() {
    
    std::vector<std::set<int>> findedStates;
    std::vector<std::set<int>> accepted_states;
    std::vector<std::set<int>> DSTATES;
    std::map<std::set<int>, std::map<char, std::set<int>>> transitions;
    std::vector<std::string> alphabet = getAlphabet(this->treeExpr);
    std::map<std::set<int>, char> terminators; //Sirve para indiar a que estaddo de aceptación pertenece cada

    findedStates.push_back(this->root->getFirstPos());
    DSTATES.push_back(this->root->getFirstPos());

    while (!DSTATES.empty()) {
        std::set<int> current = DSTATES.back();
        auto result = findCommonElement(current, this->acceptedPos);
        if (result.first) {
            accepted_states.push_back(current);
            printf("Common pos: %d\n", result.second);
            printf("Common pos char: %c\n", idValue[result.second]);
            terminators[current] = idValue[result.second]; //Linkear cada estado de aceptación con su terminador
        }
        DSTATES.pop_back();

        for (const std::string& symbol : alphabet) {
            std::set<int> newState;
            for (int pos : current) {
                if (idValue[pos] == symbol[0]) {
                    newState = setUnion(newState, followPosTable[pos]);
                }
            }

            if (!newState.empty()) {

                if (std::find(findedStates.begin(), findedStates.end(), newState) == findedStates.end()) {
                    findedStates.push_back(newState);
                    DSTATES.push_back(newState);
                }
                transitions[current][symbol[0]] = newState;
            }
        }
    }

    int stateNum = 0;
    for (const auto& state : findedStates) {
        //std::cout << "State " << stateNum++ << ": { ";
        for (const int& val : state) {
            std::cout << val << " ";
        }
        //std::cout << "}\n";
    }

    for (const auto& [state, symbolMap] : transitions) {
        //std::cout << "From state { ";
        for (int val : state) std::cout << val << " ";
        //std::cout << "}\n";
        
        for (const auto& [symbol, nextState] : symbolMap) {
            //std::cout << "  On '" << symbol << "' -> { ";
            for (int val : nextState) std::cout << val << " ";
            //std::cout << "}\n";
        }
    }
    return std::make_tuple(findedStates, accepted_states, DSTATES, alphabet, transitions, terminators);
}





    


    