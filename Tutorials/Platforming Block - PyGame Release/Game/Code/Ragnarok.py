##    Ragnarok Engine copyright 2010 Clinton Myers
##    This library is free software: you can redistribute it and/or modify
##    it under the terms of the GNU Lesser General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    This program is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU Lesser General Public License for more details.
##
##    You should have received a copy of the GNU Lesser General Public License
##    along with this program.  If not, see <http://www.gnu.org/licenses/lgpl.html>.
##    Ragnarok Version 1.0
##
##
##    Developer Note: This is a very early version of a work in progress. Several of the classes
##      have many segments commented out and may not function properly. If you have any questions, contact
##      me at lotusxp@live.com


import pygame, math, numbers, operator, random, StateTypes, os
os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'

class Vector2(object):
    def __init__(self, X = 0.0, Y = 0.0):
        self.X = X
        self.Y = Y

    def __add__(self, other):
        if isinstance(other, Vector2):
            new_vec = Vector2()
            new_vec.X = self.X + other.X
            new_vec.Y = self.Y + other.Y
            return new_vec
        else:
            raise TypeError("other must be of type Vector2")

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, Vector2):
            new_vec = Vector2()
            new_vec.X = self.X - other.X
            new_vec.Y = self.Y - other.Y
            return new_vec
        else:
            raise TypeError("other must be of type Vector2")

    def __rsub__(self, other):
        return self.__sub__(other)

    def __mul__(self, value):
        if isinstance(value, numbers.Number):
            new_vec = self.copy()
            new_vec.X = new_vec.X * value
            new_vec.Y = new_vec.Y * value
            return new_vec
        else:
            raise TypeError("value must be a number.")

    def __rmul__(self, value):
        return self.__mul__(value)

    def __div__(self, value):
        if isinstance(value, numbers.Number):
            if not(value == 0):
                new_vec = self.copy()
                new_vec.X /= value
                new_vec.Y /= value
                return new_vec
            else:
                raise ZeroDivisionError("Cannot divide by zero.")
        else:
            raise TypeError("value must be a number.")

    def __rdiv__(self, value):
        return self.__div__(value)

    def __eq__(self, other):
        """Check to see if two Vector2 objects are equal"""
        if isinstance(other, Vector2):
            if self.X == other.X    \
           and self.Y == other.Y:
                return True
        else:
            raise TypeError("other must be of type Vector2")

        return False

    def __neg__(self):
        return Vector2(-self.X, -self.Y)

    def __getitem__(self, index):
        if index > 1:
            raise IndexError("Index must be less than 2")

        if index == 0:
            return self.X
        else:
            return self.Y

    def __setitem__(self, index, value):
        if index > 1:
            raise IndexError("Index must be less than 2")

        if index == 0:
            self.X = value
        else:
            self.Y = value

    def __str__(self):
        return "<Vector2> [ " + str(self.X) + ", " + str(self.Y) + " ]"

    def __len__(self):
        return 2

    #Define our properties
    def zero():
        """Returns a Vector2 with all attributes set to 0"""
        return Vector2(0, 0)

    def one():
        """Returns a Vector2 with all attribures set to 1"""
        return Vector2(1, 1)

    def copy(self):
        """Create a copy of this Vector"""
        new_vec = Vector2()
        new_vec.X = self.X
        new_vec.Y = self.Y
        return new_vec

    def length(self):
        """Gets the length of this Vector"""
        return math.sqrt( (self.X * self.X) + (self.Y * self.Y) )

    def normalize(self):
        """Gets the normalized Vector"""
        length = self.length()
        if length > 0:
            self.X /= length
            self.Y /= length
        else:
            print "Length 0, cannot normalize."

    def normalize_copy(self):
        """Create a copy of this Vector, normalize it, and return it."""
        vec = self.copy()
        vec.normalize()
        return vec

    def distance(vec1, vec2):
        """Calculate the distance between two Vectors"""
        if isinstance(vec1, Vector2)   \
        and isinstance(vec2, Vector2):
            dist_vec = vec2 - vec1
            return dist_vec.length()
        else:
            raise TypeError("vec1 and vec2 must be Vector2's")

    def dot(vec1, vec2):
        """Calculate the dot product between two Vectors"""
        if isinstance(vec1, Vector2)   \
        and isinstance(vec2, Vector2):
            return ( (vec1.X * vec2.X) + (vec1.Y * vec2.Y) )
        else:
            raise TypeError("vec1 and vec2 must be Vector2's")

    def angle(vec1, vec2):
        """Calculate the angle between two Vector2's"""
        dotp = Vector2.dot(vec1, vec2)
        mag1 = vec1.length()
        mag2 = vec2.length()
        result = dotp / (mag1 * mag2)
        return math.acos(result)

    def lerp(vec1, vec2, time):
        """Lerp between vec1 to vec2 based on time. Time is clamped between 0 and 1."""
        if isinstance(vec1, Vector2)    \
        and isinstance(vec2, Vector2):
            #Clamp the time value into the 0-1 range.
            if time < 0:
                time = 0
            elif time > 1:
                time = 1

            x_lerp = vec1[0] + time * (vec2[0] - vec1[0])
            y_lerp = vec1[1] + time * (vec2[1] - vec1[1])
            return Vector2(x_lerp, y_lerp)
        else:
            raise TypeError("Objects must be of type Vector2")

    def from_polar(degrees, magnitude):
        """Convert polar coordinates to Carteasian Coordinates"""
        vec = Vector2()
        vec.X = math.cos(math.radians(degrees)) * magnitude

        #Negate because y in screen coordinates points down, oppisite from what is
        #expected in traditional mathematics.
        vec.Y = -math.sin(math.radians(degrees)) * magnitude
        return vec

    def component_mul(vec1, vec2):
        """Multiply the components of the vectors and return the result."""
        new_vec = Vector2()
        new_vec.X = vec1.X * vec2.X
        new_vec.Y = vec1.Y * vec2.Y
        return new_vec

    def component_div(vec1, vec2):
        """Divide the components of the vectors and return the result."""
        new_vec = Vector2()
        new_vec.X = vec1.X / vec2.X
        new_vec.Y = vec1.Y / vec2.Y
        return new_vec

    zero = staticmethod(zero)
    one = staticmethod(one)
    distance = staticmethod(distance)
    dot = staticmethod(dot)
    lerp = staticmethod(lerp)
    from_polar = staticmethod(from_polar)
    component_mul = staticmethod(component_mul)
    component_div = staticmethod(component_div)

class Vector3(object):
    """Provides basic 3D Vector operations"""

    def __init__(self, x = 0.0, y = 0.0, z = 0.0):
        """Constructs a Vector3 object with the default position of the object."""
        #Check for potential problems while converting the values.
        try:
            self.x = float(x)
            self.y = float(y)
            self.z = float(z)
        except (TypeError):
            raise TypeError("x, y, and z must be a numerical type.")

    def __len__(self):
        """Returns the number of attributes contained in this class."""
        return 3

    def __str__(self):
        """Builds a string representation of this object."""
        return "<Vector3>: { " + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + " }"

    #Provide our operator overloaded methods
    def __eq__(self, other):
        """Check to see if two Vector3 instances are equal"""
        if not isinstance(other, Vector3):
            raise TypeError("other must be of type Vector3")

        if self.x == other.x    \
       and self.y == other.y    \
       and self.z == other.z:
            return True
        else:
            return False

    def __ne__(self, other):
        """Check to see if two Vector3 instances are not equal"""
        if not isinstance(other, Vector3):
            raise TypeError("other must be of type Vector3")

        if not(self.x == other.x)  \
        or not(self.y == other.y)  \
        or not(self.z == other.z):
            #True, the objects are not equal to each other.
            return True
        else:
            #False, the objects are equal to each other
            return False

    def __add__(self, other):
        """Adds two Vector3 objects, or a single float to the x, y, and z attributes."""
        if isinstance(other, Vector3):
            vec3 = Vector3()
            vec3.x = self.x + other.x
            vec3.y = self.y + other.y
            vec3.z = self.z + other.z
            return vec3
        else:
            #The object isn't of a correct type, return self to prevent errors.
            raise TypeError("other must be of type Vector3")

    def __radd__(self, other):
         return self.__add__(other)

    def __sub__(self, other):
        """Subtract two Vector3 objects, or a single float from the x, y, and z attributes"""
        if isinstance(other, Vector3):
            vec3 = Vector3()
            vec3.x = self.x - other.x
            vec3.y = self.y - other.y
            vec3.z = self.z - other.z
            return vec3
        else:
            raise TypeError("other must be of type Vector3")

    def __rsub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other):
        """Multiply a Vector3 and a scalar."""
        if isinstance(other, numbers.Number):
            vec3 = Vector3()
            vec3.x = self.x * other
            vec3.y = self.y * other
            vec3.z = self.z * other
            return vec3
        else:
            raise TypeError("other must be a single number")

    def __rmul__(self, other):
        return self.__mul__(other)

    def __div__(self, other):
        """Divide a Vector3 and a scalar."""
        if operator.isNumberType(other):
            vec3 = Vector3()
            vec3.x = self.x / other
            vec3.y = self.y / other
            vec3.z = self.z / other
            return vec3
        else:
            raise TypeError("other must be a single number")

    def __rdiv__(self, other):
        return self.__div__(other)

    def __neg__(self):
        """Negate the Vector"""
        neg_vec = Vector3()
        neg_vec.x = -self.x
        neg_vec.y = -self.y
        neg_vec.z = -self.z
        return neg_vec

    def __setitem__(self, index, value):
        """Set an internal value."""
        if index > 2:
            raise IndexError("index must be between 0 and 2 inclusive.")

        try:
            if index == 0:
                self.x = value
            elif index == 1:
                self.y = value
            else:
                self.z = value
        except (TypeError):
            raise TypeError("value must be a numerical type.")


    def __getitem__(self, index):
        """Get an internal value."""
        if index > 2:
            raise IndexError("index must be between 0 and 2 inclusive.")

        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            return self.z


    #Define our methods
    def copy(self):
        """Create a copy of the Vector"""
        cpy_vec = Vector3()
        cpy_vec.x = self.x
        cpy_vec.y = self.y
        cpy_vec.z = self.z
        return cpy_vec

    def to_vec4(self, isPoint):
        """Converts this vector3 into a vector4 instance."""
        vec4 = Vector4()
        vec4.x = self.x
        vec4.y = self.y
        vec4.z = self.z
        if isPoint:
            vec4.w = 1
        else:
            vec4.w = 0

        return vec4

    def length(self):
        """Gets the length of the Vector"""
        return math.sqrt((self.x * self.x) + (self.y * self.y) + (self.z * self.z))

    def normalize(self):
        """Normalizes this Vector"""
        vlength = self.length()

        #Make sure the length isn't 0
        if vlength > 0:
            self.x /= vlength
            self.y /= vlength
            self.z /= vlength
        else:
            return Vector3(0, 0, 0)

    def normalize_copy(self):
        """Creates and returns a new Vector3 that is a normalized version of this Vector"""
        newVec = self.copy()
        newVec.normalize()
        return newVec

    def clamp(self, clampVal):
        """Clamps all the components in the vector to the specified clampVal."""
        if self.x > clampVal:
            self.x = clampVal
        if self.y > clampVal:
            self.y = clampVal
        if self.z > clampVal:
            self.z = clampVal

    #Define our static methods
    def up():
        """Return a Vector that points in the up direction."""
        return Vector3(0, 1, 0)

    up = staticmethod(up)

    def tuple_as_vec(xyz):
        """
        Generates a Vector3 from a tuple or list.
        """
        vec = Vector3()
        vec[0] = xyz[0]
        vec[1] = xyz[1]
        vec[2] = xyz[2]
        return vec

    tuple_as_vec = staticmethod(tuple_as_vec)

    def cross(vec1, vec2):
        """Returns the cross product of two Vectors"""
        if isinstance(vec1, Vector3) and isinstance(vec2, Vector3):
            vec3 = Vector3()
            vec3.x = (vec1.y * vec2.z) - (vec1.z * vec2.y)
            vec3.y = (vec1.z * vec2.x) - (vec1.x * vec2.z)
            vec3.z = (vec1.x * vec2.y) - (vec1.y * vec2.x)
            return vec3
        else:
            raise TypeError("vec1 and vec2 must be Vector3's")

    cross = staticmethod(cross)

