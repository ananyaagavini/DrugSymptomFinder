"""
Symptom Synonym Dictionary and Autocomplete Suggestions
Bridges lay terms to CDSCO clinical indications.
"""

SYNONMY_MAP = {
    "fever": ["pyrexia", "fever", "hyperthermia", "febrile", "temperature"],
    "cold": ["rhinitis", "nasal congestion", "coryza", "bronchitis", "respiratory tract infection", "common cold", "stuffy nose"],
    "cough": ["cough", "bronchitis", "anti-tussive", "antitussive", "expectorant", "sputum", "phlegm", "productive cough"],
    "high blood pressure": ["hypertension", "antihypertensive", "high blood pressure", "essential hypertension", "cardiovascular"],
    "high blood sugar": ["diabetes mellitus", "hyperglycemia", "glycemic", "diabetes", "diabetic", "type-2 diabetes", "type-ii diabetes"],
    "joint pain": ["arthritis", "rheumatoid", "osteoarthritis", "joint", "musculoskeletal", "arthritic", "ankylosing spondylitis"],
    "pain": ["analgesic", "pain", "painful", "ache", "bodyache", "inflammation", "musculoskeletal pain"],
    "headache": ["migraine", "headache", "cephalea"],
    "seizures": ["epileptic", "convulsive", "seizure", "epilepsy", "convulsion", "tonic-clonic", "status epilepticus"],
    "skin rash": ["dermatitis", "eczema", "pruritus", "urticaria", "dermatoses", "psoriasis", "erythema", "skin infection", "rash"],
    "bacterial infection": ["antibiotic", "antibacterial", "bacterial", "infection", "gram +ve", "gram -ve", "microorganism"],
    "fungal infection": ["antifungal", "fungal", "candidiasis", "tinea", "mycosis", "dermatomycosis", "candida"],
    "nausea": ["nausea", "vomiting", "antiemetic", "anti-emetic", "emesis", "dyspepsia", "motion sickness"],
    "vomiting": ["vomiting", "nausea", "antiemetic", "emesis", "nausea & vomiting"],
    "diarrhea": ["diarrhoea", "diarrhea", "antidiarrhoeal", "anti-diarrhoeal", "gastroenteritis", "loose motion"],
    "stomach ulcer": ["peptic ulcer", "gastric ulcer", "duodenal ulcer", "anti-ulcer", "gastritis", "gerd", "acid reflux", "heartburn"],
    "acne": ["acne", "acne vulgaris", "pimples", "blackheads"],
    "asthma": ["asthma", "bronchial asthma", "bronchodilator", "copd", "bronchospasm", "airway obstruction"],
    "sleepiness": ["narcolepsy", "excessive sleepiness", "sleep apnea", "drowsiness"],
    "insomnia": ["insomnia", "hypnotic", "sleep disorder", "sleeplessness", "sedative"],
    "anxiety": ["anxiety", "anxiolytic", "panic disorder", "tension", "tranquiliser", "sedative", "neurotic"],
    "depression": ["depression", "depressive", "antidepressant", "anti depressant", "mood disorder"],
    "allergies": ["allergic", "antihistaminic", "anti-histaminic", "urticaria", "rhinitis", "allergy", "hay fever"],
    "eye infection": ["conjunctivitis", "ocular", "ophthalmic", "keratitis", "eye infection", "blepharitis"],
    "ear infection": ["otitis", "otitis media", "ear infection"],
    "urinary tract infection": ["urinary tract infection", "uti", "cystitis", "pyelonephritis", "urethritis"],
    "constipation": ["constipation", "laxative", "bowel clearance", "irritable bowel syndrome"],
    "hair loss": ["alopecia", "male pattern baldness", "hair loss"],
    "heart failure": ["congestive heart failure", "cardiac decompensation", "cardiac failure", "heart failure"],
    "chest pain": ["angina", "angina pectoris", "ischaemic heart disease", "coronary artery disease"],
    "muscle spasm": ["muscle relaxant", "spasm", "musculoskeletal", "spasticity", "muscle stiffness"],
    "wound": ["haemostatic", "wound", "ulcer", "cuts", "abrasion", "wound healing", "burns"],
    "gout": ["gout", "hyperuricemia", "gouty arthritis", "uric acid"],
    "tb": ["tuberculosis", "anti-tuberculosis", "anti t.b", "pulmonary tb"],
    "malaria": ["malaria", "antimalarial", "falciparum", "plasmodium"],
    "prostate": ["benign prostatic hyperplasia", "bph", "prostate cancer", "prostatic"],
    "vertigo": ["vertigo", "dizziness", "vestibular disturbance", "giddiness"],
    "dandruff": ["dandruff", "seborrhoeic dermatitis", "scalp psoriasis"],
    "itching": ["pruritus", "itching", "itchy skin"],
    "swelling": ["edema", "oedema", "inflammation", "swelling"],
    "obesity": ["obesity", "anti obesity", "overweight", "weight loss", "bmi"],
    "kidney disease": ["renal", "kidney", "dialysis", "hyperphosphatemia", "nephropathy"],
    "liver disease": ["hepatitis", "cirrhosis", "cholestasis", "hepatic", "liver disease"],
    "schizophrenia": ["schizophrenia", "schizophrenic", "psychosis", "psychotic"],
    "cancer": ["anticancer", "anti-cancer", "carcinoma", "tumour", "tumor", "leukaemia", "chemotherapy", "neoplastic", "lymphoma", "sarcoma"]
}

