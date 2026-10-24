
https://github.com/user-attachments/assets/9c3b4f3c-22c7-4416-ba97-835fb4b64de4
# MayaWaveGenerator
A procedural water-stream generator built with Python in Autodesk Maya. The tool generates a ribbon mesh along a user-selected NURBS curve and animates its surface with procedural wave deformation.


## Features

- **Curve-based generation:** Creates a water-stream mesh following a selected NURBS curve.
- **Procedural mesh construction:** Generates ribbon geometry from sampled curve points and tangents.
- **Animated wave deformation:** Uses sinusoidal functions to create continuous surface motion during timeline playback.
- **Multiple wave frequencies:** Combines waves with different frequencies and speeds to produce more varied ripples.
- **Multiple streams:** Supports generating and animating multiple water streams within the same scene.
- **Procedural material:** Applies a water material with an animated texture to enhance the appearance of flowing water.

## Technical Implementation

The project uses Maya's Python API and `maya.cmds` to create and manipulate geometry, materials, and animation.

Key techniques include:

- Sampling NURBS curves to obtain positions and tangents.
- Generating ribbon mesh vertices and polygon faces.
- Computing surface normals for vertex displacement.
- Applying time-dependent sinusoidal deformation to the mesh.
- Using Maya API event callbacks to update water geometry as the timeline advances.

## Project Structure

- `main.py` — Coordinates water generation, material assignment, and animation setup.
- `curve_sampling.py` — Samples selected curves to obtain points and tangents.
- `water_geometry.py` — Creates the ribbon mesh, computes normals, and updates geometry.
- `water_animation.py` — Implements procedural wave deformation and animated texture movement.
- `water_globals.py` — Stores shared configuration values and animation state.

## Requirements

- Autodesk Maya
- Maya Python environment with `maya.cmds` and `maya.api.OpenMaya`

## Usage

1. Open a Maya scene and create a NURBS curve to define the stream's path.
2. Select the curve.
3. Execute `main.py` in Maya's Python environment.
4. Adjust the configured stream width, sampling, wave amplitude, wavelength, and speed as needed.
5. Play the timeline to preview the animated water surface.

## Future Improvements

- Add a user interface for stream generation and animation controls.
- Improve code organization and animation lifecycle management.
- Add more advanced surface deformation and water-shading techniques.

## Motivation

This project explores procedural modeling and animation in Maya, with an emphasis on using Python to build geometry and create time-dependent effects.&#x20;
