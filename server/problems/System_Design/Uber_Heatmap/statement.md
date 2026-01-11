# Uber Driver Heatmap

## 🚗 Problem Statement
You are a Staff Software Engineer at Uber. You need to build a subsystem to generate a **heat map of Uber drivers** in a city and display this data in an **internal dashboard** for an analytics team.

You must handle two specific scenarios:
1.  **Near Real-Time:** The dashboard displays the heatmap for the **past 20 minutes**.
2.  **Historical (Batch):** The dashboard displays heatmap data after 24 hours, **bucketized by the hour**.

## 🛑 Constraints & Assumptions
*   **Scale:** ~50,000 active drivers in the city.
*   **Frequency:** Each driver pings location every 5 seconds.
*   **Throughput:** ~10,000 events/second (Write-heavy).
*   **Resolution:** Spatial aggregation required (Grid-based, e.g., Google S2 or Uber H3).
*   **Latency:**
    *   Real-time: Seconds to sub-minute latency.
    *   Historical: High latency allowed (24hr lag).

## 🎯 Task
Design the **Ingestion, Processing, Storage, and Serving** layers.
Focus on:
*   Handling high write throughput.
*   Efficient spatial aggregation.
*   Managing state for the 20-minute sliding window.
*   Cost-effective massive long-term storage for historical data.
