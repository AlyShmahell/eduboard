#include <iostream>
#include <stdio.h>
#include <utility>
#include <stack>
#include <queue>
#include <string>
#include <string.h>
#define MAX 1000000
using namespace std;

char start,goal;
char input[3];
pair <char,char> edges[MAX];
stack<char> stage;
queue<char> visited;
char route[MAX];
int edge_space;
int k=3;
void retract();
bool sear(char node);
bool child(char node);
void dfs();
void print();
bool isvisited(char node);
bool isleaf(char node);
bool isroot(char node);

int main()
{
    int t;
    cout<<"Please input your desired number of test cases : \n";
    cin>>t;
    cout<<"good, let's begin testing : \n";
    do
    {
    cout<<"test case : "<<t<<endl;
        cin.ignore();
        edge_space=0;
        while(gets(input)&&strlen(input)==3)
        {
            if(strlen(input)!=3)
                break;

            edges[edge_space].first=input[0];
            edges[edge_space].second=input[2];
            cout<<edges[edge_space].first<<"  :  "<<edges[edge_space].second<<endl;
            edge_space++;
        }
        cout<<"edge_space  :  "<<edge_space<<endl<<"please specify a starting point : \n";
        cin>>start;
        cout<<"please specify a goal to reach : \n";
        cin>>goal;
        bool offgrid = 1;
        for(int i=0; i<edge_space; i++)
        {
            if(edges[i].first==goal||edges[i].second==goal)
            {
                offgrid=0;
                stage.push(start);
                dfs();
                break;

            }
            offgrid=1;
        }
        if(offgrid)
            cout<<"Goal is Off Grid\n";
    }
    while(t--);
}
void retract()
{
    stage.pop();
}
bool sear(char node)
{

}
void print()
{
    while(!stage.empty()&&!isroot(stage.top()))
    {
        cout<<stage.top()<<" <- ";
        stage.pop();
    }
    if(!stage.empty())
    {
        cout<<stage.top();
        stage.pop();
    }
    cout<<endl;
}
bool child(char node)
{
    for(int i=0; i<edge_space; i++)
    {
        if(edges[i].first==node)
        {
            stage.push(edges[i].second);
            edges[i].first='0';
            edges[i].second='0';
            break;
        }
    }
}
bool isleaf(char node)
{
    for(int i=0; i<edge_space; i++)
        if(edges[i].first==node)
            return 0;
    return 1;
}
bool isroot(char node)
{
    if(node==start)
        return 1;
    return 0;
}
void dfs()
{
    char now = stage.top();
    if(now==goal)
        print();
    else if(isroot(now)&&isleaf(now))
        printf("Can't go there from here");
    else
    {

        if(!isleaf(now))
        {
            child(now);
            dfs();
        }
        else
        {
            retract();
            dfs();
        }
    }

}

