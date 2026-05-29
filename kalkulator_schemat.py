#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import math


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title):
    print("=" * 70)
    print(f"{title:^70}")
    print("=" * 70)


def print_section(title):
    print(f"\n\033[1;36m{title}\033[0m")
    print("-" * 50)


def print_result(label, value, unit="", color="green"):
    colors = {
        "green": "\033[1;32m",
        "yellow": "\033[1;33m",
        "red": "\033[1;31m",
        "blue": "\033[1;34m"
    }
    color_code = colors.get(color, "\033[1;32m")
    print(f"{label:<35}: {color_code}{value}\033[0m {unit}")


def print_warning(text):
    print(f"\033[1;33m⚠ {text}\033[0m")


def print_info(text):
    print(f"\033[1;34mℹ {text}\033[0m")


def print_danger(text):
    print(f"\033[1;31m⚡ {text}\033[0m")


def oblicz_srednice_przewodu(prad):
    """
    Oblicza minimalna srednice przewodu na podstawie pradu
    z marginesem bezpieczenstwa 2x
    """
    # Gestosc pradu dla miedzi: 3A/mm² (bezpieczna wartosc)
    gestosc_pradu = 3.0  # A/mm²

    # Wymagany przekroj z zapasem 2x
    przekroj_min = (prad * 2) / gestosc_pradu

    # Srednica przewodu (mm) - zakladamy przekroj kola
    srednica = 2 * math.sqrt(przekroj_min / math.pi)

    return przekroj_min, srednica


def generuj_schemat_polaczen(napiecie_zasilacza, prad_zasilacza, dlugosc_drutu_m, srednica_drutu, z_pwm=False):
    """
    Generuje tekstowy schemat polaczen dla przecinarki
    """
    print_section("SCHEMAT POŁĄCZEŃ ELEKTRYCZNYCH")

    # Okreslenie typu zasilacza na podstawie napiecia
    if napiecie_zasilacza <= 12:
        typ_zasilacza = "ZASILACZ 12V"
    elif napiecie_zasilacza <= 24:
        typ_zasilacza = "ZASILACZ 24V"
    else:
        typ_zasilacza = "ZASILACZ 36V"

    # Okreslenie bezpiecznika na podstawie pradu
    if prad_zasilacza <= 2:
        bezpiecznik = "F 2A"
    elif prad_zasilacza <= 3:
        bezpiecznik = "F 3A"
    elif prad_zasilacza <= 5:
        bezpiecznik = "F 5A"
    else:
        bezpiecznik = "F 10A"

    # Generowanie schematu
    if z_pwm:
        schemat = [
            "Sieć 230V AC",
            "     │",
            " [BEZPIECZNIK]",
            "     │",
            "[WŁĄCZNIK GŁÓWNY]",
            "     │",
            f"┌─────────────────┐",
            f"│ {typ_zasilacza} │",
            f"│   {napiecie_zasilacza}V/{prad_zasilacza:.1f}A   │",
            f"└─────────────────┘",
            "     │ +",
            f"  [{bezpiecznik}]",
            "     │",
            "┌─────────────────┐",
            "│ REGULATOR PWM   │",
            "│   10A-30A       │",
            "└─────────────────┘",
            "     │",
            "[WŁĄCZNIK DRUTU]",
            "     │",
            "┌─────────────────┐",
            "│ DRUT OPOROWY    │",
            f"│ Długość: {dlugosc_drutu_m:.1f}m      │",
            f"│ Średnica: {srednica_drutu:.1f}mm    │",
            "└─────────────────┘",
            "     │",
            "   GND"
        ]
    else:
        schemat = [
            "Sieć 230V AC",
            "     │",
            " [BEZPIECZNIK]",
            "     │",
            "[WŁĄCZNIK GŁÓWNY]",
            "     │",
            f"┌─────────────────┐",
            f"│ {typ_zasilacza} │",
            f"│   {napiecie_zasilacza}V/{prad_zasilacza:.1f}A   │",
            f"└─────────────────┘",
            "     │ +",
            f"  [{bezpiecznik}]",
            "     │",
            "[WŁĄCZNIK DRUTU]",
            "     │",
            "┌─────────────────┐",
            "│ DRUT OPOROWY    │",
            f"│ Długość: {dlugosc_drutu_m:.1f}m      │",
            f"│ Średnica: {srednica_drutu:.1f}mm    │",
            "└─────────────────┘",
            "     │",
            "   GND"
        ]

    # Wyswietlanie schematu z kolorowaniem
    for i, linia in enumerate(schemat):
        if i == 0:  # Siec
            print(f"\033[1;31m{linia}\033[0m")
        elif "BEZPIECZNIK" in linia or "F " in linia:
            print(f"\033[1;33m{linia}\033[0m")
        elif "WŁĄCZNIK" in linia:
            print(f"\033[1;36m{linia}\033[0m")
        elif "ZASILACZ" in linia:
            print(f"\033[1;32m{linia}\033[0m")
        elif "PWM" in linia or "REGULATOR" in linia:
            print(f"\033[1;35m{linia}\033[0m")
        elif "DRUT OPOROWY" in linia:
            print(f"\033[1;35m{linia}\033[0m")
        else:
            print(linia)

    print()
    print_info("Legenda:")
    print("• \033[1;31mCzerwony\033[0m - Sieć 230V AC")
    print("• \033[1;33mŻółty\033[0m - Bezpieczniki")
    print("• \033[1;36mCyjan\033[0m - Włączniki")
    print("• \033[1;32mZielony\033[0m - Zasilacz")
    print("• \033[1;35mFiolet\033[0m - Regulator PWM / Drut oporowy")


