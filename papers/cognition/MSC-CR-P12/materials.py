"""Generate the candidate bank. All values describe fictional situations."""
import json


def bank():
    designs = {
        "mobilnosc": ("kurs", "czas dotarcia [%d min]", "liczba przesiadek", "jedna przesiadka"),
        "ekologia": ("stanowisko", "wzrost roślin [%d mm]", "liczba godzin światła", "trzy godziny światła"),
        "wyposazenie": ("zestaw", "czas pracy [%d h]", "masa", "co najwyżej 3 kg"),
    }
    entries = []
    for domain, (label, metric, attribute, criterion) in designs.items():
        for form in range(3):
            for index in range(16):
                offset = 2 + (3 * index + form) % 13
                answers = [f"{label.capitalize()} A", f"{label.capitalize()} B"]
                family = index % 4
                eligible = (index // 4 + form) % 2
                values = [offset + 1, offset]
                if family == 2:
                    values = [offset, offset + 1]
                if domain == "mobilnosc":
                    detail = ["1", "2"] if eligible == 0 else ["2", "1"]
                    objective = "Wybierz najkrótszy kurs spośród kursów z jedną przesiadką."
                    quality = "krótszy zmierzony czas"
                elif domain == "ekologia":
                    detail = ["3", "5"] if eligible == 0 else ["5", "3"]
                    objective = "Wybierz stanowisko z największym zmierzonym wzrostem spośród stanowisk z trzema godzinami światła."
                    quality = "większy zmierzony wzrost"
                else:
                    detail = ["2 kg", "4 kg"] if eligible == 0 else ["4 kg", "2 kg"]
                    objective = "Wybierz zestaw o najdłuższym czasie pracy spośród zestawów ważących najwyżej 3 kg."
                    quality = "dłuższy zmierzony czas"
                evidence = [
                    f"{answer}. {metric % value}. {attribute.capitalize()} {extra}."
                    for answer, value, extra in zip(answers, values, detail)
                ]
                justification = f"spełnia warunek kwalifikacji ({criterion})"
                if family in (1, 3):
                    evidence = [f"Karta {line}" for line in evidence[::-1]]
                if family in (2, 3):
                    # Both options eligible; the optimization criterion determines the key.
                    evidence = [line.replace(detail[1 - eligible] + ".", detail[eligible] + ".")
                                for line in evidence]
                    eligible = values.index(min(values) if domain == "mobilnosc" else max(values))
                    justification = f"zapewnia {quality} wśród opcji spełniających warunek"
                advice = [f"Proponuję opcję {x}. Uważam, że {justification}." for x in answers]
                entries.append(dict(
                    id=f"{domain}-{form}-{index:02}", domain=domain, form=form,
                    family=family, objective=objective, evidence=evidence,
                    answers=answers, correct=eligible, advice=advice,
                    rationale=f"Klucz {answers[eligible]}. Weryfikuj kwalifikację przed porównaniem wyników.",
                ))
    return entries


if __name__ == "__main__":
    print(json.dumps(bank(), ensure_ascii=False, indent=2))
