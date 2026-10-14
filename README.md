# Stock Market Listings Analysis

This is a small exploratory data analysis (EDA) project I did on a CSV of securities listed on US exchanges. I'm still learning data science, so I picked this one to practice cleaning a real-world file and getting useful answers from data that has no numbers to chart, only categories and codes.

## About the Dataset

The file is `stock_market_csv.csv`. It has **8,049 rows and 12 columns**, and every row is one traded security (stocks, ETFs, trusts and so on). It looks like a NASDAQ symbol directory. There are no prices or returns in it. It is purely a listing of what trades and where.

| Column | What it means |
|---|---|
| Nasdaq Traded | Whether the security trades on NASDAQ (Y for every row) |
| Symbol | Ticker symbol |
| Security Name | Full name of the security |
| Listing Exchange | Exchange code where it is listed (A, N, P, Q, Z) |
| Market Category | NASDAQ tier (Q, G, S). Blank for non-NASDAQ listings |
| ETF | Y if it is an ETF, N if not |
| Round Lot Size | Standard trading lot size |
| Test Issue | Whether it is a test security (N for every row) |
| Financial Status | NASDAQ compliance status (only filled for NASDAQ listings) |
| CQS Symbol | Symbol used in the CQS system |
| NASDAQ Symbol | Symbol used by NASDAQ |
| NextShares | Whether it is a NextShares fund |

## What I Did

1. Loaded the data with pandas and checked shape, data types and missing values
2. Looked at each categorical column with value counts
3. Cross-tabulated exchange against ETF, market category and financial status
4. Checked for duplicates and odd values (lot sizes, symbol lengths, repeated names)
5. Wrote down what I found

## Data Cleaning Notes

- **Missing values:** Financial Status is empty in 4,666 rows, CQS Symbol in 3,383 rows. This is not bad data. Financial Status only exists for NASDAQ-listed securities, and CQS Symbol only exists for the ones that are not. Market Category is also blank (a space) for 4,666 rows, for the same reason. One thing to watch: when reading the CSV with pandas, the letter **N** can be turned into NaN by default, so I used `keep_default_na=False` to avoid losing real values.
- **Constant columns:** Nasdaq Traded and Test Issue have only one value in every row, so they add no information for analysis.
- **Duplicates:** Symbols are unique (8,049 of 8,049). Security names are not. 4 names appear twice, such as "MFS Municipal Income Trust Common Stock" (CMU and MFM) and a few iShares ETFs. These are different tickers for the same name, so I kept them.
- **Symbol mismatch:** In 3 rows the Symbol and the NASDAQ Symbol are different. I left these as they are.

## Key Findings

**1. NASDAQ is the biggest listing venue.**
Out of 8,049 securities, 3,383 (about 42%) are listed on NASDAQ (Q). NYSE (N) has 2,520 (about 31%), NYSE Arca (P) has 1,542 (about 19%), Cboe BZX (Z) has 351 (about 4%) and NYSE American (A) has 253 (about 3%).

**2. About 1 in 4 securities is an ETF.**
2,165 are ETFs (about 27%) and 5,884 are not. Almost all of the ETFs sit on NYSE Arca (1,435 of 1,542 listings there) and on NASDAQ (395). NYSE has none at all, and Cboe BZX is mostly ETFs too (334 out of 351).

**3. NASDAQ's three market tiers are fairly balanced.**
Of the 3,383 NASDAQ listings, 1,531 are in the Global Select tier (Q), 952 are in the Capital Market (S) and 900 are in the Global Market (G).

**4. Most NASDAQ companies are in good standing.**
3,180 (about 94%) have a normal financial status. 191 are deficient, 8 are delinquent and 4 are both. So roughly 6% have some kind of compliance issue.

**5. Almost everything trades in lots of 100.**
8,044 securities use a round lot of 100. Only 5 are different: four have a lot size of 10 (BH, DIT, MKL, NVR) and one has a lot size of 1 (SEB). From what I could see, these are mostly high-priced stocks, which would make sense, but I haven't checked that because the file has no price data.

**6. NextShares is very rare.**
Only 3 securities are NextShares funds, all from Eaton Vance.

**7. Most tickers are short.**
Four-letter tickers are the most common (4,634), followed by three-letter ones (2,859). Only 21 tickers are one letter.

## Limitations

- No prices, volumes, dates or sector information, so I can't say anything about performance or trends over time
- It is a snapshot, so I can't tell when each security was listed
- The meaning of the exchange and category codes comes from NASDAQ's documentation, not from the file itself

## Tools Used

- Python
- pandas
- Jupyter Notebook / Google Colab

## What I Would Do Next

- Join this with a price dataset (for example from Yahoo Finance) to compare ETFs and stocks on returns
- Group the securities by type using the names (common stock, preferred, warrants, depositary shares) and chart them
- Build a few visualizations of the exchange and tier breakdown

## About Me

I'm Tirath, NEW in data analytics who is building a portfolio one project at a time.

- GitHub: https://github.com/Tirath-singh
- LinkedIn: https://www.linkedin.com/in/tirath-singh-35b550422/
