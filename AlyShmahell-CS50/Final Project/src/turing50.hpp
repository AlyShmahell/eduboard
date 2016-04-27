/**
Copyright © 2015 Aly Shmahell
*/

#include <stdio.h>
#include <iostream>
#include <fstream>
#include <string>
#include <queue>
#include "bigint_255.hpp"
using namespace std;
#ifndef TURING50_INCLUDED
#define TURING50_INCLUDED

//functional mode input
long long int finput;
//functional mode output
long long int foutput;
//this is where data is stored
long long int cell_range[5000];
//this is where a single command is temporarily stored
char command;
//this is where commands are stored
char line[5000];
//this is the data pointer
int ptr=0;
//this is the command index
int indx=0;
//this is a stop signal for the while loop
int stop=0;
//this is where every line is stored prior to interpretation
queue <char> mainq;

//loop level
int loop_level=0;

void interpret(string mode)
{

    if(command==',')
    {
        if(mode=="functional")
        {
            cell_range[ptr]=finput;
        }
        else
            cin>>cell_range[ptr];
        indx++;

    }
    if(command=='.')
    {
        if(mode=="functional")
        {
            foutput=cell_range[ptr];
        }
        else
            cout<<cell_range[ptr]<<" ";
        indx++;
    }
    if(command=='>')
    {
        ++ptr;
        indx++;
    }
    if(command=='<')
    {
        --ptr;
        indx++;
    }
    if(command=='+')
    {
        ++cell_range[ptr];
        indx++;
    }
    if(command=='-')
    {
        --cell_range[ptr];
        indx++;
    }
    if(command=='[')
    {

        loop_level++;
        queue <char> tempq;
        while(!mainq.empty())
        {

            command = mainq.front();
            mainq.pop();

            if(command=='[')
            {
                interpret(mode);
            }

            if(command==']'&&loop_level>=0)
                break;

            else
            {
                tempq.push(command);
                interpret(mode);
            }
        }

        while(cell_range[ptr]&&!tempq.empty())
        {
            command=tempq.front();
            tempq.pop();
            tempq.push(command);
            interpret(mode);
        }
        loop_level--;
    }

    if(command==']')
    {
        indx++;
    }
}
//functional mode
void functional_mode(string strng)
{
    for(int i=0; i<5000; i++)
        cell_range[i]=0;
    int length = strlen(strng.c_str());
    for(int i=0; i<length; i++)
    {
        mainq.push(strng.c_str()[i]);
    }
    while(!mainq.empty())
    {
        command=mainq.front();
        mainq.pop();
        interpret("functional");
    }
}
void FreeStyle()
{

    while(1)
    {
        cout<<"\n~ ";
        scanf("%s",&line);
        for(int i=0; line[i]!='\0'; i++)
        {
            mainq.push(line[i]);
        }
        while(!mainq.empty())
        {
            command=mainq.front();
            mainq.pop();
            interpret("freestyle");
        }
    }
}
void FileInterpret(char* argz)
{
    if(argz)
    {
        ifstream in(argz);
        if(!in)
        {
            cout<<"No such file\n Reverting back to FreeStyle\n";
            FreeStyle();
        }
        else
        {
            cout<<"\n~ ";
            int i=0;
            while(in)
            {
                in.get(line[i]);
                cout<<line[i];
                mainq.push(line[i]);
                i++;
            }
            line[i]='\0';
        }
        while(!mainq.empty())
        {
            command=mainq.front();
            mainq.pop();
            interpret("file");
        }
        cout<<"\n#######################################################\n"
            <<"#              ~~End of Interpretation~~              #\n"
            <<"#######################################################\n";
    }
}

#endif
