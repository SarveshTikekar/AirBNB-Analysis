# Airbnb Market & Investment Analysis

A comprehensive business intelligence solution built using **Power BI Project (.pbip)** format and **Tabular Model Definition Language (TMDL)**. This project analyzes multi-city Airbnb listing dynamics, pricing behavior, seasonal occupancy rates, host performance, guest satisfaction ratings, and investment potential across key global markets.

---

## Project Introduction & Problem Statement

### Introduction
The short-term rental market has evolved into a multi-billion dollar ecosystem driven by dynamic pricing algorithms, shifting guest preferences, and localized regulatory environments. For real estate investors, property managers, and hospitality operators, optimizing listing yields, occupancy, and guest satisfaction requires granular market intelligence.

### Problem Statement
Property managers and real estate investors often struggle to extract actionable strategic insights from raw short-term rental datasets. Core challenges include:

*   **Pricing Strategy Optimization:** Balancing base pricing, seasonal rate fluctuations, and cleaning fees to maximize Average Daily Rate (ADR) without sacrificing occupancy.
*   **Occupancy & Revenue Yields:** Identifying peak booking windows and evaluating Revenue per Available Room (RevPAR) across different property types and neighborhoods.
*   **Host Operations & Quality Control:** Assessing host tiering (Superhosts vs. standard hosts), response times, cancellation policies, and guest satisfaction drivers.
*   **Geographic & Investment Targeting:** Mapping high-growth urban hubs and neighborhood clusters to identify high-yield investment opportunities.

This project addresses these challenges by constructing a robust, star-schema-based interactive dashboard system that transforms complex short-term rental data into executive-level visual analytics.

---

## Geographic Coverage

The dashboard incorporates short-term rental data across the following cities and countries:

| Country | Cities |
| :--- | :--- |
| **Australia** | Adelaide, Brisbane, Melbourne, Sydney |
| **Brazil** | Florianopolis, Rio, Salvador, Sao Paulo, Ubatuba |
| **China** | Hong Kong |
| **Egypt** | Cairo, Hurghada |
| **France** | Lyon, Marseille |
| **India** | Bangalore, Delhi, Mumbai |
| **Japan** | Kyoto, Osaka |
| **South Africa** | Cape Town, Johannesburg |
| **Thailand** | Bangkok, Pattaya |
| **United Arab Emirates** | Abu Dhabi, Dubai |
| **United Kingdom** | Birmingham, Edinburgh, London |
| **United States of America** | Los Angeles, Miami, New York |

---

## Key Achievements & Features

The project delivers a developer-friendly, interactive dashboard system built with the PBIP version control standard and TMDL model architecture.

### Implementation Summary

<table>
  <thead>
    <tr>
      <th align="left">Metric Category</th>
      <th align="center">Count</th>
      <th align="left">Highlights / Details</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>Unique DAX Measures</b></td>
      <td align="center"><b>84</b></td>
      <td>Revenue, ADR, RevPAR, TTM & L90D metrics, Occupancy rates, multi-currency conversions, and dynamic selection measures.</td>
    </tr>
    <tr>
      <td><b>Unique Charts & Visualizations</b></td>
      <td align="center"><b>30</b></td>
      <td>Line, Bar, Column, Donut, Scatter, Waterfall, Shape Map, Azure Map, Sparkline KPI cards, and custom HTML content visuals.</td>
    </tr>
    <tr>
      <td><b>Unique Slicers</b></td>
      <td align="center"><b>17</b></td>
      <td>Filtering across City, Listing Type, SuperHost status, Currency, Date, Cancellation Policy, and more.</td>
    </tr>
    <tr>
      <td><b>Star Schema Tables</b></td>
      <td align="center"><b>18</b></td>
      <td>Dimension and fact tables spanning Listings, Calendar Rates, Ratings, Cities, Amenities, Cancellation Policies, and more.</td>
    </tr>
    <tr>
      <td><b>Model Relationships</b></td>
      <td align="center"><b>11</b></td>
      <td>1-to-many and bi-directional relationships enabling seamless cross-filtering across the entire data model.</td>
    </tr>
    <tr>
      <td><b>Dashboard Pages</b></td>
      <td align="center"><b>4</b></td>
      <td>AirBNB Host, Listings, Geographical, and AirBNB Specific dashboards.</td>
    </tr>
  </tbody>
</table>

---

## Data Design / Schema

The data model uses a clean **Star Schema** centered around the `Listings` fact table, with `Calendar Rates` and `Ratings` as supporting fact tables. Dimension tables are linked via `1:*` relationships, enabling seamless cross-filtering and high-performance DAX evaluations.

<!-- Add Star Schema diagram image here -->

---

## Dashboards

### 1. AirBNB Host Dashboard

<!-- Add AirBNB Host Dashboard image here -->

---

### 2. Listings Dashboard

<!-- Add Listings Dashboard image here -->

---

### 3. Geographical Dashboard

<!-- Add Geographical Dashboard image here -->

---

### 4. AirBNB Specific Dashboard

<!-- Add AirBNB Specific Dashboard image here -->

---

## Implementation Videos

<!-- Add implementation video links here -->

---

## References & Links

*   **Data Source:** [AIRROI Data Portal](https://www.airroi.com) — up-to-date, comprehensive Airbnb short-term rental market data.
