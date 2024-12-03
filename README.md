# 3D Function Renderer

## Overview

This project is a **Python3-based 3D function renderer** built using the Pygame library. It allows users to input mathematical functions and visualize them as 3D shapes projected onto a 2D screen. This tool is designed to make understanding and exploring mathematical functions in three dimensions easier and more interactive.  

### Key Features:
- **3D Visualization of Mathematical Functions**: Render mathematical functions in 3D space with customizable parameters.
- **Parameters**: Users can define the range for x and y values and adjust the step size for more control over resolution and detail.
- **Dynamic Perspective**: Includes a camera system to adjust views and explore the rendered function interactively.
- **Modular Design**: Easily extendable for new mathematical functions and additional features.

---

## Functions

To change function go to ```src/mesh.py``` and find ```black_box``` function.

```python
def black_box(self, x, y):
    return <put some function here>
```

### Examples

Here are some example visualizations created with the 3D Function Renderer:

#### Visualization of \(x^2 - y^2\)
![x^2 - y^2](imgs/Screenshot%202024-12-02%20194112.png)

#### Visualization of \(x^2 + y^2\)
![x^2 + y^2](imgs/Screenshot%202024-12-02%20194240.png)

---

## Grid and Step size

To change grid or/and step size go to ```src/mesh.py``` and find class ```Fun```. Go to its init. Find parameters ```self.minp``` and ```self.maxp```. These are limits for x and y.
For example, ```self.minp = [-2, -3, 0]``` means that x has min limit of -2 and y has a limit of -3, z has no limit doesn't matter the number. To change step size you will need to change ```self.stepx``` and ```self.stepy```. Which will change step size taken in x and y direction.

```python
class Fun(GenericObject):
    def __init__ (self, pos):
        self.minp = [-2,-2,0]
        self.maxp = [2,2,2]
        self.stepx = 0.2
        self.stepy = 0.2

```

### Examples

Here are some example visualizations created with the 3D Function Renderer:

#### Visualization of \(x^2 - y^2\) with self.minp = [-2,-2,0] self.maxp = [2,2,2] self.stepx = 0.8 self.stepy = 0.8
![x^2 - y^2](imgs/Screenshot%202024-12-02%20204608.png)

#### Visualization of \(x^2 - y^2\) with self.minp = [-2,-2,0] self.maxp = [2,2,2] self.stepx = 0.4 self.stepy = 0.4
![x^2 - y^2](imgs/Screenshot%202024-12-02%20194112.png)

#### Visualization of \(x^2 - y^2\) with self.minp = [-2,-2,0] self.maxp = [2,2,2] self.stepx = 0.2 self.stepy = 0.2
![x^2 - y^2](imgs/Screenshot%202024-12-02%20204730.png)

#### Visualization of \(x^2 - y^2\) with self.minp = [0,0,0] self.maxp = [2,2,2] self.stepx = 0.1 self.stepy = 0.1
![x^2 - y^2](imgs/Screenshot%202024-12-02%20204912.png)

---

## Achievements

This project demonstrates the power of combining mathematical computation with basic graphics rendering. **Here are some of the highlights of what was achieved:**

- **Custom 3D Rendering**: Created a 3D-to-2D projection system from scratch, showcasing the rendering process without relying on advanced graphics libraries.
- **Function Visualization**: Successfully visualized complex mathematical functions by generating 3D polygons dynamically based on user-defined inputs.
- **Input Handling**: Enabled users to easily input custom functions and parameters, making the tool flexible for various use cases.
- **Educational Value**: This project serves as a hands-on example for learning basic 3D rendering techniques and working with Pygame for graphical representation.

---

## Known Bugs

While this project successfully achieves its main objectives, there are a few known issues that can be addressed in future iterations. These are minor and do not detract significantly from the functionality or purpose of the tool:  

1. **Polygons Rendered Behind the Camera**: Some polygons are drawn even when they are behind the camera.  
2. **Incorrect Polygon Rendering at Close Camera Proximity**: When the camera is too close to complex shapes, some polygons may be drawn incorrectly.  

Despite these bugs, the renderer is highly functional and provides accurate results for most use cases. These issues are opportunities for further refinement and learning, showcasing the iterative nature of software development.

---

## Installation (for Developers)

```bash
git clone git@github.com:stepan-antonyuk/3d-function-renderer.git
cd 3d-function-renderer
python3 -m venv env
source env/bin/activate
pip install -r requirements
```

## Run

```bash
python3 src/main.py
```

---

## Future Improvements

While the renderer is complete, there are exciting opportunities for further enhancements:
- Implementing clipping algorithms to handle polygons behind the camera.
- Adding a more sophisticated camera system to improve the handling of close-up views.
- Incorporating shading techniques to improve visual clarity and aesthetics.

---

## Sources

This project took inspiration and references from the following source:
- [Simple Python 3D Engine](https://github.com/FinFetChannel/SimplePython3DEngine/tree/main)

---

This project is a great demonstration of combining mathematics, programming, and computer graphics to create a powerful and interactive tool. Contributions and feedback are welcome to make it even better!