# Curated list of ~45 common lay symptom terms for autocomplete dropdown
AUTOCOMPLETE_SYMPTOMS = [
    "Acne & Pimples",
    "Allergies & Sneezing",
    "Anxiety & Tension",
    "Asthma & Breathing Difficulty",
    "Bacterial Infection",
    "Body Pain & Aches",
    "Chest Pain & Angina",
    "Cold & Stuffy Nose",
    "Constipation",
    "Cough & Sputum",
    "Dandruff & Scalp Itch",
    "Depression & Low Mood",
    "Diarrhea & Loose Motions",
    "Dizziness & Vertigo",
    "Dry Eye & Eye Irritation",
    "Ear Infection & Otitis",
    "Eye Infection & Conjunctivitis",
    "Fever & High Temperature",
    "Fungal Infection & Ringworm",
    "Gout & Uric Acid",
    "Hair Loss & Alopecia",
    "Headache & Migraine",
    "Heart Failure & Cardiac Care",
    "High Blood Pressure (Hypertension)",
    "High Blood Sugar (Diabetes)",
    "Insomnia & Sleep Trouble",
    "Itching & Pruritus",
    "Joint Pain & Arthritis",
    "Kidney Care & Dialysis",
    "Liver Disease & Hepatitis",
    "Malaria",
    "Muscle Spasm & Stiffness",
    "Nausea & Vomiting",
    "Obesity & Weight Control",
    "Prostate Enlargement (BPH)",
    "Schizophrenia",
    "Seizures & Epilepsy",
    "Skin Rash & Eczema",
    "Stomach Ulcer & GERD Acid",
    "Swelling & Edema",
    "Tuberculosis (TB)",
    "Urinary Tract Infection (UTI)",
    "Wounds, Cuts & Burns"
]

def expand_symptom_query(query: str) -> list[str]:
    """
    Expands a user input query using the synonym dictionary.
    Returns a list of search terms (original query + expanded clinical terms).
    """
    clean_query = query.strip().lower()
    terms = [clean_query]
    
    # Direct match or partial key match in SYNONMY_MAP
    for key, synonyms in SYNONMY_MAP.items():
        if key in clean_query or clean_query in key:
            for s in synonyms:
                if s.lower() not in terms:
                    terms.append(s.lower())
                    
    return terms