def tabela_przewodow():
    print("Prad maks. | Przekroj min. | Srednica | Typ przewodu")
    print("-----------|---------------|----------|-------------")
    print("1A         | 0.7 mm2       | 1.0 mm   | cienki (np. krokodylek)")
    print("2A         | 1.3 mm2       | 1.3 mm   | cienki")
    print("3A         | 2.0 mm2       | 1.6 mm   | sredni")
    print("5A         | 3.3 mm2       | 2.0 mm   | gruby")
    print("10A        | 6.7 mm2       | 2.9 mm   | bardzo gruby")
    print("15A        | 10.0 mm2      | 3.6 mm   | ekstra gruby")
    print()
    print_info("Uzyj przewodow wielozylowych dla lepszej elastycznosci")


def kalkulator_transformatora():
    print_header("KALKULATOR DOBORU TRANSFORMATORA DO PRZECINARKI STYROPINU")
    print()

    try:
        dlugosc_drutu = float(input("długosc drutu [cm]: ")) / 100  # konwersja na metry
        srednica_drutu = float(input("średnica drutu [mm]: "))
        opor_na_metrze = float(input("opor drutu [Ω/m]: "))
        dlugosc_przewodow_dc = float(input("długość przewodów DC (zasilacz→drut) [m]: "))

        # Obliczenia podstawowe
        opor_calkowity = opor_na_metrze * dlugosc_drutu
        napiecie_optymalne = opor_calkowity * 3  # Dla pradu ok 3A
        moc_potrzebna = napiecie_optymalne * 3
        prad_obwodu = 3.0  # Zakladamy staly prad

        # Zaokraglenie do dostepnych wartosci
        if napiecie_optymalne <= 12:
            napiecie_zasilacza = 12
        elif napiecie_optymalne <= 24:
            napiecie_zasilacza = 24
        else:
            napiecie_zasilacza = 36

        prad_zasilacza = moc_potrzebna / napiecie_zasilacza
        moc_zasilacza = napiecie_zasilacza * prad_zasilacza

        # Obliczanie temperatury (przyblizone)
        przekroj_drutu = 3.14159 * (srednica_drutu / 2) ** 2  # mm²
        srednica_m = srednica_drutu / 1000  # m
        powierzchnia = 3.14159 * srednica_m * dlugosc_drutu  # m²

        # Gestosc mocy [W/m²]
        gestosc_mocy = moc_potrzebna / powierzchnia if powierzchnia > 0 else 0

        # Przyblizona temperatura (°C) - uwzglednia material drutu
        # Kanthal A1: maksymalna temperatura pracy 1400°C, optymalna 400-800°C
        temp_roznica = gestosc_mocy / 15 if gestosc_mocy > 0 else 0
        temperatura = 20 + temp_roznica

        # Korekta temperatury dla Kanthal A1
        if temperatura > 1400:
            temperatura = 1400 + (temperatura - 1400) * 0.1
        elif temperatura > 800:
            temperatura = 800 + (temperatura - 800) * 0.5

        # Ocena temperatury
        if temperatura < 100:
            ocena_temp = "🟢 Niska - moze byc za wolna"
            temp_status = "niska"
        elif temperatura < 300:
            ocena_temp = "🟡 Srednia - dobra do cienkich materialow"
            temp_status = "srednia"
        elif temperatura < 600:
            ocena_temp = "🔵 Wysoka - optymalna do przecinania"
            temp_status = "wysoka"
        elif temperatura < 900:
            ocena_temp = "🟠 Bardzo wysoka - szybkie przecinanie"
            temp_status = "bardzo_wysoka"
        else:
            ocena_temp = "🔴 Ekstremalna - wymaga regulacji!"
            temp_status = "ekstremalna"

        # Obliczanie przekroju przewodow zasilajacych
        przekroj_zasilajacy, srednica_zasilajacego = oblicz_srednice_przewodu(prad_zasilacza)

        # Spadki napiecia w przewodach DC
        opor_udzialowy_miedzi = 0.017  # Ω/mm²/m
        opor_przewodu_jednego = (opor_udzialowy_miedzi * dlugosc_przewodow_dc) / przekroj_zasilajacy
        spadek_napiecia_jeden_przewod = prad_zasilacza * opor_przewodu_jednego
        spadek_napiecia_razem = spadek_napiecia_jeden_przewod * 2  # Tam i z powrotem
        spadek_procentowy = (spadek_napiecia_razem / napiecie_zasilacza) * 100

        # Wyprowadzenie wynikow
        print_section("PARAMETRY DRUTU OPOROWEGO")
        print_result("Długość drutu", f"{dlugosc_drutu:.2f}", "m")
        print_result("Średnica drutu", f"{srednica_drutu:.1f}", "mm")
        print_result("Przekrój drutu", f"{przekroj_drutu:.2f}", "mm²")
        print_result("Opór całkowity drutu", f"{opor_calkowity:.2f}", "Ω")

        print_section("PARAMETRY ELEKTRYCZNE")
        print_result("Napięcie optymalne", f"{napiecie_optymalne:.1f}", "V")
        print_result("Prąd obciążenia", f"{prad_obwodu:.1f}", "A")
        print_result("Moc grzania", f"{moc_potrzebna:.1f}", "W")

        print_section("REKOMENDACJA ZASILACZA")
        print_result("Zalecane napięcie", f"{napiecie_zasilacza}", "V")
        print_result("Minimalny prąd", f"{prad_zasilacza:.1f}", "A")
        print_result("Minimalna moc", f"{moc_zasilacza:.1f}", "W")

        print_section("PARAMETRY TERMICZNE")
        print_result("Szacowana temperatura", f"{temperatura:.0f}", "°C")
        print(f"{'Ocena temperatury':<35}: {ocena_temp}")
        print_result("Gęstość mocy", f"{gestosc_mocy:.0f}", "W/m²")

        # Rekomendacja co do temperatury
        if temperatura > 800:
            print_warning("WYSOKA TEMPERATURA!")
            print_info("Ryzyko przyspieszonego zużycia drutu")
            print_info("Zalecane użycie regulatora PWM do kontroli temperatury")
        elif temperatura > 600:
            print_info("Optymalna temperatura do przecinania")
            print_info("Można rozważyć regulator PWM dla precyzyjnej kontroli")

        print_section("PRZEWODY ZASILAJĄCE DC")
        print_result("Długość przewodów DC", f"{dlugosc_przewodow_dc:.1f}", "m")
        print_result("Wymagany przekrój", f"{przekroj_zasilajacy:.2f}", "mm²")
        print_result("Minimalna średnica przewodu", f"{srednica_zasilajacego:.1f}", "mm")
        print_result("Opór jednego przewodu", f"{opor_przewodu_jednego:.3f}", "Ω")
        print_result("Spadek napięcia łącznie", f"{spadek_napiecia_razem:.2f}", "V")
        print_result("Spadek procentowy", f"{spadek_procentowy:.1f}", "%")

        # Ocena spadku napiecia
        if spadek_procentowy > 5:
            print_danger(f"Duży spadek napięcia! ({spadek_procentowy:.1f}%)")
            print_warning("Zwiększ przekrój przewodów lub skróć ich długość")
        elif spadek_procentowy > 2:
            print_warning(f"Średni spadek napięcia ({spadek_procentowy:.1f}%)")
            print_info("Rozważ zwiększenie przekroju przewodów")
        else:
            print_result("Spadek napięcia", "Akceptowalny", "", "green")

        # Rekomendacja regulatora PWM
        potrzebuje_pwm = False
        if temperatura > 800 or temp_status == "ekstremalna":
            potrzebuje_pwm = True
            print_section("REKOMENDACJA REGULATORA PWM")
            print_danger("EKSTREMALNA TEMPERATURA!")
            print_warning("Bezwzględnie konieczne użycie regulatora PWM!")
            print_info("Zużycie drutu będzie bardzo szybkie bez regulacji")
            print_info("Ryzyko przepalenia drutu")
            print_info("Zalecany regulator: PWM 10A-30A z wentylatorem")
        elif temperatura > 600:
            potrzebuje_pwm = True
            print_section("REKOMENDACJA REGULATORA PWM")
            print_warning("WYSOKA TEMPERATURA")
            print_info("Zalecane użycie regulatora PWM dla:")
            print("• Kontroli temperatury")
            print("• Wydłużenia żywotności drutu")
            print("• Precyzyjnego przecinania")
            print("• Oszczędności energii")
        else:
            print_section("REGULATOR PWM")
            print_info("Dla tej konfiguracji regulator PWM jest opcjonalny")
            print_info("Może być użyty dla precyzyjnej kontroli temperatury")

        # Generowanie schematu polaczen
        generuj_schemat_polaczen(napiecie_zasilacza, prad_zasilacza, dlugosc_drutu, srednica_drutu, potrzebuje_pwm)

        # Rekomendacje przewodow
        print_section("REKOMENDACJE PRZEWODÓW")
        if srednica_zasilajacego <= 1.0:
            print("• Przewody cienkie (np. krokodylki, przewody elektronika)")
            print("• Przekrój: minimum 0.7 mm²")
        elif srednica_zasilajacego <= 1.6:
            print("• Przewody średnie (np. cienkie przewody głośnikowe)")
            print("• Przekrój: minimum 1.3 mm²")
        elif srednica_zasilajacego <= 2.5:
            print("• Przewody grube (np. grubsze przewody głośnikowe)")
            print("• Przekrój: minimum 2.0 mm²")
        else:
            print("• Przewody bardzo grube (np. przewody głośnikowe ekstra)")
            print("• Przekrój: minimum 3.3 mm²")

        print("• Użyj przewodów wielożyłowych")
        print("• Zastosuj osobne przewody dla PLUS i MINUS")
        print("• Zabezpiecz obwód bezpiecznikiem")
        print("• Użyj zacisków typu banana lub krokodyli")

        # Ogólne rekomendacje
        print_section("OGÓLNE REKOMENDACJE")
        print("• Wybierz zasilacz o mocy:", f"{moc_zasilacza:.0f}W")
        print("• Zastosuj zasilacz z regulacją napięcia")
        print("• Użyj transformatora obniżającego napięcie")
        print("• Zastosuj przełącznik do włączania drutu")

        if temperatura > 600:
            print_warning("Wysoka temperatura - zapewnij dobrą wentylację!")
        if prad_zasilacza > 5:
            print_warning("Duży prąd - użyj grubych przewodów!")

        print_info("Drut Kanthal potrzebuje chwili na rozgrzanie")
        print_info("Nie dotykaj drutu podczas pracy!")

        # Specjalne ostrzezenia dla wysokich temperatur
        if temperatura > 800:
            print_danger("UWAGA BEZPIECZEŃSTWA!")
            print("• Nie zostawiaj urządzenia bez nadzoru")
            print("• Zapewnij odpowiednią wentylację")
            print("• Trzymaj materiał palny w bezpiecznej odległości")
            print("• Miej gaśnicę lub wodę w pobliżu")
            print("• Używaj odpowiedniego ochraniacza")

    except ValueError:
        print("\033[1;31m❌ Błąd: Wprowadź poprawne wartości liczbowe!\033[0m")
    except ZeroDivisionError:
        print("\033[1;31m❌ Błąd: Dzielenie przez zero!\033[0m")
    except Exception as e:
        print(f"\033[1;31m❌ Nieoczekiwany błąd: {e}\033[0m")


