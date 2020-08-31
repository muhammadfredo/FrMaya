'''
## SCRIPT HEADER ##

Created By   : Muhammad Fredo Syahrul Alam
Email        : muhammadfredo@gmail.com
Start Date   : 1 Okt 2017
Purpose      : 

'''
# TODO: multiply, cross, dot product, rmultipy, normalize

import math, numbers

class Vector(object):
    '''
    Vector class
    '''
    
    # def __init__(self, VectorList = [ 0, 0, 0 ]):
    def __init__(self, VectorList = []):
        '''
        Vector class
        
        :param VectorList: List of 3 numbers, [ x, y, z ]
        '''

        if len(VectorList) == 3:
            self.__values__ = VectorList
        elif len(VectorList) == 0:
            self.__values__ = [0,0,0]
        else:
            raise ValueError('Input should be 3 index list of numbers')
    
    # private properties
    __values__ = [ 0, 0, 0 ]
    
    def __add__(self, Vec):
        '''
        Add operator for Vector
        
        self.__add__(Vec) <==> self + Vec
        
        :param Vec: Vector object added to
        '''
        
        # addition by another vector
        if isinstance( Vec, Vector ):
            x = self.x() + Vec.x()
            y = self.y() + Vec.y()
            z = self.z() + Vec.z()
            
            # return new vector
            return Vector( [ x, y, z ] )
        else:
            raise ValueError('Vector can only be add by another Vector object')

    def __copy__(self):
        '''
        Copy this object

        :return: New vector object with same value as this object
        '''

        return Vector( self.__values__ )

    def __div__(self, Val):
        '''
        Divide operator for Vector
        
        self.__div__(Val) <==> self / Val
        
        :param Val: Vector object, or number divided to
        '''
        
        # divided by another vector
        if isinstance( Val, Vector ):
            x = self.x() / Val.x()
            y = self.y() / Val.y()
            z = self.z() / Val.z()
        # divided by scalar value
        elif isinstance( Val, numbers.Number ):
            x = self.x() / Val
            y = self.y() / Val
            z = self.z() / Val
            
        else:
            raise ValueError('Vector can only be divided by Vector object or instance of number')
        
        # return new vector
        return Vector( [ x, y, z ] )

    def __eq__(self, Vec):
        '''
        Equal comparison operator for Vector
        
        self.__eq__(Vec) <==> self == Vec
        
        :param Vec: Vector object equal compared to
        '''
        
        # equal compare to another vector
        if isinstance( Vec, Vector ):
            for i, o in enumerate(Vec):
                if not self.__values__[i] == o:
                    return False
            return True
        else:
            raise ValueError('Vector can only be compared to Vector object')
    
    def __ge__(self, Vec):
        '''
        Greater than or equal operator for Vector
        
        self.__ge__(Vec) <==> self >= Vec
        
        :param Vec: Vector object Greater than or equal to
        '''
        
        # greater than equal to another vector
        if isinstance( Vec, Vector ):
            for i, o in enumerate(Vec):
                if not self.__values__[i] >= o:
                    return False
            return True
        else:
            raise ValueError('Vector can only be compared to Vector object')
    
    def __getitem__(self, index):
        '''
        Get Vector value from given index
        
        x.__getitem__(y) <==> x[y]
        
        :param index: Number
        '''
        
        if isinstance( index, numbers.Number ):
            return self.__values__[index]
        else:
            raise ValueError('Index should be number')
    
    def __gt__(self, Vec):
        '''
        Greater than operator for Vector
        
        self.__gt__(Vec) <==> self > Vec
        
        :param Vec: Vector object Greater than to
        '''
        
        # greater than equal to another vector
        if isinstance( Vec, Vector ):
            for i, o in enumerate(Vec):
                if not self.__values__[i] > o:
                    return False
            return True
        else:
            raise ValueError('Vector can only be compared to Vector object')
    
    def __le__(self, Vec):
        '''
        Less than or equal operator for Vector
        
        self.__le__(Vec) <==> self <= Vec
        
        :param Vec: Vector object Less than or equal to
        '''
        
        # less than equal to another vector
        if isinstance( Vec, Vector ):
            for i, o in enumerate(Vec):
                if not self.__values__[i] <= o:
                    return False
            return True
        else:
            raise ValueError('Vector can only be compared to Vector object')
    
    def __len__(self):
        '''
        Length of Vector as list
        '''
        
        return len(self.__values__)
    
    def __lt__(self, Vec):
        '''
        Less than operator for Vector

        self.__lt__(Vec) <==> self < Vec

        :param Vec: Vector object Less than to
        '''

        # less than to another vector
        if isinstance(Vec, Vector):
            for i, o in enumerate(Vec):
                if not self.__values__[i] < o:
                    return False
            return True
        else:
            raise ValueError('Vector can only be compared to Vector object')
    
    def __mul__(self, Val):
        '''
        Multiply operator for Vector
        
        self.__mul__(Val) <==> self * Val
        
        :param Val: Vector object or Number multiplied to
        '''

        # multiply by another vector
        if isinstance( Val, Vector ):
            x = self.x() * Val.x()
            y = self.y() * Val.y()
            z = self.z() * Val.z()
        # multiply by scalar value
        elif isinstance( Val, numbers.Number ):
            x = self.x() * Val
            y = self.y() * Val
            z = self.z() * Val
        else:
            raise ValueError('Vector can only be multiply by Vector object or instance of number')

        # return new vector
        return Vector( [ x, y, z ] )
    
    def __ne__(self, Vec):
        '''
        Negative equal comparison operator for Vector

        self.__ne__(Vec) <==> self != Vec

        :param Vec: Vector object negative equal compared to
        '''

        # negative equal comparison
        return not self.__eq__( Vec )
    
    def __neg__(self):
        '''
        Returns a new vector containing the negative version of this vector

        self.__neg__() <==> -self
        '''

        # return new vector
        return Vector( [ -self.x(), -self.y(), -self.z() ] )
    
    def __radd__(self, Vec):
        '''
        Right add operator for Vector

        self.__radd__(Vec) <==> Vec + self

        :param Vec: Vector object right added to
        '''

        # addition by another vector
        if isinstance( Vec, Vector ):
            x, y, z = self.__add__( Vec ).asList()

            # return new vector
            return Vector( [ x, y, z ] )
        else:
            raise ValueError( 'Vector can only be right add by another Vector object' )
    
    def __rdiv__(self, Val):
        '''
        Right divide operator for Vector

        self.__rdiv__(Val) <==> Val / self

        :param Vec: Vector object, or number right divided to
        '''

        # divided by another vector
        if isinstance( Val, Vector ):
            x = Val.x() / self.x()
            y = Val.y() / self.y()
            z = Val.z() / self.z()

        # divided by scalar value
        elif isinstance( Val, numbers.Number ):
            x = Val / self.x()
            y = Val / self.y()
            z = Val / self.z()

        else:
            raise ValueError( 'Vector can only be right divided by Vector object or instance of number' )

        # return new vector
        return Vector( [ x, y, z ] )

    def __repr__(self):
        '''
        Retrun string of Vector object which can be eval with python

        self.__repr__() <==> repr(self)
        '''

        x = self.x(); y = self.y(); z = self.z()

        return 'Vector( [ {0}, {1}, {2} ] )'.format( x, y, z )
    
    def __rmul__(self, Val):
        '''
        Right multiplication operator for Vector
        
        self.__rmul__(Val) <==> Val * self
        
        :param Val: Vector object, or number right multiplied to
        '''

        # multiply by another vector
        if isinstance( Val, Vector ):
            x = Val.x() * self.x()
            y = Val.y() * self.y()
            z = Val.z() * self.z()
        # multiply by scalar value
        elif isinstance( Val, numbers.Number ):
            x = Val * self.x()
            y = Val * self.y()
            z = Val * self.z()
        else:
            raise ValueError( 'Vector can only be right multiply by Vector object or instance of number' )

        # return new vector
        return Vector( [ x, y, z ] )
    
    def __rsub__(self, Vec):
        '''
        Substract operator for Vector

        self.__rsub__(Vec) <==> Vec - self

        :param Vec: Vector object subed to
        '''

        # addition by another vector
        if isinstance( Vec, Vector ):
            x = Vec.x() - self.x()
            y = Vec.y() - self.y()
            z = Vec.z() - self.z()

            # return new vector
            return Vector( [ x, y, z ] )
        else:
            raise ValueError( 'Vector can only be right sub by another Vector object' )
    
    def __setitem__(self, index, value):
        '''
        Set Vector index from given value
        
        self.__setitem__( index, value ) <==> self[ index ] = value
        
        :param index: Index of Vector, 0-2 int, [ x, y, z ]
        :param value: Value which will change on Vector index
        '''
        
        self.__values__[index] = value
    
    # def __str__(self):
    #     '''
    #     Retrun pretty print of Vector object
    #     '''
    #
    #     x = self.x(); y = self.y(); z = self.z()
    #
    #     return 'Vector ( {0} {1} {2} )'.format( x, y, z )
    
    def __sub__(self, Vec):
        '''
        Substract operator for Vector
        
        self.__sub__( Vec ) <==> self - Vec
        
        :param Vec: Vector object substracted to
        '''
        
        if isinstance( Vec, Vector):
            x = self.x() - Vec.x()
            y = self.y() - Vec.y()
            z = self.z() - Vec.z()
            
            return Vector( [ x, y, z ] )
        else:
            raise ValueError('Vector can only be substract by Vector object')

    def dot(self, Vec):
        '''
        Dot product of vector

        :param Vec: Vector object which will be calculated
        :return: A float number, result of dot product of the 2 vectors
        '''

        if isinstance( Vec, Vector ):
            x = self.x() * Vec.x()
            y = self.y() * Vec.y()
            z = self.z() * Vec.z()

            return x + y + z
        else:
            raise ValueError( 'Dot product need Vector object to operate' )

    def cross(self, Vec):
        '''
        Cross product of vector

        :param Vec: Vector object crossed to
        :return: New vector perpendicular to this vector and the input vector
        '''

        ax = self.x(); ay = self.y(); az = self.z()
        bx = Vec.x(); by = Vec.y(); bz = Vec.z()

        x = ay * bz - az * by
        y = az * bx - ax * bz
        z = ax * by - ay * bx

        return Vector( [ x, y, z ] )

    def angle(self, Vec):
        '''
        Calculate angle in degrees between this vector and other

        :param Vec: Vector object
        :return: A float number in degrees
        '''

        return math.acos( self.dot(Vec) ) / ( self.length() * Vec.length() )
    
    def length(self):
        '''
        Calculate magnitude / length of this vector
        '''
        
        x = self.x() ** 2
        y = self.y() ** 2
        z = self.z() ** 2
        
        return math.sqrt( x + y + z )

    magnitude = length
    
    def normal(self):
        '''
        Get a new vector containing the normalized version of this vector
        '''

        vlength = self.length()

        x = self.x() / vlength
        y = self.y() / vlength
        z = self.z() / vlength

        return Vector( [ x, y, z ] )

    def normalize(self):
        '''
        Normalizes this vector in-place and returns a new reference to it
        '''

        vlength = self.length()

        x = self.x() / vlength
        y = self.y() / vlength
        z = self.z() / vlength

        self.__values__ = [ x, y, z ]

        return self

    def asList(self):
        '''
        Get Vector as list, [ x, y, z ]
        '''

        return self.__values__

    def setValue(self, value):
        '''
        Set all x, y, z value of this Vector

        self.setValue( [x, y, ,z] ) <==> self - Vec

        :param value: list of 3 number
        '''

        if len(value) == 3:
            self.__values__ = value

            return self
        else:
            raise ValueError( 'Value should be list of 3 number' )
    
    def x(self):
        '''
        Get vector x part
        '''
        
        return self.__values__[0]
    
    def y(self):
        '''
        Get vector y part
        '''
        
        return self.__values__[1]
    
    def z(self):
        '''
        Get vector z part
        '''
        
        return self.__values__[2]
