# Structured table from BS 8110 extract
exposure_data = {
    "Mild": {
        "Nominal cover (mm)": [25, 20, "20a", "20a", "20a"],
        "w/c ratio": 0.65,
        "cement content (kg/m3)": 275,
        "min concrete grade": "C30"
    },
    "Moderate": {
        "Nominal cover (mm)": ["—", 35, 30, 25, 20],
        "w/c ratio": 0.60,
        "cement content (kg/m3)": 300,
        "min concrete grade": "C35"
    },
    "Severe": {
        "Nominal cover (mm)": ["—", "—", 40, 30, 25],
        "w/c ratio": 0.55,
        "cement content (kg/m3)": 325,
        "min concrete grade": "C40"
    },
    "Very severe": {
        "Nominal cover (mm)": ["—", "—", "50b", "40b", 30],
        "w/c ratio": 0.50,
        "cement content (kg/m3)": 350,
        "min concrete grade": "C45"
    },
    "Most severe": {
        "Nominal cover (mm)": ["—", "—", "—", "—", 50],
        "w/c ratio": 0.45,
        "cement content (kg/m3)": 400,
        "min concrete grade": "C50"
    },
    "Abrasive": {
        "Nominal cover (mm)": ["—", "—", "—", "See NOTE 3", "See NOTE 3"],
        "w/c ratio": None,
        "cement content (kg/m3)": None,
        "min concrete grade": None
    }
}

columns = ["Slab", "Beam", "Column", "Wall", "Footing"]

# Display available exposure conditions
print("Choose an Exposure Condition:")
for condition in exposure_data:
    print("-", condition)

# Get user input
user_input = input("\nEnter the exposure condition: ").strip()

# Display results if valid
if user_input in exposure_data:
    data = exposure_data[user_input]
    print(f"\n📋 Exposure Condition: {user_input}")
    print("\nNominal Cover Requirements:")
    for col, cover in zip(columns, data["Nominal cover (mm)"]):
        print(f"  - {col}: {cover} mm")

    if data["w/c ratio"] is not None:
        print(f"\n✅ Maximum water/cement ratio: {data['w/c ratio']}")
        print(f"✅ Minimum cement content: {data['cement content (kg/m3)']} kg/m³")
        print(f"✅ Minimum concrete grade: {data['min concrete grade']}")
    else:
        print("\n⚠️ Cement ratio, content, and grade: See NOTE 3")
else:
    print("❌ Invalid input. Please enter a valid exposure condition from the list.")