class Vector4(object):
    """Provides basic 3D Vector operations"""

    def __init__(self, x = 0.0, y = 0.0, z = 0.0, w = 0.0):
        """Constructs a Vector4 object with the default position of the object."""
        #Check for potential problems while converting the values.
        try:
            self.x = float(x)
            self.y = float(y)
            self.z = float(z)
            self.w = float(w)
        except (TypeError):
            raise TypeError("x, y, z, and w must be a numerical type.")

    def __len__(self):
        """Returns the number of attributes contained in this class."""
        return 4

    def __str__(self):
        """Builds a string representation of this object."""
        return "<Vector4>: { " + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ", " + str(self.w) + " }"

    #Provide our operator overloaded methods
    def __eq__(self, other):
        """Check to see if two Vector4 instances are equal"""
        if not isinstance(other, Vector4):
            return False

        if self.x == other.x    \
       and self.y == other.y    \
       and self.z == other.z    \
       and self.w == other.w:
            return True
        else:
            return False

    def __ne__(self, other):
        """Check to see if two Vector4 instances are not equal"""
        if not isinstance(other, Vector4):
            raise TypeError("other must be of type Vector4")

        if not(self.x == other.x)  \
        or not(self.y == other.y)  \
        or not(self.z == other.z)  \
        or not(self.w == other.w):
            #True, the objects are not equal to each other.
            return True
        else:
            #False, the objects are equal to each other
            return False

    def __add__(self, other):
        """Adds two Vector4 objects."""
        if isinstance(other, Vector4):
            vec4 = Vector4()
            vec4.x = self.x + other.x
            vec4.y = self.y + other.y
            vec4.z = self.z + other.z
            vec4.w = self.w + other.w
            return vec4
        else:
            #The object isn't of a correct type, return self to prevent errors.
            raise TypeError("other must be of type Vector3")

    def __radd__(self, other):
         return self.__add__(other)

    def __sub__(self, other):
        """Subtract two Vector4 objects."""
        if isinstance(other, Vector4):
            vec4 = Vector4()
            vec4.x = self.x - other.x
            vec4.y = self.y - other.y
            vec4.z = self.z - other.z
            vec4.w = self.w - other.w
            return vec4
        else:
            raise TypeError("other must be of type Vector4")

    def __rsub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other):
        """Multiply a Vector4 and a scalar."""
        if isinstance(other, numbers.Number):
            vec4 = Vector4()
            vec4.x = self.x * other
            vec4.y = self.y * other
            vec4.z = self.z * other
            vec4.w = self.w * other
            return vec4
        else:
            raise TypeError("other must be a single number")

    def __rmul__(self, other):
        return self.__mul__(other)

    def __div__(self, other):
        """Divide a Vector4 and a scalar."""
        if operator.isNumberType(other):
            vec4 = Vector4()
            vec4.x = self.x / other
            vec4.y = self.y / other
            vec4.z = self.z / other
            vec4.w = self.w / other
            return vec4
        else:
            raise TypeError("other must be a single number")

    def __rdiv__(self, other):
        return self.__div__(other)

    def __neg__(self):
        """Negate the Vector"""
        neg_vec = Vector4()
        neg_vec.x = -self.x
        neg_vec.y = -self.y
        neg_vec.z = -self.z
        neg_vec.w = -self.w
        return neg_vec

    def __setitem__(self, index, value):
        """Set an internal value."""
        if index > 3:
            raise IndexError("index must be between 0 and 3 inclusive.")

        try:
            if index == 0:
                self.x = value
            elif index == 1:
                self.y = value
            elif index == 2:
                self.z = value
            else:
                self.w = value
        except (TypeError):
            raise TypeError("value must be a numerical type.")


    def __getitem__(self, index):
        """Get an internal value."""
        if index > 3:
            raise IndexError("index must be between 0 and 3 inclusive.")

        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        elif index == 2:
            return self.z
        else:
            return self.w

    #Define our methods
    def copy(self):
        """Create a copy of the Vector"""
        cpy_vec = Vector4()
        cpy_vec.x = self.x
        cpy_vec.y = self.y
        cpy_vec.z = self.z
        cpy_vec.w = self.w
        return cpy_vec

    def to_vec3(self):
        """Convert this vector4 instance into a vector3 instance."""
        vec3 = Vector3()
        vec3.x = self.x
        vec3.y = self.y
        vec3.z = self.z

        if self.w != 0:
            vec3 /= self.w

        return vec3

    def length(self):
        """Gets the length of the Vector"""
        return math.sqrt((self.x * self.x) + (self.y * self.y) + (self.z * self.z) + (self.w * self.w))

    def normalize(self):
        """Normalizes this Vector"""
        vlength = self.length()

        #Make sure the length isn't 0
        if vlength > 0:
            self.x /= vlength
            self.y /= vlength
            self.z /= vlength
            self.w /= vlength
        else:
            return Vector4(0, 0, 0, 0)

    def normalize_copy(self):
        """Creates and returns a new Vector3 that is a normalized version of this Vector"""
        newVec = self.copy()
        newVec.normalize()
        return newVec

    def clamp(self, clampVal):
        """Clamps all the components in the vector to the specified clampVal."""
        if self.x > clampVal:
            self.x = clampVal
        if self.y > clampVal:
            self.y = clampVal
        if self.z > clampVal:
            self.z = clampVal
        if self.w > clampVal:
            self.w = clampVal

    #Define our static methods
    def up():
        """Return a Vector that points in the up direction."""
        return Vector4(0, 1, 0, 0)

    up = staticmethod(up)

    def tuple_as_vec(xyzw):
        """
        Generates a Vector4 from a tuple or list.
        """
        vec = Vector4()
        vec[0] = xyzw[0]
        vec[1] = xyzw[1]
        vec[2] = xyzw[2]
        vec[3] = xyzw[3]
        return vec

    tuple_as_vec = staticmethod(tuple_as_vec)

def dot(vec1, vec2):
    """Returns the dot product of two Vectors"""
    if isinstance(vec1, Vector3) and isinstance(vec2, Vector3):
        return (vec1.x * vec2.x) + (vec1.y * vec2.y) + (vec1.z * vec2.z)
    elif isinstance(vec1, Vector4) and isinstance(vec2, Vector4):
        return (vec1.x * vec2.x) + (vec1.y * vec2.y) + (vec1.z * vec2.z) + (vec1.w * vec2.w)
    else:
        raise TypeError("vec1 and vec2 must a Vector type")


def distance(vec1, vec2):
    """Returns the distance between two Vectors"""
    vec3 = vec2 - vec1
    return vec3.length()

def angle(vec1, vec2):
    """Returns the angle between two vectors"""
    dot_vec = dot(vec1, vec2)
    mag1 = vec1.length()
    mag2 = vec2.length()
    result = dot_vec / (mag1 * mag2)
    return math.acos(result)

def project(vec1, vec2):
    """Project vector1 onto vector2."""
    if isinstance(vec1, Vector3) and isinstance(vec2, Vector3) \
    or isinstance(vec1, Vector4) and isinstance(vec2, Vector4):
        return dot(vec1, vec2) / vec2.length() * vec2.normalize_copy()
    else:
        raise ValueError("vec1 and vec2 must be Vector3 or Vector4 objects.")

def component_add(vec1, vec2):
    """Add each of the components of vec1 and vec2 together and return a new vector."""
    if isinstance(vec1, Vector3) and isinstance(vec2, Vector3):
        addVec = Vector3()
        addVec.x = vec1.x + vec2.x
        addVec.y = vec1.y + vec2.y
        addVec.z = vec1.z + vec2.z
        return addVec

    if isinstance(vec1, Vector4) and isinstance(vec2, Vector4):
        addVec = Vector4()
        addVec.x = vec1.x + vec2.x
        addVec.y = vec1.y + vec2.y
        addVec.z = vec1.z + vec2.z
        addVec.w = vec1.w + vec2.w
        return addVec

def reflect(vec1, vec2):
    """Take vec1 and reflect it about vec2."""
    if isinstance(vec1, Vector3) and isinstance(vec2, Vector3) \
    or isinstance(vec1, Vector4) and isinstance(vec2, Vector4):
        return 2 * dot(vec1, vec2) * vec2 - vec2
    else:
        raise ValueError("vec1 and vec2 must both be a Vector type")

def sign(val):
    """
    Returns the sign of a number.
    """
    if val > 0:
        return 1
    elif val < 0:
        return -1

    return 0

class Ray(object):
    def __init__(self, origin = Vector3(0,0,0), direction = Vector3(0,0,0)):
        self.origin = origin
        self.direction = direction
        #Normalize our Vector
        self.direction.normalize()

    def get_point(self, scalar_val):
        """Get a point along the ray."""
        return scalar_val * self.direction + self.origin

