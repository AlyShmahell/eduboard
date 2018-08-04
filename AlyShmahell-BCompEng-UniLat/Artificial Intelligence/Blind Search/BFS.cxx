#include<iostream>
#include<stdio.h>
#include<stack>
#include<queue>
#include<string>
#include<string.h>
#define MAX 1000000
using namespace std;

queue <string> path;
queue <char> stage;
pair<char,char> edges[MAX];
int edge_space;
char input[3];
char start,goal;
bool isroot(char node);
bool isleaf(char node);
void print();
void bfs();
void child(char node, string route);

int main()
{
    int t;
    cout<<"please input the desired number of test cases\n";
    cin>>t;
    cout<<"good now let's begin\n";
    do
    {
        cout<<"Test Case : "<<t<<endl;
        edge_space=0;
        cin.ignore();
        while(gets(input)&&strlen(input)==3)
        {
            edges[edge_space].first=input[0];
            edges[edge_space].second=input[2];
            cout<<input[0]<<" : "<<input[2]<<endl;
            edge_space++;
            if(strlen(input)!=3)
                break;
        }
        cout<<"edge space : "<<edge_space<<endl;
        cout<<"enter starting node\n";
        cin>>start;
        cout<<"enter goal node\n";
        cin>>goal;
        bool offgrid = 1;
        for(int i=0; i<edge_space; i++)
        {
            if(edges[i].first==goal||edges[i].second==goal)
            {
                offgrid=0;
                string temp="";
                temp+=start;
                path.push(temp);
                stage.push(start);
                bfs();
                break;

            }
            offgrid=1;
        }
        if(offgrid)
            cout<<"Goal is Off Grid\n";
    }
    while(t--);
}
bool isroot(char node)
{
    if(node==start)
        return 1;
    return 0;
}
bool isleaf(char node)
{
    for(int i=0; i<edge_space; i++)
    {
        if(edges[i].first==node)
        {
            return 0;
            break;
        }
    }
    return 1;
}
void print()
{
    cout<<"Path Found : ";
    if(!path.empty())
    {
        int i;
        string route = path.front();
        for(i = 0;i<strlen(route.c_str())-1;i++)
        cout<<route[i]<<" -> ";
        cout<<route[i];
    }
    cout<<endl;
}
void child(char node, string route)
{
    string t_route;
    for(int i=0; i<edge_space; i++)
    {
        if(edges[i].first==node)
        {
            stage.push(edges[i].second);
            t_route=route;
            t_route+=edges[i].second;
            path.push(t_route);
        }
    }
}
void retract()
{
    if(!stage.empty())
        stage.pop();
    if(!path.empty())
        path.pop();
}
void bfs()
{
    char now;
    if(!stage.empty())
        now  = stage.front();

    string route;
    if(!path.empty())
        route=path.front();

    if(goal==now)
        print();

    else if(isroot(now)&&isleaf(now))
        printf("you can't go there from here\n");

    else
    {
        if(!isleaf(now))
        {
            retract();
            child(now,route);
            bfs();
        }
        else
        {
            retract();
            bfs();
        }
    }
}
