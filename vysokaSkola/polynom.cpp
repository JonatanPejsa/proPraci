#ifndef __PROGTEST__
#include <cstring>
#include <cstdlib>
#include <cstdio>
#include <cctype>
#include <climits>
#include <cmath>
#include <cfloat>
#include <cassert>
#include <unistd.h>
#include <iostream>
#include <iomanip>
#include <sstream>
#include <string>
#include <vector>
#include <span>
#include <algorithm>
#include <memory>
#include <compare>
#include <complex>
#endif /* __PROGTEST__ */

// keep this dummy version if you do not implement a real manipulator
std::ios_base & ( * poly_var ( const std::string & name ) ) ( std::ios_base & x )
{
    return [] ( std::ios_base & ios ) -> std::ios_base & { return ios; };
}

// Class represents a polynomial with real coefficients
class CPolynomial {
public:
    /** Default constructor */
    CPolynomial() = default;

    /**
     * Multiplication of two polynomials.
     * @param[in] other Polynomial to multiply by.
     * @return polynomial *this multiplied by other.
     */
    CPolynomial operator*(const CPolynomial & other) const {
        size_t degT = degree();
        size_t degO = other.degree();
        CPolynomial result;
        result.coeffs.resize(degT + degO +1);
        for(size_t i = 0; i <= degT; i++) {
            if((*this)[i]==0)
                continue;
            for(size_t j = 0; j <= degO; j++)
                result[i + j] += (*this)[i]* other[j];
        }
        return result;
    }

    /** polynomial multiplication.
     * @param[in] other Polynomial to multiply by.
     */
    void operator*=(const CPolynomial & other) {
        (*this) = (*this * other); 
    }

    /**
     * Scalar multiplication, multiply polinomial by scalar.
     * @param[in] scalar
     * @returns polynomial *this multiplied by scalar.
     */
    CPolynomial operator*(double scalar) const {
        size_t deg = this->degree();
        CPolynomial result;
        result.coeffs.resize(deg+1);
        for(size_t x=0; x<=deg;x++)
            result[x]= (*this)[x]*scalar;
        return result;
    }

    /** 
     * Scalar multiplication, multiply polinomial by scalar.
     * @param[in] scalar 
     */
    void operator*=(double scalar) {
        size_t deg = this->degree();
        for(size_t x=0; x<=deg;x++) 
            (*this)[x]*=scalar;
    }

    /** Equality comparison of polinomials (*this to other)
     * @param[in] other Polynomial to which it compares
     * @returns true if the polynomials are equal, false otherwise
     */
    bool operator==(const CPolynomial& other) const {
        size_t degO = other.degree();
        size_t degT = this->degree();
        if (degO<degT) {
            // checking if polinomials have the same lenght(degree)
            for(size_t x = degT; x > degO; x--) {
                if (this->coeffs[x]!=0)
                    return false;
            }
            // coeff to coeff co comparison
            for (int x = static_cast<int>(degO); x >= 0; x--) {
                if(other.coeffs[x] != this->coeffs[x])
                    return false;
            }
        }
        else {
            // checking if polinomials have the same lenght(degree)
            for(size_t x = degO; x > degT; x--) {
                if (other.coeffs[x]!=0)
                    return false;
            }
            // coeff to coeff co comparison
            for (int x = static_cast<int>(degT); x >= 0;x--) {
                if(other.coeffs[x] != this->coeffs[x])
                    return false;
            }
        }
        return true;
    }
    /** Inequality comparison. 
     * @param[in] other Polynomial to which it compares
     * @returns true if the polynomials are not equal, false otherwise
     */
    bool operator!=(const CPolynomial& other) const {
        return !(*this == other); 
    }

    /** Write coefficient access 
     * @param[in] index Index of the coefficient in coeffs
     * @returns reference to element from coeffs
     */
    double& operator[](size_t index) {
        if(coeffs.size() <= index)
            coeffs.resize(index + 1);
        return coeffs[index];
    }
    /** Read coefficient access
     * @param[in] index Index of the coefficient in coeffs
     * @returns element from coeffs
     */
    double operator[](size_t index) const {
        if (index >coeffs.size())
            return 0.0;
            
        return coeffs[index];
    }

    /** Evaluate polynomial with x 
     * @param[in] x 
     * @returns result of the evaluation
     */
    double operator()(double x) const {
        double sum = 0;
        for(size_t i = 0; i <= degree(); i++)
            sum += (*this)[i] * std::pow(x, i);
        return sum;
    }

    /** Returns true if it is a zero polynomial */
    bool operator!() const { 
        if (this->degree()==0) {
            if ((*this).coeffs[0]==0.0)
                return true;
        }
        return false;
    }

    /** Cast to bool (true if polynomial is non‑zero) */
    explicit operator bool() const { 
        if (!(*this)) 
            return false;
        return true;
    }

    /** Highest non‑zero element of coeffs (highest power,degree) */
    size_t degree() const {
        for(size_t x = coeffs.size(); x > 0; x--)
            if(coeffs[x - 1] != 0.0) 
                return x - 1;
        return 0;
    }

