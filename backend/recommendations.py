def generate_recommendations(borrower_data, risk_probability):
    """
    borrower_data: dict with keys like 'dti', 'fico_range_low', 'int_rate',
                   'acc_open_past_24mths', 'mort_acc', 'emp_length_numeric',
                   'home_ownership', 'purpose', 'term'
    risk_probability: float, model's predicted probability of default
    """
    recommendations = []

    # DTI - confirmed: higher DTI correlates with more defaults (avg 20.2% vs 17.8%)
    if borrower_data.get("dti", 0) > 20:
        recommendations.append(
            "Your debt-to-income ratio is high. Paying down existing debt before "
            "taking on new credit, or increasing income, can lower this ratio and "
            "reduce default risk."
        )

    # FICO - confirmed: defaulters average ~10 points lower
    if borrower_data.get("fico_range_low", 750) < 690:
        recommendations.append(
            "Your credit score is below the typical safe-borrower range. Making "
            "on-time payments consistently and reducing credit utilization over "
            "the next several months can help raise it before taking on further debt."
        )

    # Loan term - confirmed: 60-month loans default at 2x the rate of 36-month
    if borrower_data.get("term") == "60 months":
        recommendations.append(
            "Longer-term (60-month) loans carry roughly double the default rate of "
            "36-month loans in this data. If affordable, a shorter loan term reduces "
            "long-term risk exposure, even with a higher monthly payment."
        )

    # Recently opened accounts - confirmed: more recent accounts = more risk
    if borrower_data.get("acc_open_past_24mths", 0) > 5:
        recommendations.append(
            "You've opened several credit accounts in the past 24 months. Slowing "
            "down new credit applications can reduce perceived risk and improve "
            "your profile over time."
        )

    # Employment length - confirmed: longer tenure = lower risk, though modest effect
    if borrower_data.get("emp_length_numeric", 10) < 2:
        recommendations.append(
            "Shorter employment history is associated with somewhat higher default "
            "rates. This factor naturally improves over time and isn't something "
            "to act on directly, but lenders may weigh it alongside other factors."
        )

    # Purpose - confirmed: small_business is the riskiest category (29.7%)
    if borrower_data.get("purpose") == "small_business":
        recommendations.append(
            "Small business loans have the highest default rate of any loan "
            "purpose in this data (29.7%). Maintaining a cash reserve for loan "
            "payments, separate from business operating funds, may reduce risk "
            "of missed payments during slow periods."
        )

    # Home ownership - confirmed: renters default more than mortgage holders
    if borrower_data.get("home_ownership") == "RENT":
        recommendations.append(
            "Renters show a somewhat higher default rate than homeowners in this "
            "data, likely reflecting broader financial stability factors rather "
            "than renting itself. This isn't directly actionable, but may factor "
            "into how lenders assess risk."
        )

    # Mortgage accounts - confirmed: counterintuitive, more mort_acc = LESS risk
    # (included as an explanatory note only, not actionable)

    if not recommendations:
        recommendations.append(
            "Your profile doesn't show the specific risk factors most strongly "
            "associated with default in this dataset. The model's prediction may "
            "reflect a combination of smaller factors."
        )

    return {
        "risk_probability": round(risk_probability, 4),
        "risk_level": "High" if risk_probability >= 0.55 else "Low",
        "recommendations": recommendations
    }
