export interface FeatureField {
  name: string;
  label: string;
  kind: 'number' | 'select';
  defaultValue: number | string;
  min?: number;
  max?: number;
  required: boolean;
  options?: string[];
}

export const FEATURE_FIELDS: FeatureField[] = [
  { name: 'loan_amnt', label: 'Loan Amount ($)', kind: 'number', defaultValue: 10000, min: 500, max: 40000, required: true },
  { name: 'funded_amnt', label: 'Funded Amount ($)', kind: 'number', defaultValue: 10000, min: 500, max: 40000, required: true },
  { name: 'funded_amnt_inv', label: 'Funded Amount by Investors ($)', kind: 'number', defaultValue: 10000, min: 0, max: 40000, required: true },
  { name: 'term', label: 'Loan Term', kind: 'select', defaultValue: ' 36 months', required: true, options: [' 36 months', ' 60 months'] },
  { name: 'int_rate', label: 'Interest Rate (%)', kind: 'number', defaultValue: 13.5, min: 5, max: 31, required: true },
  { name: 'installment', label: 'Monthly Installment ($)', kind: 'number', defaultValue: 320, min: 10, max: 1600, required: true },
  { name: 'grade', label: 'Loan Grade', kind: 'select', defaultValue: 'C', required: true, options: ['A', 'B', 'C', 'D', 'E', 'F', 'G'] },
  { name: 'sub_grade', label: 'Loan Sub-Grade', kind: 'select', defaultValue: 'C2', required: true,
    options: ['A1','A2','A3','A4','A5','B1','B2','B3','B4','B5','C1','C2','C3','C4','C5','D1','D2','D3','D4','D5','E1','E2','E3','E4','E5','F1','F2','F3','F4','F5','G1','G2','G3','G4','G5'] },
  { name: 'emp_length', label: 'Employment Length', kind: 'select', defaultValue: '10+ years', required: true,
    options: ['< 1 year','1 year','2 years','3 years','4 years','5 years','6 years','7 years','8 years','9 years','10+ years'] },
  { name: 'home_ownership', label: 'Home Ownership', kind: 'select', defaultValue: 'MORTGAGE', required: true,
    options: ['MORTGAGE', 'RENT', 'OWN', 'ANY', 'OTHER', 'NONE'] },
  { name: 'annual_inc', label: 'Annual Income ($)', kind: 'number', defaultValue: 65000, min: 0, max: 1000000, required: true },
  { name: 'verification_status', label: 'Income Verification', kind: 'select', defaultValue: 'Source Verified', required: true,
    options: ['Source Verified', 'Verified', 'Not Verified'] },
  { name: 'purpose', label: 'Loan Purpose', kind: 'select', defaultValue: 'debt_consolidation', required: true,
    options: ['debt_consolidation','credit_card','home_improvement','other','major_purchase','medical','small_business','car','moving','vacation','house','wedding','renewable_energy','educational'] },
  { name: 'addr_state', label: 'State', kind: 'select', defaultValue: 'CA', required: true,
    options: ['AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY','DC'] },
  { name: 'dti', label: 'Debt-to-Income Ratio (%)', kind: 'number', defaultValue: 18, min: 0, max: 60, required: true },
  { name: 'delinq_2yrs', label: 'Delinquencies (past 2 yrs)', kind: 'number', defaultValue: 0, min: 0, max: 20, required: true },
  { name: 'fico_range_low', label: 'FICO Score (low end)', kind: 'number', defaultValue: 695, min: 300, max: 850, required: true },
  { name: 'fico_range_high', label: 'FICO Score (high end)', kind: 'number', defaultValue: 699, min: 300, max: 850, required: true },
  { name: 'inq_last_6mths', label: 'Credit Inquiries (last 6 mo)', kind: 'number', defaultValue: 1, min: 0, max: 20, required: true },
  { name: 'open_acc', label: 'Open Credit Accounts', kind: 'number', defaultValue: 11, min: 0, max: 80, required: true },
  { name: 'pub_rec', label: 'Public Records (derogatory)', kind: 'number', defaultValue: 0, min: 0, max: 20, required: true },
  { name: 'revol_bal', label: 'Revolving Balance ($)', kind: 'number', defaultValue: 15000, min: 0, max: 500000, required: true },
  { name: 'revol_util', label: 'Revolving Utilization (%)', kind: 'number', defaultValue: 50, min: 0, max: 150, required: true },
  { name: 'total_acc', label: 'Total Credit Accounts', kind: 'number', defaultValue: 24, min: 0, max: 150, required: true },
  { name: 'initial_list_status', label: 'Initial List Status', kind: 'select', defaultValue: 'w', required: true, options: ['w', 'f'] },
  { name: 'application_type', label: 'Application Type', kind: 'select', defaultValue: 'Individual', required: true, options: ['Individual', 'Joint App'] },
  { name: 'acc_now_delinq', label: 'Accounts Now Delinquent', kind: 'number', defaultValue: 0, min: 0, max: 10, required: true },
  { name: 'tot_coll_amt', label: 'Total Collection Amount ($)', kind: 'number', defaultValue: 0, min: 0, max: 100000, required: true },
  { name: 'tot_cur_bal', label: 'Total Current Balance ($)', kind: 'number', defaultValue: 140000, min: 0, max: 5000000, required: true },
  { name: 'total_rev_hi_lim', label: 'Total Revolving Credit Limit ($)', kind: 'number', defaultValue: 30000, min: 0, max: 1000000, required: true },
  { name: 'acc_open_past_24mths', label: 'Accounts Opened (past 24 mo)', kind: 'number', defaultValue: 4, min: 0, max: 30, required: true },
  { name: 'avg_cur_bal', label: 'Average Current Balance ($)', kind: 'number', defaultValue: 13000, min: 0, max: 500000, required: true },
  { name: 'bc_open_to_buy', label: 'Bankcard Open-to-Buy ($)', kind: 'number', defaultValue: 8000, min: 0, max: 500000, required: true },
  { name: 'bc_util', label: 'Bankcard Utilization (%)', kind: 'number', defaultValue: 55, min: 0, max: 200, required: true },
  { name: 'delinq_amnt', label: 'Delinquent Amount ($)', kind: 'number', defaultValue: 0, min: 0, max: 100000, required: true },
  { name: 'mort_acc', label: 'Mortgage Accounts', kind: 'number', defaultValue: 2, min: 0, max: 30, required: true },
  { name: 'num_accts_ever_120_pd', label: 'Accounts Ever 120+ Days Past Due', kind: 'number', defaultValue: 0, min: 0, max: 20, required: true },
  { name: 'num_actv_bc_tl', label: 'Active Bankcard Accounts', kind: 'number', defaultValue: 4, min: 0, max: 30, required: true },
  { name: 'num_actv_rev_tl', label: 'Active Revolving Accounts', kind: 'number', defaultValue: 6, min: 0, max: 40, required: true },
  { name: 'num_bc_sats', label: 'Satisfactory Bankcard Accounts', kind: 'number', defaultValue: 5, min: 0, max: 30, required: true },
  { name: 'num_bc_tl', label: 'Total Bankcard Accounts', kind: 'number', defaultValue: 8, min: 0, max: 40, required: true },
  { name: 'num_il_tl', label: 'Installment Accounts', kind: 'number', defaultValue: 5, min: 0, max: 40, required: true },
  { name: 'num_op_rev_tl', label: 'Open Revolving Accounts', kind: 'number', defaultValue: 8, min: 0, max: 40, required: true },
  { name: 'num_rev_accts', label: 'Total Revolving Accounts', kind: 'number', defaultValue: 14, min: 0, max: 60, required: true },
  { name: 'num_rev_tl_bal_gt_0', label: 'Revolving Accounts with Balance', kind: 'number', defaultValue: 6, min: 0, max: 40, required: true },
  { name: 'num_sats', label: 'Satisfactory Accounts', kind: 'number', defaultValue: 11, min: 0, max: 60, required: true },
  { name: 'pct_tl_nvr_dlq', label: 'Percent Accounts Never Delinquent', kind: 'number', defaultValue: 95, min: 0, max: 100, required: true },
  { name: 'pub_rec_bankruptcies', label: 'Public Record Bankruptcies', kind: 'number', defaultValue: 0, min: 0, max: 10, required: true },
  { name: 'tax_liens', label: 'Tax Liens', kind: 'number', defaultValue: 0, min: 0, max: 10, required: true },
];