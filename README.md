# ✈️ Flight Price Prediction - Data 400 Capstone Project

<p align="center">
  <img src="https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=800" alt="Airplane in sky">
</p>

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

Hi! Welcome to our Data 400 capstone project! 👋 

This project aims to address the question: **Can we predict flight prices?**<br>
Using machine learning and automated data collection from the Amadeus Flight API, We've built a project that gathers real-time flight data for major cross-country flight patterns and develops predictive models to forecast ticket prices.

**Why does this matter?**<br>
Airlines use complex algorithms to dynamically price tickets based on demand, seasonality, route popularity, and countless other factors. By analyzing these patterns, we can help travelers make more informed decisions about when to book their flights! 💰✈️

---

## 📊 Project Overview

### Key Features
- **Robust Data Workflow**: GitHub Actions run our workflow 2x daily to collect up-to-date flight data
- **Real-Time API Integration**: Uses Amadeus Flight Offers Search API
- **Large-Scale Dataset**: over 600,000 observations collected
- **Machine Learning Models**: Multiple ML approaches to predict flight prices
- **Quality Data Visualizations**: Many visualizations showing the capabilities of our data

### Technologies Used
- **Python 3.8+** for data processing, visualizaing, and modeling
- **Amadeus API** for data collection
- **GitHub Actions** for automated workflows
- **Pandas & NumPy** for data manipulation
- **Scikit-learn** for machine learning
- **Matplotlib/Seaborn** for visualization

---

## 📁 Repository Structure

```
Data400_Final_Project/
│
├── .github/workflows/           # GitHub Actions automation
│   └── collect_flights.yml      # Scheduled workflow for daily data collection
│
├── code/                         # Analysis and modeling scripts
│   ├── EDA.ipynb                 # EDA & data visualization
│   ├── data_concatination.ipynb  # Data concatenation (for saving example dataset)
│   ├── feature_engineering.ipynb # Feature engineering and modeling preparation
│   └── modeling.ipynb            # Machine learning models
│
├── data/                         # Flight data storage
│   ├── final_flight_data.csv     # Example dataset (first ~500,000 observations collected)
│
├── collect_flights.py            # Main data collection script
├── requirements.txt              # Python package dependencies
├── .gitignore                    # Git ignore rules
└── README.md                     # You are here
```

### 📄 File Descriptions

#### `collect_flights.py`
This script:
- Connects to the Amadeus API using secure credentials
- Queries flight offers for major airport routes
- Handles pagination and rate limiting
- Stores data in structured CSV format
- Uploads data directly to Dropbox
- Includes error handling and logging

#### `.github/workflows/`
Contains the GitHub Actions configuration that automatically runs `collect_flights.py` on a schedule. This ensures we're constantly gathering fresh data without manual intervention. The workflow runs twice daily at 12:00 AM and 12:00 PM UTC.

#### `code/`
Houses all analysis and modeling scripts:
- **Exploratory Data Analysis**: Understanding price distributions, seasonal patterns, route popularity, and much nmore!
- **Feature Engineering**: Creating meaningful predictors from raw data
- **Modeling**: Building and evaluating machine learning models

#### `data/`
Stores a sample of the data for our project. *Note: Large data files are gitignored to avoid file size issues.*

#### `requirements.txt`
Lists all Python packages needed to run the project. Install with:
```bash
pip install -r requirements.txt
```

---

## 🔄 Data Collection

The automated data collection pipeline follows these steps:

1. **GitHub Actions Trigger** 📅
   - Workflow runs twice daily
   - Can also be triggered manually

2. **API Authentication** 🔐
   - Authenticates Amadeus API credentials

4. **Flight Search** 🔍
   - Queries major US airport pairs (e.g., JFK↔LAX, ORD↔MIA)
   - Searches for flights across multiple departure dates
   - Collects various cabin classes and booking options

5. **Data Storage** 💾
   - New data is saved to Dropbox as a .csv with a date and time label

6. **Error Handling** ⚠️
   - Logs API errors and rate limit issues
   - Implements retry logic for failed requests
   - Sends notifications for critical failures

### API Rate Limits
- The Amadeus API has very strict usage limits
- Multiple API keys are used in each data collection run

---

## 📊 Dataset Description

### Amadeus Variables

Each flight observation includes the following variables:

