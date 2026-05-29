# Kalkulator Przecinarki Styropianu

🔧 **Kalkulator doboru zasilacza i przewodów do przecinarki do styropianu z drutem oporowym**

## 📋 Opis projektu

Ten kalkulator pomaga w prawidłowym doborze zasilacza, transformatora i przewodów do budowy przecinarki do styropianu z wykorzystaniem drutu oporowego. Oblicza wszystkie niezbędne parametry elektryczne i termiczne, aby zapewnić bezpieczną i efektywną pracę urządzenia.

## ✨ Funkcje

- 🧮 Obliczanie wymaganych parametrów zasilacza
- 🔌 Dobór odpowiedniego przekroju przewodów zasilających
- 🌡️ Szacowanie temperatury drutu oporowego
- ⚡ Analiza spadków napięcia w przewodach
- 📊 Tabele z parametrami typowych drutów Kanthal
- 🎯 Rekomendacje konkretnej konfiguracji

## 🚀 Instalacja

### Wymagania
- Python 3.x

### Uruchomienie

```bash
# Pobierz repozytorium
git clone https://github.com/twoja-nazwa/kalkulator-przecinarki.git
cd kalkulator-przecinarki
```
# Uruchom kalkulator
```bash
python kalkulator_przecinarki.py
```
## 💻 Użycie

Po uruchomieniu programu wybierz jedną z opcji z menu głównego:

1. **Kalkulator transformatora** - główne narzędzie do obliczeń
2. **Tabela typowych drutów** - parametry drutów Kanthal i innych materiałów  
3. **Przykładowe obliczenia** - gotowe przykłady konfiguracji

### Przykład użycia:
```bash
długosc drutu [cm]: 150 
średnica drutu [mm]: 1.0 
opor drutu [Ω/m]: 1.71 
długość przewodów DC (zasilacz→drut) [m]: 1.0
```

## 📊 Przykładowe wyniki
```text
Dla drutu 150cm, Kanthal 1.0mm (1.71Ω/m):
- Opór całkowity: 2.57Ω
- Zalecany zasilacz: 12V/3A (36W)
- Temperatura: ~450°C
- Przewody DC: przekrój 2.0mm², średnica 1.6mm
- Spadek napięcia: ~0.3V (2.5%)
```

## 🔧 Wymagania sprzętowe

### Drut oporowy
- **Zalecany**: Drut Kanthal A1
- **Średnice**: 0.3mm - 1.0mm
- **Temperatura pracy**: 350-800°C

### Zasilacz
- **Napięcie**: 12V, 24V lub 36V (w zależności od konfiguracji)
- **Prąd**: minimum 3A
- **Moc**: odpowiednio do obliczonej mocy grzania

### Przewody zasilające
- **Typ**: wielożyłowe miedziane
- **Przekrój**: 1.5mm² - 10mm² (w zależności od prądu)
- **Długość**: zależnie od potrzeb (uwzględniane w obliczeniach)

## ⚠️ Uwagi bezpieczeństwa

- **Nie dotykaj drutu podczas pracy** - osiąga bardzo wysoką temperaturę
- **Zapewnij odpowiednią wentylację** - drut wydziela opary styropianu
- **Użyj bezpieczników** - zabezpieczenie przed przegrzaniem
- **Izoluj wszystkie połączenia** - ryzyko porażenia prądem
- **Nie zostawiaj urządzenia bez nadzoru** - ryzyko pożaru

## 📈 Dokładność obliczeń

Obliczenia mają charakter przybliżony i opierają się na:
- Uproszczonych modelach termicznych
- Średnich wartościach parametrów
- Założeniu stałego prądu 3A (można dostosować)

## 🛠️ Technologie

- **Python 3.x**
- **CLI (Command Line Interface)**
- **Cross-platform** (Windows, Linux, macOS)

## 🤝 Wkład w projekt

Projekt jest otwarty na sugestie i ulepszenia! Jeśli masz pomysły na rozwój:

1. Forkuj repozytorium
2. Stwórz branch z opisową nazwą
3. Zaimplementuj zmiany
4. Wyślij Pull Request

## 📄 Licencja

MIT License - zobacz plik [LICENSE](LICENSE) dla szczegółów

## 📞 Kontakt

Jeśli masz pytania lub sugestie, utwórz issue w repozytorium lub skontaktuj się przez [email].

---
Made with ❤️ for makers and DIY enthusiasts