def tabela_typowych_drutow():
    print_header("TABELA TYPOWYCH DRUTÓW KANTHAL")

    print("\n\033[1;36mKANTHAL A1 - Parametry podstawowe:\033[0m")
    print("Średnica | Przekrój | Opór    | Moc@12V | Moc@24V | Temp. rob. | Max temp.")
    print("---------|----------|---------|---------|---------|------------|----------")
    print("0.3 mm   | 0.07 mm² | 18.0Ω/m | 8 W/m   | 32 W/m  | 600-800°C   | 1400°C")
    print("0.4 mm   | 0.13 mm² | 10.2Ω/m | 14 W/m  | 56 W/m  | 550-750°C   | 1400°C")
    print("0.5 mm   | 0.20 mm² | 6.5Ω/m  | 22 W/m  | 89 W/m  | 500-700°C   | 1400°C")
    print("0.6 mm   | 0.28 mm² | 4.5Ω/m  | 32 W/m  | 128 W/m | 450-650°C   | 1400°C")
    print("0.8 mm   | 0.50 mm² | 2.6Ω/m  | 55 W/m  | 221 W/m | 400-600°C   | 1400°C")
    print("1.0 mm   | 0.79 mm² | 1.71Ω/m | 84 W/m  | 337 W/m | 350-550°C   | 1400°C")

    print("\n\033[1;36mINNE MATERIAŁY:\033[0m")
    print("Materiał    | Opór [Ω/m] dla 1mm | Temp. max. | Uwagi")
    print("------------|-------------------|------------|-------")
    print("Miedź       | 0.017             | -          | Nie do przecinania!")
    print("Nichrom     | 1.0-1.5           | 1200°C     | Alternatywa")
    print("Stal        | 0.1-0.2           | 800°C      | Krótkotrwałe użycie")

    print_section("TABELA PRZEKROJÓW PRZEWODÓW")
    tabela_przewodow()

    print_section("ZALECENIA DOTYCZĄCE TEMPERATURY")
    print("• 350-550°C: Optymalna do cienkich materiałów")
    print("• 550-700°C: Optymalna do przecinania standardowego")
    print("• 700-900°C: Szybkie przecinanie, zwiększone zużycie")
    print("• >900°C: Wymaga regulatora PWM, szybkie zużycie")


