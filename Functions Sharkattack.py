def clean_sex_column_f(x):
    sex_mapping = {"N": "unknown","lli": "unknown",".": "unknown","M x 2": "M"}
    return sex_mapping.get(x, x)

def finalize_value_f(x):
    val = str(x).strip().lower()
    if val in ['m', 'f']:
        return val.upper()
    return 'unknown'

def clean_attack_mapping_f(x):
    # 1. Define the mapping inside or outside the function
    type_mapping = {
         "Unprovoked": "Unprovoked",
    "Provoked": "Provoked",
    "Boating": np.nan,
    "Invalid": np.nan,
    "Sea Disaster": "Unprovoked",
    "?":  np.nan,
    "Boat": np.nan,
    "Invalid ": np.nan,
    "Questionable": np.nan,
    "Unconfirmed": np.nan,
    "Unverified": np.nan,
    "Under investigation": np.nan,
    "Watercraft": np.nan,
    "unprovoked": "Unprovoked",
    "Invalid Incident": np.nan,
    "Invalid ": np.nan    
    }
    
    # 2. Handle the mapping first
    # If the text is in our dictionary, change it. If not, keep original.
    val_as_str = str(x).strip()
    if val_as_str in type_mapping:
        x = type_mapping[val_as_str]

    # 3. Standardize to Provoked/Unprovoked/Unknown
    value = str(x).strip().lower()
    if value in ['unprovoked', 'provoked']:
        return value.title()
    else:
        return 'Unknown'


def clean_activities_f(df, col, n_keywords=20, top_n=10):
    # 1. Basic Clean: lowercase, strip, remove quotes
    df2[col] = df2[col].str.lower().str.strip().str.replace(r"[\"']", '', regex=True)
    
    # 2. Quick Discovery: Find most common words (5+ chars)
    all_words = re.findall(r'\w{5,}', ' '.join(df[col].astype(str)))
    common_words = [w for w, c in Counter(all_words).most_common(n_keywords)]
    print(f"Suggested keywords: {common_words}")
    
    # 3. Consolidation: Map keywords to standardized labels
    selected = ["spearfishing", "fishing", "kayaking", "wading", "surfing", "swimming", "diving", "skiing"]
    
    for val in selected:
        df.loc[df[col].str.contains(val, na=False), col] = val
        
    # 4. Filter: Remove blanks and keep only the top N most frequent
    df = df[df[col].str.strip() != '']
    top_index = df[col].value_counts().nlargest(top_n).index
    
    return df[df[col].isin(top_index)].copy()


def categorize_injury_f(text):
    text = str(text).lower()
    
    category_map = {
        'Lower Extremity': ['leg', 'thigh', 'calf', 'knee', 'foot', 'feet', 'ankle', 'toe'],
        'Upper Extremity': ['arm', 'hand', 'finger', 'wrist', 'elbow', 'shoulder', 'forearm'],
        'Torso': ['torso', 'chest', 'back', 'abdomen', 'trunk'],
        'Head/Neck': ['head', 'face', 'neck', 'scalp'],
        'Equipment/None': ['no injury', 'board', 'kayak', 'boat', 'propeller']
    }
    
    found_categories = []
    for category, keywords in category_map.items():
        if any(word in text for word in keywords):
            found_categories.append(category)
            
    # --- FIX: This logic must be indented to stay INSIDE the function ---
    if len(found_categories) > 1:
        return 'Multiple Categories'
    elif len(found_categories) == 1:
        return found_categories[0]
    else:
        return 'Unspecified'

def get_continent_f(country):
    # Mapping the specific 20 countries to their continents
    continent_map = {
        'Australia': 'Oceania',
        'New Caledonia': 'Oceania',
        'French Polynesia': 'Oceania',
        'New Zealand': 'Oceania',
        'Fiji': 'Oceania',
        'USA': 'North America',
        'Mexico': 'North America',
        'Costa Rica': 'North America',
        'Cuba': 'North America',
        'Bahamas': 'North America',
        'Brazil': 'South America',
        'Ecuador': 'South America',
        'Spain': 'Europe',
        'South Africa': 'Africa',
        'Mozambique': 'Africa',
        'Egypt': 'Africa',
        'Reunion': 'Africa',
        'Philippines': 'Asia',
        'Indonesia': 'Asia',
        'Japan': 'Asia'
    }
    
    # Return the continent if found, otherwise 'Other/Unknown'
    return continent_map.get(country, 'Other/Unknown')