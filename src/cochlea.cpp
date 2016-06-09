#include "cochlea.hpp"


$extra_functions


void Cochlea_t::setup()
{
    N = n_channels;
    set_arrays();
    gaussian_elimination_init();
}

void Cochlea_t::gaussian_elimination_init()
{
    b[0] = -alpha-1;
    c[0] = alpha;


    //alpha = mass/2/dx/density*mass_effective
    //beta = dx / height*mass_effective

    //asb = mass height
    //      -----------
    //      2 dx**2 density

    asb =  alpha/beta;

    for (int i = 1; i < N; i++)
    {
        a[i] = asb;
        b[i] = -2*asb-1;
        c[i] = asb;
    }
    
    b[N-1] = 1.0;
    a[N-1] = 0.0;


    c[0] = c[0] / b[0];
 
    /* loop from 1 to N - 1 inclusive */
    for (int i = 1; i < N; i++){
        k[i] = 1.0f / (b[i] - a[i] * c[i - 1]);
        c[i] = c[i] * k[i];
    }
 
}

void Cochlea_t::operator() (  floating_vector &X , floating_vector &dXdt , floating t )
{
    /*
     * X  = vector with current state for in out
     * Variable j channel i 
     * X[i*n_vars + j]

     * dX/dT = derivative vector
     * t    = time
     */

    int i = n_vars; // range(n_vars, N*n_vars, n_vars)
    int j = 1; // range(1, N)
    
    for(; i < N*n_vars; i+=n_vars, j++)
    {
   
        //Assign g[i]
        $g_assignation
        $debug0 cout << "(i:"<< i <<"," << "g[i]:" << g[i] <<")"; 
    }
    
    $debug0 cout << endl;

    floating input_0 = $input_0;

    $debug0 cout << "t:"<< t <<"," << "input_0:" << input_0 <<endl;; 
    
    if(fluid)
    {
        //COPMUTE p solving Ap = (q-g);
        p[0] = (-input_0 + g[0]) / b[0];
    
        for (int i = 1; i < N; i++)
        {
            floating input_i = $input_i;
            p[i] = (-input_i + g[i] - a[i] * p[i - 1]) * k[i];
        }
      
        ///* loop from N - 2 to 0 inclusive */
        for (int i = N - 2; i >=0; i--)
            p[i] = p[i] - c[i] * p[i + 1];
    }
    
    
    //boundary conditions
    $system_equation_0

    i = n_vars; // range(n_vars, N*n_vars, n_vars)
    j = 1; // range(1, N)
    
    for(; i < N*n_vars; i+=n_vars, j++)
    {
        //equations example
        // dXdt[i+0] = X[i+1];
        // dXdt[i+1] =  -p[i] - g[i];
        // dXdt[i+2] = X[i+3];
        // dXdt[i+3] = -X[i+2];

        $system_equation_i

        $debug0 cout << "(i:"<< i <<"," << "dXdt["<<i<<"+0]:" << dXdt[i+0]; 
        $debug0 cout << "," << "dXdt["<<i<<"+1]:" << dXdt[i+1] <<")"; 
    }
    $debug0 cout << endl;

}

void Cochlea_t::set_arrays()
{
    g.resize(N,0);
    a.resize(N,0);
    b.resize(N,0);
    c.resize(N,0);
    p.resize(N,0);
    k.resize(N,0);
    X.resize(N*n_vars,0);
}