class Matrix4(object):
    def __init__(self, *args):
        """
        *args defines a function that can accept a variable number of parameters.
        This allows us to be a bit more flexible in how we can create a Matrix,
        as the user can define all four rows, or only one or two rows upon init.
        """
        #A list of four Vector4's
        self.dta = []

        #Find the number of arguments the user passed to us.
        argLen = len(args)

        #Make sure we don't accept more than 4 lists.
        if argLen > 4:
            raise ValueError("*args should not contain more than four lists.")

        #Create an identity matrix if the user isn't filling all the rows with data.
        if argLen != 4:
            self.dta = Matrix4.identity().dta

        #Take each arg and append it to our dta list.
        for index, arg in enumerate(args):
            if isinstance(arg, Vector4) \
            or isinstance(arg, tuple) \
            or isinstance(arg, list):
                if len(arg) == 4:
                    self.dta.append(Vector4(arg[0], arg[1], arg[2], arg[3]))
                else:
                    raise ValueError("Each argument must contain four values or be a Vector4.")
            else:
                raise ValueError("Each argument must contain four values or be a Vector4.")

    def __getitem__(self, index):
        """Get a row from the matrix."""
        return self.get_row(index)

    def get_row(self, row):
        if row > -1 and row < 4:
            return self.dta[row].copy()

    def set_row(self, row, vec4):
        if row > -1 and row < 4:
            self.dta[row] = vec4.copy()

    def get_col(self, col):
        if col > -1 and col < 4:
            return Vector4(self.dta[0][col],
                           self.dta[1][col],
                           self.dta[2][col],
                           self.dta[3][col])

    def set_col(self, col, vec4):
        if col > -1 and col < 4:
            self.dta[col][0] = vec4.x,
            self.dta[col][1] = vec4.y,
            self.dta[col][2] = vec4.z,
            self.dta[col][3] = vec4.w

    def __mul__(self, other):
        if isinstance(other, Matrix4):
            return Matrix4 ( (dot(self.get_row(0), other.get_col(0)), dot(self.get_row(0), other.get_col(1)), dot(self.get_row(0), other.get_col(2)), dot(self.get_row(0), other.get_col(3))),
                             (dot(self.get_row(1), other.get_col(0)), dot(self.get_row(1), other.get_col(1)), dot(self.get_row(1), other.get_col(2)), dot(self.get_row(1), other.get_col(3))),
                             (dot(self.get_row(2), other.get_col(0)), dot(self.get_row(2), other.get_col(1)), dot(self.get_row(2), other.get_col(2)), dot(self.get_row(2), other.get_col(3))),
                             (dot(self.get_row(3), other.get_col(0)), dot(self.get_row(3), other.get_col(1)), dot(self.get_row(3), other.get_col(2)), dot(self.get_row(3), other.get_col(3))) )

        if isinstance(other, Vector4):
            vec = Vector4( dot(self.get_row(0), other),
                            dot(self.get_row(1), other),
                            dot(self.get_row(2), other),
                            dot(self.get_row(3), other) )
            return vec

        if isinstance(other, numbers.Number):
            return Matrix4( self.dta[0] * other,
                            self.dta[1] * other,
                            self.dta[2] * other,
                            self.dta[3] * other )

        raise TypeError("other must be of type Matrix4, Vector4, or number")

    def __rmul__(self, other):
        return self.__mul__(other)

    def __str__(self):
        string = ""
        for vec in self.dta:
            string += "[ " + str(vec.x) + " " + str(vec.y) + " " + str(vec.z) + " " + str(vec.w) + " ]\n"
        return string

    def transpose(self):
        """Create a transpose of this matrix."""
        ma4 = Matrix4( self.get_col(0),
                       self.get_col(1),
                       self.get_col(2),
                       self.get_col(3) )
        return ma4

    def is_identity():
        """Check to see if this matrix is an identity matrix."""
        for index, row in enumerate(self.dta):
            if row[index] == 1:
                for num, element in enumerate(row):
                    if num != index:
                        if element != 0:
                            return False
            else:
                return False

        return True

    def is_orthogonal():
        """Check to see if this matrix is orthogonal."""
        return (self * self.transpose()).is_identity()

    def inverse_as_orghogonal():
        """Get the inverse of this matrix, assuming this matrix is orthogonal."""
        return self.transpose()

    def identity():
        """Create and return an identity matrix."""
        ma4 = Matrix4( (1, 0, 0, 0),
                       (0, 1, 0, 0),
                       (0, 0, 1, 0),
                       (0, 0, 0, 1) )
        return ma4

    def translate(translationAmt):
        """Create a translation matrix."""
        if not isinstance(translationAmt, Vector3):
            raise ValueError("translationAmt must be a Vector3")

        ma4 = Matrix4( (1, 0, 0, translationAmt.x),
                       (0, 1, 0, translationAmt.y),
                       (0, 0, 1, translationAmt.z),
                       (0, 0, 0, 1) )
        return ma4

    def scale(scaleAmt):
        """
        Create a scale matrix.
        scaleAmt is a Vector3 defining the x, y, and z scale values.
        """
        if not isinstance(scaleAmt, Vector3):
            raise ValueError("scaleAmt must be a Vector3")

        ma4 = Matrix4( (scaleAmt.x, 0, 0, 0),
                       (0, scaleAmt.y, 0, 0),
                       (0, 0, scaleAmt.z, 0),
                       (0, 0, 0, 1) )
        return ma4

    def z_rotate(rotationAmt):
        """Create a matrix that rotates around the z axis."""
        ma4 = Matrix4( (math.cos(rotationAmt), -math.sin(rotationAmt), 0, 0),
                       (math.sin(rotationAmt), math.cos(rotationAmt), 0, 0),
                       (0, 0, 1, 0),
                       (0, 0, 0, 1) )

        return ma4

    def y_rotate(rotationAmt):
        """Create a matrix that rotates around the y axis."""
        ma4 = Matrix4( (math.cos(rotationAmt), 0, math.sin(rotationAmt), 0),
                       (0, 1, 0, 0),
                       (-math.sin(rotationAmt), 0, math.cos(rotationAmt), 0),
                       (0, 0, 0, 1) )
        return ma4

    def x_rotate(rotationAmt):
        """Create a matrix that rotates around the x axis."""
        ma4 = Matrix4( (1, 0, 0, 0),
                       (0, math.cos(rotationAmt), -math.sin(rotationAmt), 0),
                       (0, math.sin(rotationAmt), math.cos(rotationAmt), 0),
                       (0, 0, 0, 1) )

        return ma4

    def build_rotation(vec3):
        """
        Build a rotation matrix.
        vec3 is a Vector3 defining the axis about which to rotate the object.
        """
        if not isinstance(vec3, Vector3):
            raise ValueError("rotAmt must be a Vector3")
        return Matrix4.x_rotate(vec3.x) * Matrix4.y_rotate(vec3.y) * Matrix4.z_rotate(vec3.z)

    identity = staticmethod(identity)
    translate = staticmethod(translate)
    scale = staticmethod(scale)
    z_rotate = staticmethod(z_rotate)
    y_rotate = staticmethod(y_rotate)
    x_rotate = staticmethod(x_rotate)
    build_rotation = staticmethod(build_rotation)

class Ragnarok(object):
    world = None
    def __init__(self, preferred_backbuffer_size = (-1, -1), window_name = "Ragnarok Game"):
        global world
        """
        Prepares the Ragnarok library for use.
        preferred_back_size attempts to set the resolution of the window to the specified size. (-1, -1) attempts native resolution.
        window_name is the text that displays on the top-left of the pygame window.
        """
        print 'Booting Ragnarok\n'

        pygame.init()

        self.__is_running = True

        #The number of times our engine should update per second.
        self.preferred_fps = 60

        #Create a clock to manage our update frequency
        self.__clock = pygame.time.Clock()

        #Init our world
        world = World()
        if preferred_backbuffer_size == Vector2(-1, -1):
            world.set_display_at_native_res()
        else:
            world.set_backbuffer(preferred_backbuffer_size)

        pygame.display.set_caption(window_name)

        #Used to print the fps of the game onto the console window.
        self.fpsTimer = 0.0

    	#Should Ragnarok print the number of frames the game is running at?
    	self.print_frames = False

    	#The number of milliseconds between printing out the frame rate
    	self.print_fps_frequency = 1000

    	#Used to tell Ragnarok how to handle certain events.
    	#Once set, it must be explicitely unset
    	#Flag 0 means to skip updating
    	#Flag 1 means to skip drawing
    	#Flag 2 means to discard timing values
    	self.event_flags = []

    def get_world():
        return world

    get_world = staticmethod(get_world)

    def exit(self):
        """Exit the game"""
        self.__is_running = False

    def __handle_events(self):
        """This is the place to put all event handeling."""
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.exit()

    def run(self):
        """Start the game loop"""
        global world
        self.__is_running = True
        while(self.__is_running):
            #Our game loop

            #Catch our events
            self.__handle_events()

	        #Update our clock
            self.__clock.tick(self.preferred_fps)
            elapsed_milliseconds = self.__clock.get_time()
    	    if 2 in self.event_flags:
                self.elapsed_milliseconds = 0

            #Print the fps that the game is running at.
    	    if self.print_frames:
                self.fpsTimer += elapsed_milliseconds
                if self.fpsTimer > self.print_fps_frequency:
                    print "FPS: ", self.__clock.get_fps()
                    self.fpsTimer = 0.0

            #Update all of our objects
    	    if not 0 in self.event_flags:
        	   world.update(elapsed_milliseconds)

            #Draw all of our objects
    	    if not 1 in self.event_flags:
        	   world.draw(elapsed_milliseconds)

            #Make our world visible
            pygame.display.flip()

class Pool(object):
    """Create a pool of reusable objects. Reduces memory allocations due to new objects being constantly generated (such as in bullets being fired, etc.)"""
    def __init__(self, object_count = 0, init_function = None):
        """
        object_count is the number of objects we want to store in our pool.
        init_function is an optional delegate that specifies how the object should be inited.
            init_function should return the type of object that we want to use.
        """
        #A list containing all of our objects.
        self.queue = []

        #The number of objects left in the pool.
        self.objects_in_pool = 0

        #The number of ojects the user has checked out and not returned.
        self.active_objects = 0

        #The function used to init our objects.
        self.init_function = init_function

        #Generate our pool.
        for i in range(object_count):
            self.__init_object()


    def __init_object(self):
        """Create a new object for the pool."""
        #Check to see if the user created a specific initalization function for this object.
        if self.init_function is not None:
            new_obj = self.init_function()
            self.__enqueue(new_obj)
        else:
            raise TypeError("The Pool must have a non None function to fill the pool.")

    def __dequeue(self):
        """Pull an object from the list."""
        self.objects_in_pool -= 1
        return self.queue.pop()

    def __enqueue(self, item):
        """Add an object to the list."""
        self.objects_in_pool += 1
        self.queue.append(item)

    def request_object(self):
        """Grab an object from the pool. If the pool is empty, a new object will be generated and returned."""
        obj_to_return = None
        if self.queue.count > 0:
            obj_to_return = self.__dequeue()
        else:
            #The queue is empty, generate a new item.
            self.__init_object()
            object_to_return = self.__dequeue()
        self.active_objects += 1
        return obj_to_return

    def return_object(self, obj):
        """Return a checked out object back into the queue."""
        self.__enqueue(obj)
        self.active_objects -= 1

class UpdatableObj(object):
    """
    The base class of our game engine.
    Represents an object that can be updated.
    """
    #The number of objects that have existed so far. Used to create a unique object id.
    __total_id = 0

    def __init__(self, update_order = 0):
        #The order in which this object should update relative to the other objects.
        self.update_order = update_order

        #Represents the unique identifer for this object.
        self.obj_id = self.__total_id

        #Keeps track of the total number of object created since game start.
        UpdatableObj.__total_id += 1

        #Is the object allowed to update druing the update loop?
        self.is_enabled = True

        #Does the object stay in one place even if the camera is moving?
        self.is_static = True

        #Represents the location of the object in world space.
        self.coords = Vector2()

        #Allows the user to define the object as they want.
        self.tag = ""

    def __str__(self):
        return "{ \nUpdateableObj: \t Update Order: " + str(self.update_order) + "\t Object ID: " \
               + str(self.obj_id) + "\t Is Enabled: " + str(self.is_enabled)+ "\n}"

    def update(self, milliseconds):
        #Update the object.
        pass

class DrawableObj(UpdatableObj):
    """An object that represents something that can be drawn."""
    def __init__(self, update_order = 0, draw_order = 0):
        super(DrawableObj, self).__init__(update_order)
        self.draw_order = draw_order

        #Should the object draw during the update loop?
        self.is_visible = True

    def show(self):
        """Enable and show the object."""
        self.is_enabled = true
        self.is_visible = true

    def hide(self):
        """Disable and hide the object."""
        self.is_enabled = false
        self.is_visible = false

    def is_visible_to_camera(self, camera):
        """Is the object visible to the camera?"""
        return True

    def draw(self, milliseconds, render_surface):
        #Draw the object
        pass

class Sprite(DrawableObj):
    def __init__(self, update_order = 0, draw_order = 0):
        super(Sprite, self).__init__(update_order, draw_order)

        #The surface rendered onto the screen when draw is called.
        self.image = pygame.surface.Surface( (0, 0) )

        #Our unrotated and unscaled image. This must be used, else PyGame will grind to a halt and crash if many rotations and/or scales are used.
        self.untransformed_image = self.image

        #Determines the area of the image that will be drawn out
##        self.rect = pygame.Rect(0, 0, 0, 0)
        self.source = pygame.Rect(0, 0, 0, 0)

        #Basic transformation data
        #Used to set the origin when the surface is scaled or rotated. Contains the
        #original origin (in a value between 0 - 1) that was set by the user or Ragnarok.
        self.__untransformed_nor_origin = Vector2()
        self.__origin = Vector2()
        self.__rotation = 0.0
        self.__scale = Vector2(1, 1)
        self.tint_color = pygame.Color(255,255,255,255)

        #Is a scale operation pending?
        self.__is_scale_pending = False

        #Is a rotation operation pending?
        self.__is_rot_pending = False

        self.__horizontal_flip = False
        self.__vertical_flip = False

    def get_origin(self):
        return self.__origin

    def set_origin(self, orig):
        #Do not continue if setting the origin would result in division by zero.
        if self.untransformed_image.get_width() == 0      \
        or self.untransformed_image.get_height() == 0:
            return

        self.__origin = orig
        self.__untransformed_nor_origin = Vector2(self.__origin.X / self.untransformed_image.get_width(),
                                                  self.__origin.Y / self.untransformed_image.get_height())

    def center_origin(self):
        """Sets the origin to the center of the image."""
        self.set_origin( Vector2(self.image.get_width() / 2.0, self.image.get_height() / 2.0) )

    def get_rotation(self):
        return self.__rotation

    def set_rotation(self, degrees):
        if degrees > 360:
            degrees -= 360
        elif degrees < 0:
            degrees -= 360

        self.__rotation = degrees
        self.__is_rot_pending = True

    def get_scale(self):
        return self.__scale

    def scale_to(self, width_height = Vector2()):
        """Scale the texture to the specfied width and height."""
        scale_amt = Vector2()
        scale_amt.X = float(width_height.X) / self.image.get_width()
        scale_amt.Y = float(width_height.Y) / self.image.get_height()
        self.set_scale(scale_amt)

    def set_scale(self, scale_amt):
        """
        Scale the texture.
        scale_amt is a Vector2 whose values are between 0 and 1, where 1 is the full texture, and 0 is scaled so that the texture is invisible.
        A scale_amt value greater than one will scale the texture to a greater size.
        """
        self.__scale = scale_amt
        self.__is_scale_pending = True

    def get_hflip(self):
        return self.__horizontal_flip

    def set_hflip(self, val):
        """val is True or False that determines if we should horizontally flip the surface or not."""
        if self.__horizontal_flip is not val:
            self.__horizontal_flip = val
            self.image = pygame.transform.flip(self.untransformed_image, val, self.__vertical_flip)

    def get_vflip(self):
        return self.__vertical_flip

    def set_vflip(self, val):
        """val is True or False that determines if we should vertically flip the surface or not."""
        if self.__vertical_flip is not val:
            self.__vertical_flip = val
            self.image = pygame.transform.flip(self.untransformed_image, self.__horizontal_flip, val)

    origin = property(get_origin, set_origin)
    rotation = property(get_rotation, set_rotation)
    scale = property(get_scale, set_scale)
    h_flip = property(get_hflip, set_hflip)
    v_flip = property(get_vflip, set_vflip)

    def load_texture(self, file_path):
        """Generate our sprite's surface by loading the specified image from disk. Note that this automatically centers the origin."""
        self.image = pygame.image.load(file_path)
        self.apply_texture(self.image)

    def apply_texture(self, image):
        """Place a preexisting texture as the sprite's texture."""
        self.image = image.convert_alpha()
        self.untransformed_image = self.image.copy()
