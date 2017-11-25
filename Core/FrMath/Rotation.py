'''
## SCRIPT HEADER ##

Created By   : Muhammad Fredo Syahrul Alam
Email        : muhammadfredo@gmail.com
Start Date   : 27 Aug 2017
Purpose      : 

'''

import math, numbers

class Quaternion(object):
    '''
    Quaternion class
    '''
    
    def __init__(self, QuaternionList):
        '''
        Quaternion class
        
        :param QuaternionList: List of 4 numbers, [ x, y, z, w ]
        '''
        
        if len(QuaternionList) == 4:
            self.__values__ = QuaternionList
        else:
            raise ValueError('Input should be 4 index list of numbers')

    def x(self):
        '''
        Get quaternion x part
        '''
        
        return self.__values__[0]
    
    def y(self):
        '''
        Get quaternion y part
        '''
        
        return self.__values__[1]
    
    def z(self):
        '''
        Get quaternion z part
        '''
        
        return self.__values__[2]
    
    def w(self):
        '''
        Get quaternion w part
        '''
        
        return self.__values__[3]
    
    def asList(self):
        '''
        Return Quaternion as list, [ x, y, z, w ]
        '''
        
        return self.__values__
    
    def toEulerian(self):
        '''
        Return Quaternion as Eulerian class
        '''
        
        x = self.x(); y = self.y(); z = self.z(); w = self.w()
        
        sqrt = y * y
        
        # X
        t0 = +2.0 * ( w * x + y * z )
        t1 = +1.0 - 2.0 * ( x * x + sqrt )
        eulerX = math.degrees( math.atan2( t0, t1) )
        
        # Y
        t2 = +2.0 * ( w * y - z * x )
        t2 =  1 if t2 > 1 else t2
        t2 = -1 if t2 < -1 else t2
        eulerY = math.degrees( math.asin( t2 ) )
        
        # Z
        t3 = +2.0 * ( w * z + x * y )
        t4 = +1.0 - 2.0 * ( sqrt + z * z )
        eulerZ = math.degrees( math.atan2( t3, t4 ) )
        
        return Eulerian( [ eulerX, eulerY, eulerZ ] )
    
    def normalized(self):
        '''
        Return normalized Quaternion
        '''
        
        x = self.x(); y = self.y(); z = self.z(); w = self.w()
        n = math.sqrt( x*x + y*y + z*z + w*w )
        
        return Quaternion( [ x / n, y / n, z / n, w / n ] )
    
    def conjugated(self):
        '''
        Return conjugated Quaternion class
        '''
        
        x = self.x(); y = self.y(); z = self.z(); w = self.w()
        
        return Quaternion( [ -x, -y, -z, w ] )
    
    def __getitem__(self, index):
        '''
        Get Quaternion from given index
        
        :param index: Index of Quaternion, 0-3 int, [ x, y, z, w ]
        '''
        
        return self.__values__[index]
    
    def __setitem__(self, index, value):
        '''
        Set Quaternion index from given value
        
        :param index: Index of Quaternion, 0-3 int, [ x, y, z, w ]
        :param value: Value which will change on Quaternion index
        '''
        
        self.__values__[index] = value
    
    def __len__(self):
        '''
        Length of Quaternion as list
        '''
        
        return len(self.__values__)

    def __eq__(self, Quat):
        '''
        Comparison operator for Quaternion
        
        :param Quat: Quaternion class compared to
        '''
        
        if isinstance( Quat, Quaternion ):
            for i, x in enumerate(Quat):
                if self.__values__[i] != x:
                    return False
            return True
        else:
            raise ValueError('Quaternion can only be compared to Quaternion class')
    
    def __add__(self, Quat):
        '''
        Add operator for Quaternion
        
        :param Quat: Quaternion class added to
        '''
        
        if isinstance( Quat, Quaternion ):
            x = self.x() + Quat.x()
            y = self.y() + Quat.y()
            z = self.z() + Quat.z()
            w = self.w() + Quat.w()
            
            return Quaternion( [ x, y, z, w ] )
        else:
            raise ValueError('Quaternion can only be add by Quaternion class')
    
    def __sub__(self, Quat):
        '''
        Substract operator for Quaternion
        
        :param Quat: Quaternion class substracted to
        '''
        
        if isinstance( Quat, Quaternion):
            x = self.x() - Quat.x()
            y = self.y() - Quat.y()
            z = self.z() - Quat.z()
            w = self.w() - Quat.w()
            
            return Quaternion( [ x, y, z, w ] )
        else:
            raise ValueError('Quaternion can only be substract by Quaternion class')
    
    def __mul__(self, Quat):
        '''
        Multiply operator for Quaternion
        
        :param Quat: MQuarternion class multiplied to
        '''
        
        if isinstance( Quat, Quaternion ):
            Ax = self.x(); Ay = self.y(); Az = self.z(); Aw = self.w()
            Bx = Quat.x(); By = Quat.y(); Bz = Quat.z(); Bw = Quat.w()
            
            x =  Ax * Bw + Ay * Bz - Az * By + Aw * Bx
            y = -Ax * Bz + Ay * Bw + Az * Bx + Aw * By
            z =  Ax * By - Ay * Bx + Az * Bw + Aw * Bz
            w = -Ax * Bx - Ay * By - Az * Bz + Aw * Bw
            
            return Quaternion( [ x, y, z, w ] )
        else:
            raise ValueError('Quaternion can only be multiply by Quaternion class')
    
    def __rmul__(self, scalar):
        '''
        Right multiplication operator for Quaternion
        
        :param scalar: int/float scalar value multiplied to
        '''
        
        if isinstance( scalar, numbers.Number ):
            x = self.x() * scalar
            y = self.y() * scalar
            z = self.z() * scalar
            w = self.w() * scalar
            
            return Quaternion( [ x, y, z, w ] )
        else:
            raise ValueError('Scalar value must be numbers')
    
    def __str__(self):
        '''
        Retrun pretty print of Quaternion class
        '''
        
        x = self.x(); y = self.y(); z = self.z(); w = self.w()

        return 'Quaternion ( {0} {1} {2} {3} )'.format( x, y, z, w )