def przykladowe_obliczenia():
    print_header("PRZYKŁADOWE OBLICZENIA")

    print("\n\033[1;36mPRZYKŁAD 1: Drut 150cm, Kanthal 1.0mm (1.71Ω/m), przewody 1m\033[0m")
    print("• Opór całkowity drutu: 1.71 × 1.5 = 2.57Ω")
    print("• Napięcie optymalne: 2.57 × 3A = 7.7V → Zasilacz 12V")
    print("• Moc: 12V × 3A = 36W")
    print("• Temperatura: ~450°C (optymalna)")
    print("• Zasilacz: 12V/3A (36W)")
    print("• Przewody DC (1m): przekrój 2.0mm², średnica 1.6mm")
    print("• Spadek napięcia: ~0.3V (2.5%)")
    print("• Regulator PWM: opcjonalny")

    print("\n\033[1;36mPRZYKŁAD 2: Drut 100cm, Kanthal 0.8mm (2.6Ω/m), przewody 2m\033[0m")
    print("• Opór całkowity drutu: 2.6 × 1.0 = 2.6Ω")
    print("• Napięcie optymalne: 2.6 × 3A = 7.8V → Zasilacz 12V")
    print("• Moc: 12V × 3A = 36W")
    print("• Temperatura: ~500°C (optymalna)")
    print("• Zasilacz: 12V/3A (36W)")
    print("• Przewody DC (2m): przekrój 2.0mm², średnica 1.6mm")
    print("• Spadek napięcia: ~0.6V (5%)")
    print("• Regulator PWM: opcjonalny")

    print("\n\033[1;36mPRZYKŁAD 3: Drut 80cm, Kanthal 0.5mm (6.5Ω/m), przewody 0.5m\033[0m")
    print("• Opór całkowity drutu: 6.5 × 0.8 = 5.2Ω")
    print("• Napięcie optymalne: 5.2 × 3A = 15.6V → Zasilacz 24V")
    print("• Moc: 24V × 3A = 72W")
    print("• Temperatura: ~650°C (wysoka)")
    print("• Zasilacz: 24V/3A (72W)")
    print("• Przewody DC (0.5m): przekrój 3.3mm², średnica 2.0mm")
    print("• Spadek napięcia: ~0.3V (1.2%)")
    print("• Regulator PWM: zalecany")

    print("\n\033[1;36mPRZYKŁAD 4: Drut 50cm, Kanthal 0.3mm (18.0Ω/m), przewody 1m\033[0m")
    print("• Opór całkowity drutu: 18.0 × 0.5 = 9.0Ω")
    print("• Napięcie optymalne: 9.0 × 3A = 27.0V → Zasilacz 36V")
    print("• Moc: 36V × 3A = 108W")
    print("• Temperatura: ~950°C (ekstremalna)")
    print("• Zasilacz: 36V/3A (108W)")
    print("• Przewody DC (1m): przekrój 3.3mm², średnica 2.0mm")
    print("• Spadek napięcia: ~0.3V (0.8%)")
    print("• Regulator PWM: BEZWZGLĘDNIE KONIECZNY!")


