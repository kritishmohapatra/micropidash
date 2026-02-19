---
title: "micropidash: A lightweight, asynchronous web dashboard library for MicroPython"
tags:
  - MicroPython
  - IoT
  - Embedded Systems
  - uasyncio
  - Web Dashboard
  - Real-time Systems
authors:
  - name: Kritish Mohapatra
    orcid: 0009-0001-5279-7918
    affiliation: 1
affiliations:
  - name: Odisha University of Technology and Research, Bhubaneswar, India
    index: 1
date: 2026-02-19
bibliography: paper.bib
---

# Summary

`micropidash` is an open-source, asynchronous web dashboard library intended for MicroPython-based microcontrollers like ESP32 and Raspberry Pi Pico 2 W. This library helps embedded systems display real-time, interactive web dashboards without needing any external servers or cloud services. Using the `uasyncio` library, `micropidash` helps embedded systems run hardware control tasks and web server tasks concurrently, ensuring that the user interface is not blocked by time-critical embedded system tasks.

# Statement of Need

Developers and researchers working on embedded systems may need real-time visualization and control interfaces for sensors and actuators. Current IoT dashboard solutions may depend on external cloud infrastructure, which can cause latency, internet connectivity, and privacy issues. Furthermore, most MicroPython web servers are based on blocking architectures or heavy boilerplate code for frontend development.



`micropidash` overcomes these challenges with a self-contained, lightweight dashboard solution that is fully executed on the microcontroller. The library provides ready-to-use UI elements such as toggles, labels, and progress bars and maintains the state of the device in synchronization with multiple web clients using JSON polling. The library has an asynchronous design that prevents the web interface from interfering with the real-time operations of the hardware.

# Implementation


The library is written in MicroPython and relies on the networking and socket APIs provided by MicroPython to deliver static HTML, CSS, and JavaScript pages as well as a JSON-based data endpoint. The backend holds a dictionary-based state model for all dashboard widgets and updates the client-side views via periodic HTTP polling.

To provide a stable environment for running on devices with limited memory, `micropidash` uses chunked HTTP responses and garbage collection to reduce memory fragmentation. The order of widgets is maintained through alphabetical sorting of the widget identifiers.
# Architecture

`micropidash` is based on a state-driven architecture where the `Dashboard` class serves as a central controller for UI components. The frontend periodically polls the device state through a lightweight `/data` endpoint, and backend operations update widget values asynchronously through `uasyncio`. This architecture enables multiple web clients to monitor and control the embedded system concurrently with low overhead.



The library has been validated on ESP32 and Raspberry Pi Pico 2 W boards and functions properly even in low-memory conditions typical of microcontroller systems.

# State of the Field

In the MicroPython community, web servers are usually implemented with blocking libraries such as `socket` or simple asynchronous wrappers. Current solutions such as `MicroWebSrv2` offer rich functionality but come with a large memory footprint, making them hard to integrate with devices that have very limited RAM, such as the original ESP8266, or with complex control loops running alongside the web server. `micropidash` bridges this gap by providing a minimalist state-driven dashboard instead of a full-fledged web server.

# Software Design

The software is designed around a singleton class named `Dashboard` that handles a list of widget objects. When a user adds a widget (for example, `add_toggle`), the backend marks its state in a global dictionary. The communication protocol follows a REST-lite paradigm where the frontend pulls the entire state dictionary as a JSON object. This makes the synchronization logic straightforward and prevents the microcontroller from having to handle complicated per-client session states.

# Research Impact Statement

`micropidash` is a low-cost, highly efficient tool for researchers in the Physical Sciences and Engineering. It eliminates the requirement for expensive proprietary DAQ (Data Acquisition) systems in basic laboratory setups by allowing real-time visualization directly on microcontrollers. It has already been used in the MicroPython community, as it is included in the **Awesome MicroPython** list.

# AI Usage Disclosure

The author wishes to acknowledge the use of generative AI tools (such as Google Gemini) during the development of this project. AI assistance was used for optimizing certain asynchronous logic in the MicroPython code, improving the documentation of the library, and organizing this paper according to JOSS formatting guidelines. All suggestions produced by the AI were reviewed, tested, and incorporated by the author to ensure technical correctness and system stability.

# Acknowledgements

The author would like to thank the MicroPython community and the maintainers of the Awesome MicroPython list for their recognition and support.