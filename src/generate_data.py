import numpy as np
import pandas as pd

N_BORROWERS = 200
SEED = 42

def generate_borrowers(n, seed):
	"""Return a table with one row per made-up borrower."""
	rng=np.random.default_rng(seed)
	list_of_sectors = ["retail","manufacturing", "services", "agriculture"] 
	ten_1 = ["12","24","36","48","60"]
	data= {
	    "borrower_id": range(1, n+1),
	    "loan_amount": rng.integers(200000, 5000000, size=n),
	    "sector": rng.choice(list_of_sectors, size=n),
	    "annual_interest_rate": rng.uniform(9,14,size=n),
	    "tenure_months":rng.choice(ten_1, size=n),	    	    
	    "monthly_revenue": rng.integers(100000,200000, size=n),
	}
	return pd.DataFrame(data)
if __name__=="__main__":
	df=generate_borrowers(N_BORROWERS, SEED)
	df.to_csv("data/borrowers.csv",index=False)
	print(df.head())