class Eulerian(object):
    '''
    Maya Eulerian class
    '''
    
    def __init__(self, EulerianList):
        '''
        Maya Eulerian class
        
        :param EulerianList: List of 3 numbers
        '''

        if len(EulerianList) == 3:
            self.__values__ = EulerianList
        else:
            raise ValueError('Input should be 3 index list of numbers')
    
    def x(self):
        '''
        Get eulerian x part
        '''

        return self.__values__[0]
    
    def y(self):
        '''
        Get eulerian y part
        '''

        return self.__values__[1]
    
    def z(self):
        '''
        Get eulerian z part
        '''

        return self.__values__[2]
    
    def asList(self):
        '''
        Return Eulerian as list, [ x, y, z ]
        '''

        return self.__values__
    
    def toQuaternion(self):
        '''
        Return Eulerian as Quaternion class
        '''

        # Never forget to convert to radians before convert to Quaternion
        x = math.radians( self.x() )
        y = math.radians( self.y() )
        z = math.radians( self.z() )
        
        cz = math.cos( z * 0.5 )
        sz = math.sin( z * 0.5 )
        cx = math.cos( x * 0.5 )
        sx = math.sin( x * 0.5 )
        cy = math.cos( y * 0.5 )
        sy = math.sin( y * 0.5 )

        # Got this equation from wikipedia
        quatW = cz * cx * cy + sz * sx * sy
        quatX = cz * sx * cy - sz * cx * sy
        quatY = cz * cx * sy + sz * sx * cy
        quatZ = sz * cx * cy - cz * sx * sy
        # xyz
#         quatW = -sx * sy * sz + cx * cy * cz
#         quatX = sx * cy * cz + sy * sz * cx
#         quatY = -sx * sz * cy + sy * cx * cz
#         quatZ = sx * sy * cz + sz * cx * cy
        # zyx
#         quatW = sz * sy * sx + cz * cy * cx
#         quatX = -sz * sy * cx + sx * cz * cy
#         quatY = sz * sx * cy + sy * cz * cx
#         quatZ = sz * cy * cx - sy * sx * cz
        
        return Quaternion( [ quatX, quatY, quatZ, quatW ] )
    
    def __str__(self):
        '''
        Retrun pretty print of Eulerian class
        '''

        x = self.x(); y = self.y(); z = self.z()

        return 'Eulerian ( {0} {1} {2} )'.format( x, y, z )
