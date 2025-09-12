# 🌤️ Weather Data Pipeline

A comprehensive toolkit for downloading, processing, and combining weather data from the SILO database ([Queensland Government – Long Paddock](https://www.longpaddock.qld.gov.au/)) for weather stations across **NSW, QLD, and VIC**.

## ✨ Features

- 📊 Automated weather station data collection
- 🔄 Seamless data processing and aggregation
- 🗺️ Multi-state coverage (NSW, QLD, VIC)
- 📈 State-level weather metric averages
- 🛠️ Easy-to-use command-line interface

---

## 📊 Data Dictionary

The final `avg_weather_from_date_to_date.csv` file contains the following columns:

| Column | Description |
|--------|-------------|
| `daily_rain` | Daily rainfall (mm) |
| `max_temp` | Maximum temperature (°C) |
| `min_temp` | Minimum temperature (°C) |
| `radiation` | Solar radiation – total incoming downward shortwave radiation on a horizontal surface (MJ/m²) |
| `rh_tmax` | Relative humidity at the time of maximum temperature (%) |
| `rh_tmin` | Relative humidity at the time of minimum temperature (%) |

## 🚀 Getting Started

### Prerequisites

- Python virtual environment
- Stable internet connection
- Access to SILO Point Data API

### 0. Environment Setup

Before running any scripts, activate your virtual environment:

```bash
# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

---

## 📋 Step-by-Step Workflow

### 1. 🔍 Parse Station Numbers

Extract weather station IDs from the Long Paddock XML database.

```bash
python station_number_parser.py
```

**Source:** https://www.longpaddock.qld.gov.au/  
**Output:** List of station IDs for NSW, QLD, and VIC states

---

### 2. 📥 Download Weather Data

Crawl daily weather data for all parsed stations within your specified date range.

```bash
python crawl_temp.py
```

**Source:** SILO Point Data API  
**Output:** `all_station_from_date_to_date.csv`

This comprehensive file contains weather data for each station and each day in the specified time window.

---

### 3. 🔧 Process & Combine Data

Merge all station-level data and compute state-based averages.

```bash
python combine_weather_data.py
```

**Input:** `all_station_from_date_to_date.csv`  
**Output:** `avg_weather_from_date_to_date.csv`

The final output contains average daily weather metrics for each state.

## 🎯 Quick Start Example

```bash
# Step 0: Activate virtual environment
source venv/bin/activate

# Step 1: Parse station numbers
python station_number_parser.py

# Step 2: Download raw weather data
python crawl_temp.py

# Step 3: Generate state-level averages
python combine_weather_data.py
```

---

## ⚠️ Important Notes

- **Network Stability:** Ensure a stable internet connection when downloading data from SILO
- **Processing Time:** Large date ranges may require significant processing time
- **File Format:** All outputs are saved as CSV files for seamless integration with data analysis tools
- **Data Source:** Weather data is sourced from the official Queensland Government SILO database

---

## 🤝 Contributing

We welcome contributions! Please feel free to submit pull requests or open issues for any improvements or bug fixes.

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

*Weather data courtesy of the Queensland Government's Long Paddock SILO database.*