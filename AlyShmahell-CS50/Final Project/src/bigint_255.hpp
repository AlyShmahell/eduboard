/**
 * Copyright (C) 2015-2016 Aly Shmahell
 */

#include<iostream>
#include<string.h>
#include<cmath>
using namespace std;
#ifndef BIGINT_255_INCLUDED
#define BIGINT_255_INCLUDED

class bigint_255
{
private :
    //inner string
    string inn;
    //bit counter
    int counter;
    //carry flag
    short flag =0;
    //integer store array
    unsigned short val[255];
    //signal
    char sign = '+';
public :
    bigint_255();
    bigint_255(char in);
    bigint_255(int in);
    bigint_255(long int in);
    bigint_255(long long int in);
    bigint_255(string in);

    friend ostream &operator<<( ostream & output,const bigint_255 &bigint_)
    {

        int i =0;
        while(bigint_.val[i]==0)
            i++;

        if(bigint_.val[i]==10)
        {
            output<<0;
            return output;
        }

        if(bigint_.sign=='-')
            output<<bigint_.sign;

        for(i; bigint_.val[i]<10; i++)
            output<<bigint_.val[i];

        return output;
    }

    friend istream &operator>>(istream &input, bigint_255 &bigint_)
    {
        input>>bigint_.inn;
        unsigned length  = strlen(bigint_.inn.c_str());
        int i=0;
        int j=0;
        if(bigint_.inn[0]=='-')
        {
            bigint_.sign='-';
            j++;
        }
        else
            bigint_.sign='+';

        bigint_.counter=length-j;
        for(i=0; i<bigint_.counter; i++)
        {
            bigint_.val[i]=bigint_.inn[i+j]-'0';
        }
        bigint_.val[i]=10;
        return input;
    }
    void operator=(const bigint_255 &bigint_ )
    {
        counter = bigint_.counter;
        for(int i =0; i<255; i++)
            val[i] = bigint_.val[i];
    }
    bigint_255 &operator--()
    {
        if(sign=='-')
        {
            {
                int i =counter-1;
                while( val[i]==9&&i>-1)
                {
                    val[i]=0;
                    --i;
                }
                if(i<0)
                {
                    for(int j=counter; j>=0; j--)
                    {
                        val[j+1]=val[j];
                    }
                    val[counter+2]=10;
                    val[0]=0;
                    ++i;
                    ++flag;
                }

                ++val[i];
                return *this;
            }
        }
        else
        {
            if(counter==1&&val[0]==0)
            {
                val[0]=1;
                sign='-';
            }
            else
            {
                int i =counter-1;
                while( val[i]==0)
                {
                    val[i]=9;
                    --i;
                }
                --val[i];
                return *this;
            }

        }
    }


    bigint_255 &operator++()
    {
        if(sign=='-')
        {
            {
                if(counter==1&&val[0]==0)
                {
                    val[0]=1;
                    sign='-';
                }
                else
                {

                    int i =counter-1;
                    if(flag==1)
                    {
                        flag--;
                        i++;
                    }
                    while( val[i]==0)
                    {
                        val[i]=9;
                        --i;
                    }
                    --val[i];
                    return *this;
                }

            }
        }
        else
        {
            int i =counter-1;
            while( val[i]==9&&i>-1)
            {
                val[i]=0;
                --i;
            }
            if(i<0)
            {
                for(int j=counter; j>=0; j--)
                {
                    val[j+1]=val[j];
                }
                val[counter+2]=10;
                val[0]=0;
                ++i;
            }

            ++val[i];
            return *this;
        }
    }
    bool operator &&(int second)
    {
        bool logic1 = 0;
        bool logic2 = 0;
        if(second!=0)
            logic2=1;
        for (int i = 0; i<counter; i++)
        {
            if(val[i]!=0)
            {
                logic1=1;
                break;
            }
        }
        if(logic1&&logic2)
        return true;
        else
        return false;
    }
};

bigint_255::bigint_255()
{
    val[0]=0;
    val[1]=10;
    counter = 0;
}
bigint_255::bigint_255(char in)
{
    val[0]=in-'0';
    val[1]=10;
    counter = 0;
}
bigint_255::bigint_255(int in)
{
    if(in<0)
    {
        sign = '-';
        in*=-1;
    }

    int loga = log10(in);
    counter = loga;
    loga++;
    val[loga]=10;
    while(loga)
    {
        val[loga-1]=in%10;
        in/=10;
        loga--;
    }
}
bigint_255::bigint_255(long int in)
{
    if(in<0)
    {
        sign = '-';
        in*=-1;
    }

    int loga = log10(in);
    counter = loga;
    loga++;
    val[loga]=10;
    while(loga)
    {
        val[loga-1]=in%10;
        in/=10;
        loga--;
    }
}
bigint_255::bigint_255(long long int in)
{
    if(in<0)
    {
        sign = '-';
        in*=-1;
    }

    int loga = log10(in);
    counter = loga;
    loga++;
    val[loga]=10;
    while(loga)
    {
        val[loga-1]=in%10;
        in/=10;
        loga--;
    }
}
bigint_255::bigint_255(string in)
{
    unsigned length  = strlen(in.c_str());
    unsigned i=0;
    if(in[0]=='-')
    {
        sign='-';
        i++;
    }
    counter = length-i-1;
    for(i; i<length; i++)
        val[i]=in[i]-'0';
    val[++i]=10;
}


#endif
