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
        Node(std::string value, int id);

        void setFirstPos(int pos);

        int getFirstPos();

        void setLastPos(int pos);

        void setSon(Node* son, int position);

        Node* getSon(int pos);
};

#endif