##        self.rect.x = 0
##        self.rect.y = 0
##        self.rect.width = self.image.get_width()
##        self.rect.height = self.image.get_height()
        self.source.x = 0
        self.source.y = 0
        self.source.width = self.image.get_width()
        self.source.height = self.image.get_height()
        center = Vector2(self.source.width / 2.0,
                         self.source.height / 2.0)
        self.set_origin(center)
##        self.rect.x = self.w_coords.X
##        self.rect.y = self.w_coords.Y

    def __resize_surface_extents(self):
        """Handles surface cleanup once a scale or rotation operation has been performed."""
        #Set the new location of the origin, as the surface size may increase with rotation
        self.__origin.X = self.image.get_width() * self.__untransformed_nor_origin.X
        self.__origin.Y = self.image.get_height() * self.__untransformed_nor_origin.Y

##        #Update the size of the rectangle
##        self.rect = self.image.get_rect()
##
##        #Reset the coordinates of the rectangle to the user defined value
##        self.set_coords(self.w_coords)

        #We must now resize the source rectangle to prevent clipping
        self.source.width = self.image.get_width()
        self.source.height = self.image.get_height()

    def __execute_scale(self, surface, size_to_scale_from):
        """Execute the scaling operation"""
        x = size_to_scale_from[0] * self.__scale[0]
        y = size_to_scale_from[1] * self.__scale[1]
        scaled_value = (int(x), int(y))

##        #Find out what scaling technique we should use.
##        if self.image.get_bitsize >= 24:
##            #We have sufficient bit depth to run smooth scale
##            self.image = pygame.transform.smoothscale(self.image, scaled_value)
##        else:
            ##Surface doesn't support smooth scale, revert to regular scale
        self.image = pygame.transform.scale(self.image, scaled_value)

        self.__resize_surface_extents()

    def __execute_rot(self, surface):
        """Executes the rotating operation"""
        self.image = pygame.transform.rotate(surface, self.__rotation)
        self.__resize_surface_extents()

    def __handle_scale_rot(self):
        """Handle scaling and rotation of the surface"""
        if self.__is_rot_pending == True:
            self.__execute_rot(self.untransformed_image)
            self.__is_rot_pending = False

            #Scale the image using the recently rotated surface to keep the orientation correct
            self.__execute_scale(self.image, self.image.get_size())
            self.__is_scale_pending = False

        #The image is not rotating while scaling, thus use the untransformed image to scale.
        if self.__is_scale_pending == True:
            self.__execute_scale(self.untransformed_image, self.untransformed_image.get_size())
            self.__is_scale_pending = False

    def is_visible_to_camera(self, camera):
        if self.coords.X > camera.view_bounds.right:
            return False

        if (self.coords.X + self.image.get_width()) < camera.view_bounds.left:
            return False

        height = self.image.get_height()
        if (self.coords.Y - height) > camera.view_bounds.bottom:
            return False

        if (self.coords.Y + height) < camera.view_bounds.top:
            return False

        return True

    def update(self, milliseconds):
        """Update the sprite and its nodes."""
        if self.is_enabled:
            #Scale and rotate the sprite as necessary
            self.__handle_scale_rot()



    def draw(self, milliseconds, render_surface):
        """Draw the image to the specified surface."""
        if self.is_visible:
            if not(self.__scale[0] == 0 or self.__scale[1] == 0):
                if self.image is not None:
                    #Create our rectangle to describe our sprite.
                    tmpRect = pygame.Rect(self.coords.X - self.__origin.X, \
                                self.coords.Y - self.__origin.Y, \
                                self.image.get_width(),
                                self.image.get_height())
                    #Apply tinting to the sprite.
                    #tintedSurface = self.image.copy()
                    #self.image.fill(self.tint_color, special_flags = pygame.BLEND_RGB_MULT)
                    render_surface.blit(self.image, tmpRect, self.source, special_flags = 0)

class Text(DrawableObj):
    def __init__(self, update_order = 0, draw_order = 0, font_path = "", font_size = 0, color = (0,0,0)):
        super(Text, self).__init__(update_order, draw_order)

        #We use a sprite to provide text rotation and scaling capibilities.
        self.__font_sprite = Sprite(update_order, draw_order)
        self.__font = None
        self.__text = ""
        self.__font_size = font_size
        self.__font_path = font_path
        self.__color = color
        self.load_font(font_path, font_size)

    def load_font(self, font_path, font_size):
        """Load the specified font from a file."""
        self.__font_path = font_path
        self.__font_size = font_size
        if font_path != "":
            self.__font = pygame.font.Font(font_path, font_size)
            self.__set_text(self.__text)

    def __set_font_size(self, font_size):
        """Sets the size of the font."""
        #We need to reload the font in order to change the font's size.
        self.load_font(self.__font_path, font_size)

    def __get_font_size(self):
        """Gets the current size of the font."""
        return self.__font_size

    def __render_onto_sprite(self):
        """Render the font onto a surface and store the surface into a sprite so we can do more complex stuff with it. (such as rotation and scale)"""
        font_surface = self.__font.render(self.__text, True, self.color)
        self.__font_sprite.apply_texture(font_surface)
        self.__font_sprite.center_origin()

    def __set_text(self, string):
        """Set the text that displays."""
        self.__text = string

        #Render the new text into a sprite.
        self.__render_onto_sprite()

    def __get_text(self):
        """Get the text that is currently displaying."""
        return self.__text

    def __set_scale(self, scale):
        """Set the scale of the font."""
        self.__font_sprite.scale = scale

    def __get_scale(self):
        """Get the scale of the font."""
        return self.__font_sprite.scale

    def __set_rotation(self, rotation):
        """Rotate the font."""
        self.__font_sprite.rotation = rotation

    def __get_rotation(self):
        """Get the rotation of the font."""
        return self.__font_sprite.rotation

    def __set_color(self, color):
        self.__color = color
        self.__render_onto_sprite()

    def __get_color(self):
        return self.__color

    #Create our properties.
    text = property(__get_text, __set_text)
    scale = property(__get_scale, __set_scale)
    rotation = property(__get_scale, __set_scale)
    font_size = property(__get_font_size, __set_font_size)
    color = property(__get_color, __set_color)

    def update(self, milliseconds):
        self.__font_sprite.update(milliseconds)
        super(Text, self).update(milliseconds)

    def draw(self, milliseconds, surface):
        #print self.__font_sprite.image.get_size()
        self.__font_sprite.coords = self.coords
        self.__font_sprite.draw(milliseconds, surface)
        super(Text, self).draw(milliseconds, surface)


class Particle(Sprite):
    def __init__(self, image_path = "", color_start = (255,255,255), color_end = (255,255,255), \
                rotation_range = (0, 0), rotation_speed = 1.0, start_scale = Vector2(1, 1), \
                end_scale = Vector2(1,1), lifetime = 1000.0):
        """
        image_path is the path to the texture we wish to load.
        color_start is the starting color of the particle.
        color_end is the ending color of the particle.
        rotation_range is a tuple that defines the potential starting rotational values. The rotation will be between the first and second arguments.
        rotation_speed is how fast the particle rotates per second.
        start_scale is the starting scale of the particle.
        end_scale is the ending scale of the particle.
        lifetime is the length that the particle exists before dying.
        """
        super(Particle, self).__init__()
        self.load_texture(image_path)
        self.image_path = image_path
        self.start_color = color_start
        self.end_color = color_end
        self.rotation_range = rotation_range
        self.rotation_speed = rotation_speed
        self.start_scale = start_scale
        self.end_scale = end_scale
        self.lifetime = lifetime
        self.current_time = 0.0
        self.physics = PhysicsObj()

    def is_living(self):
        """Is the particle instance still living?"""
        if self.current_time >= self.lifetime:
            return False

        return True

    def initalize(self, physics_dta):
        """
        Prepare our particle for use.
        physics_dta describes the velocity, coordinates, and acceleration of the particle.
        """
        self.rotation = random.randint(self.rotation_range[0], self.rotation_range[1])
        self.current_time = 0.0
        self.color = self.start_color
        self.scale = self.start_scale
        self.physics = physics_dta

    def update(self, gametime):
        self.current_time += gametime
        self.physics.update(gametime)
        self.coords = self.physics.coords
        self.scale = Vector2.lerp(self.start_scale, self.end_scale, self.current_time / self.lifetime)
        self.rotation += self.rotation_speed * (gametime / 1000.0)
        super(Particle, self).update(gametime)

    def draw(self, milliseconds, surface):
        super(Particle, self).draw(milliseconds, surface)

class ParticleEmitter(DrawableObj):
    def __init__(self, coords = Vector2(0, 0), particle_type = None, \
        lifetime = 1000.0, emit_rate = 1000.0, direction_range = (0, 0), \
        particle_speed = 1, max_particles = 1000):
        """
        coords is the position of the emitter.
        particle_type is the type of particle to generate.
        lifetime is the length that the particle system lasts (not the particles.) -1 means to last for eternity.
        emit_rate is the amount of time that must elapse before a new particle is generated.
        direction_range is the direction in which the particles are emitted.
        """
        super(ParticleEmitter, self).__init__()

        #Our list of particle attractors.
        self.coords = coords
        self.attractors = []
        self.particle = particle_type

        #The particles that are currently being updated and rendered.
        self.particles = []
        self.lifetime = lifetime
        self.emit_rate = emit_rate
        self.lifetime_timer = Timer(lifetime)
        self.particle_create_timer = Timer(emit_rate)
        self.max_particles = max_particles
        self.direction_range = direction_range
        self.particle_speed = particle_speed
        self.current_particle_count = 0

        self.particle_pool = Pool(max_particles, self.__particle_generate)

    def __particle_generate(self):
        new_particle = Particle(self.particle.image_path, self.particle.start_color,
            self.particle.end_color, self.particle.rotation_range, self.particle.rotation_speed,\
            self.particle.start_scale, self.particle.end_scale, self.particle.lifetime)
        return new_particle

    def __create_particle(self, milliseconds):
        self.particle_create_timer.update(milliseconds)
        if self.particle_create_timer.is_ringing():
            self.particle_create_timer.reset()
            if self.current_particle_count < self.max_particles:
                self.__release_particle()

    def __release_particle(self):
        """Pull a particle from the queue and add it to the active list."""
        #Calculate a potential angle for the particle.
        angle = random.randint(int(self.direction_range[0]), int(self.direction_range[1]))
        velocity = Vector2.from_polar(angle, self.particle_speed)

        physics = PhysicsObj(self.coords, Vector2(), velocity)
        particle = self.particle_pool.request_object()
        particle.initalize(physics)
        self.particles.append(particle)
        self.current_particle_count += 1

    def update(self, milliseconds):
        self.__create_particle(milliseconds)

        if self.lifetime_timer.alarm_time is not -1:
            self.lifetime_timer.update(milliseconds)
            if self.lifetime_timer.is_ringing():
                #Remove all particles from the system and prevent any more updates
                for particle in self.particles:
                    self.particle_pool.return_object(particle)
                    self.particles.remove(particle)
                self.current_particle_count = 0
                return

        for particle in self.particles:
            particle.update(milliseconds)
            if particle.is_living() is False:
                self.particle_pool.return_object(particle)
                self.particles.remove(particle)
                self.current_particle_count -= 1

        super(ParticleEmitter, self).update(milliseconds)

    def draw(self, milliseconds, surface):
        for particle in self.particles:
            particle.draw(milliseconds, surface)
        super(ParticleEmitter, self).draw(milliseconds, surface)

