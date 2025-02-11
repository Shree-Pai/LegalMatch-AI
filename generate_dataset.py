import pandas as pd
import numpy as np

# Generate realistic lawyer data
np.random.seed(42)

# Generate number of lawyers
n_lawyers = 100

# Lists for categorical data
specializations = [
    'Criminal Law', 'Family Law', 'Corporate Law', 'Civil Rights',
    'Property Law', 'Immigration Law', 'Tax Law', 'Employment Law',
    'Intellectual Property', 'Personal Injury'
]

law_schools = [
    'Harvard Law School', 'Yale Law School', 'Stanford Law School',
    'Columbia Law School', 'NYU School of Law', 'UC Berkeley Law',
    'University of Chicago Law', 'University of Michigan Law',
    'Georgetown Law', 'Northwestern Law'
]

locations = [
    'New York, NY', 'Los Angeles, CA', 'Chicago, IL', 'Houston, TX',
    'Phoenix, AZ', 'Philadelphia, PA', 'San Antonio, TX', 'San Diego, CA',
    'Dallas, TX', 'San Jose, CA'
]

# Generate data
lawyers_data = {
    'lawyer_id': range(1, n_lawyers + 1),
    'name': [f"Lawyer_{i}" for i in range(1, n_lawyers + 1)],
    'specialization': np.random.choice(specializations, n_lawyers),
    'experience_years': np.random.randint(1, 35, n_lawyers),
    'success_rate': np.random.uniform(0.60, 0.95, n_lawyers),
    'feedback_score': np.random.uniform(3.5, 5.0, n_lawyers),
    'cases_handled': np.random.randint(50, 1000, n_lawyers),
    'hourly_rate': np.random.randint(150, 800, n_lawyers),
    'law_school': np.random.choice(law_schools, n_lawyers),
    'location': np.random.choice(locations, n_lawyers),
    'bar_admission_year': np.random.randint(1990, 2023, n_lawyers),
    'pro_bono_cases': np.random.randint(0, 50, n_lawyers)
}

# Create descriptions based on other attributes
descriptions = []
for i in range(n_lawyers):
    exp = lawyers_data['experience_years'][i]
    spec = lawyers_data['specialization'][i]
    loc = lawyers_data['location'][i]
    school = lawyers_data['law_school'][i]
    success = round(lawyers_data['success_rate'][i] * 100)
    
    description = f"Experienced {spec.lower()} attorney with {exp} years of practice. "
    description += f"Graduate of {school}, practicing in {loc}. "
    description += f"Maintains a {success}% success rate in cases. "
    
    if lawyers_data['pro_bono_cases'][i] > 25:
        description += "Actively involved in pro bono work. "
    if lawyers_data['feedback_score'][i] >= 4.5:
        description += "Highly rated by clients. "
    
    descriptions.append(description)

lawyers_data['description'] = descriptions

# Create DataFrame
lawyers_df = pd.DataFrame(lawyers_data)

# Add some past cases data (synthetic)
past_cases = []
for idx in range(n_lawyers):
    n_cases = np.random.randint(10, 30)
    for _ in range(n_cases):
        case_type = lawyers_data['specialization'][idx]
        outcome = np.random.choice(['won', 'lost'], p=[lawyers_data['success_rate'][idx], 1-lawyers_data['success_rate'][idx]])
        past_cases.append({
            'lawyer_id': lawyers_data['lawyer_id'][idx],
            'case_type': case_type,
            'case_duration_months': np.random.randint(1, 24),
            'outcome': outcome,
            'client_satisfaction': np.random.uniform(3.0, 5.0) if outcome == 'won' else np.random.uniform(2.0, 4.0),
            'complexity_score': np.random.uniform(1, 10),
            'year': np.random.randint(2020, 2024)
        })

past_cases_df = pd.DataFrame(past_cases)

# Save to CSV files
lawyers_df.to_csv('lawyers_data.csv', index=False)
past_cases_df.to_csv('past_cases_data.csv', index=False)

print("Generated lawyers_data.csv and past_cases_data.csv")
print(f"Number of lawyers: {len(lawyers_df)}")
print(f"Number of past cases: {len(past_cases_df)}")