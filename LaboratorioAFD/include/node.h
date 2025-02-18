#ifndef NODE_H
#define NODE_H
#include <string>

class Node {
    private:
        int firstPos;
        int lastPos;
        int id;
        char value;
        bool nullable;
        Node* leftSon;
        Node* rightSon;
    public:
        Node(char value);
        Node(char value, int id);
        void setFirstPos(int pos);
        int getFirstPos();
        void setLastPos(int pos);
        void setSon(Node* son, int position);
        Node* getSon(int pos);
        void display();
        bool getNullable();
        void setNullable(bool newVal);
        char getValue();
};

#endif