class SpriteSheet(Sprite):
    def __init__(self):
        super(SpriteSheet, self).__init__()
        #An array of rectangles that contains the position of each cell.
        self.cells = []

        #The total number of cells present in the spritesheet
        self.num_of_cells = 0

        #The size of each cell in the spritesheet.
        self.__cell_bounds = (0 , 0)

    def __cell_width(self):
        return self[0].width

    def __cell_height(self):
        return self[0].height

    cell_width = property(__cell_width, None)
    cell_height = property(__cell_height, None)

    #Allow the user to treat this as an array
    def __getitem__(self, index):
        """Get the rectangular bounding area of a specified cell."""
        return self.cells[index]

    def load_texture(self, file_path, cell_size = (256, 256)):
        """
        Load a spritesheet texture.
        cell_size is the uniform size of each cell in the spritesheet.
        """
        super(SpriteSheet, self).load_texture(file_path)
        self.__cell_bounds = cell_size
        self.__generate_cells()

    def __generate_cells(self):
        y_loop_max = int(self.image.get_height() / self.__cell_bounds[1])
        x_loop_max = int(self.image.get_width() / self.__cell_bounds[0])
        self.num_of_cells = y_loop_max * x_loop_max

        x_coord = 0
        y_coord = 0

        for y in range(y_loop_max):
            next_y = y_coord + self.__cell_bounds[1]
            for x in range(x_loop_max):
                next_x = x_coord + self.__cell_bounds[0]
                cell_bounds = pygame.Rect(x_coord, y_coord, self.__cell_bounds[0], self.__cell_bounds[1])
                self.cells.append(cell_bounds)
                x_coord = next_x
            y_coord = next_y
            x_coord = 0

        #print "Animation generated these cells: \n", self.cells

    def draw(self, milliseconds, surface, cell):
        """Draw out the specified cell"""
        #print self.cells[cell]
        self.source = self.cells[cell].copy()
        #Find the current scale of the image in relation to its original scale.
        current_scale = Vector2()
        current_scale.X = self.rect.width / float(self.untransformed_image.get_width())
        current_scale.Y = self.rect.height / float(self.untransformed_image.get_height())
        #self.source.x *= self.scale.X
        #self.source.y *= self.scale.Y
        self.source.width *= current_scale.X
        self.source.height *= current_scale.Y
        super(SpriteSheet, self).draw(milliseconds, surface)

class Animation(DrawableObj):
    def __init__(self, sprite_sheet, frame_rate = 24, end_frame = 0):
        """
        sprite_sheet is a SpriteSheet that our animation will pull its cells from.
        end_frame is the ending frame of the animation. 0 or less indicates to use the number of frames in the sprite_sheet
        Note that the animation cannot run any faster than the game's FPS. If the game runs at 60fps, the best the animation can do is 60fps as well.
        """
        super(DrawableObj, self).__init__()
        self.current_frame = 0
##        self.frame_rate = 24
        self.set_frame_rate(frame_rate)
        if end_frame > 0:
            self.end_frame = end_frame
        else:
            self.end_frame = sprite_sheet.num_of_cells
        self.sprite_sheet = sprite_sheet

##        #Calculate the number of milliseconds we should pause before progressing to the next frame
##        self.delay_between_frames = 1000 / self.frame_rate
##        self.timer = Timer(self.delay_between_frames)

        def __str__(self):
            return self.draw_order

    def get_frame_rate(self):
        return frame_rate

    def set_frame_rate(self, value):
        #Calculate the number of milliseconds we should pause before progressing to the next frame
        self.__frame_rate = value
        if value > 0:
            self.delay_between_frames = 1000 / self.frame_rate
        elif value == 0:
            self.delay_between_frames = 0.0
        self.timer = Timer(self.delay_between_frames)

    frame_rate = property(get_frame_rate, set_frame_rate)

    def increment_frame(self):
        """Increment a frame of the animation."""
        self.current_frame += 1

        if self.current_frame >= self.end_frame:
            #Wrap back to the beginning of the animation.
            self.current_frame = 0

    def update(self, milliseconds):
        super(Animation, self).update(milliseconds)
        self.timer.update(milliseconds)
        if self.timer.is_ringing():
            #Increment our current frame
            self.increment_frame()
            self.timer.reset()

    def draw(self, milliseconds, surface):
        super(Animation, self).draw(milliseconds, surface)

        #Draw out the current frame.
        self.sprite_sheet.draw(milliseconds, surface, self.current_frame)

class AnimationList(DrawableObj):
    """Represents an animation that is made up of seperate images rather than a single spritesheet."""
    def __init__(self):
        super(AnimationList, self).__init__()
        #The list of images that make up our animation
        self.images = []

        #The frame rate is the number of frames that should display per second.
        self.set_frame_rate(24)

        #The current fame we are displaying.
        self.current_frame = 0

        #Should the animation repeat when it has completed?
        self.should_repeat = False

        #The current location of our animation.
        self.__coords = Vector2()

        self.__horizontal_flip = False
        self.__vertical_flip = False

    def get_frame_rate(self):
        return self.__frame_rate

    def set_frame_rate(self, value):
        #Calculate the number of milliseconds we should pause before progressing to the next frame
        self.__frame_rate = value
        if value > 0:
            self.delay_between_frames = 1000 / self.frame_rate
        elif value == 0:
            self.delay_between_frames = 0.0

        self.timer = Timer(self.delay_between_frames)

    def get_origin(self):
        """Get the origin of the currently displayed frame."""
        return self.images[self.current_frame].origin

    def get_image_width(self):
        """Get the width of the currently displayed image."""
        return self.images[self.current_frame].image.get_width()

    def get_image_height(self):
        """Get the height of the currently displayed image."""
        return self.images[self.current_frame].image.get_height()

    def get_coords(self):
        return self.__coords

    def set_coords(self, value):
        """Set all the images contained in the animation to the specified value."""
        self.__coords = value
        for image in self.images:
            image.coords = value

    def get_hflip(self):
        """Get the horizontal flip status of the animation."""
        return self.__horizontal_flip

    def set_hflip(self, val):
        """Flip all the images in the animation list horizontally."""
        self.__horizontal_flip = val
        for image in self.images:
            image.h_flip = val

    def get_vflip(self):
        """Get the vertical flip status of the animation."""
        return self.__vertical_flip

    def set_vflip(self, val):
        """Flip all the images in the animation list vertically."""
        self.__vertical_flip = val
        for image in self.images:
            image.v_flip = val

    frame_rate = property(get_frame_rate, set_frame_rate)
    origin = property(get_origin, None)
    coords = property(get_coords, set_coords)
    h_flip = property(get_hflip, set_hflip)
    v_flip = property(get_vflip, set_vflip)

    def copy(self):
        """Create a copy of the animation."""
        animation = AnimationList()
        animation.set_frame_rate(self.frame_rate)
        animation.__coords = self.__coords
        animation.__horizontal_flip = self.__horizontal_flip
        animation.__vertical_flip = self.__vertical_flip
        animation.should_repeat = self.should_repeat
        animation.draw_order = self.draw_order
        animation.update_order = self.update_order
        for image in self.images:
            new_image = Sprite()
            new_image.coords = image.coords
            new_image.apply_texture(image.image)
            animation.images.append(new_image)

        return animation

    def get_currently_display_image(self):
        """Get the image that is currently displaying in this animation."""
        return self.images[self.current_frame]

    def increment_frame(self):
        """Increment a frame of the animation."""
        if self.current_frame < len(self.images):
            self.current_frame += 1

            if self.current_frame >= len(self.images):
                #Wrap back to the beginning of the animation if should_repeat is true.
                if self.should_repeat:
                    self.current_frame = 0
                else:
                    #Clamp the current frame to the number of images we have in our list
                    self.current_frame = len(self.images) - 1

            #Set the image that is currently displaying.
            if self.current_frame < len(self.images):
                self.image = self.images[self.current_frame]
                self.image.coords = self.coords

    def update(self, milliseconds):
        super(AnimationList, self).update(milliseconds)
        self.images[self.current_frame].update(milliseconds)
        self.timer.update(milliseconds)
        if self.timer.is_ringing():
            #Increment our current frame
            self.increment_frame()
            self.timer.reset()

    def draw(self, milliseconds, surface):
        self.images[self.current_frame].draw(milliseconds, surface)
        super(AnimationList, self).draw(milliseconds, surface)


class Timer(UpdatableObj):
    def __init__(self, alarm_time = 0.0):
        super(Timer, self).__init__()

        #The timer at which the timer is currently at (in milliseconds)
        self.__current_time = 0.0

        #The time at which the timer should begin ringing (in milliseconds)
        self.alarm_time = alarm_time

    #Define our getter methods
    def get_current_time(self):
        """Get the current time that the timer is at."""
        return self.__current_time

    #Define our wrapper properties
    current_time = property(get_current_time)

    def is_ringing(self):
        """Is the timer ringing?"""
        if self.__current_time >= self.alarm_time:
            return True

        return False

    def reset(self):
        """Reset the time inside of the timer."""
        self.__current_time = 0.0

    def update(self, milliseconds):
        super(Timer, self).update(milliseconds)
        if not self.is_ringing():
            self.__current_time += milliseconds

class PhysicsObj(UpdatableObj):
    """A class with basic physics implemented."""
    def __init__(self, coords = Vector2(), acceleration = Vector2(), velocity = Vector2()):
        self.acceleration = acceleration
        self.velocity = velocity
        self.coords = coords

    def update(self, milliseconds):
        #vf = vi + a * t
        time = (milliseconds / 1000.0)
        self.velocity += self.acceleration * time
        self.coords += self.velocity * time

class CollidableObj(DrawableObj):
    """Provides an abstract base class for collidable objects."""
    def __init__(self, collision_function = None, tag = "", parent = None):
        """
        collision_function is the function that should execute when there is a collision.
        It should take one parameter, a reference to the other collision object.
        parent is the object that this collidable object is attached to.
        """
        super(CollidableObj, self).__init__()
        self.collision_function = collision_function

        #The object that owns this collision object.
        self.parent = parent

        #Tags are used to identify collisions. A collision handler function could read in this tag and decide if it should register the collision or not.
        self.tag = tag

    def is_colliding(self, other):
        pass

    def collision_response(self, other):
        """
        The method that executes when a collision is detected.
        collision_function(self, other) is called when this method is executed.
        """
        if self.collision_function is not None:
            self.collision_function(other)

    def draw(self, milliseconds, surface):
        """Render the bounds of this collision ojbect onto the specified surface."""
        super(CollidableObj, self).draw(milliseconds, surface)

class BoundingCircle(CollidableObj):
    def __init__(self, coords = Vector2(0.0, 0.0), radius = 0.0, collision_response = None, tag = ""):
        super(BoundingCircle, self).__init__(collision_response, tag)
        self.coords = coords
        self.radius = radius

    def is_colliding(self, other):
        """Check to see if two circles are colliding."""
        if isinstance(other, BoundingCircle):
            #Calculate the distance between two circles.
            distance = Vector2.distance(self.coords, other.coords)

            #Check to see if the sum of thier radi are greater than or equal to the distance.
            radi_sum = self.radius + other.radius

            if distance <= radi_sum:
                #There has been a collision
##                print "Distance: ", distance, "\nRadi Sum: ", radi_sum
##                print "Self Coords: ", self.coords, "\nOther Coords: ", other.coords
                return True

            #No collision.
            return False

    def draw(self, milliseconds, surface):
        pygame.draw.circle(surface, (0, 255, 0), self.coords, self.radius, 2)
        super(BoundingCircle, self).draw(milliseconds, surface)

