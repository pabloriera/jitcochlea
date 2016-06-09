#include "stdio.h"
#include <boost/numeric/odeint.hpp>
#include "cochlea.hpp"

using namespace std;
using namespace boost::numeric::odeint;

extern "C" void run(floating *X_t, floating* tt, floating* X_0, floating* inputs, floating* coefficients, floating* parameters, floating* base_parameters, int* dimensions, floating* solver_options ) 
{

    Cochlea_t C;

    C.pa = parameters;
    C.co = coefficients;
    C.in = inputs;

    C.n_t = dimensions[0]; 
    C.n_vars = dimensions[1];
    C.n_channels = dimensions[2];
    C.n_inputs = dimensions[3];
    C.n_parameters = dimensions[4];
    C.n_coefficients = dimensions[5];
    int fs = dimensions[6];
    int dec = dimensions[7];

    C.alpha = base_parameters[0];
    C.beta = base_parameters[1];
    C.mef = base_parameters[2];
    C.fluid = base_parameters[3];
    
    // cout << "C.alpha:" << C.alpha << "\t";
    // cout << "C.beta:" << C.beta << "\t";
    // cout << "C.mef:" << C.mef << "\t";
    // cout << "C.n_t:" << C.n_t << "\t";
    // cout << "C.n_vars:" << C.n_vars << "\t";
    // cout << "C.n_channels:" << C.n_channels << "\t";
    // cout << "C.n_inputs:" << C.alpha << "\t";
    // cout << "C.n_parameters:" << C.n_parameters << "\t";
    // cout << "fs:" << fs << "\t";
    // cout << "dec:" << dec << "\n";

    floating dt = 1.0/fs;  
    floating tmax = (C.n_t - 1)*dt;

    C.dt = dt;
    C.setup(); 
    
    floating_vector X;

    X.resize(C.n_vars*C.n_channels,0);

    for(int i = 0;i<C.n_vars*C.n_channels;i++)
    {
        X[i] = X_0[i];
    }

    long int solver = (long int)solver_options[0];
    floating abs_tol = solver_options[1];
    floating rel_tol = solver_options[2];   

    // cout << "solver:" << solver << "\t";
    // cout << "abs_tol:" << abs_tol<< "\t";
    // cout << "rel_tol:" << rel_tol << "\n";

    //Runge Kutta constant dt 
    if(solver==0)
    {
        Observer_t obs(X_t,tt,C.n_vars*C.n_channels,dec);

        runge_kutta4< floating_vector > stepper;
        integrate_const( stepper , C , X , 0.0, tmax , dt ,obs );
    }
    //Runge Kutta Dopri dense ouput
    if(solver==1)
    {
        Observer_t obs(X_t,tt,C.n_vars*C.n_channels);

        size_t steps = integrate_const( make_dense_output< runge_kutta_dopri5< floating_vector > >( abs_tol, rel_tol ),
                        C , X , 0.0 , tmax , dt , obs );

        cout << "Number of steps: " << steps << endl;
    }
    //Runge Kutta Cash Karp54 dense ouput
    if(solver==2)
    {
        Observer_t obs(X_t,tt,C.n_vars*C.n_channels);
    
        size_t steps = integrate_const( make_controlled< runge_kutta_cash_karp54< floating_vector >  >( abs_tol , rel_tol) , 
                        C , X , 0.0 , tmax , dt, obs );

        cout << "Number of steps: " << steps << endl;
    }
    
}

