# Intelligent-printer-development-based-on-Aerotech-gantry
In this project, our team is customizing the Aerotech AGS15000HL gantry to function as an intelligent 3D printing system.

![Aerotech_system](https://github.com/user-attachments/assets/c9f76d6c-af07-4c69-898e-6fa56399767d)

Since the gantry's control can be realized through either Automation Studio (Aerotech’s proprietary control software) or APIs (Python, C, Java), there are typically two methods for integrating external hardware:

1. **Controlling hardware via the additional interface on Aerotech**: The Aerotech printer is equipped with an extra interface, allowing for the connection of external hardware, which can be controlled through commands in Automation Studio. Early versions of customization often adopted this approach. Its main advantage is the ease of programming using Aerotech's commercial software, which offers fast response times and a straightforward implementation. However, this approach limits the number of hardware components to the available interface ports, making the development of more complex functionalities challenging. We used a similar strategy for customizing another project involving the Makergear M2 printer.

2. **Controlling the gantry and hardware via Python**: The Aerotech gantry provides interfaces compatible with common coding languages like Python, C, and Java. Using Python, we can control the gantry’s movements while also managing external hardware through Serial communication with an Arduino board. The Arduino, in turn, controls its connected hardware components. The key advantage of this method is the high degree of freedom in development, with no theoretical limit to the number of connected devices. Additionally, Python’s extensive libraries, particularly in machine learning, facilitate the development of a smarter printer. The downside, however, is that this method requires multi-threaded programming, which is more complex, and the serial communication introduces slight latency. For greater flexibility and ease in future developments, we opted for the second approach.

The project is structured as follows: Initially, two pneumatic control systems will be set up to achieve basic DIW (Direct Ink Writing) printing functionality and validate the feasibility of the Controlling the gantry and hardware via Python approach. Subsequently, new features will be continuously added based on the requirements of various research projects within the group. The ongoing projects include, but are not limited to:

1. **DIW Printing Material Heating System**: This system involves integrating a heating mechanism to regulate the temperature of the materials being extruded in the DIW process.

2. **Low-Temperature Chamber for DIW Printing of Biomaterials**: A specialized low-temperature environment designed for the printing of biomaterials that require strict temperature control.

3. **UV Curing System for DIW Printhead**: A UV light-based curing system attached to the printhead to solidify materials during or after the printing process.

4. **Volumetric Extrusion Material Dispensing System Based on Motor, Worm Gear, and Piston**: A precise volumetric extrusion system using mechanical components like motors, worm gears, and pistons to control material flow.

5. **Volumetric Extrusion Printhead Based on Motor and Piston**: This printhead employs a motor-driven piston mechanism to control the material extrusion in volumetric extrusion processes.

6. **Nozzle Rotation System Based on Motor and Air Slip Ring**: A nozzle system capable of rotating, controlled by a motor and equipped with an air slip ring for rotational movements.

7. **Automated Calibration System Based on Camera and Computer Vision**: A vision-based system that uses camera feedback and computer vision algorithms to automatically calibrate the 3D printer.

8. **Real-Time Defects Monitoring and Print Parameter Adjustment System Based on Camera and Computer Vision**: This system monitors defects in real-time during the printing process using computer vision and adjusts printing parameters automatically to mitigate defects.

This phased development approach ensures flexibility and allows for the addition of multiple complex functionalities that cater to the evolving needs of advanced research applications.

**Document overview**:

