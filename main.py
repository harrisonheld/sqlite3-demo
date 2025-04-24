from database import Person, Company, Employment

if __name__ == "__main__":
    person = Person(name="Harrison")
    person.save()

    company = Company(name="HarrisonCorp")  # kinda like LexCorp but good instead of evil
    company.save()

    one_bajillion_dollars = 1000000000
    employment = Employment(person_id=person.id, company_id=company.id, salary=one_bajillion_dollars)
    employment.save()

    employment.print()