class AABoundingBox(CollidableObj):
    """Represents an axis aligned bounding box."""
    def __init_(self, rect = None):
        super(AABoundingBox, self).__init__()
        self.rect = rect

    def is_colliding(self, other):
        """Check to see if two AABoundingBoxes are colliding."""
        if isinstance(other, AABoundingBox):
            if self.rect.colliderect(other.rect):
                return True
            return False

    def draw(self, milliseconds, surface):
        pygame.draw.rect(surface, pygame.Color(0, 255, 0), self.rect, 2)
        super(AABoundingBox, self).draw(milliseconds, surface)

class CollisionManager(DrawableObj):
    """Handles the collisions between all Collidable Objects."""
    collidable_objects = []

    def __init__(self):
        super(CollisionManager, self).__init__(10000, 10000)
        global collidable_objects
        collidable_objects = []
        self.is_visible = False

        #The depths determine if we should only notice the first collision and object runs into per update
        #or if we should pay attention to all collisions the object collides with.
        self.SHALLOW_DEPTH = "SHALLOW"
        self.DEEP_DEPTH = "DEEP"
        self.collision_depth = self.SHALLOW_DEPTH

    def add_object(collision_object):
        """Add a collision object to the Manager"""
        global collidable_objects
        if isinstance(collision_object, CollidableObj):
            #print "Collision object of type ", type(collision_object), " added to the collision manager."
            collidable_objects.append(collision_object)

    def remove_object(collision_object):
        """Remove the collision object from the Manager"""
        global collidable_objects
        if isinstance(collision_object, CollidableObj):
            #print "Collision object of type ", type(collision_object), " removed from the collision manager."
            try:
                collidable_objects.remove(collision_object)
            except:
                print "Ragnarok Says: Collision_Object with ID # " + str(collision_object.obj_id) + " could not be found in the Collision Manager. Skipping over..."

    def remove_all():
        """Remove all objects from the collosion manager."""
        global collidable_objects
        collidable_objects = []

    def find_by_tag(tag):
        """Find a collision object based on its tag property."""
        for obj in collidable_objects:
            if tag == obj.tag:
                return obj

        return None

    def query_collision(collision_object):
        """
        Check to see if the specified object is colliding with any of the objects currently in the Collision Manager
        Returns the first object we are colliding with if there was a collision and None if no collisions was found
        """
        global collidable_objects
        #Note that we use a Brute Force approach for the time being. It performs horribly under heavy loads, but it meets
        #our needs for the time being.
        for obj in collidable_objects:
            #Make sure we don't check ourself against ourself.
            if obj.obj_id is not collision_object.obj_id:
                if collision_object.is_colliding(obj):
                    #A collision has been detected. Return the object that we are colliding with.
                    return obj

        #No collision was noticed. Return None.
        return None

    def query_all_collisions(collision_object):
        """
        Check for and return the full list of objects colliding with collision_object
        """
        global collidable_objects
        colliding = []
        for obj in collidable_objects:
            #Make sure we don't check ourself against ourself.
            if obj is not collision_object:
                if collision_object.is_colliding(obj):
                    #A collision has been detected. Add the object that we are colliding with.
                    colliding.append(obj)

        return colliding

    def run_brute(self):
        """
        A nightmare if looked at by a performance standpoint, but it gets the job done,
        at least for now.

        Checks everything against everything and handles all collision reactions.
        """
        global collidable_objects
        if self.collision_depth == self.SHALLOW_DEPTH:
            for obj in collidable_objects:
                collision = self.query_collision(obj)
                if collision is not None:
                    #Execute the reactions for both of the colliding objects.
                    obj.collision_response(collision)
                    collision.collision_response(obj)
        elif self.collision_depth == self.DEEP_DEPTH:
            for obj in collidable_objects:
                collisions = self.query_all_collisions(obj)
                for collision in collisions:
                    #Execute the reactions for both of the colliding objects.
                    obj.collision_response(collision)
                    collision.collision_response(obj)


    query_collision = staticmethod(query_collision)
    query_all_collisions = staticmethod(query_all_collisions)
    remove_object = staticmethod(remove_object)
    add_object = staticmethod(add_object)
    find_by_tag = staticmethod(find_by_tag)
    remove_all = staticmethod(remove_all)

    def update(self, milliseconds):
        if self.is_enabled:
            #Use the brute force method to check all objects against all objects.
            self.run_brute()

    def draw(self, milliseconds, surface):
        """Render each of the collision objects onto the specified surface."""
        if self.is_visible:
            global collidable_objects
            for obj in collidable_objects:
                if obj.is_visible:
                    obj.draw(milliseconds, surface)
            super(CollisionManager, self).draw(milliseconds, surface)

class GUIButton(DrawableObj):
    def __init__(self):
        """
        NOTE: This button doesn't display any graphics by itself. Inherit from it to define its behavior.
        """
        #Is the button currently selected by the user?
        self.is_selected = False

        #Is the mouse currently hovering over the button?
        self.is_mouse_hovering = False

        #The button will activate if the mouse is over these bounds.
        self.selection_bounds = pygame.Rect(0,0,0,0)

    def roll_over_action(self):
        """
        rollOverAction is the function that executes when the player moves the mouse (or key) over the button.
        Override this in the inherited class.
        """
        self.is_selected = True
##        print "GUIButton roll over method entered"

    def roll_away_action(self):
        """
        rollAwayAction is the function that executes when the player moves the mouse (or key) away from the button.
        Override this in the inherited class.
        """
        self.is_selected = False
##        print "GUIButton roll away method entered"

    def clicked_action(self):
        """
        ClickedAction is the function that executes when the player clicks the button.
        Override this in the inherited class.
        """
##        print "GUIButton clicked action method entered"
        pass

    def update(self, milliseconds):
        #Check to see if the mouse is hovering over the button. If true, set is_mouse_hovering to true, else, turn it off.
        pos = pygame.mouse.get_pos()
        if self.selection_bounds.collidepoint(pos):
            self.is_mouse_hovering = True
        else:
            self.is_mouse_hovering = False

        super(GUIButton, self).update(milliseconds)

    def draw_debug(self, surface, color = (0, 255, 0)):
        #Draw the selection rectangle onto the surface.
        #TODO: Draw a rectangle onto the surface so the user can see where the bounds are instead of guessing.
        pass

class GUIMenu(DrawableObj):
    def __init__(self):
        super(GUIMenu, self).__init__()
        #The type of input we are currently acceopting. We can only accept one type of input at a time.
        self.input_focus = StateTypes.KEYBOARD

        #The keyboard button that selects the button above the currently selected button.
        self.move_up_button = pygame.K_UP

        #The keyboard button that selects the button below the currently selected button.
        self.move_down_button = pygame.K_DOWN

        #The keyboard button we will querty for clicked events.
        self.select_button = pygame.K_RETURN

        #The mouse button we will query for clicked events.
        self.mouse_select_button = StateTypes.M_LEFT

        #The index of the currently selected button.
        self.current_index = -1

        #Our list of buttons.
        self.gui_buttons = []

    def set_keyboard_focus(self, move_up, move_down, select):
        """
        Set the keyboard as the object that controls the menu.
        move_up is from the pygame.KEYS enum that defines what button causes the menu selection to move up.
        move_down is from the pygame.KEYS enum that defines what button causes the menu selection to move down.
        select is from the pygame.KEYS enum that defines what button causes the button to be selected.
        """
        self.input_focus = StateTypes.KEYBOARD
        self.move_up_button = move_up
        self.move_down_button = move_down
        self.select_button = select

    def set_mouse_focus(self):
        """
        Set the mouse as the object that controls the menu.
        """
        self.input_focus = StateTypes.MOUSE

    def __wrap_index(self):
        """Wraps the current_index to the other side of the menu."""
        if self.current_index < 0:
            self.current_index = len(self.gui_buttons) - 1
        elif self.current_index >= len(self.gui_buttons):
            self.current_index = 0

    def __handle_selections(self, old_index, new_index):
        #Don't perform any deselections or selections if the currently selected button hasn't changed.
        if old_index is not new_index:
            #Deselect the old button
            self.gui_buttons[old_index].roll_away_action()
##            print "Button " + str(old_index) + " deselected."

            #Select the new button.
            self.gui_buttons[new_index].roll_over_action()
##            print "Button " + str(new_index) + " selected."

    def move_up(self):
        """
        Try to select the button above the currently selected one.
        If a button is not there, wrap down to the bottom of the menu and select the last button.
        """
        old_index = self.current_index
        self.current_index -= 1
        self.__wrap_index()
        self.__handle_selections(old_index, self.current_index)

    def move_down(self):
        """
        Try to select the button under the currently selected one.
        If a button is not there, wrap down to the top of the menu and select the first button.
        """
        old_index = self.current_index
        self.current_index += 1
        self.__wrap_index()
        self.__handle_selections(old_index, self.current_index)

    def __update_mouse(self, milliseconds):
        """
        Use the mouse to control selection of the buttons.
        """
        for button in self.gui_buttons:
            was_hovering = button.is_mouse_hovering
            button.update(milliseconds)

            #Provides capibilities for the mouse to select a button if the mouse is the focus of input.
            if was_hovering == False and button.is_mouse_hovering:
                #The user has just moved the mouse over the button. Set it as active.
                old_index = self.current_index
                self.current_index = self.gui_buttons.index(button)
                self.__handle_selections(old_index, self.current_index)
            elif Ragnarok.get_world().Mouse.is_clicked(self.mouse_select_button) and button.is_mouse_hovering:
                #The main mouse button has just depressed, click the current button.
                button.clicked_action()

    def __update_keyboard(self, milliseconds):
        """
        Use the keyboard to control selection of the buttons.
        """
        if Ragnarok.get_world().Keyboard.is_clicked(self.move_up_button):
            self.move_up()
        elif Ragnarok.get_world().Keyboard.is_clicked(self.move_down_button):
            self.move_down()
        elif Ragnarok.get_world().Keyboard.is_clicked(self.select_button):
            self.gui_buttons[self.current_index].clicked_action()

        for button in self.gui_buttons:
            button.update(milliseconds)


    def update(self, milliseconds):
        #Set the default selected button. This is necessary to to get correct behavior when the menu first starts running.
        if self.current_index == -1:
            self.current_index = 0
            self.gui_buttons[self.current_index].roll_over_action()

        #Call the correct update method depending on what the user has the focus currently set as.
        if self.input_focus == StateTypes.KEYBOARD:
            self.__update_keyboard(milliseconds)
        elif self.input_focus == StateTypes.MOUSE:
            self.__update_mouse(milliseconds)

        super(GUIMenu, self).update(milliseconds)

    def draw(self, milliseconds, surface):
        for button in self.gui_buttons:
            button.draw(milliseconds, surface)
        super(GUIMenu, self).draw(milliseconds, surface)

class MouseState(object):
    """A structure that contains the states of our mouse buttons."""
    def __init__(self):
        #Stores the pressed value of the left mouse button.
        self.left_pressed = False

        #Stores the pressed value of the middle mouse button.
        self.middle_pressed = False

        #Stores the pressed value of the right mouse button.
        self.right_pressed = False

        #The location of the mouse pointer on the screen.
        self.mouse_pos = Vector2()

    def copy(self):
        """Create a copy of this MouseState and return it."""
        ms = MouseState()
        ms.left_pressed = self.left_pressed
        ms.middle_pressed = self.middle_pressed
        ms.right_pressed = self.right_pressed
        ms.mouse_pos = self.mouse_pos
        return ms

    def query_state(self, StateType):
        """
        Is a button depressed?
        True if a button is pressed, false otherwise.
        """
        if(StateType == StateTypes.M_LEFT):
            #Checking left mouse button
            return self.left_pressed
        elif(StateType == StateTypes.M_MIDDLE):
            #Checking middle mouse button
            return self.middle_pressed
        elif(StateType == StateTypes.M_RIGHT):
            #Checking right mouse button
            return self.right_pressed

