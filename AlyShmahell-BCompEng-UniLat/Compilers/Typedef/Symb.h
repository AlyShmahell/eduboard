#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define _int 1
#define _real 2
#define _char 3
#define _chain 4


typedef struct node
{
    char val[90];
    int type;
    struct node *next;
}node;

node *list_ = NULL;

int put_symb(char *val, int type)
{
    node *curr = (node*) malloc(sizeof(node));
    curr = list_;
    while(curr!=NULL)
    {
        if(strcmp(curr->val,val)==NULL)
            return 0;
        curr = curr->next;
    }
    node *new_=(node*)malloc(sizeof(node));
    strcpy(new_->val,val);
    new_->type=type;
    new_->type=type;
    new_->next=list_;
    list_=new_;
    return 1;
}

int get_symb(char* val)
{
    node* curr = list_;
    while(curr!=NULL)
    {
        if(strcmp(curr->val,val)==NULL)
            return 1;
        curr = curr->next;
    }
    return 0;
}

int get_type(char* val)
{
    node* curr = list_;
    while(curr!=NULL)
    {
        if(strcmp(curr->val,val)==NULL)
            return curr->type;
        curr = curr->next;
    }
    return 0;
}
