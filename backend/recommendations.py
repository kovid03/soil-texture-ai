def get_recommendations(soil_type):
    rules = {
        'Clay': {
            'crops': ['Rice', 'Broccoli', 'Cabbage', 'Cauliflower'],
            'fertilizers': ['Organic compost', 'Gypsum to improve drainage', 'Slow-release Nitrogen fertilizers']
        },
        'Loam': {
            'crops': ['Wheat', 'Sugarcane', 'Cotton', 'Tomatoes', 'Peppers'],
            'fertilizers': ['Balanced NPK fertilizer', 'Well-rotted manure', 'Bone meal']
        },
        'Sandy': {
            'crops': ['Carrots', 'Potatoes', 'Radishes', 'Watermelon', 'Peanuts'],
            'fertilizers': ['Frequent light applications of Nitrogen', 'Kelp meal', 'Potassium-rich fertilizers']
        },
        'Loamy Sand': {
            'crops': ['Corn', 'Onions', 'Garlic', 'Zucchini'],
            'fertilizers': ['Compost tea', 'Blood meal', 'Phosphorus-rich fertilizers']
        },
        'Sandy Loam': {
            'crops': ['Beans', 'Peas', 'Strawberries', 'Sweet Potatoes'],
            'fertilizers': ['Green manure', 'Fish emulsion', 'NPK 10-10-10']
        }
    }
    
    return rules.get(soil_type, {
        'crops': ['General crops suitable for local climate'],
        'fertilizers': ['Standard NPK composite']
    })