class Mouse(UpdatableObj):
    """Wraps around Pygame's Mouse module to provide some more information to the user, such as what buttons were pressed on the previous frame."""
    def __init__(self):
        super(Mouse, self).__init__()
        self.current_mouse_state = MouseState()
        self.previous_mouse_state = MouseState()

    def is_down(self, MouseStateType):
        """Check to see if a button is down."""
        return self.current_mouse_state(MouseStateType)

    def is_up(self, MouseStateType):
        """Check to see if a button is up."""
        return not self.current_mouse_state(MouseStateType)

    def is_clicked(self, MouseStateType):
        """
        Did the user depress and release the button to signify a click?
        MouseStateType is the button to query. Values found under StateTypes.py
        """
        return self.previous_mouse_state.query_state(MouseStateType) and (not self.current_mouse_state.query_state(MouseStateType))

    def update(self, milliseconds):
        #Update our mouse states.
        self.previous_mouse_state = self.current_mouse_state.copy()

        #Get the mouse buttons currently down.
        mouse1, mouse2, mouse3 = pygame.mouse.get_pressed()
        self.current_mouse_state.left_pressed = mouse1
        self.current_mouse_state.middle_pressed = mouse2
        self.current_mouse_state.right_pressed = mouse3
        self.current_mouse_state.mouse_pos = pygame.mouse.get_pos

        super(Mouse, self).update(milliseconds)

class KeyState(object):
    def __init__(self):
        #Contains a reference to all pressed status of all the keys
        self.key_states = []

    def copy(self):
        new_keys = []
        for key in self.key_states:
            new_keys.append(key)
        state_cpy = KeyState()
        state_cpy.key_states = new_keys
        return state_cpy

    def query_state(self, key):
        """
        Query the state of a key. True if the key is down, false if it is up.
        key is a pygame key.
        """
        return self.key_states[key]

class Keyboard(UpdatableObj):
    def __init__(self):
        super(Keyboard, self).__init__()
        self.current_state = KeyState()
        self.previous_state = KeyState()
        self.current_state.key_states = pygame.key.get_pressed()

    def is_down(self, key):
        return self.current_state.query_state(key)

    def is_up(self, key):
        return not self.current_state.query_state(key)

    def is_clicked(self, key):
        return self.previous_state.query_state(key) and (not self.current_state.query_state(key))

    def is_any_down(self):
        """Is any button depressed?"""
        for key in range(len(self.current_state.key_states)):
            if self.is_down(key):
                return True
        return False

    def is_any_clicked(self):
        """Is any button clicked?"""
        for key in range(len(self.current_state.key_states)):
            if self.is_clicked(key):
                return True
        return False

    def update(self, milliseconds):
        keys = pygame.key.get_pressed()
        self.previous_state = self.current_state.copy()
        self.current_state.key_states = keys
        super(Keyboard, self).update(milliseconds)

class TileMapObject(Sprite):
    """Represents an object to be placed in the tile map."""
    def __init__(self, tileMap):
        super(TileMapObject, self).__init__()
        #Is the object allowed to interact with warps?
        self.can_warp = False
        self.tile_map = tileMap


class Warp(Sprite):
    """Allows the player to warp to a different level or to a different location on the current level."""
    def __init__(self, map_association):
        super(Warp, self).__init__()
        #The map this warp is associated with.
        self.map_association = map_association

        #The warp the player should come out from when entering this warp.
        self.exitWarp = None

        self.bounding_box = AABoundingBox(self.warp_object)
        Ragnarok.get_world().CollisionMgr.add_object(self.bounding_box)

    def warp_object(self, tileMapObj):
        """Warp the tile map object from one warp to another."""
        print "Collision"
        if tileMapObj.can_warp:
            #Check to see if we need to load a different tile map
            if self.map_association != self.exitWarp.map_association:
                #Load the new tile map.
                TileMapManager.load(exitWarp.map_association)

            tileMapObj.parent.coords = self.exitWarp.coords

class Tile(DrawableObj):
    def __init__(self, binding_type = []):
        """
        binding_type is an array of strings telling us what type of tile this is.
        For example, we could pass in a string "DamageTile". When a character collides with a set of tiles,
        we could check the list of tiles they touched to see if any are a "DamageTile". If so we can cause damage
        to the character.

        We could also specify ["DamageTile", "Walkthrough"], which we could interpert as allowing the character
        to pass through the tile, but causing damage to them while they do so.
        """
        super(Tile, self).__init__()
        self.binding_type = [binding_type]
        self.coords = Vector2()
        self.source = pygame.Rect(0, 0, 0, 0)

    def generate_bbox(self, collision_function = None, tag = ""):
        """Create a bounding box around this tile so that it can collide with objects not included in the TileManager"""
        boundingBox = AABoundingBox(None, collision_function, tag)
        CollisionManager.add_object(boundingBox)

    def draw(self, milliseconds, surface):
        """Draw the image to the specified surface."""
        surface.blit(self.image, self.coords, self.source, special_flags = 0)

class TileMap(DrawableObj):
    def __init__(self, spritesheet, tile_bindings, tile_map, collision_map, object_map, object_ary, level_name):
        """
        spritesheet is the spritesheet by which we will pull our sprites from.
        tile_bindings is used to give our tiles game-implementation-specific meaning.
        tile_map is our file that defines what tiles should display and where they should display at.
        collision_map defines what tiles are solid or not.
        object_map allows us to place objects into the map (such as enemies) by pulling thier instance data from the object_ary.
        object_ary is an array of initalization functions. These functions are used to create new objects and add them to the tile map.
        The object_ary functions should accept a parameter of type TileMap. This is used to pass to the TileMapObjects.
        """
        super(TileMap, self).__init__(self)
        self.is_static = True
        self.tile_bindings = tile_bindings
        self.spritesheet = spritesheet

        self.tilemap_path = tile_map
        self.collisionmap_path = collision_map
        self.objectmap_path = object_map

        self.tilemap = ""
        self.collisionmap = ""
        self.objectmap = ""

        self.object_ary = object_ary
        self.level_name = level_name

        #The location the player starts at on the tile map.
        self.start_location = Vector2()

        #Our tiles that will be rendered onto the screen.
        self.tiles = []

        #The objects associated with the tile map.
        self.objects = []

        self.drawn_rects = []

        #The (x, y) size of the tilemap in tiles.
        self.size_in_tiles = Vector2()

        #The (x, y) size of the tilemap in pixels.
        self.size_in_pixels = Vector2()

    def __is_number(self, character):
        val = ord(character)
        if val >= 48 and val <= 57:
            return True

        return False

    def parse_tilemap(self):
        fs = open(self.tilemap_path, "r")
        self.tilemap = fs.readlines()
        fs.close()

        current_obj_line = ""
        current_col_line = ""
        tile_pos = Vector2(0, 0)
        increment_x = self.spritesheet[0].width
        increment_y = self.spritesheet[0].height
        self.size_in_tiles = Vector2()
        self.size_in_pixels = Vector2()
        y_index = 0
        x_index = 0
        for line in self.tilemap:
            #Ignore comments
            if line[0] is "#":
                continue

            row = []
            x_index = 0
            for char in line:
                if char is "":
                    continue
                #An empty character is the same as index 0
                elif char is " ":
                    char = 0
                elif not self.__is_number(char):
                    continue

                index = int(char)
                new_tile = Tile()

                #Grab the cell from the spritesheet and set it as the tile's rendering bounds
                new_tile.source = self.spritesheet[index]
                new_tile.coords = tile_pos.copy()

                #Add the tile to our tile list.
                row.append(new_tile)

                #Set the location where the next tile will render.
                tile_pos.X += increment_x

                x_index += 1

            self.tiles.append(row)
            tile_pos.X = 0
            tile_pos.Y += increment_y
            y_index += 1

        self.size_in_tiles.X = x_index - 1
        self.size_in_tiles.Y = y_index - 1
        self.size_in_pixels.X = self.size_in_tiles.X * increment_x
        self.size_in_pixels.Y = self.size_in_tiles.Y * increment_y

    def parse_collisions(self):
        """Parses the collision map and sets the tile states as necessary."""
        fs = open(self.collisionmap_path, "r")
        self.collisionmap = fs.readlines()
        fs.close()

        x_index = 0
        y_index = 0
        for line in self.collisionmap:
            if line[0] is "#":
                continue
            for char in line:
                if char is "":
                    continue
                #An empty character is the same as collision type 0
                elif char is " ":
                    char = "0"
                elif char is "s":
                    #Placing the start location
                    self.start_location = self.tiles_to_pixels(Vector2(x_index, y_index))
                    char = "0"
                elif not (char in self.tile_bindings):
                    continue

                self.tiles[y_index][x_index].binding_type = self.tile_bindings[char]
                x_index += 1

            x_index = 0
            y_index += 1

    def parse_objects(self):
        fs = open(self.objectmap_path, "r")
        self.objectmap = fs.readlines()
        fs.close()

        x_index = -1
        y_index = 0
        for line in self.objectmap:
            if line[0] is "#" or line[0] is "\n" or line[0] is "":
                continue
            for char in line:
                x_index += 1
                if char is "":
                    continue
                #An empty character is the same as object type 0
                #Exit, as a value of 0 does not represent any objects
                if char is " " or char is "0":
                    continue
                elif not self.__is_number(char):
                    continue

                #Instantiate the desired object by calling the instantiation method.
                #Subtract by 1 because we reserve 0 as a special None slot
                index = int(char) - 1
                obj = self.object_ary[index](self)
                obj.coords = self.tiles_to_pixels(Vector2(x_index, y_index))
                print obj.coords
                self.objects.append(obj)

            x_index = -1
            y_index += 1

    def pixels_to_tiles(self, coords, clamp=True):
        """
        Convert pixel coordinates into tile coordinates.
        clamp determines if we should clamp the tiles to ones only on the tilemap.
        """
        tile_coords = Vector2()
        tile_coords.X = int(coords[0]) / self.spritesheet[0].width
        tile_coords.Y = int(coords[1]) / self.spritesheet[0].height

        if clamp:
            tile_coords.X, tile_coords.Y = self.clamp_within_range(tile_coords.X, tile_coords.Y)

        return tile_coords

    def clamp_within_range(self, x, y):
        """
        Clamp x and y so that they fall within range of the tilemap.
        """
        x = int(x)
        y = int(y)

        if x < 0:
            x = 0
        if y < 0:
            y = 0
        if x > self.size_in_tiles.X:
            x = self.size_in_tiles.X
        if y > self.size_in_tiles.Y:
            y = self.size_in_tiles.Y

        return x, y

    def tiles_to_pixels(self, tiles):
        """Convert tile coordinates into pixel coordinates"""
        pixel_coords = Vector2()
        pixel_coords.X = tiles[0] * self.spritesheet[0].width
        pixel_coords.Y = tiles[1] * self.spritesheet[0].height
        return pixel_coords

    def is_valid_tile(self, x, y):
        """Check to see if the requested tile is part of the tile map."""
        x = int(x)
        y = int(y)

        if x < 0:
            return False
        if y < 0:
            return False
        if x > self.size_in_tiles.X:
            return False
        if y > self.size_in_tiles.Y:
            return False

        return True

    def grab_collisions(self, coords):
        """
        Return all the tiles the position is colliding with.
        Tiles returned in this order:
            Top Left
            Top Right
            Bottom Left
            Bottom Right
        """
        collisions = []
        top_left = self.pixels_to_tiles(coords)
        collisions.append(self.tiles[top_left.Y][top_left.X])

        #Check to see if we are perfectly aligned with a tile
        tile_width = int(self.spritesheet[0].width)
        tile_height = int(self.spritesheet[0].width)
        x_aligned = int((coords.X)) & (tile_width - 1)
        y_aligned = int((coords.Y)) & (tile_height - 1)

        if x_aligned > 0:
            #Append the top right tile touching the rectangle
            if self.is_valid_tile(top_left.X + 1, top_left.Y):
                collisions.append(self.tiles[top_left.Y][top_left.X + 1])

        if y_aligned > 0:
            #Append the bottom left tile touching the rectangle
            if self.is_valid_tile(top_left.X, top_left.Y + 1):
                collisions.append(self.tiles[top_left.Y + 1][top_left.X])

            if x_aligned > 0:
                if self.is_valid_tile(top_left.X + 1, top_left.Y + 1):
                    collisions.append(self.tiles[top_left.Y + 1][top_left.X + 1])

        return collisions

    def draw(self, milliseconds, surface):
        """Draw out the tilemap."""
        self.drawn_rects = []
        cam = Ragnarok.get_world().Camera
        cX, cY, cXMax, cYMax = cam.get_cam_bounds()

        #Draw out only the tiles visible to the camera.
        start_pos = self.pixels_to_tiles( (cX, cY) )
        start_pos -= Vector2(1, 1)
        end_pos = self.pixels_to_tiles( (cXMax, cYMax) )
        end_pos += Vector2(1, 1)

        start_pos.X, start_pos.Y = self.clamp_within_range(start_pos.X, start_pos.Y)
        end_pos.X, end_pos.Y = self.clamp_within_range(end_pos.X, end_pos.Y)

        cam_pos = cam.get_world_pos()
        for x in range(start_pos.X, end_pos.X + 1):
            for y in range(start_pos.Y, end_pos.Y + 1):
                tile = self.tiles[y][x]
                translate_posX = tile.coords.X - cam_pos.X
                translate_posY = tile.coords.Y - cam_pos.Y
                surface.blit(self.spritesheet.image, (translate_posX, translate_posY), tile.source, special_flags = 0)