| Variable Name | Type | Description |
|--------------|------|-------------|
| `flight_id` | string | Unique identifier for the specific flight - engineered |
| `origin` | string | Origin airport code (e.g., 'JFK', 'LAX') |
| `destination` | string | Destination airport code |
| `departure_date` | datetime | Scheduled departure date and time |
| `arrival_date` | datetime | Scheduled arrival date and time |
| `price` | float | **Target variable** - Flight price in Euros |
| `currency` | string | Currency of the price (in EUR, transformed to USD) |
| `airline` | string | Operating airline carrier code |
| `stops` | integer | Number of stops (e.g. 0 = nonstop, etc.) |
| `duration` | string | Total flight duration (e.g., 'PT5H30M') |
| `cabin_class` | string | Booking class (ECONOMY, PREMIUM_ECONOMY, BUSINESS, FIRST) |
| `seats_available` | integer | Number of seats remaining at this price |
| `booking_class` | string | Fare booking code |
| `days_until_departure` | integer | Days between search date and departure |
| `search_date` | datetime | When the price was recorded |

### Engineered Features

Features used for Modeling:

- **Historical Prices**
  - lagged price features
  - rolling window statistics
  
- **Route Features**
  - route competition features
  - route durations
  - route volatility

- **Temporal Features**
  - red-eye indicators
  - time of day indicators
  - flight durations
  - departure day features
 
- **Airline Features**
  - airline volatility
  - premium vs lowcost carrier

- **Bookable Seats Features**
  - distance from 4 bookable seats (see EDA)
  - scarcity indicators

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

### Running Analysis

Explore the data:
```bash
python code/EDA.ipynb
```

Prepare data for modeling:
```bash
python code/feature_engineering.ipynb
```

Train models:
```bash
python code/modeling.ipynb
```

---

## 📈 Exploratory Analysis - Sample Visualizations

**Price by Airline** <br>
<img width="987" height="590" alt="image" src="https://github.com/user-attachments/assets/144bc5f0-6774-4092-9852-06050768662d" />

**Route-Level Visualization** <br>
<img width="1789" height="790" alt="image" src="https://github.com/user-attachments/assets/dd3f0b88-3e49-48b1-9292-debf68b7bd95" />

**Booking Window Visualization** <br>
<img width="989" height="590" alt="image" src="https://github.com/user-attachments/assets/6c1faaf5-21ca-48b3-af4d-1575c28aafb1" />

**Temporal Visualization** <br>
<img width="1589" height="590" alt="image" src="https://github.com/user-attachments/assets/2293092f-bcac-457e-b6cb-326e1ded08db" />

**Bookable Seats Visualization** <br>
<img width="989" height="590" alt="image" src="https://github.com/user-attachments/assets/5a4d83a0-e82a-4485-84f8-e915ad115dc5" />

--

## 📈 Machine Learning Model Performance

Machine learning models tackle the question: Can we predict a flight's next day price?

**Models Tested:**<br>
- Linear Regression
- Decision Tree
- Random Forest
- XGBoost

**Model Performance:**
<img width="989" height="590" alt="image" src="https://github.com/user-attachments/assets/5ab3faa2-7780-4d8a-8286-26c24ade07dc" />

**Feature Importance:**
<img width="995" height="789" alt="image" src="https://github.com/user-attachments/assets/9ae62f4c-8c90-4641-a024-f1c57829c107" />

**Results Discussion**

---

### ❓ Questions ❓

Have any questions? Contact us at our email below or open an issue!

- 📧 Email: bartletw@dickinson.edu| KEVIN EMAIL
- 💬 Open an [Issue](https://github.com/wbartlett1/Data400_Final_Project/issues)
- 🎓 This project was completed for the Data Analytics Capstone at Dickinson College

---

## 📚 References & Resources

- [Amadeus for Developers](https://developers.amadeus.com/)
- [Scikit-learn Documentation](https://scikit-learn.org/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

## 🙏 Acknowledgments

- **Professor Bilen** 
- **Dickinson College** 
- **Amadeus** for providing API access
- The data science community for inspiration and resources

---

<p align="center">
  Made by Will Bartlett & Kevin Tran<br>
  Dickinson College<br>
  <i>Data Analytics Department</i>
</p>

---

## 🔗 Quick Links

- [Project Repository](https://github.com/wbartlett1/Data400_Final_Project)
- [Data Collection Workflow](https://github.com/wbartlett1/Data400_Final_Project/actions)
- [Issue Tracker](https://github.com/wbartlett1/Data400_Final_Project/issues)

---

*Last Updated: December 2025*