    /** Output operator, prints polynomial 
     * @param[out] os Output stream receiving the formatted polynomial
     * @param[in] poly Polynomial to be written
     * @returns reference to the os
     */
    friend std::ostream& operator<<(std::ostream& os, const CPolynomial& poly) {
        bool firstTime=true;
        if (poly.degree()==0) {
            os<<"0";
            return os;
        }
        for (int i = poly.degree(); i >= 0;i--) {
            if (i == 0) {
                if (poly.coeffs[i]<0) 
                    os<<" - "<<-1*poly.coeffs[i];
                else if (poly.coeffs[i]>0) {
                    if (firstTime) {
                        os<<" "<<poly.coeffs[i];
                        firstTime=false;
                    }
                    else 
                        os<<" + "<<poly.coeffs[i];
                }
                continue;
            }
            if (poly.coeffs[i]<0) {
                if (poly.coeffs[i]==-1) {
                    if (firstTime)
                        os<<"- "<<"x^"<<i;
                    else 
                        os<<" - "<<"*x^"<<i;
                }
                else {
                    if (firstTime) 
                        os<<"- "<<-1*poly.coeffs[i]<<"*x^"<<i;
                    else 
                        os<<" - "<<-1*poly.coeffs[i]<<"*x^"<<i;
                }
                firstTime = false;
            }
            else if (poly.coeffs[i]==1) {
                if (firstTime) {
                    os<<"x^"<<i;
                    firstTime=false;
                }
                else
                    os<<" + "<<"x^"<<i;
            }
            else if (poly.coeffs[i]>0) {
                if (firstTime) {
                    os<<" "<<poly.coeffs[i]<<"*x^"<<i;
                    firstTime=false;
                }
                else
                    os<<" + "<<poly.coeffs[i]<<"*x^"<<i;
            }
        }
        return os;
    }

private:
    /** @var Vector of coefficients (coeffs[p] -> x^p) */
    std::vector<double> coeffs; 
};

#ifndef __PROGTEST__
/** Compares two float numbers
 * @param[in] a First number to compare
 * @param[in] b Second number to compare
 * @return true If the numbers are exactly equal, false otherwise
 */
bool smallDiff(double a, double b) { 
    return a == b; 
}

/** Polynomial coeffs match a reference vector
 * @param[in] poly Polynomial where coefficients are tested
 * @param[in] ref  Vector containing the reference coefficients
 * @return true If every coefficient is equal, false otherwise
  */
bool dumpMatch(const CPolynomial& poly, const std::vector<double>& ref) {
    for(size_t i = 0; i <= poly.degree();i++)
        if(poly[i] != ref[i]) 
            return false;
    return true;
}


int main ()
{
  CPolynomial a, b, c;
  std::ostringstream out, tmp;

  a[0] = -10;
  a[1] = 3.5;
  a[3] = 1;
  //assert ( smallDiff ( a ( 2 ), 5 ) );
  out . str ("");
  out << a;

  assert ( out . str () == "x^3 + 3.5*x^1 - 10" );

  c = a * -2;

  std::cout<<a<<"\n";
  std::cout<<c<<"\n";
  assert ( c . degree () == 3
           && dumpMatch ( c, std::vector<double>{ 20.0, -7.0, -0.0, -2.0 } ) );
  std::cout<<"ahoj\n";
  out . str ("");
  out << c;

  assert ( out . str () == "- 2*x^3 - 7*x^1 + 20" );
  out . str ("");
  std::cout<<"ahoj\n";
  out << b;
  std::cout<<"ahoj\n";
  assert ( out . str () == "0" );
  b[5] = -1;
  b[2] = 3;
  out . str ("");
  out << b;
  std::cout<<b<<"\n";
  assert ( out . str () == "- x^5 + 3*x^2" );

  c = a * b;
  std::cout<<c.degree()<<"\n";
  std::cout<<c<<"\n";
  assert ( c . degree () == 8
           && dumpMatch ( c, std::vector<double>{ -0.0, -0.0, -30.0, 10.5, -0.0, 13.0, -3.5, 0.0, -1.0 } ) );

  out . str ("");
  out << c;
  assert ( out . str () == "- x^8 - 3.5*x^6 + 13*x^5 + 10.5*x^3 - 30*x^2" );
  a *= 5;
  assert ( a . degree () == 3
           && dumpMatch ( a, std::vector<double>{ -50.0, 17.5, 0.0, 5.0 } ) );

  a *= b;
  assert ( a . degree () == 8
           && dumpMatch ( a, std::vector<double>{ 0.0, 0.0, -150.0, 52.5, -0.0, 65.0, -17.5, -0.0, -5.0 } ) );

  assert ( a != b );
  b[5] = 0;
  assert ( static_cast<bool> ( b ) );
  assert ( ! ! b );
  b[2] = 0;
  assert ( !(a == b) );
  a *= 0;
  assert ( a . degree () == 0
           && dumpMatch ( a, std::vector<double>{ 0.0 } ) );

  assert ( a == b );
  assert ( ! static_cast<bool> ( b ) );
  assert ( ! b );

  // bonus - manipulators
/*
  out . str ("");
  out << poly_var ( "y" ) << c;
  assert ( out . str () == "- y^8 - 3.5*y^6 + 13*y^5 + 10.5*y^3 - 30*y^2" );
  out . str ("");
  tmp << poly_var ( "abc" );
  out . copyfmt ( tmp );
  out << c;
  assert ( out . str () == "- abc^8 - 3.5*abc^6 + 13*abc^5 + 10.5*abc^3 - 30*abc^2" );
  */
  return EXIT_SUCCESS;
}
#endif /* __PROGTEST__ */
