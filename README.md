# ✈️ Flight Price Prediction - Data 400 Capstone Project

<p align="center">
  <img src="https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=800" alt="Airplane in sky">
</p>

> *Predicting flight prices using machine learning and real-time data from the Amadeus API*

[![Data Collection Status](https://github.com/wbartlett1/Data400_Final_Project/workflows/Collect%20Flight%20Data/badge.svg)](https://github.com/wbartlett1/Data400_Final_Project/actions)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## 📋 Table of Contents
- [Introduction](#-introduction)
- [Project Overview](#-project-overview)
- [Repository Structure](#-repository-structure)
- [Data Collection](#-data-collection)
- [Dataset Description](#-dataset-description)
- [Installation & Setup](#-installation--setup)
- [Usage](#-usage)
- [Results & Analysis](#-results--analysis)
- [Contributing](#-contributing)
- [Contact](#-contact)

---

## 🎯 Introduction

Welcome to my Data 400 capstone project! 👋 

This project tackles a question we've all wondered about: **Can we predict flight prices?** Using machine learning and automated data collection from the Amadeus Flight API, I've built a system that gathers real-time flight data across major US airports and develops predictive models to forecast ticket prices.

Why does this matter? Airlines use complex algorithms to dynamically price tickets based on demand, seasonality, route popularity, and countless other factors. By analyzing these patterns, we can help travelers make more informed decisions about when to book their flights! 💰✈️

---

## 🔍 Project Overview

### Key Features
- 🤖 **Automated Data Collection**: GitHub Actions workflow runs daily to collect fresh flight data
- 🌐 **Comprehensive Coverage**: Tracks flights across major US airports
- 📊 **Large-Scale Dataset**: 200,000+ flight observations collected
- 🧠 **Machine Learning Models**: Multiple ML approaches to predict flight prices
- 📈 **Real-Time API Integration**: Uses Amadeus Flight Offers Search API

### Technologies Used
- **Python 3.8+** for data processing and modeling
- **Amadeus API** for real-time flight data
- **GitHub Actions** for automated workflows
- **Pandas & NumPy** for data manipulation
- **Scikit-learn** for machine learning
- **Matplotlib/Seaborn** for visualization

---

## 📁 Repository Structure

```
Data400_Final_Project/
│
├── .github/workflows/          # GitHub Actions automation
│   └── collect_flights.yml     # Scheduled workflow for daily data collection
│
├── code/                       # Analysis and modeling scripts
│   ├── exploratory_analysis.py # EDA and data visualization
│   ├── feature_engineering.py  # Feature creation and transformation
│   └── modeling.py             # Machine learning models
│
├── data/                       # Flight data storage
│   ├── raw/                    # Raw API responses
│   ├── processed/              # Cleaned and processed datasets
│   └── features_engineered/    # Engineered features for modeling
│
├── collect_flights.py          # Main data collection script
├── requirements.txt            # Python package dependencies
├── .gitignore                 # Git ignore rules
└── README.md                  # You are here! 📍
```

### 📄 File Descriptions

#### `collect_flights.py`
The heart of the data collection system! This script:
- Connects to the Amadeus API using secure credentials
- Queries flight offers for major airport routes
- Handles pagination and rate limiting
- Stores data in structured CSV format
- Includes error handling and logging

#### `.github/workflows/`
Contains the GitHub Actions configuration that automatically runs `collect_flights.py` on a schedule. This ensures we're constantly gathering fresh data without manual intervention.

#### `code/`
Houses all analysis and modeling scripts:
- **Exploratory Data Analysis**: Understanding price distributions, seasonal patterns, and route popularity
- **Feature Engineering**: Creating meaningful predictors from raw data
- **Modeling**: Building and evaluating machine learning models

#### `data/`
Stores all collected flight data in organized subdirectories. *Note: Large data files are gitignored to keep the repo lightweight.*

#### `requirements.txt`
Lists all Python packages needed to run the project. Install with:
```bash
pip install -r requirements.txt
```

---

## 🔄 Data Collection

### How It Works

The automated data collection pipeline follows these steps:

1. **GitHub Actions Trigger** 📅
   - Workflow runs daily at scheduled times
   - Can also be triggered manually

2. **API Authentication** 🔐
   - Securely retrieves Amadeus API credentials from GitHub Secrets
   - Generates OAuth access token

3. **Flight Search** 🔍
   - Queries major US airport pairs (e.g., JFK↔LAX, ORD↔MIA)
   - Searches for flights across multiple departure dates
   - Collects various cabin classes and booking options

4. **Data Storage** 💾
   - Appends new data to existing datasets
   - Maintains data quality and consistency
   - Timestamps all collections for tracking

5. **Error Handling** ⚠️
   - Logs API errors and rate limit issues
   - Implements retry logic for failed requests
   - Sends notifications for critical failures

### API Rate Limits
- The Amadeus API has usage limits (check current tier)
- Collection script respects rate limits automatically
- Data is collected strategically to maximize coverage

---

## 📊 Dataset Description

### Data Variables

Each flight observation includes the following variables:

| Variable Name | Type | Description |
|--------------|------|-------------|
| `flight_id` | string | Unique identifier for the flight offer |
| `origin` | string | Origin airport code (e.g., 'JFK', 'LAX') |
| `destination` | string | Destination airport code |
| `departure_date` | datetime | Scheduled departure date and time |
| `arrival_date` | datetime | Scheduled arrival date and time |
| `price` | float | **Target variable** - Flight price in USD |
| `currency` | string | Currency of the price (typically 'USD') |
| `airline` | string | Operating airline carrier code |
| `stops` | integer | Number of stops (0 = nonstop, 1 = one stop, etc.) |
| `duration` | string | Total flight duration (e.g., 'PT5H30M') |
| `cabin_class` | string | Booking class (ECONOMY, PREMIUM_ECONOMY, BUSINESS, FIRST) |
| `seats_available` | integer | Number of seats remaining at this price |
| `booking_class` | string | Fare booking code |
| `days_until_departure` | integer | Days between search date and departure |
| `search_date` | datetime | When the price was recorded |

### Engineered Features

Additional features created for modeling:

- **Temporal Features**
  - `day_of_week`: Departure day (Monday=0 to Sunday=6)
  - `month`: Month of travel
  - `is_weekend`: Boolean for weekend travel
  - `is_holiday_season`: Peak travel periods
  
- **Route Features**
  - `route_distance`: Approximate distance in miles
  - `route_popularity`: Frequency of flights on this route
  - `hub_airport`: Whether origin/destination is a major hub

- **Price History Features**
  - `price_trend`: Direction of price movement
  - `min_price_seen`: Lowest price observed for this route
  - `price_percentile`: Where current price falls historically

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Amadeus API credentials ([Get them here](https://developers.amadeus.com/))

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/wbartlett1/Data400_Final_Project.git
   cd Data400_Final_Project
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API credentials**
   
   Create a `.env` file in the root directory:
   ```
   AMADEUS_API_KEY=your_api_key_here
   AMADEUS_API_SECRET=your_api_secret_here
   ```

4. **Verify setup**
   ```bash
   python collect_flights.py --test
   ```

---

## 🚀 Usage

### Collecting Flight Data

Run manual data collection:
```bash
python collect_flights.py
```

Collect for specific routes:
```bash
python collect_flights.py --routes JFK-LAX ORD-MIA
```

### Running Analysis

Explore the data:
```bash
python code/exploratory_analysis.py
```

Train models:
```bash
python code/modeling.py
```

---

## 📈 Results & Analysis

### Sample Visualizations

*Coming soon: Add screenshots of your analysis here!*

- Price distribution across routes
- Seasonal pricing trends
- Impact of booking window on prices
- Model performance comparisons

### Key Findings

📌 **Booking Window Effect**: Prices typically increase as departure date approaches, with optimal booking around 6-8 weeks in advance

📌 **Day of Week Impact**: Tuesday and Wednesday flights tend to be cheaper than Friday and Sunday departures

📌 **Route Characteristics**: Hub-to-hub routes show more price volatility due to higher competition

📌 **Model Performance**: [Add your best model's performance metrics here]

---

## 🤝 Contributing

This is an academic capstone project, but feedback and suggestions are always welcome! Feel free to:

- 🐛 Report bugs or data issues
- 💡 Suggest improvements to data collection
- 📊 Share ideas for additional analyses
- 🔧 Propose code optimizations

### Discussion & Questions

Have questions about the project? Want to discuss the methodology? 

- 📧 Email: [your-email@dickinson.edu]
- 💬 Open an [Issue](https://github.com/wbartlett1/Data400_Final_Project/issues)
- 🎓 This project was completed as part of Data 400 at Dickinson College

---

## 📚 References & Resources

- [Amadeus for Developers](https://developers.amadeus.com/)
- [Flight Price Prediction Research Papers](add-links)
- [Scikit-learn Documentation](https://scikit-learn.org/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **Professor [Name]** and the Data 400 course for guidance and support
- **Dickinson College** Data Analytics Department
- **Amadeus** for providing API access
- The data science community for inspiration and resources

---

<p align="center">
  Made with ☕ and 💻 by Will Bartlett<br>
  Dickinson College Class of 2025<br>
  <i>Data Analytics & Quantitative Economics Major</i>
</p>

---

## 🔗 Quick Links

- [Project Repository](https://github.com/wbartlett1/Data400_Final_Project)
- [Data Collection Workflow](https://github.com/wbartlett1/Data400_Final_Project/actions)
- [Issue Tracker](https://github.com/wbartlett1/Data400_Final_Project/issues)

---

*Last Updated: December 2025*
