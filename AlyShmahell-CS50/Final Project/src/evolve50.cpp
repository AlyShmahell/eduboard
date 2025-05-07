/**
 * Copyright (C) 2015-2016 Aly Shmahell
 */

#include "evolve50.hpp"
#include "turing50.hpp"

#define GENERATIONS 100

int main()
{

    cout<<"\n#######################################################################\n"
        <<"This is the Evolve50 AI tool                                          #\n"
        <<"a Gene-Pool-Effect tool that generates program generations            #\n"
        <<"to solve arithmetic and cryptographic problems!                       #\n"
        <<"#######################################################################\n";

    cout<<"\n#######################################################################\n"
        <<"Please specify 3 pairs of \'Single_Input Single_Output\' testcases      #\n"
        <<"and let the tool find a suitable program to solve the problem at hand #\n"
        <<"#######################################################################\n";
    initialize();
    for(int i = 0; i<3; i++)
    {
        cout<<"testcase pair #"<<i+1<<": ";
        scanf("%llu %llu",&dinput[i],&doutput[i]);
    }
    for(int i=0; i<GENERATIONS; i++)
    {
        cout<<"generation #"<<i<<endl;
        cycle();
    }

}
