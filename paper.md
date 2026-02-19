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

# Acknowledgements

The author would like to thank the MicroPython community and the maintainers of the Awesome MicroPython list for their recognition and support.