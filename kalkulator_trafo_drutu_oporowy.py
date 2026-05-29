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
    Oblicza minimalną średnicę przewodu na podstawie prądu
    z marginesem bezpieczeństwa 2x
    """
    # Gęstość prądu dla miedzi: 3A/mm² (bezpieczna wartość)
    gestosc_pradu = 3.0  # A/mm²

    # Wymagany przekrój z zapasem 2x
    przekroj_min = (prad * 2) / gestosc_pradu

    # Średnica przewodu (mm) - zakładamy przekrój koła
    srednica = 2 * math.sqrt(przekroj_min / math.pi)

    return przekroj_min, srednica


def tabela_przewodow():
    print("Prąd maks. | Przekrój min. | Średnica | Typ przewodu")
    print("-----------|---------------|----------|-------------")
    print("1A         | 0.7 mm²       | 1.0 mm   | cienki (np. krokodylek)")
    print("2A         | 1.3 mm²       | 1.3 mm   | cienki")
    print("3A         | 2.0 mm²       | 1.6 mm   | średni")
    print("5A         | 3.3 mm²       | 2.0 mm   | gruby")
    print("10A        | 6.7 mm²       | 2.9 mm   | bardzo gruby")
    print("15A        | 10.0 mm²      | 3.6 mm   | ekstra gruby")
    print()
    print_info("Użyj przewodów wielożyłowych dla lepszej elastyczności")


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
        napiecie_optymalne = opor_calkowity * 3  # Dla prądu ok 3A
        moc_potrzebna = napiecie_optymalne * 3
        prad_obwodu = 3.0  # Zakładamy stały prąd

        # Zaokrąglenie do dostępnych wartości
        if napiecie_optymalne <= 12:
            napiecie_zasilacza = 12
        elif napiecie_optymalne <= 24:
            napiecie_zasilacza = 24
        else:
            napiecie_zasilacza = 36

        prad_zasilacza = moc_potrzebna / napiecie_zasilacza
        moc_zasilacza = napiecie_zasilacza * prad_zasilacza

        # Obliczanie temperatury (przybliżone)
        przekroj_drutu = 3.14159 * (srednica_drutu / 2) ** 2  # mm²
        srednica_m = srednica_drutu / 1000  # m
        powierzchnia = 3.14159 * srednica_m * dlugosc_drutu  # m²

        # Gęstość mocy [W/m²]
        gestosc_mocy = moc_potrzebna / powierzchnia if powierzchnia > 0 else 0

        # Przybliżona temperatura (°C)
        temp_roznica = gestosc_mocy / 15 if gestosc_mocy > 0 else 0
        temperatura = 20 + temp_roznica

        # Korekta temperatury
        if temperatura > 800:
            temperatura = 800 + (temperatura - 800) * 0.3

        # Ocena temperatury
        if temperatura < 100:
            ocena_temp = "🟢 Niska - może być za wolna"
        elif temperatura < 300:
            ocena_temp = "🟡 Średnia - dobra do cienkich materiałów"
        elif temperatura < 600:
            ocena_temp = "🔵 Wysoka - optymalna do przecinania"
        else:
            ocena_temp = "🔴 Bardzo wysoka - szybkie przecinanie"

        # Obliczanie przekroju przewodów zasilających
        przekroj_zasilajacy, srednica_zasilajacego = oblicz_srednice_przewodu(prad_zasilacza)

        # Spadki napięcia w przewodach DC
        opor_udzialowy_miedzi = 0.017  # Ω/mm²/m
        opor_przewodu_jednego = (opor_udzialowy_miedzi * dlugosc_przewodow_dc) / przekroj_zasilajacy
        spadek_napiecia_jeden_przewod = prad_zasilacza * opor_przewodu_jednego
        spadek_napiecia_razem = spadek_napiecia_jeden_przewod * 2  # Tam i z powrotem
        spadek_procentowy = (spadek_napiecia_razem / napiecie_zasilacza) * 100

        # Wyprowadzenie wyników
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

        print_section("PRZEWODY ZASILAJĄCE DC")
        print_result("Długość przewodów DC", f"{dlugosc_przewodow_dc:.1f}", "m")
        print_result("Wymagany przekrój", f"{przekroj_zasilajacy:.2f}", "mm²")
        print_result("Minimalna średnica przewodu", f"{srednica_zasilajacego:.1f}", "mm")
        print_result("Opór jednego przewodu", f"{opor_przewodu_jednego:.3f}", "Ω")
        print_result("Spadek napięcia łącznie", f"{spadek_napiecia_razem:.2f}", "V")
        print_result("Spadek procentowy", f"{spadek_procentowy:.1f}", "%")

        # Ocena spadku napięcia
        if spadek_procentowy > 5:
            print_danger(f"Duży spadek napięcia! ({spadek_procentowy:.1f}%)")
            print_warning("Zwiększ przekrój przewodów lub skróć ich długość")
        elif spadek_procentowy > 2:
            print_warning(f"Średni spadek napięcia ({spadek_procentowy:.1f}%)")
            print_info("Rozważ zwiększenie przekroju przewodów")
        else:
            print_result("Spadek napięcia", "Akceptowalny", "", "green")

        # Rekomendacje przewodów
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

    except ValueError:
        print("\033[1;31m❌ Błąd: Wprowadź poprawne wartości liczbowe!\033[0m")
    except ZeroDivisionError:
        print("\033[1;31m❌ Błąd: Dzielenie przez zero!\033[0m")
    except Exception as e:
        print(f"\033[1;31m❌ Nieoczekiwany błąd: {e}\033[0m")


def tabela_typowych_drutow():
    print_header("TABELA TYPOWYCH DRUTÓW KANTHAL")

    print("\n\033[1;36mKANTHAL A1 - Parametry podstawowe:\033[0m")
    print("Średnica | Przekrój | Opór    | Moc@12V | Moc@24V | Temp. rob.")
    print("---------|----------|---------|---------|---------|-----------")
    print("0.3 mm   | 0.07 mm² | 18.0Ω/m | 8 W/m   | 32 W/m  | 600-800°C")
    print("0.4 mm   | 0.13 mm² | 10.2Ω/m | 14 W/m  | 56 W/m  | 550-750°C")
    print("0.5 mm   | 0.20 mm² | 6.5Ω/m  | 22 W/m  | 89 W/m  | 500-700°C")
    print("0.6 mm   | 0.28 mm² | 4.5Ω/m  | 32 W/m  | 128 W/m | 450-650°C")
    print("0.8 mm   | 0.50 mm² | 2.6Ω/m  | 55 W/m  | 221 W/m | 400-600°C")
    print("1.0 mm   | 0.79 mm² | 1.71Ω/m | 84 W/m  | 337 W/m | 350-550°C")

    print("\n\033[1;36mINNE MATERIAŁY:\033[0m")
    print("Materiał    | Opór [Ω/m] dla 1mm | Uwagi")
    print("------------|-------------------|-------")
    print("Miedź       | 0.017             | Nie do przecinania!")
    print("Nichrom     | 1.0-1.5           | Alternatywa")
    print("Stal        | 0.1-0.2           | Krótkotrwałe użycie")

    print_section("TABELA PRZEKROJÓW PRZEWODÓW")
    tabela_przewodow()


def przykladowe_obliczenia():
    print_header("PRZYKŁADOWE OBLICZENIA")

    print("\n\033[1;36mPRZYKŁAD 1: Drut 150cm, Kanthal 1.0mm (1.71Ω/m), przewody 1m\033[0m")
    print("• Opór całkowity drutu: 1.71 × 1.5 = 2.57Ω")
    print("• Napięcie optymalne: 2.57 × 3A = 7.7V → Zasilacz 12V")
    print("• Moc: 12V × 3A = 36W")
    print("• Temperatura: ~450°C")
    print("• Zasilacz: 12V/3A (36W)")
    print("• Przewody DC (1m): przekrój 2.0mm², średnica 1.6mm")
    print("• Spadek napięcia: ~0.3V (2.5%)")

    print("\n\033[1;36mPRZYKŁAD 2: Drut 100cm, Kanthal 0.8mm (2.6Ω/m), przewody 2m\033[0m")
    print("• Opór całkowity drutu: 2.6 × 1.0 = 2.6Ω")
    print("• Napięcie optymalne: 2.6 × 3A = 7.8V → Zasilacz 12V")
    print("• Moc: 12V × 3A = 36W")
    print("• Temperatura: ~500°C")
    print("• Zasilacz: 12V/3A (36W)")
    print("• Przewody DC (2m): przekrój 2.0mm², średnica 1.6mm")
    print("• Spadek napięcia: ~0.6V (5%)")

    print("\n\033[1;36mPRZYKŁAD 3: Drut 80cm, Kanthal 0.5mm (6.5Ω/m), przewody 0.5m\033[0m")
    print("• Opór całkowity drutu: 6.5 × 0.8 = 5.2Ω")
    print("• Napięcie optymalne: 5.2 × 3A = 15.6V → Zasilacz 24V")
    print("• Moc: 24V × 3A = 72W")
    print("• Temperatura: ~650°C")
    print("• Zasilacz: 24V/3A (72W)")
    print("• Przewody DC (0.5m): przekrój 3.3mm², średnica 2.0mm")
    print("• Spadek napięcia: ~0.3V (1.2%)")


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
