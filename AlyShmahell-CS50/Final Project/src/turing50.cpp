/**
Copyright © 2015 Aly Shmahell
*/

#include "turing50.hpp"

int main(int argc, char** argv)
{
    cout<<"\n#######################################################\n"
    <<"The Turing50 Interpreter 0.1 Alpha                    #\n"
    <<"Copyright 2015 Aly Shmahell                           #\n"
    <<"                                                      #\n"
    <<"Usage :                                               #\n"
    <<"        File Interpretation : ./Turing50 filename.b   #\n"
    <<"        FreeStyle : ./Turing50                        #\n"
    <<"                                                      #\n"
    <<"   Turing50 is a Tape Programming Language similar to #\n"
    <<"                     Brainf*ck & P"<<'"'<<"                   #\n"
    <<"                                                      #\n"
    <<"Commands :                                            #\n"
    <<"             ,     Input decimal at current pointer   #\n"
    <<"             .     Output decimal at current pointer  #\n"
    <<"             >     Increase Pointer                   #\n"
    <<"             <     Decrease Pointer                   #\n"
    <<"             +     Increase Value at pointer          #\n"
    <<"             -     Decrease Value at Pointer          #\n"
    <<"             [     Start Loop                         #\n"
    <<"             ]     End Loop                           #\n"
    <<"                                                      #\n"
    <<"#######################################################\n";
    if(argv[1])
    FileInterpret(argv[1]);
    else
    FreeStyle();
}