def main():
    while True:
        clear_screen()
        print_header("MENU GŁÓWNE")
        print()
        print("  \033[1;32m1\033[0m. Kalkulator transformatora")
        print("  \033[1;32m2\033[0m. Tabela typowych drutów")
        print("  \033[1;32m3\033[0m. Przykładowe obliczenia")
        print("  \033[1;31m4\033[0m. Wyjście")
        print()

        try:
            wybor = input("\033[1;33mWybierz opcję (1-4): \033[0m")

            if wybor == "1":
                clear_screen()
                kalkulator_transformatora()
            elif wybor == "2":
                clear_screen()
                tabela_typowych_drutow()
            elif wybor == "3":
                clear_screen()
                przykladowe_obliczenia()
            elif wybor == "4":
                clear_screen()
                print_header("DO WIDZENIA!")
                print("\033[1;32mDziękujemy za skorzystanie z kalkulatora!\033[0m")
                break
            else:
                print("\033[1;31m❌ Nieprawidłowy wybór!\033[0m")

        except KeyboardInterrupt:
            clear_screen()
            print_header("DO WIDZENIA!")
            print("\033[1;32mProgram został przerwany przez użytkownika.\033[0m")
            break
        except Exception as e:
            print(f"\033[1;31m❌ Błąd: {e}\033[0m")

        print()
        input("\033[1;33mNaciśnij Enter, aby kontynuować...\033[0m")


if __name__ == "__main__":
    main()
