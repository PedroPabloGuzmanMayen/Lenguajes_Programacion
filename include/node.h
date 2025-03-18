#ifndef NODE_H
#define NODE_H
#include <string>
#include <set>

class Node {
    private:
        std::set<int> firstPos;
        std::set<int> lastPos;
        int id;
        char value;
        bool nullable;
        Node* leftSon;
        Node* rightSon;
    public:
        Node(char value);
        Node(char value, int id);
        void setFirstPos(std::set<int> pos);
        std::set<int> getFirstPos();
        std::set<int> getLastPos();
        void setLastPos(std::set<int> pos);
        void setSon(Node* son, int position);
        Node* getSon(int pos);
        void display();
        bool getNullable();
        void setNullable(bool newVal);
        char getValue();
        int getID();
};

#endif