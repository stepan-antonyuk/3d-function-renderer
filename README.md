# 3D Function Renderer

## Overview

This project is a **Python3-based 3D function renderer** built using the Pygame library. It allows users to input mathematical functions and visualize them as 3D shapes projected onto a 2D screen. This tool is designed to make understanding and exploring mathematical functions in three dimensions easier and more interactive.  

### Key Features:
- **3D Visualization of Mathematical Functions**: Render mathematical functions in 3D space with customizable parameters.
- **Parameters**: Users can define the range for x and y values and adjust the step size for more control over resolution and detail.
- **Dynamic Perspective**: Includes a camera system to adjust views and explore the rendered function interactively.
- **Modular Design**: Easily extendable for new mathematical functions and additional features.

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
