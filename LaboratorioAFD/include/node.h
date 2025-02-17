#ifndef NODE_H
#define NODE_H
#include <string>

class Node {
    private:
        int firstPos;
        int lastPos;
        int id;
        std::string value;
        Node* leftSon;
        Node* rightSon;

    public:
        Node(std::string value){ value = value; }

        void setFirstPos(int pos){ firstPos = pos; }

        int getFirstPos(){ return firstPos; }

        void setLastPos(int pos){ lastPos = pos; }

        void setSon(Node* son, int position){ position == 0 ? leftSon = son: rightSon = son; } //0 para hijo izquierdo, 1 para hijo derecho

        Node* getSon(int pos){pos == 0 ? leftSon: rightSon; }
};

#endif