import numpy as np
import OpenGL.GL as gl
import OpenGL.GLUT as glut
import OpenGL.GLU as glu

# Configurações iniciais
width, height = 800, 600

def setup():
    gl.glClearColor(0.0, 0.0, 0.0, 1.0)
    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    glu.gluPerspective(45, width / height, 0.1, 100.0)
    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glLoadIdentity()

def draw_cube():
    gl.glBegin(gl.GL_QUADS)
    
    # Front Face
    gl.glColor3f(1.0, 0.0, 0.0)
    gl.glVertex3f(-1.0, -1.0,  1.0)
    gl.glVertex3f( 1.0, -1.0,  1.0)
    gl.glVertex3f( 1.0,  1.0,  1.0)
    gl.glVertex3f(-1.0,  1.0,  1.0)
    
    # Back Face
    gl.glColor3f(0.0, 1.0, 0.0)
    gl.glVertex3f(-1.0, -1.0, -1.0)
    gl.glVertex3f(-1.0,  1.0, -1.0)
    gl.glVertex3f( 1.0,  1.0, -1.0)
    gl.glVertex3f( 1.0, -1.0, -1.0)
    
    # Top Face
    gl.glColor3f(0.0, 0.0, 1.0)
    gl.glVertex3f(-1.0,  1.0, -1.0)
    gl.glVertex3f(-1.0,  1.0,  1.0)
    gl.glVertex3f( 1.0,  1.0,  1.0)
    gl.glVertex3f( 1.0,  1.0, -1.0)
    
    # Bottom Face
    gl.glColor3f(1.0, 1.0, 0.0)
    gl.glVertex3f(-1.0, -1.0, -1.0)
    gl.glVertex3f( 1.0, -1.0, -1.0)
    gl.glVertex3f( 1.0, -1.0,  1.0)
    gl.glVertex3f(-1.0, -1.0,  1.0)
    
    # Right face
    gl.glColor3f(1.0, 0.0, 1.0)
    gl.glVertex3f( 1.0, -1.0, -1.0)
    gl.glVertex3f( 1.0,  1.0, -1.0)
    gl.glVertex3f( 1.0,  1.0,  1.0)
    gl.glVertex3f( 1.0, -1.0,  1.0)
    
    # Left Face
    gl.glColor3f(0.0, 1.0, 1.0)
    gl.glVertex3f(-1.0, -1.0, -1.0)
    gl.glVertex3f(-1.0, -1.0,  1.0)
    gl.glVertex3f(-1.0,  1.0,  1.0)
    gl.glVertex3f(-1.0,  1.0, -1.0)
    
    gl.glEnd()

def display():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    gl.glLoadIdentity()
    glu.gluLookAt(0.0, 0.0, 5.0,  0.0, 0.0, 0.0,  0.0, 1.0, 0.0)

    # Draw the cube
    draw_cube()

    glut.glutSwapBuffers()

def reshape(width, height):
    gl.glViewport(0, 0, width, height)
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    glu.gluPerspective(45, width / height, 0.1, 100.0)
    gl.glMatrixMode(gl.GL_MODELVIEW)

def main():
    glut.glutInit()
    glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGB | glut.GLUT_DEPTH)
    glut.glutInitWindowSize(width, height)
    glut.glutCreateWindow(b'OpenGL Clipping Example')
    
    setup()
    
    glut.glutDisplayFunc(display)
    glut.glutReshapeFunc(reshape)
    
    glut.glutMainLoop()

if __name__ == "__main__":
    main()
