#ifndef NODE_H
#define NODE_H
#include <string>
#include <set>

class Node {
<<<<<<< HEAD
    private:
        std::set<int> firstPos;
=======
    public:
        int firstPos;
>>>>>>> refs/remotes/origin/main
        int lastPos;
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
        void setLastPos(int pos);
        void setSon(Node* son, int position);
        Node* getSon(int pos);
        void display();
        bool getNullable();
        void setNullable(bool newVal);
        char getValue();
        int getID();
        void insert_to_firstPost(int value);
};

#endif