#include<iostream>
#include<string>
using namespace std;
class docData{
    public:
    int id;
    docData(int id,int pos){
        id = id;
        addPosition(pos);
    }
    int positons[10];
    int counter = 0;
    void addPosition(int pos){
        positions[counter++] = pos;
    }
};


class wordData{
    public:
        string name;
        int frequency;
        docData* docs[10];
        int docCounter = 0;
        wordData(string s){
            name = s;
            frequency = 0;
        }

        void addDocument(int id, int pos){
            int newDocCounter = docCounter;
            frequency++
            for(int i =0;i<docCounter;i++){
                if(docs[docCounter]->id == id){
                    docs[newDocCounter++]->addPosition(pos);
                    break;
                }
            }
            if(newDocCounter==docCounter){
                docs[docCounter++] = new docData(id,pos)
            }
        }
}

int main()
{
 return 0;
}