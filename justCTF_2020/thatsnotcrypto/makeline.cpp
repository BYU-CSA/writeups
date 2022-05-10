#include <iostream>
#include <string>
#include <stdio.h>
#include <stdlib.h>
#include <fstream>

using namespace std;

int main(int argc, char* argv[]) {
    string chars = "acbdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ`~!@#$%^&*()-_=+[{]}\\|'\";:/?.>,<";
    //string chars = "`~!@#$%^&*()-_=+[{]}\\|'\";:/?.>,<";

    string answer = "";
    for (int k = 0; k < 57; k++) {
        for (int j = 0; j < chars.length(); j++) {
            string value = answer;
            for (int i = 0; i < 57-k; i++) {
                value += chars[j];
            }
            //cout << value << endl;

            string command = "echo \"" + value + "\" | python3 checker2.py > outputfiles/" + to_string(j) + "";
            cout << command << endl;
            system(command.c_str());

            
        }
        string grep = "grep \"~";
        for (int b = 0; b < k; b++) {
            grep += "~";
        }
        
        grep += "\" outputfiles/* > successfulCharacter.txt";
        system(grep.c_str());

        ifstream ifs;
        ifs.open("successfulCharacter.txt");

        string input;
        getline(ifs, input);

        string successfulCharacter = input.substr(12,2);
        int index;

        try {
            index = stoi(successfulCharacter);
        }
        catch (...) {
            index = stoi(successfulCharacter.substr(0,1));
        }
        
        cout << to_string(index) << endl;
        answer += chars[index];
    }

    return 0;
}