class TileMapManager(object):
    """
    Manages our various tile maps.
    Allows us to load and unload maps.
    """
    __tile_maps = {}
    active_map = None
    def __init__(self):
        global __tile_maps
        #Our dictionary of tile maps.
        __tile_maps = {}

        #The map that is currently displaying on the screen.
        active_map = None

    def add_map(mapObj):
        """Add a map to the map manager."""
        global __tile_maps
        __tile_maps[mapObj.level_name] = mapObj

    add_map = staticmethod(add_map)

    def unload():
        """Unload the current map from the world."""
        global __tile_maps
        global active_map
        if TileMapManager.active_map != None:
            world = Ragnarok.get_world()

            for obj in TileMapManager.active_map.objects:
                world.remove_obj(obj)
            world.remove_obj(TileMapManager.active_map)

    unload = staticmethod(unload)

    def load(name):
        """Parse the tile map and add it to the world."""
        global __tile_maps
        #Remove the current map.
        TileMapManager.unload()

        TileMapManager.active_map = __tile_maps[name]
        TileMapManager.active_map.parse_tilemap()
        TileMapManager.active_map.parse_collisions()
        TileMapManager.active_map.parse_objects()

        world = Ragnarok.get_world()
        world.add_obj(TileMapManager.active_map)

        for obj in TileMapManager.active_map.objects:
            world.add_obj(obj)

    load = staticmethod(load)

class CameraUpdater(UpdatableObj):
    """Provides a class that updates the camera."""
    def __init__(self):
        super(CameraUpdater, self).__init__()

    def update(self, milliseconds, camera, desiredPan):
        pass

class SpringCameraUpdater(CameraUpdater):
    def __init__(self):
        super(SpringCameraUpdater, self).__init__()
        self.rest_length = 0.0
        self.damp = .05
        self.spring_stiffness = 1.75
        self.velocity = Vector2.zero()

    def update(self, milliseconds, camera):
        #Calculate and apply our spring equation to the camera.
        springVec = camera.desired_pan - camera.pan
        currentLength = springVec.length()
        displacement = currentLength - self.rest_length

        #Calculate the direction in which the spring should be moving.
        if displacement > 0:
            springDirection = springVec / displacement
        else:
            springDirection = Vector2.zero()

        force = springDirection * (displacement * self.spring_stiffness)
        self.velocity += force
        self.velocity *= self.damp
        camera.pan += self.velocity

class Camera(UpdatableObj):
    def __init__(self):
        super(Camera, self).__init__()

        #The center of the screen is the origin of the camera.
        self.world_center = Vector2(0, 0)
        self.pan = self.world_center
        self.desired_pan = self.pan
        self.previous_pos = self.pan

        #The extent to which the camera is allowed to move.
        #None indicates that there are no constraints.
        self.camera_bounds = None

        #The class that controls how the camera updates. Default is SpringCameraUpdater()
        self.update_handeler = SpringCameraUpdater()

        #Contains the visible portions of the camera.
        self.view_bounds = pygame.Rect(0, 0, 0, 0)
        self.update_order = 50000

    def get_world_pos(self):
        """Get the position of the camera in world coordinates."""
        return self.pan - self.world_center

    def get_movement_delta(self):
        """Get the amount the camera has moved since get_movement_delta was last called."""
        pos = self.pan - self.previous_pos
        self.previous_pos = Vector2(self.pan.X, self.pan.Y)
        return pos

    def Reset(self):
        """Reset the camera back to its defaults."""
        self.pan = self.world_center
        self.desired_pan = self.pos

    def check_bounds(self):
        """Make sure the camera is not outside if its legal range."""
        if not(self.camera_bounds == None):
            if self.__pan.X < self.camera_bounds.Left:
                self.__pan[0] = self.camera_bounds.Left

            if self.__pan.X > self.camera_bounds.Right:
                self.__pan[0] = self.camera_bounds.Right

            if self.__pan.Y < self.camera_bounds.Top:
                self.__pan[1] = self.camera_bounds.Top

            if self.__pan.Y > self.camera_bounds.Bottom:
                self.__pan[1] = self.camera_bounds.Bottom

    def get_cam_bounds(self):
        """Return the bounds of the camera in x, y, xMax, and yMax format."""
        world_pos = self.get_world_pos()
        screen_res = Ragnarok.get_world().get_backbuffer_size() * .5
        return (self.pan.X - screen_res.X), (self.pan.Y - screen_res.Y), (self.pan.X + screen_res.X), (self.pan.Y + screen_res.Y)

    def update_view_bounds(self):
        """Update the camera's view bounds."""
        self.view_bounds.left = self.pan.X - self.world_center.X
        self.view_bounds.top = self.pan.Y - self.world_center.Y
        self.view_bounds.width = self.world_center.X * 2
        self.view_bounds.height = self.world_center.Y * 2

    def update(self, milliseconds):
        self.update_handeler.update(milliseconds, self)
        self.check_bounds()
        self.update_view_bounds()
        super(Camera, self).update(milliseconds)

class World(object):
    def __init__(self):
        #The color we will use to clear the screen with
        self.clear_color = (0, 0, 0)

        #Init the display modes that we can use.
        self.display_modes = pygame.display.list_modes()
        self.__backbuffer = pygame.surface.Surface((0,0))

        #A list of the sprites in our world that are update only
        self.__up_objects = []

        #A list of the sprites in our world that draw
        self.__draw_objects = []

        #Do we need to sort our list of updatable objects?
        self.__do_need_sort_up = False

        #Do we need to sort our list of drawable objects?
        self.__do_need_sort_draw = False

        #Create the core components of our engine.
        #This allows them to be easily accessed by simply going to world.Mouse, or world.CollisionMgr, etc
        self.Mouse = Mouse()
        self.Keyboard = Keyboard()
        self.CollisionMgr = CollisionManager()
        self.Camera = Camera()
        self.TileMapMgr = TileMapManager()

        #Add our core components to the world.
        self.add_obj(self.Mouse)
        self.add_obj(self.CollisionMgr)
        self.add_obj(self.Keyboard)
        self.add_obj(self.Camera)

    def get_backbuffer(self):
        return self.__backbuffer

    def set_backbuffer(self, preferred_backbuffer_size, flags = 0):
        """Create the backbuffer for the game."""
        if not(isinstance(preferred_backbuffer_size, Vector2)):
            raise ValueError("preferred_backbuffer_size must be of type Vector2")

        self.__backbuffer = pygame.display.set_mode(preferred_backbuffer_size, flags)
        self.Camera.world_center = preferred_backbuffer_size / 2.0

    backbuffer = property(get_backbuffer, set_backbuffer)

    def set_display_at_native_res(self, should_be_fullscreen = True):
        """Sets the resolution to the display's native resolution. Sets as fullscreen if should_be_fullscreen is true."""
        #Loop through all our display modes until we find one that works well.
        for mode in self.display_modes:
            color_depth = pygame.display.mode_ok(mode)
            if color_depth is not 0:
                if should_be_fullscreen:
                    should_fill = pygame.FULLSCREEN
                else:
                    should_fill = 0

                self.backbuffer = pygame.display.set_mode(mode, should_fill, color_depth)
                break

    def pixel_to_screen(self, pixelPos):
        """Normalize a pixel position into [0, 0] through [1, 1] coordinates."""
        return Vector2.component_div(pixelPos, self.get_backbuffer_size())

    def screen_to_pixel(self, screenPos):
        """Convert [0, 0] - [1, 1] screen coords into pixel coordinates."""
        return Vector2.component_mul(screenPos, self.get_backbuffer_size())

    def get_backbuffer_size(self):
        """Get the width and height of the backbuffer as a Vector2."""
        vec = Vector2()
        vec.X = self.backbuffer.get_width()
        vec.Y = self.backbuffer.get_height()
        return vec

    def clear_backbuffer(self):
        """Clear the backbuffer"""
        self.backbuffer.fill(self.clear_color)

    def add_obj(self, obj):
        if isinstance(obj, DrawableObj):
            #Add to both the draw and update lists
            self.__up_objects.append(obj)
            self.__draw_objects.append(obj)
            self.__do_need_sort_draw = True
            self.__do_need_sort_up = True
        elif isinstance(obj, UpdatableObj):
            #The object does not draw, add only to the update lists
            self.__up_objects.append(obj)
            self.__do_need_sort_up = True

    def remove_obj(self, obj):
        try:
            if isinstance(obj, DrawableObj):
                #Remove from both the draw and update lists
                obj.is_in_world = False
                self.__draw_objects.remove(obj)
                self.__up_objects.remove(obj)
            elif isinstance(obj, UpdatableObj):
                #Remove from the update list only
                obj.is_in_world = False
                self.__up_objects.remove(obj)
        except:
            print "Ragnarok Says: Object with ID # " + str(obj.obj_id) + " could not be found in the World collection. Skipping over..."

    def find_obj_by_tag(self, tag):
        """Search through all the objects in the world and return the first instance whose tag matches the specified string."""
        for obj in self.__up_objects:
            if obj.tag == tag:
                return obj

        for obj in self.__draw_objects:
            if obj.tag == tag:
                return obj

        return None

    def remove_by_tag(self, tag):
        """
        Remove the first encountered object with the specified tag from the world.
        Returns true if an object was found and removed.
        Returns false if no object could be removed.
        """
        obj = self.find_obj_by_tag(tag)
        if obj != None:
            self.remove_obj(obj)
            return True

        return False

    def remove_all(self, tag):
        """Remove all objects with the specified tag from the world."""
        while(self.remove_by_tag(tag)): pass

    def __draw_cmp(self, obj1, obj2):
        """Defines how our drawable objects should be sorted"""
        if obj1.draw_order > obj2.draw_order:
            return 1
        elif obj1.draw_order < obj2.draw_order:
            return -1
        else:
            return 0

    def __up_cmp(self, obj1, obj2):
        """Defines how our updatable objects should be sorted"""
        if obj1.update_order > obj2.update_order:
            return 1
        elif obj1.update_order < obj2.update_order:
            return -1
        else:
            return 0

    def __sort_up(self):
        """Sort the updatable objects according to ascending order"""
        if self.__do_need_sort_up:
            self.__up_objects.sort(self.__up_cmp)
            self.__do_need_sort_up = False

    def __sort_draw(self):
        """Sort the drawable objects according to ascending order"""
        if self.__do_need_sort_draw:
            self.__draw_objects.sort(self.__draw_cmp)
            self.__do_need_sort_draw = False

    def update(self, milliseconds):
        """Updates all of the objects in our world."""
        self.__sort_up()
        for obj in self.__up_objects:
            obj.update(milliseconds)

    def draw(self, milliseconds):
        """Draws all of the objects in our world."""
        cam = Ragnarok.get_world().Camera
        camPos = cam.get_world_pos()
        self.__sort_draw()
        self.clear_backbuffer()
        for obj in self.__draw_objects:
            #Check to see if the object is visible to the camera before doing anything to it.
            if obj.is_static or obj.is_visible_to_camera(cam):
                #Offset all of our objects by the camera offset.
                old_pos = obj.coords
                xVal = obj.coords.X - camPos.X
                yVal = obj.coords.Y - camPos.Y
                obj.coords = Vector2(xVal, yVal)
                obj.draw(milliseconds, self.backbuffer)
                obj.coords = old_pos