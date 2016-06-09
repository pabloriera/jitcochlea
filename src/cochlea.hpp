#ifndef COCHLEA_H_
#define COCHLEA_H_


#include <cmath>
#include <vector>
#include <iostream>
using namespace std;

#define PI 3.14159265358979323846

typedef double floating;
typedef vector<floating> floating_vector;
typedef floating* floating_pointer;

class Cochlea_t {

    public:
        Cochlea_t(){}
        
        void gaussian_elimination_init();
        void set_arrays();
        
        void setup();
        
        void operator()( floating_vector &X , floating_vector &dXdt , floating t );
        
        floating_vector g;
        floating_vector a;
        floating_vector b;
        floating_vector c;
        floating_vector p;
        floating_vector k;

        floating_pointer co;
        floating_pointer pa;
        floating_pointer in;

        floating_vector X;
        floating_pointer X_t;
        
        floating dt;
        
        
        int n_t, n_vars, n_channels, n_parameters, n_coefficients, n_inputs, N;
        
        floating alpha, beta, asb, fluid, mef;
    
};

struct Observer_t {

    int c,k;
    floating_pointer &m_X_t;
    floating_pointer &m_times;
    int m_n_eq;
    int m_dec;

    Observer_t( floating_pointer &X_t , floating_pointer &times, int n_eq, int decimate=1 )
              : m_X_t( X_t ) , m_times( times ) , m_dec(decimate), m_n_eq(n_eq) {c = 0;k=0; }

    void operator()( const floating_vector &X , floating t )
    {
        if (k%m_dec==0)
        {
            // cout << k << " " << c << endl;
            m_times[c] = t;
            for(int i = 0; i<m_n_eq; i++)
            {
                m_X_t[c*m_n_eq+i] = X[i];
            }
            c++;
        }
        k++;        
//            cout << c << endl;
    }

};

struct Observer_variable_t {

    vector<floating_vector> &m_X_t;
    vector<floating> &m_times;
    
    Observer_variable_t( vector<floating_vector> &X_t , vector<floating> &times ): m_X_t( X_t ) , m_times( times ){ }

    void operator()( const floating_vector &X , floating t )
    {
        m_times.push_back(t);
        m_X_t.push_back(X);
    }

};

inline floating linear_interpolation(floating_pointer S, floating k)
{
    size_t k_1  = floor(k);
    size_t k_2  = k_1 + 1;
    floating ee = k - k_1;
    return S[k_1]*(1-ee) + S[k_2]*ee;
}


inline floating linear_interpolation_row(floating_pointer S, floating m, int col, int N, int M)
{
    int m_1  = floor(m);
    int m_2  = m_1 + 1;
    floating ee = m - m_1;

    //cout << m_2 <<"\t"<< M <<"\t"<< col << endl;

    if ((m_1*M+col>0) && (m_2*M + col < N*M))
        return S[m_1*M+col]*(1-ee) + S[m_2*M + col]*ee;
    else
        return 0;
}

#endif