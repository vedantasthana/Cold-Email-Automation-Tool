def segregate_companies(df, backup_dict):
    companies_to_generate = []
    companies_in_backup = []

    for _, row in df.iterrows():
        company_name = row["Company"]
        website = row["Website"]

        if company_name not in backup_dict:
            companies_to_generate.append({
                "company_name": company_name,
                "website": website
            })
        else:
            companies_in_backup.append(company_name)

    return companies_to_generate, companies_in_backup