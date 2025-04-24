from database import Person, Company, Employment

if __name__ == "__main__":

    # make people
    harrison = Person(name="Harrison")
    harrison.save()

    nadia = Person(name="Nadia")
    nadia.save()

    # make companies
    harrisoncorp = Company(name="HarrisonCorp")  # kinda like LexCorp but good instead of evil
    harrisoncorp.save()

    # make jobs
    one_bajillion_dollars = 1000000000
    harrisonjob = Employment(person_id=harrison.id, company_id=harrisoncorp.id, salary=one_bajillion_dollars)
    harrisonjob.save()

    nadia_salary = harrisonjob.salary - 1  # boss gets paid the most
    nadiajob = Employment(person_id=nadia.id, company_id=harrisoncorp.id, salary=nadia_salary)
    nadiajob.save()

    # print
    harrisonjob.print()
    nadiajob.print()